# Phase 1 - Step 14: Derived Read Models and Aggregations (Planning-only)
_FROZEN by phase1_freeze_1.0.0_

## 1. Purpose and Scope

This step defines planning-only derived read models and aggregations for Phase 1. Derived models are computed views over planning artifacts that:

* summarize state for UX and reporting
* enable filtering and navigation without requiring consumers to recompute business meaning
* remain fully reproducible from planning snapshots (Step 08)

This step is declarative. It defines required view semantics and minimal fields, without prescribing storage, denormalization strategy, caching, or query implementation.

In scope:

* Derived read models for planning navigation (project summaries, mission summaries)
* Aggregations (counts, totals, coverage, load)
* Conflict summaries (from Step 13)
* Staffing coverage and gaps
* Timeline occupancy and overlaps at a summary level

Out of scope:

* Financial calculations (costing, payroll, billing)
* Execution metrics (actual hours, check-in/out)
* Optimization outputs
* Runtime performance guarantees

## 2. Authority and Precedence

* Step 01 planning-as-source-of-truth: all derived models must be computable from planning artifacts.
* Step 02 invariants: derived models must not mask or override invalid states.
* Step 04 API contracts: derived models may be exposed as read-only resources or embedded expansions.
* Step 08 snapshots: derived models must be reproducible at a snapshot time.
* Step 10 errors: invalid or missing prerequisite data must map to Step 10 categories when surfaced.
* Step 12 lifecycle: state counts must be consistent with lifecycle semantics.
* Step 13 conflicts: conflict summaries must match conflict taxonomy and statuses.

If any derived metric requires product policy (e.g., what counts as staffed), STOP and escalate to governance before proceeding.

## 3. Derived Model Conventions

### 3.1 Read-Only and Non-Authoritative

* Derived models are read-only.
* They do not introduce new source-of-truth fields.
* Any discrepancy is resolved by the underlying planning artifacts, not by derived views.

### 3.2 Determinism

Given the same snapshot, derived models must compute to the same result.

### 3.3 Time Windows and Time Zones

* All derived time computations use the canonical UTC timestamps stored on missions/assignments.
* Presentation time zones are outside Phase 1 scope.

## 4. Canonical Derived Read Models

This section defines the minimal shapes and semantics. Field names are illustrative; API exposure is not mandated.

### 4.1 ProjectSummary

Purpose: Provide a project-level rollup for dashboards and lists.

Minimum fields:

* project_id
* lifecycle_state (Step 12)
* mission_counts_by_state: map[state -> int]
* assignment_counts_by_state: map[state -> int]
* date_window: { start_utc, end_utc } derived from missions (min start, max end) for non-archived missions
* staffing_coverage: { required_slots, filled_slots, gap_slots }
* conflict_summary: see 4.5
* last_activity_at (latest audit event timestamp affecting project scope)

Semantics:

* required_slots derives from mission staffing requirements (if declared); if requirements are absent, required_slots defaults to 0.
* filled_slots counts confirmed assignments only.
* gap_slots = max(required_slots - filled_slots, 0).

### 4.2 MissionSummary

Purpose: Provide a mission-level rollup for planning lists, board tiles, and quick inspection.

Minimum fields:

* mission_id
* project_id
* lifecycle_state
* time_window_utc: { start_utc, end_utc }
* assignment_counts_by_state
* staffing_coverage: { required_slots, filled_slots, gap_slots }
* role_breakdown: list[{ role_key, required, filled, gap }]
* conflict_summary
* locked: boolean (true when state is locked)

Semantics:

* role_breakdown is computed by matching assignments to required roles (if declared).
* filled counts confirmed assignments for the role.

### 4.3 CollaboratorLoadSummary

Purpose: Show collaborator workload and risk for a time window.

Minimum fields:

* collaborator_id
* window_utc: { start_utc, end_utc }
* total_assignment_count
* confirmed_assignment_count
* total_scheduled_minutes (sum of confirmed assignments intersection with window)
* overlap_count (count of temporal overlap conflicts from Step 13)
* availability_conflict_count (unavailable conflicts from Step 13)
* lifecycle_state (active/suspended/archived)

Semantics:

* total_scheduled_minutes is derived from assignment windows.
* overlap_count counts open conflicts of type collaborator_time_overlap.

### 4.4 TimelineOccupancySummary

Purpose: Support timeline views without requiring full assignment expansion.

Minimum fields:

* scope: project | mission | collaborator
* scope_id
* buckets: list[{ bucket_start_utc, bucket_end_utc, occupancy_ratio, filled_slots, required_slots, conflict_count }]

Semantics:

* Buckets are computed using a fixed bucket size chosen by the consumer (e.g., 15/30/60 minutes). Phase 1 does not prescribe bucket size.
* occupancy_ratio is a normalized measure:
  * for mission: filled_slots / max(required_slots, 1)
  * for collaborator: scheduled_minutes / bucket_minutes
* occupancy_ratio is clamped to a maximum of 1.0.

### 4.5 ConflictSummary

Purpose: Provide summarized conflict info attached to other derived models.

Minimum fields:

* total_open
* by_severity: { info, warn, block }
* by_type: map[type -> int] (optional)
* blocking_open: int
* overridden_open: int

Semantics:

* total_open counts conflicts with status open or acknowledged.
* blocking_open counts status open/acknowledged with severity block.
* overridden_open counts status overridden where the underlying conflict severity is warn/info.

## 5. Aggregations and Metrics

### 5.1 Counts by State

* All resources that have lifecycles (Step 12) must support counts by state in their parent scope.
* Archived artifacts should be excluded from default counts unless explicitly requested.

### 5.2 Staffing Coverage and Gaps

Coverage definitions:

* required_slots: sum of declared role requirements for missions in scope
* filled_slots: number of confirmed assignments that match a required role and are within the mission time window
* gap_slots: required_slots - filled_slots (min 0)

Non-requirement behavior:

* If a mission has no declared requirements, required_slots is 0 and gaps are 0.

### 5.3 Load Views

Load is derived as:

* total_scheduled_minutes
* number of assignments
* capacity utilization if capacity is declared (Step 13 capacity conflicts)

Capacity utilization (optional):

* utilization_ratio = scheduled_minutes / max(capacity_minutes, 1)

## 6. Staleness and Snapshot Alignment

Derived models must be attributable to:

* a snapshot_id (Step 08) OR
* a computed_at timestamp plus the planning revision token (if available)

Phase 1 does not mandate revision tokens; it only requires the derived view to be traceable to a planning state.

## 7. Error and Missing Data Handling

Derived models must not silently fabricate meaning.

Rules:

* If required prerequisite fields are missing (e.g., mission has no time window), derived fields dependent on them must be null and may surface a warn conflict (Step 13 invalid_time_window); the derived view remains incomplete rather than failing globally.
* If a consumer requests a derived model that cannot be computed due to invalid data, the system may respond with problem details:
  * error code: planning.derived_view_unavailable
  * include reasons in extensions (non-normative)

## 8. Integration Notes

* Step 04 API may expose these models as:
  * dedicated read-only endpoints (e.g., /projects/{id}/summary)
  * embedded expansions (e.g., include=summary)
  * separate query models

No exposure pattern is mandated in Phase 1.

## 9. Validation Checklist

Before implementation work proceeds:

* Each derived model is computable from artifacts defined in Step 01 and contracts in Step 04.
* Conflict summaries match Step 13 statuses and severities.
* Staffing coverage definitions are consistent across project and mission scopes.
* Derived models can be attributed to a snapshot or identifiable planning state.
* Any referenced error codes exist in Step 10 registry.
