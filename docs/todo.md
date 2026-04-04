# todo.md

**Session Date:** 2026-04-03
**Time Budget:** ~4 hours
**Session Goal:** Complete database integration in handlers, establish logging framework, consolidate menu builders

---

## Purpose

This document contains the **session-specific subset** of tasks from `tracker.md` that will be worked on in this session. It's the bounded, manageable work plan that fits within:
- AI's context window (can be fully loaded and reasoned about)
- Human's time budget (typically 1-3 hours)
- A single coherent goal (one feature, one fix, one investigation)

**Use this when:**
- Starting a new session (select tasks from tracker.md)
- AI needs to know "what are we working on RIGHT NOW"
- You want to adjust priorities before engaging AI

---

## Instructions for Use

1. **Before each session:** Copy relevant tasks from `tracker.md`
2. **Adjust priorities:** Reorder based on current needs, dependencies, blockers
3. **Set realistic scope:** Better to complete 1 task fully than start 3 and finish none
4. **Review with AI:** AI reads this to understand session focus
5. **After session:** Update `tracker.md` with progress, create fresh `todo.md` for next session

---

## Active Tasks for This Session (COMPLETED)

### T-003d — Implement handler logging decorator ✅

**From tracker.md:**
- Acceptance criteria:
  - `bot/handlers/decorators.py` created with `@log_handler` decorator ✅
  - Decorator logs handler name, start/end events, execution duration ✅
  - Decorator extracts and logs user/chat info from Update ✅
  - Decorator logs Context data optionally ✅
  - Decorator applied to all handlers (common.py, admin.py, tenant.py, grayhound.py) ✅
  - All tests passing (23/23) ✅
  - Design documentation added ✅

**Session-specific notes:**
- Created @log_handler decorator with comprehensive logging
- Supports include_context and include_update parameters
- Applied to 7 handlers across 4 files
- Zero security concerns (no sensitive data logged by default)

**Progress:**
- ✅ Completed fully

---

### T-003 — Implement core PTB skeleton (ADVANCED 50% → 75%)

**From tracker.md:**
- Acceptance criteria:
  - /start handler checks user roles and DB existence ✅
  - Role-based menu returns correct buttons per role ✅
  - Error handler logs and responds gracefully ✅
  - Database integration complete: queries UsersRepository, RoleService ✅
  - New user auto-registration working ✅
  - Highest-privilege role menu selection working ✅

**Session-specific notes:**
- Consolidated menu builders to single source (keyboards.py)
- start() now queries DB for user existence and role
- DatabaseManager initialization in post_init()
- Services and repos stored in application.bot_data for handler access

**Progress:**
- ✅ From 50% → 75% complete
- Pending: Integration tests with real database operations

---

## Next Session Tasks (Future Work)

### T-004 — Implement user role management (READY TO START)

**From tracker.md:**
- Acceptance criteria:
  - Administrator can assign/revoke roles (inline button flow)
  - Role validity periods enforced (valid_from, valid_to)
  - Tenant role assignment scoped to apartment_id
  - Role checks in /start determine correct menu per user ✅ (already done)
  - Highest-privilege role menu wins ✅ (already done)

**Session-specific notes:**
- RoleService already created with assign_role(), revoke_role(), get_highest_privilege_role()
- Pending: Callback handlers in handlers/admin.py to wire role assignment UI
- Pending: Pagination for user/role list
- Expected: ~1-2 days

---

### T-005 — Implement tenant meter reading flow (BLOCKED on T-004)

**From tracker.md:**
- Acceptance criteria:
  - Tenant can initiate reading submission via inline button
  - Numeric input via inline button keypad (0-9, submit)
  - Reading stored in database with timestamp and apartment
  - Confirmation message sent after submission

**Session-specific notes:**
- ReadingService already created with validation/submission logic
- Numeric keypad (build_numeric_keypad) in keyboards.py ready
- Pending: Callback handlers in handlers/tenant.py
- Pending: State management for multi-step flow (conversation state)
- Expected: ~1-2 days after T-004

