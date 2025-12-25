# Phase 1 - Roadmap Index
_FROZEN by phase1_freeze_1.0.0_

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
  - Future docs reuse the locked envelope and codes; any change requires governance approval and a downstream phase request.

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

### Step 13 - Conflict Detection and Resolution Rules (Planning-only)
- [Step 13 - Conflict Detection and Resolution Rules (Planning-only)](../specs/phase1/step-13-conflict-detection-and-resolution-rules.md)
- Status: Approved — planning-only conflict taxonomy, blocking rules, and resolution governance locked without automation.
- Purpose: Define declarative conflict types, severities, and resolution/override expectations that gate planning transitions while honoring Phase 1 boundaries.
- Deliverables:
  - Conflict taxonomy with default severities, blocking transitions, and override allowances mapped to the Phase 1 error registry.
  - Conflict record model with audit-ready lifecycle statuses, ownership expectations, and override requirements linked to Step 08 and Step 11 roles.
  - Deterministic detection inputs, blocking/override semantics, and UX/API contract notes that remain planning-only and avoid solver or runtime behavior.
- Acceptance:
  - Conflicts remain deterministic, planning-only, and exclude optimization, scheduling automation, or runtime policy engines.
  - Blocking and override semantics align with Step 12 transitions and Step 10 error codes; block conflicts cannot be overridden.
  - Auditability and registry alignment recorded with roadmap and specs index registration for traceability.

### Step 14 - Derived Read Models and Aggregations (Planning-only)
- [Step 14 - Derived Read Models and Aggregations (Planning-only)](../specs/phase1/step-14-derived-read-models-and-aggregations.md)
- Status: Approved — planning-only derived summaries locked without prescribing storage or runtime implementations.
- Purpose: Define deterministic derived read models and aggregations for planning navigation, staffing coverage, load views, and conflict rollups reproducible from snapshots.
- Deliverables:
  - Project, mission, collaborator load, and timeline occupancy summaries with required fields, staffing coverage semantics, and conflict summary attachment rules.
  - Aggregation guidance for counts by lifecycle state, staffing gaps, and load/utilization views aligned to Phase 1 invariants.
  - Snapshot attribution, error handling, and integration notes keeping derived models read-only and deterministic.
- Acceptance:
  - Derived models and metrics are computable solely from Phase 1 planning artifacts and reproduce from snapshots.
  - Conflict summaries, lifecycle counts, and staffing coverage align with Steps 10-13 without masking invalid data.
  - Roadmap and specs indexes updated with this step and next authorized step advanced.

### Step 15 - Query Parameters and Filtering Contracts (Planning-only)
- [Step 15 - Query Parameters and Filtering Contracts (Planning-only)](../specs/phase1/step-15-query-parameters-and-filtering-contracts.md)
- Status: Approved — planning-only query semantics standardized across Phase 1 read and derived surfaces.
- Purpose: Define shared query, filtering, sorting, pagination, include/expand, and derived view selector contracts for Phase 1 resources while aligning to conflict, lifecycle, and derived model steps.
- Deliverables:
  - Parameter naming conventions, defaults, and rejection rules for unknown keys.
  - Pagination, sorting, include/expand, scope/time window, lifecycle, actor ownership, text, and conflict filter semantics with derived view selectors.
  - Error integration mapping invalid queries to the Step 10 registry plus validation checklist binding to Steps 04, 12, 13, and 14.
- Acceptance:
  - Query rules reference the canonical lifecycle, conflict, and derived model taxonomies without expanding scope.
  - Ambiguous list surfaces require explicit organization/project scope and validate time window semantics.
  - Roadmap and specs indexes are updated and error mappings align to the Step 10 registry.

### Step 16 - Concurrency and Idempotency Contracts (Planning-only)
- [Step 16 - Concurrency and Idempotency Contracts (Planning-only)](../specs/phase1/step-16-concurrency-and-idempotency-contracts.md)
- Status: Approved — planning-only concurrency control and idempotency contracts recorded for Phase 1 writes.
- Purpose: Define optimistic concurrency, idempotency key usage, retry safety, and error mappings for planning CRUD and transition endpoints without prescribing storage or runtime mechanisms.
- Deliverables:
  - Revision token and If-Match requirements for updates, transitions, and archive/unarchive actions with read-after-write token exposure.
  - Idempotency-Key guidance for create and action-style POSTs with replay consistency rules, 24-hour TTL, and mandatory If-Match for updates and transitions.
  - Error code alignment to Step 10 plus audit expectations linking prior and new revision tokens for traceability.
