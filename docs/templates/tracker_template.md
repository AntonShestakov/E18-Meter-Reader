# tracker.md

**Version:** 1.0
**Last updated:** YYYY-MM-DD
**Status:** Active task tracking — single source of truth for work items

---

## Purpose

[1-2 sentences: What is this document? How is it used?]

**Example:**
> This document tracks all tasks for {{project_name}}, their acceptance criteria, status, owners, and evidence of completion. It's the primary reference for "what needs to be done" and is updated continuously throughout the project.

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
- Owner: [Name or role]
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

**Instructions:** Tasks currently in progress (🔵) or blocked (⚠️). Keep this section lean — ideally ≤3 active tasks per person.

### Example Task:

## T-001 — Implement User Authentication
- Owner: Dev Team
- Status: 🔵 60% | Dates: started 2025-10-15, expected by 2025-10-22, last touched 2025-10-21
- Scope: scope.md § Goals (secure access)
- Design: design.md §4.1 (JWT with RS256)
- Acceptance criteria:
  - POST /auth/login returns JWT token for valid credentials
  - POST /auth/refresh rotates refresh token
  - Protected endpoints return 401 for invalid/missing tokens
  - Unit tests ≥80% coverage on auth logic
  - Integration test proves full login flow works
- Evidence: PR #12 (in review), CI run #203 (all green)
- Dependencies: None
- Notes: Using `jsonwebtoken` library; access token TTL 15min, refresh 7 days

---

[Add your active tasks here using the template above]

---

## Backlog (Not Started)

**Instructions:** Tasks defined but not yet started (⚪). Prioritize top-to-bottom.

## T-XXX — [Task Title]
- Owner: [Name]
- Status: ⚪ 0% | Dates: planned start YYYY-MM-DD, expected by YYYY-MM-DD
- Scope: [Link]
- Design: [Link]
- Acceptance criteria:
  - [Criterion 1]
  - [Criterion 2]
- Evidence: [Will be added when started]
- Dependencies: [None or T-XXX]

---

[Add backlog tasks here]

---

## Blocked Tasks

**Instructions:** Tasks that cannot proceed (⚠️). Each must have an owner for unblocking and target unblock date.

## T-XXX — [Task Title]
- Owner: [Name]
- Status: ⚠️ [X%] | Dates: started YYYY-MM-DD, blocked since YYYY-MM-DD
- Blocker: [What's blocking? Who can unblock?]
- Unblock owner: [Name or team]
- Target unblock date: YYYY-MM-DD
- Scope: [Link]
- Design: [Link]
- Acceptance criteria:
  - [Criteria]
- Evidence: [Evidence so far]
- Dependencies: [What must happen to unblock]
- Notes: [Context about the blocker]

---

[Add blocked tasks here if any]

---

## Completed Tasks

**Instructions:** Tasks that are done (✅). Keep recent completions for reference, archive older ones.

## T-XXX — [Task Title]
- Owner: [Name]
- Status: ✅ 100% | Dates: started YYYY-MM-DD, completed YYYY-MM-DD
- Scope: [Link]
- Design: [Link]
- Acceptance criteria:
  - [Criterion 1] ✅
  - [Criterion 2] ✅
- Evidence: [PR #XX merged, CI run #YYY, docs updated]
- Dependencies: [None or T-XXX]
- Notes: [Any learnings, follow-up needed]

---

[Add completed tasks here, most recent first]

---

## Task Numbering

**Instructions:** Use sequential numbering starting from T-001. Never reuse numbers.

**Current highest number:** T-XXX
**Next task:** T-XXX

---

## Task Types (Optional Tags)

Use these tags to categorize tasks:

- `[feature]` — New functionality
- `[bug]` — Fix for defect
- `[tech-debt]` — Refactoring, cleanup, improvement
- `[docs]` — Documentation-only changes
- `[infra]` — CI/CD, deployment, infrastructure
- `[research]` — Spike, investigation, proof-of-concept

**Example:**
```
## T-042 — [tech-debt] Refactor CSV parser for memory efficiency
```

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

**Instructions:** Evidence proves acceptance criteria are met. Link to concrete artifacts.

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

**Instructions:** Track what must happen before a task can complete.

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

**Instructions:** Track when this document was updated.

| Date | Changes | Author |
|------|---------|--------|
| YYYY-MM-DD | Initial tracker created | [Name] |
| | | |

---

## Instructions for Using This Template

1. **Copy this file** to your project's `docs/` directory as `tracker.md`
2. **Replace placeholders** with actual tasks
3. **Delete instruction paragraphs** after understanding them
4. **Update continuously** — after every work session
5. **Reference from handoff.md** — active tasks should appear in handoff
6. **Keep it current** — stale tracker is worse than no tracker
7. **Review weekly** — groom backlog, update statuses, resolve blockers
8. **Archive completed** — move old completed tasks to separate file if tracker gets long

**This is your single source of truth for "what needs to be done."**

---

**Relationship to Other Documents:**

- **scope.md** — Tasks should align with goals defined in scope
- **design.md** — Tasks reference design sections for technical context
- **handoff.md** — Active tasks from tracker appear in handoff Context Snapshot
- **methodology.md §5** — Defines required task format and acceptance criteria rules
- **PR descriptions** — Link to tracker task numbers for traceability

---

**End of tracker_template.md**
