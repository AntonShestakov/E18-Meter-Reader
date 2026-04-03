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
  - pyproject.toml created with python-telegram-bot, pytest, ruff, black, sqlalchemy, psycopg2, flyway (or equivalent)
  - Python virtual environment configured and activated
  - Basic dependencies installed and importable
- Evidence: Project structure created, pyproject.toml added, venv activated, imports successful
- Dependencies: None
- Notes: Use Python 3.11+, local PostgreSQL for dev

---

## Backlog (Not Started)

## T-002 — Design and implement database schema
- Owner: Developer
- Status: 🔵 0% | Dates: started 2026-04-02, expected by 2026-04-03, last touched 2026-04-02
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Tech Stack (PostgreSQL, Flyway)
- Acceptance criteria:
  - Flyway migration scripts created for tables: users, roles, role_assignments, readings
  - Schema supports three roles with time-scoped assignments
  - Local PostgreSQL database set up and migrations applied
  - Basic repository layer classes created for DB access
- Evidence: Will be added when started
- Dependencies: T-001
- Notes: Use SQLAlchemy Core for queries

## T-003 — Implement core PTB skeleton
- Owner: Developer
- Status: ⚪ 0% | Dates: planned start 2026-04-03, expected by 2026-04-04
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Architecture Overview
- Acceptance criteria:
  - main.py created with PTB Application and polling setup
  - /start command handler implemented with inline button menu
  - Basic error handling and logging configured
  - Bot responds to /start with role selection buttons
- Evidence: Will be added when started
- Dependencies: T-001
- Notes: Use async PTB v20+

## T-004 — Implement user role management
- Owner: Developer
- Status: ⚪ 0% | Dates: planned start 2026-04-04, expected by 2026-04-05
- Scope: scope.md § Phased Scope Phase 1
- Design: design.md § Project Structure (handlers/admin.py)
- Acceptance criteria:
  - Administrator can assign roles (Tenant, Grayhound) to users with start/end dates
  - Role assignment stored in database with validity periods
  - Admin UI via inline buttons to manage users and roles
  - Role checks implemented in handlers
- Evidence: Will be added when started
- Dependencies: T-002, T-003
- Notes: Roles scoped to time periods

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