- Acceptance:
  - Concurrency and idempotency behaviors remain planning-only, align with Steps 01-15, and do not bypass validation, authorization, or conflict blocking.
  - Retry guidance avoids masking validation or conflict errors and references Step 10 problem-details categories.
  - Roadmap, specs, and API indexes updated; next authorized step advanced.

### Step 17 - Export and Import Contracts (Planning-only)
- [Step 17 - Export and Import Contracts (Planning-only)](../specs/phase1/step-17-export-and-import-contracts.md)
- Status: Approved — planning-only export/import contracts recorded for Phase 1 data mobility and validation.
- Purpose: Define deterministic export formats and import semantics tied to snapshots, validation, conflicts, and idempotency without prescribing delivery mechanisms.
- Deliverables:
  - Canonical JSON export structure with optional CSV projections and manifest requirements, including snapshot attribution.
  - Import modes, scope declarations, strategies, and idempotency guidance aligned to planning invariants, lifecycle rules, and conflict handling.
  - Validation checklist, error code mapping, and audit/traceability notes ensuring dry-run safety and predictable apply results.
- Acceptance:
  - Export schemas align to Step 04 resource contracts with versioning and snapshot linkage.
  - Import semantics respect Steps 02, 12, 13, and 16 with block conflicts prevented unless payloads are corrected.
  - Roadmap and specs indexes updated and next authorized step advanced.

### Step 18 - Interop Keys and External References (Planning-only)
- [Step 18 - Interop Keys and External References (Planning-only)](../specs/phase1/step-18-interop-keys-and-external-references.md)
- Status: Approved — planning-only external reference and interop key contracts locked for Phase 1 data linking.
- Purpose: Standardize external identifier semantics for planning resources without delegating authority or introducing sync behavior.
- Deliverables:
  - External reference structure with source_system naming guidance and optional metadata fields.
  - Uniqueness scopes, mutability recommendations, and deduplication/merge semantics tied to Step 17 merge_by_key.
  - Query/filtering rules and error code mappings aligned to Steps 10 and 15 plus a validation checklist.
- Acceptance:
  - External references remain metadata honoring planning invariants and lifecycle constraints without re-parenting or authority shifts.
  - Merge_by_key usage respects organization/project boundaries, auditability, and concurrency safeguards.
  - Roadmap and specs indexes updated and the next authorized step advanced.

### Step 19 - Bulk Operations and Batch Semantics (Planning-only)
- [Step 19 - Bulk Operations and Batch Semantics (Planning-only)](../specs/phase1/step-19-bulk-operations-and-batch-semantics.md)
- Status: Approved — planning-only bulk and batch semantics locked for Phase 1 write operations.
- Purpose: Standardize deterministic bulk create, update, upsert, archive, and transition semantics with explicit atomic versus partial behavior and per-item validation.
- Deliverables:
  - Canonical bulk request and response envelopes with item correlation ids and scope enforcement.
  - Atomicity, processing order, temp_id, concurrency, and idempotency rules aligned to prior Phase 1 steps.
  - Error mappings, audit expectations, and validation checklist aligned to Step 10 and related contracts.
- Acceptance:
  - Bulk semantics reuse Step 04 resource shapes and Step 10 error registry without adding new execution scope.
  - Concurrency, conflict, and lifecycle dependencies from Steps 12, 13, and 16 are enforced per item.
  - Roadmap and specs indexes updated and the next authorized step advanced.

### Step 20 - Rate Limits, Quotas, and Abuse Controls (Planning-only)
- [Step 20 - Rate Limits, Quotas, and Abuse Controls (Planning-only)](../specs/phase1/step-20-rate-limits-quotas-and-abuse-controls.md)
- Status: Approved — planning-only rate limiting, quota, and abuse control semantics recorded for Phase 1.
- Purpose: Define consistent client-visible throttling semantics, quota concepts, and abuse controls without prescribing enforcement mechanisms.
- Deliverables:
  - 429 throttling behavior with Retry-After guidance and standardized rate limit headers.
  - Quota model placeholders by organization/project scope and operation type with policy-defined thresholds.
  - Bulk safety limits and payload constraints aligned to Step 19 batch envelopes and Step 15 query depth rules.
  - Error mapping to the Step 10 registry plus retry/backoff guidance aligned to Step 16 idempotency.
