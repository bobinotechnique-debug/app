# Phase 1 - Roadmap Index

Status: Approved — Phase 1 planning core validated for downstream specs.

## Steps

### Step 01 - Planning Core
- [Step 01 - Planning Core](step-01-planning-core.md)
- Status: Approved
- Purpose: Set the planning baseline and domain vocabulary before any Phase 1 design or development begins.
- Deliverables:
  - Phase 1 roadmap entry referencing the planning core contract.
  - Documented goals, non-goals, and domain entities for planning governance.
  - Stop conditions blocking backend, frontend, or ops work until planning is approved.
  - Validation checklist and self-audit cues to enforce readiness gates with recorded approval in the readiness audit.
- Acceptance:
  - Planning-only scope is explicit with traceability to Phase 1 artifacts.
  - Domain entity definitions and planning invariant are recorded and referenced.
  - Roadmap linkage enables downstream specs, UX, and API work to trace to this step.
  - Readiness and audit steps are documented so dependent specs, UX, and API authors can reference approvals and proceed.

### Step 02 - Domain Boundaries and Invariants
- [Step 02 - Domain Boundaries and Invariants](../specs/phase1/step-02-domain-boundaries.md)
- Status: Approved
- Purpose: Lock Phase 1 domain boundaries and invariants so downstream UX, API, and implementation work stays aligned to the planning source of truth.
- Deliverables:
  - Canonical entity responsibilities for organization, project, mission, assignment, and collaborator anchored to Phase 1 Step 01 planning.
  - Explicit boundaries and forbidden states preventing cross-organization or cross-project leakage.
  - Non-negotiable invariants to be enforced by future UX, API, DB, and backend work.
  - Deferred concerns list to prevent Phase 2+ scope creep.
- Acceptance:
  - Boundaries and invariants align with and extend Step 01 without introducing implementation detail.
  - Forbidden states and deferred concerns explicitly block out-of-scope behaviors.
  - Dependency declaration recorded to bind UX, API, database, and backend work to this specification.
