# handoff.md (canonical schema v1.1)

## Context Snapshot
- **Project Stage:** Phase 1 MVP — Core infrastructure complete, handlers/services layer 75% done
- **Database:** Local PostgreSQL 15 running with Flyway migrations applied; all 5 ORM models functional
- **Bot Framework:** Python-Telegram-Bot v20.x with async handlers; /start command fully integrated with DB role checking
- **Code Quality:** Pre-commit hooks (7/7 passing), logging decorator on all handlers, unit tests (23/23 passing)
- **Architecture:** 3-layer (handlers → services → repositories) fully async; DatabaseManager in app lifecycle
- **Key Completion:** T-001 (100%), T-002 (100%), T-003 (75%), T-003b (50%), T-003c (100%), T-003d (100%)

## Active Task(s)
- **T-003:** Implement core PTB skeleton — Status: 🔵 75% — /start now checks DB for user existence, creates new users, retrieves active roles, displays role-appropriate menu. Database integration complete; role hierarchy working.
- **T-003b:** Implement handlers and services layer — Status: 🔵 50% — Services (ReadingService, RoleService, ExportService) created; handlers common.py wired to start; logging decorator applied; pending: handler callbacks, state management, integration tests.

## Decisions Made
- **Single menu source:** Consolidated `create_menu_for_role()` from main.py → `build_main_menu_for_role()` in keyboards.py (DRY principle)
- **Handler logging:** Created `@log_handler()` decorator in bot/handlers/decorators.py with user/chat extraction, optional context logging, execution timing
- **Database lifecycle:** DatabaseManager initialization moved to `post_init()` in main.py; repositories and services stored in `application.bot_data` for handler access
- **Role checking:** /start now queries UsersRepository and RoleService; new users auto-registered in DB

## Changes Since Last Session
- **bot/handlers/decorators.py** (+110 LOC): New file with @log_handler decorator and _extract_user_info helper
- **bot/handlers/common.py** (±20 LOC): start() now queries DB for user existence and role; cancel_command() retrieves actual role
- **bot/handlers/{admin,tenant,grayhound}.py** (±3 LOC each): Added @log_handler decorator to all stubs
- **main.py** (±30 LOC): DatabaseManager, repositories, services initialization in post_init(); bot_data context setup
- **bot/keyboards.py** (±10 LOC): Fixed button constants (BUTTON_VIEW_OWN_READINGS for tenant/admin, BUTTON_VIEW_READINGS for grayhound)
- **docs/design.md** (+100 LOC): § Handler Logging & Observability section with usage examples
- **docs/tracker.md** (±50 LOC): Updated T-002 → ✅ 100%, T-003 → 🔵 75%, added T-003d → ✅ 100%

## Validation & Evidence
- **Unit tests:** 23/23 passing (6 main, 17 pre-commit) — see tests/test_main.py, tests/test_pre_commit.py
- **Code quality:** All 7 pre-commit hooks passing (ruff, black, trailing whitespace, EOF, YAML/JSON, secrets, flake8)
- **Imports:** All dependencies resolve correctly; database services initialize without error
- **Manual validation:** /start handler successfully queries DB (UsersRepository.get_by_telegram_id), creates users, retrieves roles (RoleService.get_highest_privilege_role)

## Risks & Unknowns
- **Multi-role privilege:** Highest-privilege role menu wins — implementation correct, but untested with real multiple role assignments. Owner: Developer. Review: 2026-04-05.
- **State management:** Conversation state not yet implemented; multi-step flows will reset on bot restart. Owner: Developer. Review: 2026-04-05 (pending T-003b callback wiring).
- **Error handling in handlers:** Try/except comprehensive, but graceful fallback to None role not fully tested with DB connection failures. Owner: Developer. Review: 2026-04-05.

## Next Steps
1. **T-004 — Implement user role management** (callback handlers in handlers/admin.py for role assignment flows; ~1-2 days)
2. **T-005 — Implement tenant meter reading flow** (numeric keypad, submission, DB storage; ~1-2 days)
3. **T-006 — Implement grayhound reading flow** (apartment selector, numeric input, building-scoped; ~1-2 days)

## Status Summary
- 🔵 **70%** (Phase 1 Core: Database + infrastructure complete; handlers + services layer 50-75% done; blocking feature work: T-004/T-005/T-006 ready to start)