- Acceptance:
  - Rate limiting semantics, headers, and Retry-After usage are consistent with Step 16 idempotent retry guidance.
  - Quota and bulk safety limits align with Step 19 envelopes and Step 15 query rejection behaviors.
  - Problem detail codes and fields map to the Step 10 registry with thresholds locked for Phase 1 (100 items per batch, 5 MB payload cap).
  - Roadmap and specs indexes updated and the next authorized step advanced.

### Step 21 - Observability Events and Audit Correlation (Planning-only)
- [Step 21 - Observability Events and Audit Correlation (Planning-only)](../specs/phase1/step-21-observability-events-and-audit-correlation.md)
- Status: Approved — planning-only observability vocabulary and correlation contracts recorded for Phase 1.
- Purpose: Standardize event names, correlation identifier propagation, minimal event fields, and audit linkage to keep operational signals aligned to planning contracts.
- Deliverables:
  - Event naming conventions and optional resource subtype rules anchored to planning actions.
  - Correlation identifier semantics for request_id, correlation_id, and trace_id plus propagation guidance and header recommendations.
  - Minimal logging/metrics fields, error correlation to Step 10, and audit linkage including rate limiting, bulk, and import/export coverage.
- Acceptance:
  - Event taxonomy covers planning actions with consistent result naming and optional resource specialization.
  - Correlation identifiers propagate per contract and align with audit trail linkages and retry/idempotency safeguards from Steps 08 and 16.
  - Metrics vocabulary and throttling coverage align to Steps 17, 19, and 20 with high-cardinality labels forbidden by default and audit_event_id exposed for correlation.

### Step 22 - Data Retention and Archival Policies (Planning-only)
- [Step 22 - Data Retention and Archival Policies (Planning-only)](../specs/phase1/step-22-data-retention-and-archival-policies.md)
- Status: Approved — retention durations, audit handling, and export obligations locked for Phase 1.
- Purpose: Define planning-only retention, archival, purge, and legal hold policies without mandating storage or automation.
- Deliverables:
  - Retention categories with Phase 1 defaults: planning resources and audit events indefinite; import/export artifacts 90 days; logs 30 days; metrics 180 days; traces 7 days; derived caches remain ephemeral.
  - Archival access semantics, purge eligibility safeguards, legal hold effects, and tombstone-based audit preservation aligned to lifecycle and error taxonomy steps.
  - Export expectations before purge plus validation checklist and problem detail mappings.
- Acceptance:
  - Retention defaults and purge prerequisites are recorded without conflating archival and deletion semantics.
  - Legal hold and audit integrity rules block purge unless policy-defined conditions are met, using tombstones instead of silent deletion.
  - Export obligations and error codes are aligned with Steps 10, 17, and 21, with export required before purge.
  - Roadmap and specs indexes updated; retention governance locked for Phase 1.

### Step 23 - Documentation Freeze, Versioning, and Change Management (Planning-only)
- [Step 23 - Documentation Freeze, Versioning, and Change Management (Planning-only)](../specs/phase1/step-23-documentation-freeze-versioning-and-change-management.md)
- Status: Approved — Phase 1 freeze declared with initial version 1.0.0 and governance rules locked.
- Purpose: Define the rules for freezing Phase 1 documentation, versioning releases, classifying changes, and governing amendments without mandating tooling.
- Deliverables:
  - Freeze declaration requirements with commit-level identification and initial version assignment.
  - Semantic versioning guidance and change classifications covering breaking, non-breaking, and editorial updates.
  - Amendment and deprecation policies plus backward compatibility and communication obligations.
- Acceptance:
  - Freeze declaration prerequisites and validation checklist cover all Phase 1 steps and decision items.
  - Change classifications map to MAJOR/MINOR/PATCH versioning with amendment documentation expectations and deprecations valid until a new MAJOR or new Phase.
  - Roadmap and specs indexes updated; changelog and amendment index updates are required for post-freeze changes, anchored to version 1.0.0.

## Next Authorized Step

- Phase 1 - Step 24: TBD (title and scope to be confirmed)
