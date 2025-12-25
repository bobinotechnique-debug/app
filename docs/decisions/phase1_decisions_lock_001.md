# Phase 1 Decisions Lock 001

date: 2025-12-25
rationale: simplicity, auditability, zero surprise Phase 2

the decisions below are copied verbatim from the authoritative approvals for Phase 1:

D12-1
- Unarchive is allowed from archived only.
- closed / canceled remain reopenable only if explicitly defined as reopen.

D12-2
- mission.locked:
  - no changes to time / scope / staffing requirements
  - non-structural metadata may be updated

D13-1
- mission_time_overlap_same_resource = warn (non-blocking)

D13-2
- collaborator_capacity_exceeded = warn + override_required to confirm

D13-3
- Importing overrides is forbidden. Overrides are local human decisions and are never imported.

D13-4
- warn conflicts never block by default unless explicitly marked override_required.

D14-1
- If staffing requirements are absent, required_slots = 0.

D14-2
- occupancy_ratio is clamped to 1.0.

D14-3
- Derived view incomplete:
  - dependent fields are null
  - no global error

D15-1
- Default sort is stable by id asc.

D15-2
- page_size max = 200.

D16-1
- If-Match is mandatory for every update / transition.

D16-2
- Idempotency-Key TTL = 24 hours.

D17-1
- Allowed import strategies in Phase 1: create_only, upsert.
- merge_by_key is forbidden in Phase 1.

D17-2
- Importing overrides is forbidden.

D17-3
- Export before purge is mandatory.

D18-1
- External ref uniqueness scope:
  - org/project/collaborator: org-level
  - mission/assignment: project-level

D18-2
- External refs are mutable via add/remove only.

D18-3
- Merge-immutable fields:
  - lifecycle_state
  - parent references (org_id, project_id)

D19-1
- Default bulk mode = atomic.

D19-2
- temp_id intra-batch references are forbidden in Phase 1.

D20-1
- max_items_per_batch = 100
- max_payload_bytes = 5 MB

D20-2
- High-cardinality metrics labels (org_id/project_id) are forbidden by default.

D21-1
- audit_event_id is exposed in API responses.

D21-2
- Redaction defaults:
  - no full payload logging
  - actor_id hashed or pseudonymized
  - never log raw idempotency keys

D22-1
- Retention defaults:
  - planning resources: indefinite
  - audit events: indefinite
  - import/export artifacts: 90 days
  - logs: 30 days
  - metrics: 180 days
  - traces: 7 days

D22-2
- Purge audit strategy = tombstones (no silent reference deletion).

D23-1
- Deprecation remains valid until a new MAJOR or a new Phase.

D23-2
- Phase 1 initial version = 1.0.0
