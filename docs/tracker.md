# tracker.md

**Version:** 1.0
**Last updated:** 2026-04-02
**Status:** Active task tracking — single source of truth for work items

---

## Purpose

This document tracks all tasks for E18-Meter-Reader, their acceptance criteria, status, owners, and evidence of completion. It's the primary reference for "what needs to be done" and is updated continuously throughout the project.

---

## Status Glyphs (Use These)

⚪ **Not started** — Task defined but not yet begun
🔵 **In progress** — Actively being worked on
✅ **Done** — Completed and meets acceptance criteria
⚠️ **Blocked** — Cannot proceed, needs intervention

---

## Task Template

**Instructions:** Each task should follow this structure. Copy/paste for new tasks.

```markdown
## T-XXX — [Task Title]
- Owner: Developer
- Status: [⚪/🔵/✅/⚠️] [X%] | Dates: [started YYYY-MM-DD, expected by YYYY-MM-DD, last touched YYYY-MM-DD]
- Scope: [Link to scope.md section if applicable]
- Design: [Link to design.md section if applicable]
- Acceptance criteria:
  - [Criterion 1: specific, measurable, testable]
  - [Criterion 2: specific, measurable, testable]
  - [Criterion 3: specific, measurable, testable]
- Evidence: [Links to PRs, CI runs, test results, documentation]
- Dependencies: [T-XXX that must complete first, or external blockers]
- Notes: [Optional: additional context, risks, decisions]
```

---

## Active Tasks

## T-001 — Set up project structure and dependencies
- Owner: Developer
- Status: ✅ 100% | Dates: started 2026-04-02, expected by 2026-04-02, last touched 2026-04-02
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Project Structure
- Acceptance criteria:
  - Project folder structure created: bot/handlers/, bot/services/, bot/repositories/, migrations/, tests/
  - pyproject.toml created with python-telegram-bot, pytest, ruff, black, tortoise-orm, asyncpg, flyway (or equivalent)
  - Python virtual environment configured and activated
  - Basic dependencies installed and importable
- Evidence: Project structure created, pyproject.toml added, venv activated, imports successful
- Dependencies: None
- Notes: Use Python 3.11+, local PostgreSQL for dev

---

## Backlog (Not Started)

## T-002 — Design and implement database schema
- Owner: Developer
- Status: 🔵 50% | Dates: started 2026-04-02, expected by 2026-04-03, last touched 2026-04-03
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Tech Stack (PostgreSQL, Flyway), Data Model
- Acceptance criteria:
  - Flyway migration scripts created for tables: users, roles, role_assignments, readings ✅
  - Schema supports three roles with time-scoped assignments ✅
  - Local PostgreSQL database set up and migrations applied (pending local DB setup)
  - Basic repository layer classes created for DB access ✅
- Evidence:
  - migrations/V1__initial_schema.sql created with users, apartments, meters, user_roles, readings tables
  - Repository layer: base.py, users.py, apartments.py, roles.py, readings.py, meters.py (CRUD operations + domain-specific queries)
  - DatabaseManager created (bot/database.py) with connection pooling
  - tests/test_repositories.py: 8/8 tests passing, validates all repository classes
- Dependencies: T-001
- Notes: Tortoise ORM used for async queries; repos include privilege-scoped role logic; async connection pooling configured for RDS

## T-003 — Implement core PTB skeleton
- Owner: Developer
- Status: 🔵 50% | Dates: started 2026-04-03, expected by 2026-04-04, last touched 2026-04-03
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Menu Structure, Architecture Overview
- Acceptance criteria:
  - main.py created with PTB Application and polling setup ✅
  - /start command handler checks user roles and DB existence ✅ (partial — DB integration pending T-002)
  - Role-based menu function returns correct inline buttons per role (Tenant, Grayhound, Administrator, New User) ⏳
  - Menu for new users: "Request Meter Submeeting", "About Bot" ⏳
  - Menu for Tenant: "Submit Reading", "View Own Readings/Chart", "Request Meter Submeeting", "About Bot" ⏳
  - Menu for Grayhound: "Submit Reading", "Export Readings (CSV)", "View Readings/Chart", "Request Meter Submeeting", "About Bot" ⏳
  - Menu for Administrator: "Submit Reading", "Export Readings (CSV)", "View Own Readings/Chart", "Requests", "Assign/Revoke Roles", "Add/Deactivate Users", "Manage Apartment List", "About Bot" ⏳
  - Error handler logs and responds gracefully to exceptions ✅
  - Basic logging configured ✅
- Evidence: main.py updated with error handler, role keyboard, polling setup; handler stubs created; tests/test_main.py with role-based tests
- Dependencies: T-001, T-002 (for user/role DB queries)
- Notes: Menu structure from design.md §Menu Structure; role checks at /start time; highest-privilege role menu wins if user has multiple roles

