# design.md — Power Meter Reading Telegram Bot

**Version:** 1.0
**Last updated:** 2026-04-01
**Status:** Active — defines architecture, tech stack, and implementation patterns
**Authority:** Subordinate to `scope.md`. In case of conflict, `scope.md` wins.

---

## Purpose

This document describes how the Power Meter Reading Telegram Bot is built — architecture, tech stack, data model, key flows, and implementation patterns. It is the reference for all technical decisions made during development.

---

## Architecture Overview

The system uses a 2-tier architecture:

```
┌─────────────────────────────────────────────────┐
│                  Telegram Cloud                 │
│         (message delivery, inline buttons)      │
└──────────────────────┬──────────────────────────┘
                       │ polling (getUpdates)
┌──────────────────────▼──────────────────────────┐
│               AWS EC2 (or local)                │
│                                                 │
│   ┌──────────────────────────────────────────┐  │
│   │        Python Telegram Bot (PTB)         │  │
│   │                                          │  │
│   │  ┌─────────────┐  ┌─────────────────┐    │  │
│   │  │  Handlers   │  │  Services layer │    │  │
│   │  │ (commands / │→ │ (business logic)│    │  │
│   │  │  callbacks) │  └────────┬────────┘    │  │
│   │  └─────────────┘           │             │  │
│   │                    ┌───────▼────────┐    │  │
│   │                    │  Repository    │    │  │
│   │                    │  layer (DB)    │    │  │
│   └────────────────────┴───────┬────────┘    │  │
│                                │             │  │
└────────────────────────────────┼─────────────┘  │
                                 │
┌────────────────────────────────▼────────────────┐
│           PostgreSQL (local / AWS RDS)          │
│              Migrations via Flyway              │
└─────────────────────────────────────────────────┘
```

**Key principles:**
- Polling mode only — no webhooks
- Stateless bot process: all state lives in the database
- Layered architecture: Handlers → Services → Repositories — no direct DB access from handlers
- Inline buttons only — zero free-text input from users; meter values are entered via an inline button numeric pad interface

---

## Environments

| Environment | Bot instance | Database | Hosting |
|---|---|---|---|
| DEV | DEV bot token (local) | Local PostgreSQL | Developer machine |
| UAT | UAT bot token | AWS RDS PostgreSQL | AWS EC2 (UAT) |
| PROD | PROD bot token | AWS RDS PostgreSQL | AWS EC2 (PROD) |

Each environment uses its own Telegram bot token and its own database. Config is environment-specific and never hardcoded.

---

## Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Language | Python 3.11+ | PTB library ecosystem, OCR libraries, broad community |
| Bot framework | `python-telegram-bot` v20+ (async) | Mature, well-documented, native async support |
| Database | PostgreSQL 15 | Same engine in DEV and PROD; strong JSON support for future flexibility |
| ORM / DB access | SQLAlchemy 2.x (Core or ORM, TBD) + psycopg2 | Standard Python PostgreSQL stack |
| DB migrations | Flyway | SQL-first migrations, easy CI/CD integration |
| Charts | TBD (Phase 2) — candidates: `matplotlib`, `plotly` | Decision deferred; output must be a PNG sent via Telegram `sendPhoto` |
| OCR | TBD (Phase 2) — candidates: Tesseract, Google Cloud Vision, OpenAI Vision API | Decision deferred; accuracy on meter photos to be evaluated |
| Testing | `pytest` + `pytest-asyncio` | Standard async-compatible Python test framework |
| Linting / formatting | `ruff` + `black` | Fast, modern Python linting and formatting |
| Secret management | Environment variables via `.env` (local), AWS Secrets Manager or SSM (cloud) | Secrets never hardcoded |
| Deployment (bot) | systemd service on EC2 | Simple, reliable process management for polling bot |
| Deployment (DB) | Flyway CLI in deployment script | Versioned, repeatable migrations |
| CI/CD | Shell scripts (Linux `.sh` + Windows `.bat`/`.ps1`) | Solo developer; lightweight, no CI server required initially |
| Version control | Git + GitHub (or GitLab) | PR-based workflow per methodology |

---

## Project Structure

