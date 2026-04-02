# scope.md

**Version:** 1.0  
**Last updated:** 2026-04-01  
**Status:** Active — defines project boundaries and success criteria

---

## Purpose

 This document defines what we're building, why we're building it, what success looks like, and what's explicitly out of scope for {{project_name}}.

---

## Vision

Build a Python Telegram Bot (PTB) aimed at reducing the time spent on and simplifying the process of power meter reading in a multi-family building with more than a hundred apartments. 
Upload the resulting data to a separate file or resource.  
There are three account roles: an administrator, a grayhound, and a tenant.
Dedicated persons (grayhounds) is responsible for all meters in the building, and current apartment tenants can read the meters for their apartments. 
A dedicated administrator assigns roles to other users. 
PTB should be implemented with only inline buttons, avoiding manual data entry by users. 
PTB should provide charts with the power consumption
**Instructions:** Paint the picture of the desired end state. What does success look like from a high level?

---

## Goals (what success looks like)
- A power meter reading process in a multi-family building is going with a Python Telegram Bot (PTB)
- Result data is uploaded to a cvs file from PTB
- A whole logic of meter reading is implemented in a PTB 
- The bot is implemented in a 2-level architecture: a pulling Python Telegram bot deployed as a demon to AWS EC2 and a PostgreSQL database instance as an AWS RDS
- CI/CD, code deployment is implemented with script commands for Linux and Windows, and Flyway for database deployment
- There are 2 environments in AWS cloud: UAT, PROD. There are 3 telegram bots created: DEV, UAT, PROD, respectively
- There are three user account roles in the PTB: administrators, responsible for a whole building's accounts, and tenants' accounts. 
- User roles are assigned for the time period 
- All the features in PTB are covered by test cases
- PTB is providing charts with power consumption for an apartment or for a building
- PTB is reading the meter by manual input or scanning a photo (with a recognition feature for an apartment number and a current meter) 

---

## Success Metrics (SLOs)
- PR lead time (first commit → merge) ≤ 3 days (p50), ≤ 7 days (p90)
- Changed-lines test coverage ≥ 80% on merged PRs
- Secret/SCA scans: 0 critical findings on `main`
- Session continuity: 100% sessions end with valid `handoff.md`
- Rework rate (revert/fix-forward within 48h): ≤ 10%

---

## In Scope
- A power meter reading process in a multi-family building is going with a Python Telegram Bot (PTB)
- Result data is uploaded to a cvs file from PTB
- A whole logic of meter reading is implemented in a PTB 

---

## Out of Scope (for now)
- The bot is implemented in a 2-level architecture: a pulling Python Telegram bot deployed as a demon to AWS EC2 and a PostgreSQL database instance as an AWS RDS
- CI/CD, code deployment is implemented with script commands for Linux and Windows, and Flyway for database deployment
- There are 2 environments in AWS cloud: UAT, PROD. There are 3 telegram bots created: DEV, UAT, PROD, respectively
- There are three user account roles in the PTB: administrators, responsible for a whole building's accounts, and tenants' accounts. 
- User roles are assigned for the time period 
- All the features in PTB are covered by test cases
- PTB is providing charts with power consumption for an apartment or for a building
- PTB is reading the meter by manual input or scanning a photo (with a recognition feature for an apartment number and a current meter) 


---

## Constraints & Assumptions
- Source repositories use Git and PR reviews
- The AI cannot run code; the human runs commands and returns raw outputs
- Secrets never leave the operator's local environment
- Team has basic familiarity with CI/CD concepts

---

## Stakeholders

| Stakeholder | Role | Responsibility |
|-------------|------|----------------|
| Product/Tech Lead | Sponsor | Approves scope, resolves conflicts |
| Dev Lead | Owner | Maintains methodology, updates docs |
| QA/DevEx | Advisors | Review quality gates and tooling |
| AI Assistant | Actor | Implements features per methodology |
| Engineers | Actors | Use methodology, provide feedback |

---

## Risks (initial)
- **Inconsistent handoffs** → Mitigation: Canonical schema enforced, regular reviews
- **Drift across docs** → Mitigation: SSOT rule (only `methodology.md` defines process)
- **Low adoption** → Mitigation: Pilot with one team, iterate based on feedback

---

## Milestones (target dates, adjust as needed)
To be delivered
---

## Dependencies

- CI infrastructure: Available, owned by DevOps, medium risk if downtime
- Git repository access: Available, owned by IT, low risk
- Decision on standard test framework: Pending, owned by Tech Lead, high risk if delayed

---

## Non-Goals (what we explicitly won't do)

- This is not a full SDLC methodology (no requirements gathering, product management)
- This is not a team management framework (no hiring, performance reviews, agile ceremonies)
- This is not a security framework (assumes secure infrastructure exists)
- This is not a specific tool or platform (tool-agnostic approach)

---

## Changelog

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| YYYY-MM-DD | 1.0 | Initial scope defined | [Name] |
| | | | |

---