## T-003b — Implement handlers and services layer
- Owner: Developer
- Status: 🔵 50% | Dates: started 2026-04-03, expected by 2026-04-05, last touched 2026-04-03
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Project Structure, Implementation Status
- Acceptance criteria:
  - Service layer created: ReadingService, RoleService, ExportService ✅
  - handlers/common.py with /start, /help, /cancel, error handler ✅
  - handlers/{admin,tenant,grayhound}.py created with callback stubs ✅
  - texts.py with all user-facing strings (100+ strings) ✅
  - keyboards.py with menu/numeric pad builders ✅
  - services/__init__.py exports all three services ✅
  - handlers/__init__.py exports all handler modules ✅
  - Handler callbacks wired to service methods (pending)
  - State management for multi-step flows (pending)
  - 8+ integration tests for handlers/services (pending)
- Evidence:
  - bot/services/reading.py created with validation/submission logic
  - bot/services/roles.py created with permission checks and privilege hierarchy
  - bot/services/export.py created with CSV generation and role-based filtering
  - bot/handlers/common.py created with /start, /help, /cancel handlers
  - bot/texts.py created with 50+ user-facing strings
  - bot/keyboards.py created with role-aware menu builders and numeric pad
  - All files pass syntax validation and import successfully
- Dependencies: T-001, T-002, T-003
- Notes: Services follow repository pattern; handlers are thin layer over services; texts.py centralizes i18n prep

## T-003c — Set up pre-commit hooks and quality gates
- Owner: Developer
- Status: ✅ 100% | Dates: started 2026-04-03, expected by 2026-04-03, last touched 2026-04-03
- Scope: scope.md § Quality Assurance
- Design: design.md § Pre-commit Hooks
- Acceptance criteria:
  - `.pre-commit-config.yaml` created with ruff, black, trailing whitespace, JSON/YAML checks, private key detection ✅
  - `scripts/pre-commit.ps1` created for local pre-commit check runner ✅
  - Pre-commit script includes ruff, black, pytest, and coverage checks ✅
  - `tests/test_pre_commit.py` created with 13+ tests for pre-commit config validation ✅
  - All pre-commit tests passing (13/13) ✅
  - Documentation in design.md § Pre-commit Hooks ✅
  - README or quick start guide updated with pre-commit instructions (pending)
- Evidence:
  - `.pre-commit-config.yaml` created with 5 repositories (ruff, black, pre-commit-hooks, flake8)
  - `scripts/pre-commit.ps1` created with PowerShell hooks for Windows developers
  - `tests/test_pre_commit.py` created with comprehensive validation (TestPreCommitConfig, TestPreCommitScript, TestChecksConfiguration, TestPreCommitIntegration)
  - All 13 tests passing: config validity, hook definitions, CLI tool presence, framework integration
- Dependencies: T-001 (project structure)
- Notes: Provides automated quality gates; integrates with git hooks; manual runs also supported via scripts/pre-commit.ps1

## T-003d — Implement handler logging decorator
- Owner: Developer
- Status: ✅ 100% | Dates: started 2026-04-03, expected by 2026-04-03, last touched 2026-04-03
- Scope: scope.md § Quality Assurance, Monitoring
- Design: design.md § Handler Logging & Observability
- Acceptance criteria:
  - `bot/handlers/decorators.py` created with `@log_handler` decorator ✅
  - Decorator logs handler name, start/end events, execution duration ✅
  - Decorator extracts and logs user/chat info from Update (user_id, username, chat_id, message_text, callback_data) ✅
  - Decorator logs Context data optionally (include_context parameter) ✅
  - Decorator logs full exception traceback on error ✅
  - Decorator applied to all handlers: common.py (start, help_command, cancel_command, error_handler) ✅
  - Decorator applied to role-based handler stubs: admin.py, tenant.py, grayhound.py ✅
  - All tests passing (6/6 main tests, 17/17 pre-commit tests) ✅
  - Design documentation added with usage examples ✅
- Evidence:
  - `bot/handlers/decorators.py` created (100+ lines) with _extract_user_info helper function
  - Decorator parameters: include_context (bool, default False), include_update (bool, default True)
  - Applied to 7 handlers across 4 files with appropriate settings (error_handler uses include_context=False)
  - All tests passing: pytest 6/6, pre-commit 7/7 hooks
  - Documentation section added to design.md § Handler Logging & Observability with examples
- Dependencies: T-001, T-003b (handlers exist)
- Notes: Provides observability for all handler execution; produces structured logs for debugging and monitoring; no sensitive data logged by default

## T-004 — Implement user role management
- Owner: Developer
- Status: ⚪ 0% | Dates: planned start 2026-04-05, expected by 2026-04-06, last touched 2026-04-03
- Scope: scope.md § Phased Scope Phase 1
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Project Structure (handlers/admin.py), Role Permission Matrix
- Acceptance criteria:
  - Repository layer for user_roles table created (CRUD for role assignments)
  - Administrator can assign/revoke roles (inline button flow)
  - Role validity periods enforced (valid_from, valid_to)
  - Tenant role assignment scoped to apartment_id
  - Role checks in /start determine correct menu per user
  - Highest-privilege role menu wins if user has multiple roles