```
project-root/
├── bot/
│   ├── handlers/          # Telegram update handlers (commands, callbacks)
│   │   ├── admin.py       # Administrator flows
│   │   ├── grayhound.py   # Grayhound flows
│   │   ├── tenant.py      # Tenant flows
│   │   └── common.py      # Shared handlers (start, help, error)
│   ├── services/          # Business logic (role-aware, no Telegram API calls)
│   │   ├── reading.py     # Meter reading logic
│   │   ├── roles.py       # Role assignment / validation
│   │   ├── export.py      # CSV export
│   │   └── charts.py      # Chart generation (Phase 2)
│   ├── repositories/      # DB access (SQLAlchemy queries)
│   │   ├── users.py
│   │   ├── readings.py
│   │   ├── apartments.py
│   │   └── roles.py
│   ├── models/            # SQLAlchemy model definitions
│   ├── keyboards/         # InlineKeyboardMarkup builders
│   └── main.py            # Bot entry point, Application setup
├── db/
│   └── migrations/        # Flyway SQL migration files (V1__init.sql, etc.)
├── tests/
│   ├── unit/
│   └── integration/
├── scripts/
│   ├── deploy_linux.sh
│   └── deploy_windows.ps1
├── docs/
│   ├── scope.md
│   ├── design.md
│   ├── tracker.md
│   └── handoff.md
├── .env.example           # Template for local env vars
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Data Model

### `users`

| Column | Type | Notes |
|---|---|---|
| id | BIGINT PK | Telegram user ID |
| username | VARCHAR | Telegram username (nullable) |
| full_name | VARCHAR | Display name |
| created_at | TIMESTAMPTZ | |
| is_active | BOOLEAN | Soft-delete / deactivation |

### `apartments`

| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| number | VARCHAR | Apartment number (e.g. "42", "42A") |
| floor | INT | |
| notes | TEXT | Optional |

### `user_roles`

| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| user_id | BIGINT FK → users.id | |
| role | VARCHAR | `administrator`, `grayhound`, `tenant` |
| apartment_id | BIGINT FK → apartments.id | NULL for administrator/grayhound |
| valid_from | DATE | Role valid from |
| valid_to | DATE | Role valid until (NULL = indefinite) |
| assigned_by | BIGINT FK → users.id | Administrator who assigned the role |
| created_at | TIMESTAMPTZ | |

**Notes:**
- A user can hold multiple roles simultaneously (e.g. Administrator + Grayhound)
- Role validity is checked at request time
- Tenants are scoped to one apartment via `apartment_id`

### `meters`

| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| apartment_id | BIGINT FK → apartments.id | |
| meter_number | VARCHAR | Physical meter ID / serial |
| installed_at | DATE | |
| is_active | BOOLEAN | |

### `readings`

| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| meter_id | BIGINT FK → meters.id | |
| value | NUMERIC(10,2) | kWh reading |
| read_at | TIMESTAMPTZ | When the reading was submitted |
| submitted_by | BIGINT FK → users.id | |
| source | VARCHAR | `manual`, `photo` |
| photo_file_id | VARCHAR | Telegram file_id if source=photo (Phase 2) |
| notes | TEXT | Optional |

---

## Role Permission Matrix

| Action | Tenant | Grayhound | Administrator |
|---|---|---|---|
| Submit reading for own apartment | ✅ | ✅ | ✅ |
| Submit reading for any apartment | ❌ | ✅ | ✅ |
| View own readings / chart | ✅ | ✅ | ✅ |
| View any apartment readings / chart | ❌ | ✅ | ✅ |
| View building-wide chart | ❌ | ✅ | ✅ |
| Export CSV (own apartment) | ✅ | ✅ | ✅ |
| Export CSV (all apartments) | ❌ | ✅ | ✅ |
| Assign / revoke roles | ❌ | ❌ | ✅ |
| Add / deactivate users | ❌ | ❌ | ✅ |
| Manage apartment list | ❌ | ❌ | ✅ |

---

## Key Flows

### 1. User onboarding

```
User sends /start
  → Bot checks if user exists in DB
    → New user: Bot registers user, notifies Administrator
    → Existing user with no active role: Bot shows "pending approval" message
    → Existing user with active role: Bot shows role-appropriate main menu
```

### 2. Tenant submits a meter reading

```
Tenant taps "Submit Reading" (inline button)
  → Bot shows apartment confirmation (pre-filled from role record)
  → Tenant confirms → Bot shows inline numeric pad (0–9, backspace, confirm)
  → Tenant enters value digit by digit → Bot shows confirmation: "Apartment 42 — 1234.56 kWh. Confirm?"
  → Tenant confirms → Reading saved to DB → Bot shows success + timestamp
```

### 3. Administrator assigns a role

```
Admin taps "Manage Users"
  → Bot lists registered users (paginated inline buttons)
  → Admin selects user → Bot shows current roles
  → Admin taps "Add Role" → selects role type
  → If Tenant: Admin selects apartment from inline list
  → Admin sets valid_from / valid_to (or "indefinite")
  → Bot shows confirmation → Admin confirms → Role saved to DB
```

### 4. CSV export

```
User taps "Export CSV"
  → Role check: Tenant → own apartment only; Grayhound/Admin → select scope
  → Bot queries readings, generates CSV in memory
  → Bot sends CSV as document via sendDocument
```

### 5. Chart generation (Phase 2)

```
User taps "View Chart"
  → Role check determines available scope
  → User selects apartment (or building-wide for Grayhound/Admin)
  → User selects period (last month / last 3 months / custom)
  → Service queries readings, generates PNG chart
  → Bot sends PNG via sendPhoto