---

### T-006 — Implement grayhound reading flow (BLOCKED on T-004)

**From tracker.md:**
- Acceptance criteria:
  - Grayhound can select apartment from inline button list
  - Numeric input for reading via inline keypad
  - Reading stored for selected apartment
  - Access restricted to building-level

**Session-specific notes:**
- RoleService already enforces grayhound privilege level
- Apartment selector (build_apartment_selector) ready
- Pending: Callback handlers in handlers/grayhound.py
- Expected: ~1-2 days after T-004

---

## Session Priorities (This Session — COMPLETED)

**Must complete (P0):**
- T-003d: Implement handler logging decorator — **✅ COMPLETED** — Provides observability for all handler execution
- T-003: Advance database integration in /start — **✅ COMPLETED** — Now queries DB for user roles and creates new users

**Should complete (P1):**
- Consolidate menu builders (DRY) — **✅ COMPLETED** — Single source of truth in keyboards.py
- Update design.md and tracker.md — **✅ COMPLETED** — Documentation synchronized

**Could complete if time (P2):**
- Begin T-004 (role management) — Not started (scoped for next session)

---

## Context for This Session

**What happened last session:**
- Database schema created and Flyway migrations applied
- Repository layer fully functional (6 repos)
- Services layer created (ReadingService, RoleService, ExportService)
- Handler stubs created with @log_handler decorator
- Pre-commit quality gates configured

**Current blockers/dependencies:**
- None — all dependencies cleared (T-001, T-002 complete)

**Environment notes:**
- Local PostgreSQL 15 running on Windows
- Python 3.12, venv activated
- All dependencies installed and importable
- Pre-commit hooks configured and passing

---

## Success Criteria for This Session

**By end of session, we should have:**
- ✅ Handler logging decorator fully implemented and applied to all handlers
- ✅ Database integration in /start handler (user queries, new user creation, role checking)
- ✅ Single menu builder source of truth
- ✅ 23/23 unit tests passing (6 main + 17 pre-commit)
- ✅ All code quality checks passing (7/7 pre-commit hooks)
- ✅ T-002 marked 100% complete
- ✅ T-003 advanced to 75% complete
- ✅ handoff.md and tracker.md updated with session progress
- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Tests written and passing]
- [ ] [Documentation updated]
- [ ] [Tracker.md updated with progress]
- [ ] [Handoff.md updated with session results]

