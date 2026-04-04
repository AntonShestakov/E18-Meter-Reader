# design.md — Power Meter Reading Telegram Bot

**Version:** 1.1
**Last updated:** 2026-04-02
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
│                  Telegram Cloud                  │
│         (message delivery, inline buttons)       │
└──────────────────────┬──────────────────────────┘
                       │ polling (getUpdates)
┌──────────────────────▼──────────────────────────┐
│               AWS EC2 (or local)                 │
│                                                  │
│   ┌──────────────────────────────────────────┐  │
│   │        Python Telegram Bot (PTB)          │  │
│   │                                           │  │
│   │  ┌─────────────┐  ┌─────────────────┐   │  │
│   │  │  Handlers   │  │  Services layer  │   │  │
│   │  │ (commands / │→ │ (business logic) │   │  │
│   │  │  callbacks) │  └────────┬────────┘   │  │
│   │  └─────────────┘           │             │  │
│   │                    ┌───────▼────────┐    │  │
│   │                    │  Repository    │    │  │
│   │                    │  layer (DB)    │    │  │
│   └────────────────────┴───────┬────────┘   │  │
│                                │             │  │
└────────────────────────────────┼─────────────┘  │
                                 │
┌────────────────────────────────▼────────────────┐
│           PostgreSQL (local / AWS RDS)            │
│              Migrations via Flyway                │
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

## Configuration Management

Configuration is managed through environment variables to ensure security and environment-specific settings.

### Local Development (.env.local)
For DEV environment, create a `.env.local` file in the project root with the following variables:

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_dev_bot_token_here

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/e18_meter_reader_dev

# Logging
LOG_LEVEL=INFO
```

**Note:** `.env.local` is ignored by `.gitignore` and should never be committed.

### Production Environments (UAT/PROD)
In cloud environments, configuration is managed via AWS Systems Manager (SSM) Parameter Store or Secrets Manager:
- `/e18-meter-reader/{env}/telegram-bot-token`
- `/e18-meter-reader/{env}/database-url`
- `/e18-meter-reader/{env}/log-level`

### Example Configuration File (.env.example)
A template `.env.example` is provided in the repository with placeholder values for reference.

---

## Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Language | Python 3.11+ | PTB library ecosystem, OCR libraries, broad community |
| Bot framework | `python-telegram-bot` v20+ (async) | Mature, well-documented, native async support |
| Database | PostgreSQL 15 | Same engine in DEV and PROD; strong JSON support for future flexibility |
| ORM / DB access | Tortoise ORM (async) + asyncpg | Async Python PostgreSQL stack, native async support for PTB |
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
│   ├── texts.py           # ALL user-facing strings: button labels, messages, prompts
│   └── main.py            # Bot entry point, Application setup
├── migrations/            # Flyway SQL migration files (V1__init.sql, etc.)
├── tests/
│   ├── unit/
│   └── integration/
├── scripts/
│   ├── db_deploy_linux.sh
│   └── db_deploy_windows.ps1
├── docs/
│   ├── scope.md
│   ├── design.md
│   ├── tracker.md
│   └── handoff.md
├── .env.example           # Template for local env vars
├── main.py                # Main entry point
├── pyproject.toml
├── .gitignore
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
| source | VARCHAR | `numeric` (button pad), `photo` |
| photo_file_id | VARCHAR | Telegram file_id; required when source=photo |
| notes | TEXT | Optional |

### `apartments` — additional column

The `apartments` table includes a `photo_required` flag:

| Column | Type | Notes |
|---|---|---|
| ... | | (see above) |
| photo_required | BOOLEAN | If TRUE, tenant must upload a photo; numeric-only submission is rejected |

**Notes:**
- When `photo_required = TRUE` for an apartment, the submit reading flow requires a photo upload. Numeric pad entry is still shown (to capture the value), but submission is blocked until a photo is attached.
- Grayhounds and Administrators are exempt from the `photo_required` constraint — they can always submit numerically.

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

## Menu Structure

### `/start` — role-based main menu

**New user (no role assigned):**
- Request for meter submeeting
- About Bot

**Tenant:**
- Submit Reading
- View Own Readings / Chart
- Request for Meter Submeeting
- About Bot

**Grayhound:**
- Submit Reading
- Export Readings (CSV)
- View Readings / Chart
- Request for Meter Submeeting
- About Bot

**Administrator:**
- Submit Reading
- Export Readings (CSV)
- View Own Readings / Chart
- Requests
- Assign / Revoke Roles
- Add / Deactivate Users
- Manage Apartment List
- About Bot

**Notes:**
- A user holding both Administrator and Grayhound roles sees the Administrator menu (highest-privilege menu wins)
- Menu is rebuilt on each `/start` based on active roles at that moment

---

## Key Flows

### 1. User onboarding

```
User sends /start
  → Bot checks if user exists in DB
    → New user: Bot registers user, sends notification to Administrator, shows new-user menu
    → Existing user with no active role: Bot shows "pending approval" message + new-user menu
    → Existing user with active role: Bot shows role-appropriate main menu