```

---

## UX Patterns

- **All navigation and input via inline buttons** — no slash commands beyond `/start` and `/help`; meter values entered via an inline numeric pad (digits 0–9, backspace, confirm)
- **Confirmation step** before any write operation (reading submission, role change)
- **Pagination** for lists longer than 5 items (apartments, users)
- **Back button** on every screen — users can always return to the previous menu
- **Error messages** are user-friendly ("Something went wrong, please try again") — technical details logged only
- **Session state** managed via `ConversationHandler` in PTB — state stored in memory (stateless across restarts; in-progress conversations are reset on bot restart, which is acceptable)

---

## Configuration

All configuration via environment variables. Never hardcoded.

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token |
| `DATABASE_URL` | PostgreSQL connection string |
| `ENVIRONMENT` | `dev`, `uat`, `prod` |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING` |
| `ADMIN_TELEGRAM_ID` | Bootstrap admin user ID (used for first-run setup only) |

Local development uses a `.env` file (git-ignored). UAT/PROD use AWS SSM Parameter Store or Secrets Manager.

---

## Testing Strategy

- **Unit tests:** Services and repositories tested with mocked DB / mocked PTB context
- **Integration tests:** Key flows tested against a real local PostgreSQL instance (test DB, reset between runs)
- **Coverage target:** ≥ 80% on changed lines per PR (per `scope.md` SLOs)
- **Test runner:** `pytest` with `pytest-asyncio` for async handlers
- **No manual testing replaces automated tests** — every merged feature must have tests

---

## Deployment

### Local (DEV)

```bash
cp .env.example .env          # fill in BOT_TOKEN, DATABASE_URL
flyway migrate                 # apply DB migrations
python -m bot.main             # run bot locally
```

### UAT / PROD (Linux EC2)

```bash
./scripts/deploy_linux.sh [uat|prod]
# Script responsibilities:
#   1. Pull latest code from Git
#   2. Install/update dependencies (pip)
#   3. Run Flyway migrations against target DB
#   4. Restart systemd service
```

### Windows (developer machine UAT push)

```powershell
.\scripts\deploy_windows.ps1 [uat|prod]
# Same steps as Linux script, PowerShell syntax
```

---

## Architecture Decision Records (ADRs)

### ADR-001: Polling vs. Webhooks
**Decision:** Polling mode.
**Rationale:** Simpler deployment (no public HTTPS endpoint required, no reverse proxy setup). Polling latency is acceptable for a building-internal tool with low message volume.
**Trade-off:** Slightly higher latency than webhooks; revisit if PROD load warrants it.

### ADR-002: Local PostgreSQL in DEV (not SQLite)
**Decision:** PostgreSQL locally, same as UAT/PROD.
**Rationale:** Eliminates an entire class of environment-parity bugs (data types, constraints, query behaviour). SQLite differences (e.g. no native TIMESTAMPTZ) would create false confidence in local tests.
**Trade-off:** Slightly more setup for DEV environment.

### ADR-003: Inline buttons only — including numeric meter value entry
**Decision:** Zero free-text input from users. All interactions, including meter value entry, are handled via inline buttons. Meter values are entered via an inline numeric pad (digit-by-digit buttons: 0–9, backspace, confirm).
**Rationale:** Eliminates an entire class of input validation bugs. Enforces valid state transitions at the UX level. Consistent interaction model across all roles and flows.
**Trade-off:** Numeric pad keyboard builder adds implementation complexity. Multi-digit entry requires managing an in-progress value in `ConversationHandler` state. Revisit UX if users find digit-by-digit entry slow for large values.

### ADR-004: ConversationHandler state in memory
**Decision:** PTB `ConversationHandler` state is in-memory (not persisted to DB).
**Rationale:** Simplicity. In-progress multi-step flows (e.g. reading submission) reset on bot restart. Given low message volume and infrequent restarts, this is acceptable.
**Trade-off:** Users mid-flow during a restart must start that flow again. Revisit if this proves disruptive.

### ADR-005: OCR library — deferred
**Decision:** Not decided. Evaluate in Phase 2.
**Rationale:** Accuracy on real electricity meter photos must be tested before committing. Candidates: Tesseract (free, local), Google Cloud Vision (accurate, paid), OpenAI Vision API (flexible, paid).
**Trade-off:** Phase 2 scope may shift depending on OCR evaluation results.

### ADR-006: Chart library — deferred
**Decision:** Not decided. Evaluate in Phase 2.
**Rationale:** Output must be a PNG sent via `sendPhoto`. Both `matplotlib` and `plotly` (static export) are viable. Decision depends on chart complexity required.

---

## Changelog

| Date | Version | Changes | Author |
|---|---|---|---|
| 2026-04-01 | 1.0 | Initial design document | AI-assisted |