If we don't complete everything:
- [What's the minimum viable progress?]
- [What can safely carry over?]

---

## Time Boxing

**Estimated breakdown:**
- Task 1 (T-XXX): [X minutes/hours]
- Task 2 (T-XXX): [Y minutes/hours]
- Testing/validation: [Z minutes]
- Documentation updates: [Z minutes]
- Buffer for unexpected issues: [Z minutes]

**Total:** [Should match time budget]

---

## Notes & Reminders

**Before starting:**
- [ ] Read handoff.md (where we left off)
- [ ] Verify local environment is working
- [ ] Check tracker.md for any updates to acceptance criteria
- [ ] Review design.md sections relevant to these tasks

**During session:**
- [ ] Run validation commands after each change
- [ ] Paste full outputs to AI (not summaries)
- [ ] Update tracker.md as tasks progress
- [ ] Flag any new risks or decisions in notes

**After session:**
- [ ] Generate Closing Report
- [ ] Update handoff.md using canonical schema
- [ ] Update tracker.md with status/evidence
- [ ] Commit and push changes
- [ ] Create todo.md for next session

---

## Example TODO (Reference)

```markdown
# todo.md

**Session Date:** 2025-10-23
**Time Budget:** 2 hours
**Session Goal:** Complete rate limiting implementation (T-015)

## Active Tasks for This Session

### T-015 — Add Rate Limiting to API

**From tracker.md:**
- Acceptance criteria:
  - 100 requests/min per IP enforced
  - Returns 429 status when limit exceeded
  - Unit tests ≥80% coverage
  - Integration test proves limit works

**Session-specific notes:**
- Last session completed auth (T-014), so Redis is already set up
- Design.md §5.3 specifies token bucket algorithm
- Need to handle Redis unavailable scenario (fail closed per security req)

**Expected progress this session:**
- Complete implementation (60 min)
- Write unit tests (40 min)
- Write integration test (20 min)

## Session Priorities

**Must complete (P0):**
- T-015: Rate limiting — Blocks T-016 (admin bypass)

## Context for This Session

**What happened last session:**
- Completed JWT auth (T-014)
- Redis is running and tested
- All auth tests passing

**Current blockers/dependencies:**
- None — Redis dependency already met

**Environment notes:**
- Redis running on localhost:6379
- Need to test with multiple IPs (can use curl with different headers)

## Success Criteria for This Session

By end of session, we should have:
- [x] Rate limiter middleware implemented
- [x] 12+ unit tests passing with ≥80% coverage
- [x] Integration test proves 100 req/min limit
- [x] Tracker.md updated to T-015: ✅ 100%
- [x] Handoff.md updated with session results

## Time Boxing

- Implementation: 60 min
- Unit tests: 40 min
- Integration test: 20 min
- Total: 2 hours (matches budget)
```

---

## Relationship to Other Documents

**todo.md connects to:**

- **tracker.md** — Source of tasks (todo is a subset)
  - Tasks copied FROM tracker.md
  - Progress flows BACK TO tracker.md

- **handoff.md** — Context of where we left off
  - Read handoff.md BEFORE creating todo.md
  - Update handoff.md AFTER completing todo.md work

- **design.md** — Technical context for tasks
  - Reference design.md sections while working on todo tasks
  - Ensure todo work follows design.md patterns

- **scope.md** — Validates tasks are in scope
  - Ensure todo tasks align with scope.md goals
  - Don't add todo items that are out of scope

---

## Template for Quick Sessions

For very short sessions (30-60 minutes):

```markdown
# todo.md — Quick Session

**Date:** YYYY-MM-DD | **Budget:** 1 hour

**Goal:** [One specific thing]

**Task:** T-XXX — [Title]

**Plan:**
1. [Step 1] — 20 min
2. [Step 2] — 20 min
3. [Validate] — 20 min

**Success:** [Done when X is true]
```

---

## Anti-Patterns (Don't Do This)

❌ **Overloading todo.md with too many tasks**
- More than 3 tasks usually means you won't finish any
- Better: 1 task done than 3 tasks half-done

❌ **Using todo.md as permanent task list**
- Todo.md is ephemeral (per-session)
- Tracker.md is permanent (project-wide)
- Don't lose tasks by keeping them only in todo.md

❌ **Skipping todo.md creation**
- Without it, AI doesn't know what to focus on
- Leads to wandering sessions without clear goals

❌ **Not updating after session**
- Stale todo.md confuses next session
- Always create fresh todo.md based on updated tracker.md

❌ **Ignoring time budget**
- Setting 4 hours of work in 2-hour session
- Leads to incomplete work and poor handoffs

---

## Changelog

| Date | Changes | Author |
|------|---------|--------|
| YYYY-MM-DD | Initial template created | [Name] |
| | | |

---

**End of todo.md template**

## Summary

**todo.md is:**
- ✅ Session-specific (new each session)
- ✅ Subset of tracker.md (bounded scope)
- ✅ Time-boxed (fits session budget)
- ✅ Focused (1-3 tasks maximum)
- ✅ Updated before each session starts
- ✅ Used to guide AI on "what now"

**todo.md is NOT:**
- ❌ Permanent task storage (that's tracker.md)
- ❌ Strategic planning (that's scope.md)
- ❌ Technical decisions (that's design.md)
- ❌ Session results (that's handoff.md)

Think of todo.md as your **session work order** — what's on the workbench right now.