```

### 2. About Bot

```
User taps "About Bot"
  → Bot sends static info message (text from texts.py)
  → [Back] button → returns to main menu
```

### 3. Request for Meter Submeeting

```
User taps "Request for Meter Submeeting"
  → Bot shows hint message explaining what to include (text from texts.py)
  → Bot shows inline numeric pad for the user to compose their request
     (or: a pre-defined set of reason buttons + optional free comment — TBD)
  → User submits request → Bot forwards request to Administrator(s)
  → Bot confirms: "Your request has been sent."
  → [Back] button → returns to main menu
```

> ⚠️ **Open question:** Is the request a free-text message (exception to inline-only rule) or a structured form via buttons? To be decided before Phase 1 implementation.

### 4. Submit Reading — Tenant (single apartment)

```
Tenant taps "Submit Reading"
  → Bot checks for existing reading in current month
    → Reading exists: Bot shows existing value + "Already submitted this month. Replace?" [Yes] [No]
    → No reading: proceed
  → Bot confirms apartment (pre-filled, no selection needed)
  → Bot shows inline numeric pad (digits 0–9, decimal point, backspace, confirm)
  → Tenant enters value digit by digit; current value displayed above pad
  → Tenant taps [Confirm]
    → If apartment.photo_required = TRUE:
        Bot shows "Please upload a photo of your meter"
        Tenant uploads photo → Bot shows value + photo thumbnail + [Submit] [Cancel]
    → If apartment.photo_required = FALSE:
        Bot shows "Apartment 42 — 1234.5 kWh. Confirm?" [Submit] [Cancel]
  → Tenant taps [Submit] → Reading saved to DB (source: numeric or photo)
  → Bot shows success message + timestamp → [Back] to main menu
```

### 5. Submit Reading — Grayhound (any apartment)

```
Grayhound taps "Submit Reading"
  → Bot shows paginated apartment list (inline buttons, sorted by number)
  → Grayhound selects apartment
  → Bot checks for existing reading in current month
    → Reading exists: Bot shows existing value + "Already submitted this month. Replace?" [Yes] [No]
    → No reading: proceed
  → Bot shows inline numeric pad
  → Grayhound enters value → [Confirm]
  → Bot shows "Apartment 42 — 1234.5 kWh. Confirm?" [Submit] [Cancel]
  → Grayhound taps [Submit] → Reading saved to DB
  → Bot shows success + [Submit Another] [Back to Menu]
```

> Note: `photo_required` constraint does NOT apply to Grayhounds or Administrators.

### 6. Export Readings (CSV) — Grayhound / Administrator

```
User taps "Export Readings (CSV)"
  → Bot shows paginated list of months with readings (e.g. "March 2026 — 94 apartments")
  → User selects a month (or "All time")
  → Bot generates CSV in memory, sends as document via sendDocument
  → [Back] button → returns to main menu
```

### 7. View Own Readings / Chart — Tenant / Administrator

```
Phase 1:
User taps "View Own Readings / Chart"
  → Bot generates CSV of own apartment readings
  → Bot sends CSV as document via sendDocument
  → [Back] button → returns to main menu

Phase 2:
  → Bot shows period selector (last month / last 3 months / all time)
  → Bot generates PNG chart, sends via sendPhoto
```

### 8. View Readings / Chart — Grayhound

```
To be delivered (Phase 2)
  → Will follow similar pattern to flow 7 but with apartment/building scope selection
```

### 9. Requests — Administrator

```
To be delivered
  → Administrator reviews pending submeeting requests from tenants/grayhounds
```

### 10. Assign / Revoke Roles — Administrator

```
To be delivered
  → Paginated user list → select user → view/edit roles → assign role + apartment + validity period
```

### 11. Add / Deactivate Users — Administrator

```
To be delivered
  → Manage user active status; deactivated users lose access