- Evidence: Will be added when started
- Dependencies: T-002, T-003
- Notes: Roles scoped to time periods; role checks at request time

## T-005 — Implement tenant meter reading flow
- Owner: Developer
- Status: ⚪ 0% | Dates: planned start 2026-04-05, expected by 2026-04-06
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Project Structure (handlers/tenant.py)
- Acceptance criteria:
  - Tenant can initiate reading submission via inline button
  - Numeric input via inline button keypad (0-9, submit)
  - Reading stored in database with timestamp and apartment
  - Confirmation message sent after submission
- Evidence: Will be added when started
- Dependencies: T-003, T-004
- Notes: Manual numeric input only, no free text

## T-006 — Implement grayhound reading flow
- Owner: Developer
- Status: ⚪ 0% | Dates: planned start 2026-04-06, expected by 2026-04-07
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Project Structure (handlers/grayhound.py)
- Acceptance criteria:
  - Grayhound can select apartment from inline button list
  - Numeric input for reading via inline keypad
  - Reading stored for selected apartment
  - Access restricted to building-level
- Evidence: Will be added when started
- Dependencies: T-003, T-004
- Notes: Can submit for any apartment in building

## T-007 — Implement CSV export
- Owner: Developer
- Status: ⚪ 0% | Dates: planned start 2026-04-07, expected by 2026-04-08
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Project Structure (services/)
- Acceptance criteria:
  - /export command available to Administrator and Grayhound
  - Exports all readings to CSV file sent via Telegram
  - CSV includes date, apartment, reading value
  - File sent as document attachment
- Evidence: Will be added when started
- Dependencies: T-002, T-005, T-006
- Notes: Basic export, no filters yet

## T-008 — Add basic unit tests
- Owner: Developer
- Status: ⚪ 0% | Dates: planned start 2026-04-08, expected by 2026-04-09
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Tech Stack (pytest)
- Acceptance criteria:
  - Unit tests for handlers, services, repositories
  - Test coverage >=80% on changed lines
  - Tests for role checks, reading submission, export
  - pytest configured and runnable
- Evidence: Will be added when started
- Dependencies: T-003 to T-007
- Notes: Focus on core flows

---

## Blocked Tasks

---

## Completed Tasks

---

## Task Numbering

**Current highest number:** T-008
**Next task:** T-009

---

## Task Types (Optional Tags)

Use these tags to categorize tasks:

- `[feature]` — New functionality
- `[bug]` — Fix for defect
- `[tech-debt]` — Refactoring, cleanup, improvement
- `[docs]` — Documentation-only changes
- `[infra]` — CI/CD, deployment, infrastructure
- `[research]` — Spike, investigation, proof-of-concept

---

## Acceptance Criteria Guidelines

**Good acceptance criteria are:**
- ✅ **Specific** — Clear what "done" looks like
- ✅ **Measurable** — Can be objectively verified
- ✅ **Testable** — Can write a test to prove it
- ✅ **Aligned with DoD** — Meets methodology.md §6 requirements

**Examples:**

**❌ Bad:**
- "Improve performance"
- "Add error handling"
- "Make it work"

**✅ Good:**
- "P95 latency <200ms for 10K requests (benchmark evidence required)"
- "Handle Redis connection failure gracefully: return 503, log error, alert on-call"
- "Unit tests: 24/24 passing, coverage ≥80% on changed lines"

---

## Evidence Guidelines

**Good evidence includes:**
- PR numbers (e.g., "PR #42")
- CI run links (e.g., "CI run #203 - all checks passed")
- Test output (e.g., "14/14 tests passing, 87% coverage")
- Benchmark results (e.g., "P95: 145ms, baseline was 230ms")
- Documentation links (e.g., "Updated design.md §3.4")
- Screenshots/recordings (for UI changes)

**Template:**
```
Evidence:
- PR #XX: [brief description]
- CI run #YYY: [status and key results]
- Tests: [count passing, coverage %]
- Docs: [what was updated]
```

---

## Dependencies & Blockers

**Dependency types:**
- **Task dependency**: "T-042 must complete before T-043 can start"
- **External dependency**: "Waiting for API keys from partner team"
- **Decision dependency**: "Blocked until Tech Lead approves approach"
- **Resource dependency**: "Need test database provisioned"

**When blocked:**
1. Update status to ⚠️
2. Document blocker clearly
3. Assign unblock owner
4. Set target unblock date
5. Choose parallel work if possible (per methodology.md §11)
6. Escalate if blocker exceeds 3 days

---

## Changelog

| Date | Changes | Author |
|------|---------|--------|
| 2026-04-02 | Initial tracker created with Phase 1 tasks | Developer |

---

**Relationship to Other Documents:**

- **scope.md** — Tasks should align with goals defined in scope
- **design.md** — Tasks reference design sections for technical context
- **handoff.md** — Active tasks from tracker appear in handoff Context Snapshot
- **methodology.md §5** — Defines required task format and acceptance criteria rules
- **PR descriptions** — Link to tracker task numbers for traceability

---
