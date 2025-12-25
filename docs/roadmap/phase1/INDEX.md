# Phase 1 - Roadmap Index

Status: Approved — Phase 1 planning core validated for downstream specs.

## Phase 1 Core and Dependencies

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
  - Dependency declaration recorded to bind UX, API, database, and backend work to the approved contracts.

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

## Phase 1 API Steps

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

### Step 08 - Planning Snapshots and Audit Trails
- [Step 08 - Planning Snapshots and Audit Trails](../api/phase1/step-08-planning-snapshots-and-audit-trails.md)
- Status: Approved — planning-only snapshot and audit trail contracts locked for Phase 1 traceability.
- Purpose: Provide immutable planning snapshots and append-only audit events to enable reviews, rollback discussions, and reproducible validation without introducing restoration or execution semantics.
- Deliverables:
  - Snapshot scope, DTOs, deterministic content ordering, and creation/list/read endpoints with idempotency rules aligned to Step 05.
  - Audit event DTO, allowed actions, organization scoping, and filtering rules with stable pagination semantics.
  - Standard error handling and a test matrix covering idempotency conflicts, pagination validation, deterministic ordering, and cross-org blocks.
- Acceptance:
  - Snapshots are immutable, organization-scoped, and use deterministic ordering for content and listings.
  - Audit events are append-only, organization-scoped, and filterable by entity with stable pagination and sorting.
  - Status codes and error contracts align with Steps 04-05 while remaining planning-only and excluding restore semantics.

### Step 09 - API Indexing and Cross-Doc Registration
- [Step 09 - API Indexing and Cross-Doc Registration](../api/phase1/step-09-api-indexing-and-cross-doc-registration.md)
- Status: Approved — documentation-only alignment to register Phase 1 API steps across indexes.
- Purpose: Ensure canonical indexing, cross-document registration, and navigation coherence for Phase 1 API artifacts without altering behavior contracts.
- Deliverables:
  - Canonical index entries for Steps 01-09 across API and roadmap navigation.
  - Cross-document registration checklist and drift detection guidance to keep Phase 1 API paths aligned.
  - Next authorized step pointer to continue the sequence without duplicating artifacts.
- Acceptance:
  - All Phase 1 API steps are indexed once with consistent titles and paths.
  - Roadmap and API indexes reference the same canonical files with no duplicates or missing entries.
  - Next authorized step is recorded for controlled continuation.

### Step 10 - API Error Taxonomy and Problem Details Registry
- [Step 10 - API Error Taxonomy and Problem Details Registry](../api/phase1/step-10-api-error-taxonomy-and-problem-details-registry.md)
- Status: Approved — planning-only consolidation of the error envelope and code namespace.
- Purpose: Lock a Phase 1 error code registry and problem-details conventions aligned to Steps 04-05 without introducing new behaviors.
- Deliverables:
  - Canonical list of allowed error codes with fixed HTTP status pairings and envelope shape.
  - Checklist to enforce deterministic error structures and cross-doc linkage to prior steps.
  - Drift detection guidance for catching unauthorized codes or envelope changes.
- Acceptance:
  - No new error behaviors or status mappings beyond Steps 04-05 are introduced.
  - API and roadmap indexes reference this registry once with the canonical path.
  - Future docs reuse the locked envelope and codes or raise `DECISION REQUIRED` for changes.

### Step 11 - Authorization and Access Control (Planning-Only)
- [Step 11 - Authorization and Access Control (Planning-Only)](../specs/phase1/step-11-authorization-and-access-control.md)
- Status: Approved — planning-only authorization roles and permissions recorded without runtime enforcement.
- Purpose: Define declarative roles, permissions, and scopes for planning artifacts across organization and project boundaries.
- Deliverables:
  - Canonical planning roles with permissions and restrictions aligned to Phase 1 scope.
  - Resource/permission matrix covering organization, project, mission, assignment, and collaborator artifacts.
  - Authorization invariants and validation checklist consistent with Steps 01-10 and planning error taxonomy.
- Acceptance:
  - Roles and permissions remain planning-only with no authentication or runtime enforcement implied.
  - Organization and project scopes are contained per Phase 1 domain boundaries.
  - Error handling aligns to the Phase 1 problem details registry without expanding the envelope.

### Step 12 - Planning Lifecycle and State Transitions (Planning-Only)
- [Step 12 - Planning Lifecycle and State Transitions (Planning-Only)](../specs/phase1/step-12-planning-lifecycle-and-state-transitions.md)
- Status: Approved — planning lifecycle states and transitions locked for Phase 1 without runtime automation.
- Purpose: Declare canonical lifecycle states, allowed transitions, and cross-resource constraints for planning artifacts while aligning to the planning error taxonomy.
- Deliverables:
  - Lifecycle state models and permitted transitions for organization, project, mission, assignment, and collaborator resources.
  - Cross-resource transition constraints, terminal state notes, and validation expectations mapped to Step 10 error codes.
  - Auditability requirements ensuring transitions remain traceable per Phase 1 logging contracts.
- Acceptance:
  - Transitions respect Phase 1 boundaries with no execution, notification, or automation semantics implied.
  - Constraints remain consistent with Steps 01-11 and prior invariants without introducing hard deletes.
  - Indexing and readiness criteria recorded so downstream specs and APIs can rely on locked lifecycle definitions.

## Next Authorized Step

- Phase 1 - Step 13: TBD (DECISION REQUIRED for title and scope)