```

### 12. Manage Apartment List — Administrator

```
To be delivered
  → Add apartments, set photo_required flag, edit details
```

---

## UX Patterns

- **All navigation and input via inline buttons** — no slash commands beyond `/start`; meter values entered via an inline numeric pad (digits 0–9, decimal point, backspace, confirm)
- **All user-facing strings in `texts.py`** — button labels, messages, prompts, and error texts are never hardcoded inline; always imported from `bot/texts.py`
- **Confirmation step** before any write operation (reading submission, role change)
- **Pagination** for lists longer than 5 items (apartments, users)
- **Back button** on every screen — users can always return to the previous menu
- **Error messages** are user-friendly (text from `texts.py`) — technical details logged only
- **Session state** managed via `ConversationHandler` in PTB — state stored in memory (stateless across restarts; in-progress conversations reset on bot restart, which is acceptable)

---

## Handler Logging & Observability

### `@log_handler` Decorator

All Telegram bot handlers use the `@log_handler()` decorator from `bot/handlers/decorators.py` to provide comprehensive observability.

**Decorator Location:** `bot/handlers/decorators.py`

**Decorator Features:**

The `@log_handler()` decorator automatically logs:

1. **Handler execution events:**
   - Handler name (function name)
   - Start event with timestamp
   - End event with execution duration (ms)
   - Result or error status

2. **User/Chat information** (extracted from Update):
   - `user_id` — Telegram user ID
   - `username` — Telegram username
   - `first_name`, `last_name` — User display name
   - `chat_id`, `chat_type` — Chat metadata
   - `message_text` — First 50 chars of message (for truncation)
   - `callback_data` — Inline button callback ID (for debugging)

3. **Context information** (optional):
   - `user_data` — Conversation state dictionary
   - `chat_data` — Chat-scoped state
   - `args` — Command args (if present)

4. **Error handling:**
   - Full exception traceback logged on error
   - Handler name, execution duration, exception type, and message included in error log

**Usage:**

```python
from bot.handlers.decorators import log_handler

@log_handler()  # Default: log Update data
async def my_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello!")

@log_handler(include_context=True)  # Also log Context (use with caution)
async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass

@log_handler(include_context=False, include_update=False)  # Minimal logging
async def simple_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass
```

**Parameters:**
- `include_context` (bool, default False): If True, logs Context details (user_data, chat_data, args). Use sparingly to avoid logging sensitive information.
- `include_update` (bool, default True): If True, logs extracted user/chat/message data from Update.

**Log Output Example:**

```
[my_handler] START
[my_handler] User info: {'user_id': 123456789, 'username': 'john_doe', 'chat_id': 123456789, 'chat_type': 'private'}
[my_handler] END (duration: 0.123s, result: None)
```

**Applied Handlers:**
- ✅ `bot/handlers/common.py`: start, help_command, cancel_command, error_handler
- ✅ `bot/handlers/admin.py`: admin_menu
- ✅ `bot/handlers/tenant.py`: tenant_menu
- ✅ `bot/handlers/grayhound.py`: grayhound_menu

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

## Implementation Status

### Created Files (As of 2026-04-03)

**Models & Database:**
- ✅ `bot/models.py` — Tortoise ORM model definitions (5 models: User, Apartment, Meter, UserRole, Reading)
- ✅ `bot/database.py` — DatabaseManager with async init/close/health_check
- ✅ `migrations/V1__initial_schema.sql` — Flyway migration with schema (users, apartments, meters, user_roles, readings)

**Repository Layer:**
- ✅ `bot/repositories/base.py` — BaseRepository generic async CRUD
- ✅ `bot/repositories/users.py` — UsersRepository (queries, deactivation)
- ✅ `bot/repositories/apartments.py` — ApartmentsRepository (CRUD)
- ✅ `bot/repositories/meters.py` — MetersRepository (apartment-scoped)
- ✅ `bot/repositories/roles.py` — UserRolesRepository (time-scoped role logic)
- ✅ `bot/repositories/readings.py` — ReadingsRepository (submission, history)

**Services Layer (Business Logic):**
- ✅ `bot/services/reading.py` — ReadingService (validation, submission, history)
- ✅ `bot/services/roles.py` — RoleService (assignment, permission checks, privilege hierarchy)
- ✅ `bot/services/export.py` — ExportService (CSV export, role-based filtering)

**Handlers Layer:**
- ✅ `bot/handlers/common.py` — Shared handlers (/start, /help, /cancel, errors) with @log_handler decorator
- ✅ `bot/handlers/decorators.py` — Handler logging decorator with user/chat extraction and context logging (100 lines)
- 🔵 `bot/handlers/admin.py` — Administrator-only flows (stub with @log_handler)
- 🔵 `bot/handlers/tenant.py` — Tenant flows (stub with @log_handler)
- 🔵 `bot/handlers/grayhound.py` — Grayhound flows (stub with @log_handler)

**UI & Configuration:**
- ✅ `bot/texts.py` — All user-facing strings (messages, button labels, prompts)
- ✅ `bot/keyboards.py` — InlineKeyboardMarkup builders (menus, numeric pad, confirmations)
- ✅ `.env.example` — Template for local environment variables

**Tests:**
- ✅ `tests/test_main.py` — Role-based menu tests (6/6 passing)
- ✅ `tests/test_repositories.py` — Repository initialization tests (8/8 passing)
- 🔵 `tests/test_services.py` — Service layer tests (pending)
- 🔵 `tests/test_handlers.py` — Handler integration tests (pending)

### Pending Work

**Handler Implementation:**
- Implement callback handlers in handlers/{admin,tenant,grayhound}.py
- Integrate services and repositories into handler workflows
- Add state management for multi-step flows (reading submission, role assignment)

**Database Integration in Main:**
- Initialize DatabaseManager in main() startup
- Integrate role/user queries into /start handler
- Connect menu builder to actual database role lookups

**Service Integration:**
- Wire services into handlers
- Add business logic for reading validation, role checks, exports

---

## Pre-commit Hooks

The project uses the `pre-commit` framework to automate code quality checks before every commit.

### Installation

```bash
# Install pre-commit framework
pip install pre-commit

