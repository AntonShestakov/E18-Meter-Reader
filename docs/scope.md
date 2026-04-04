# scope.md — Power Meter Reading Telegram Bot

**Version:** 1.1
**Last updated:** 2026-04-01
**Status:** Active — defines project boundaries and success criteria

---

## Purpose

This document defines what we're building, why we're building it, what success looks like, and what's explicitly out of scope for the Power Meter Reading Telegram Bot project.

---

## Vision

Build a Python Telegram Bot (PTB) that reduces the time spent on, and simplifies, the process of electricity meter reading in a multi-family residential building with 100+ apartments.

The bot replaces manual collection of meter readings with a structured, role-based, inline-button-driven workflow. Collected data is persisted in a database and exportable to CSV. The bot provides consumption charts per apartment and per building.

Three user roles exist: **Administrator** (manages accounts and role assignments), **Grayhound** (building-level role responsible for all meters in the building; an Administrator may also hold this role), and **Tenant** (reads meters for their own apartment only). All roles interact exclusively via Telegram inline buttons — no free-text data entry.

---

## Goals (what success looks like)

- Meter reading workflow for a 100+ apartment building is fully handled by the PTB
- All user interactions are inline-button-driven; no manual text input required from users
- Three roles are supported: Administrator, Grayhound, Tenant — with role assignments scoped to a time period
- Tenants can submit meter readings for their apartment (manual input or photo with OCR)
- Grayhounds can submit and view readings for any apartment in the building
- Administrators can manage user accounts, assign/revoke roles, and set role validity periods
- Collected readings are stored in a PostgreSQL database
- Data can be exported to CSV from the bot
- Power consumption charts are available per apartment and per building
- The bot runs as a polling process deployed to AWS EC2; the database runs on AWS RDS (PostgreSQL)
- Three bot instances exist: DEV (local), UAT, PROD — each with its own Telegram bot token
- Two AWS environments exist: UAT and PROD
- CI/CD is implemented via shell scripts (Linux and Windows) and Flyway for database migrations
- All features are covered by automated test cases with ≥ 80% coverage on changed lines

---

## Success Metrics (SLOs)

- PR lead time (first commit → merge): ≤ 3 days (p50), ≤ 7 days (p90)
- Changed-lines test coverage: ≥ 80% on merged PRs
- Secret/SCA scans: 0 critical findings on `main`
- Session continuity: 100% of AI sessions end with a valid `handoff.md`
- Rework rate (revert or fix-forward within 48h): ≤ 10%
- Bot availability (UAT/PROD): ≥ 99% uptime during active reading periods

---

## Phased Scope

### Phase 1 — MVP (local / DEV bot)

- Core PTB skeleton with inline-button-only UX
- Three roles: Administrator, Grayhound, Tenant
- Role assignment by Administrator, scoped to a time period
- Tenant meter reading flow (manual numeric input via inline prompts)
- Grayhound reading flow (any apartment)
- SQLite or local PostgreSQL for dev; schema managed by Flyway
- CSV export of collected readings
- Basic unit tests for core flows

### Phase 2 — Full Features

- Power consumption charts per apartment and per building
- Meter reading via photo + OCR (apartment number and meter value recognition)
- Full test coverage ≥ 80% on all changed lines
- Administrator account management UI (add/remove users, assign roles)

### Phase 3 — Cloud Deployment & CI/CD

- AWS EC2 deployment (PTB as systemd daemon / polling)
- AWS RDS PostgreSQL (UAT and PROD)
- DEV / UAT / PROD bot instances with separate tokens
- CI/CD deployment scripts for Linux and Windows
- Flyway migrations integrated into deployment pipeline
- Environment-specific configuration management

---

## Out of Scope (explicitly will not do)

- Payment processing or billing for utilities
- Integration with utility company APIs or smart meters
- Multi-building support (single building only)
- Web dashboard or mobile app (Telegram is the sole interface)
- Gas or water meter reading (electricity only)
- Real-time notifications or scheduled reminders (may be revisited post-MVP)

---

## Constraints & Assumptions

- Single developer acting as PM, developer, and future Administrator
- AI assistant generates code and documentation; the human runs all commands and provides outputs
- Secrets (bot tokens, DB credentials) never leave the operator's local environment
- All source code versioned in Git with PR-based workflow
- Telegram Bot API polling mode only (no webhooks)
- Building has a fixed set of apartments; apartment list is seeded at setup
- OCR for photo reading is a Phase 2 feature and may use a third-party library (e.g., Tesseract or a cloud vision API)

---

## Stakeholders

| Stakeholder | Role | Responsibility |
|---|---|---|
| [Your name] | PM / Developer / future Administrator | Owns all decisions: scope, architecture, priorities, final approval |
| AI Assistant | Actor | Code generation, documentation drafts, debugging assistance, tradeoff analysis |
| Building residents | End users (Tenants) | Submit meter readings via bot |
| Building manager | End user (Grayhound) | Oversees all readings; may coincide with Administrator |

---

## Risks (initial)

- **Telegram API rate limits** → Mitigation: implement retry/backoff; stay within 30 messages/second per bot limit
- **OCR accuracy for meter photos** → Mitigation: Phase 2 feature; validate with real meter images before committing to library; provide manual fallback
- **AWS cost overruns** → Mitigation: use t3.micro EC2 and db.t3.micro RDS in UAT; set billing alerts
- **RDS connection management in polling bot** → Mitigation: use async connection pooling (Tortoise ORM built-in); validate under load
- **Solo developer bottleneck** → Mitigation: keep slices small (≤ 1 day), strict DoD, frequent handoff.md updates to preserve context
- **Scope creep into multi-building or notification features** → Mitigation: explicit Out of Scope section; revisit only after Phase 3 is complete

---

## Dependencies

| Dependency | Status | Owner | Risk |
|---|---|---|---|
| Telegram Bot API token (DEV) | To obtain | Developer | Low |
| Telegram Bot API tokens (UAT, PROD) | To obtain (Phase 3) | Developer | Low |
| AWS account with EC2 + RDS access | To set up (Phase 3) | Developer | Medium |
| OCR library selection (Tesseract / cloud API) | Pending (Phase 2) | Developer | Medium — accuracy unknown |
| Flyway CLI | To install | Developer | Low |
| Git repository | To create | Developer | Low |

---

## Milestones (target dates TBD)

| Milestone | Description | Target |
|---|---|---|
| M1 — Project setup | Repo, Flyway, local DB, bot skeleton running | TBD |
| M2 — Role & account flows | Admin, Grayhound, Tenant roles working end-to-end | TBD |
| M3 — Reading flow complete | Tenant and Grayhound reading flows + CSV export | TBD |
| M4 — Charts & OCR | Consumption charts + photo reading with OCR | TBD |
| M5 — Cloud deployment | UAT and PROD live on AWS with CI/CD scripts | TBD |

---

## Non-Goals

- This is not a utility billing or payment system
- This is not a general building management platform
- This is not a multi-tenant SaaS product
- This is not a real-time monitoring or alerting system

---

## Changelog

| Date | Version | Changes | Author |
|---|---|---|---|
| 2026-04-01 | 1.0 | Initial draft from template | [Name] |
| 2026-04-01 | 1.1 | Revised: phased scope, corrected roles, real risks/deps/stakeholders | AI-assisted |
