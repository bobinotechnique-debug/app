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

### Step 03 - UX Surface Contracts
- [Step 03 - UX Surface Contracts](../ux/phase1/step-03-ux-surfaces.md)
- Status: Approved
- Purpose: Define authoritative planning-only UX surfaces that present and edit planning artifacts without implying execution, finance, or analytics behaviors.
- Deliverables:
  - UX surface contracts for organization, project, mission, assignment, and collaborator planning views.
  - Cross-surface invariants restated as UX constraints aligned to Phase 1 Steps 01 and 02.
  - Forbidden UX states and deferred concerns ensuring no execution, notification, or financial leakage in Phase 1.
- Acceptance:
  - UX surfaces restrict actions to planning-only scopes with explicit forbidden behaviors.
  - Invariants and forbidden states align with Phase 1 domain boundaries and planning source-of-truth records.
  - Dependency declaration binds downstream UX, API, and implementation work to the approved contracts.

### Step 04 - API Planning Contracts
- [Step 04 - API Planning Contracts](../api/phase1/step-04-api-planning-contracts.md)
- Status: Approved
- Purpose: Establish the planning CRUD API contract for organization, project, mission, assignment, and collaborator resources under Phase 1 boundaries.
- Deliverables:
  - Versioned Phase 1 base path and CRUD endpoints with schemas and error contract.
  - Tenancy and immutability rules aligned to planning invariants and UX needs.
  - Idempotency, pagination, sorting, and filtering conventions for Phase 1.
- Acceptance:
  - Endpoints respect organization security boundary and immutable relationships.
  - Error contract standardized across resources.
  - No execution, financial, or operational concerns introduced.

### Step 05 - API Examples and Test Matrix
- [Step 05 - API Examples and Test Matrix](../api/phase1/step-05-api-examples-and-test-matrix.md)
- Status: Approved
- Purpose: Provide request/response examples and a validation-focused test matrix that operationalize Step 04 without changing scope.
- Deliverables:
  - Locked decisions for validation codes, archive mechanism, filters, cross-org behavior, and idempotency scope.
  - Endpoint examples for happy paths and key error cases aligned to the Step 04 error contract.
  - Minimal API contract test matrix covering validation, tenancy isolation, immutability, archive rules, and idempotency.
- Acceptance:
  - Examples and tests map directly to Step 04 endpoints and schemas.
  - Decisions resolve Step 04 ambiguities without expanding features.
  - Documentation remains planning-only and Phase 1 scoped.

### Step 06 - API Validation and Conflict Detection
- [Step 06 - API Validation and Conflict Detection](../api/phase1/step-06-api-validation-and-conflict-detection.md)
- Status: Approved — validation endpoints and conflict checks locked for planning-only scope.
- Purpose: Define deterministic, read-only validation endpoints for planning data across organization, project, mission, and collaborator scopes.
- Deliverables:
  - Validation report contract with rule_version, scope metadata, blocking_errors, and warnings using deterministic sorting.
  - Validation item structure and categories for structural, temporal, overlap, load, and rest findings with optional related entities and time ranges.
  - Read-only validation endpoints with include/category filters and status code rules aligned to prior Phase 1 decisions, plus a validation test matrix.
- Acceptance:
  - Endpoints remain planning-only, deterministic, and side-effect-free while honoring organization boundaries and the established error contract.
  - Filters and result semantics match the documented report contract without introducing execution, payroll, or contract issuance behaviors.
  - Indexing updates register Step 06 within API and roadmap indexes for Phase 1 traceability.

### Step 07 - Planning State Transitions
- [Step 07 - Planning State Transitions](../api/phase1/step-07-planning-state-transitions.md)
- Status: Approved — planning lifecycle states and transitions locked for Phase 1 planning scope.
- Purpose: Define the Draft/Validated/Frozen planning state machine with transition rules aligned to prior Phase 1 planning artifacts.
- Deliverables:
  - State definitions and allowed/blocked transitions with prerequisites.
  - Parent gating rules for project/mission/assignment validation and freeze transitions.
  - Editability and parent-freeze impact rules ensuring planning-only locking semantics.
  - Dedicated planning_state transition endpoints plus a transition-focused test matrix.
- Acceptance:
  - Transitions honor planning-only scope and depend on validation findings rather than auto-fixes.
  - Parent gating prevents validated or frozen children under invalid parents while avoiding automatic freeze propagation.
  - API endpoints and test matrix follow existing error and archive patterns and remain isolated from execution/payroll behaviors.