# Set up git hooks (run once per clone)
pre-commit install

# Verify installation
pre-commit run --all-files
```

### Available Hooks

| Hook | Purpose | Auto-fix? |
|---|---|---|
| `ruff check` | Linting — detects unused imports, undefined names, complexity | Yes (with --fix) |
| `black` | Code formatting — enforces consistent style (88-char lines) | Yes |
| `trailing-whitespace` | Removes trailing whitespace | Yes |
| `end-of-file-fixer` | Ensures files end with newline | Yes |
| `check-yaml` | Validates YAML syntax | No |
| `check-json` | Validates JSON syntax | No |
| `detect-private-key` | Scans for accidentally committed secrets | No |
| `flake8` | Additional code quality checks | Partial |

### Local Usage

**Run all checks manually (Windows):**
```powershell
.\scripts\pre-commit.ps1
```

**Auto-fix issues before commit:**
```powershell
.\scripts\pre-commit.ps1 -Fix
```

**Run specific hook:**
```bash
pre-commit run ruff --all-files
pre-commit run black --all-files
pre-commit run pytest --all-files
```

**Skip hooks on a single commit (NOT RECOMMENDED):**
```bash
git commit --no-verify
```

### CI Integration

Pre-commit hooks are also run in CI/CD pipelines (see deployment scripts). All PRs must pass all hooks before merge.

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

1. **Create environment file:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your actual values
   ```

2. **Run local deployment script:**
   ```bash
   bash ./scripts/db_deploy_linux.sh
   ```

3. **Run the bot:**
   ```bash
   python main.py
   ```

**Notes:**
- `db_deploy_linux.sh` loads `.env.local` and derives Flyway settings from `DATABASE_URL`.
- `flyway.conf` is optional; the script prefers environment-derived Flyway config.
- If Flyway CLI is not installed, install it or run Flyway via Docker.

**Prerequisites:**
- Python 3.11+
- PostgreSQL 15
- Flyway CLI (for migrations) or Docker
- Telegram bot token from @BotFather

### UAT / PROD (Linux EC2)

```bash
./scripts/db_deploy_linux.sh [uat|prod]
# Script responsibilities:
#   1. Pull latest code from Git
#   2. Install/update dependencies (pip)
#   3. Run Flyway migrations against target DB
#   4. Restart systemd service
```

### Windows (developer machine UAT push)

```powershell
.\scripts\db_deploy_windows.ps1 [uat|prod]
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
| 2026-04-02 | 1.1 | Added menu structure, full flow for all roles, grayhound reading flow, photo_required per apartment, texts.py, duplicate reading guard | AI-assisted |
