# Phase 1 - Step 08: Planning Snapshots and Audit Trails (Planning-only)
_FROZEN by phase1_freeze_1.0.0_

## 1. Purpose and Scope

* Define a planning-only contract for capturing immutable snapshots of planning state and exposing an append-only audit trail.
* Snapshots and audit trails exist to support:
  * Review and rollback discussions (without auto-fixing).
  * Traceability of planning edits and state transitions.
  * Reproducible validation outcomes (Step 06) against a known planning state.
* Planning-only: no execution semantics, no payroll, no invoicing, no contract issuance.
* Out of scope:
  * Real-time streaming, event buses, or distributed tracing.
  * Any automatic restoration or conflict resolution.
  * Legal retention policies.

## 2. Authority

* Step 01: Planning is source of truth.
* Step 02: Domain boundaries and invariants.
* Step 04: API error contract and resource boundaries.
* Step 05: Status-code decisions and idempotency scope.
* Step 06: Deterministic validation.
* Step 07: Planning state transitions.

## 3. Locked Decisions

### 3.1 Snapshot vs Audit Trail

* A snapshot is an immutable capture of planning data for a scope at a point in time.
* An audit event is an append-only record of a change (create/update/archive/state transition).

### 3.2 Planning-only, No Restore in Phase 1

* Phase 1 provides snapshot creation and retrieval only.
* Restoring a snapshot is explicitly out of scope for Phase 1.
* If a future step introduces restore, it must be a dedicated endpoint with explicit conflict rules.

### 3.3 Determinism

* Snapshot content is immutable once created.
* Snapshot listing and audit event listing must be stable under pagination (no duplicates across pages when using a cursor).

### 3.4 Status Codes

* 201 Created for snapshot creation.
* 200 OK for snapshot and audit retrieval.
* 403 forbidden for cross-organization access.
* 404 not_found for missing resources within the caller organization.
* 409 conflict for idempotency payload mismatch.
* 422 validation_error for invalid query parameters or invalid scope.
* 400 bad_request only for malformed JSON or unsupported content type.

## 4. Snapshot Model

### 4.1 Snapshot Scope

Allowed snapshot scope_type:

* organization
* project
* mission

Rules:

* organization: captures all planning entities within the organization.
* project: captures the project plus its missions and assignments.
* mission: captures the mission plus its assignments.

### 4.2 Snapshot DTO

Snapshot representation returned by the API:

```json
{
  "id": "snp-1",
  "organization_id": "org-123",
  "scope": {
    "type": "project",
    "project_id": "proj-1"
  },
  "label": "pre-freeze review",
  "created_at": "2024-10-06T10:00:00Z",
  "created_by": "user-1",
  "rule_version": "phase1.v1",
  "stats": {
    "projects": 1,
    "missions": 3,
    "assignments": 12,
    "collaborators": 5
  }
}
```

Notes:

* created_by may be omitted if the auth model is not finalized in Phase 1.
* rule_version matches the validation rule version returned in Step 06 reports.
* stats are optional but recommended for UX.

### 4.3 Snapshot Content DTO

Snapshot content is returned by a dedicated endpoint and is immutable.

```json
{
  "snapshot": {"id": "snp-1", "organization_id": "org-123"},
  "content": {
    "projects": [],
    "missions": [],
    "assignments": [],
    "collaborators": []
  }
}
```

Rules:

* content includes only entities in the snapshot scope.
* content ordering must be deterministic: sort by entity type then by id ascending.

## 5. Audit Trail Model

### 5.1 Audit Event DTO

Audit events are append-only records.

```json
{
  "id": "evt-1",
  "organization_id": "org-123",
  "at": "2024-10-06T10:00:00Z",
  "actor_id": "user-1",
  "entity_type": "mission",
  "entity_id": "msn-1",
  "action": "planning_state_changed",
  "summary": "mission planning_state draft -> validated",
  "details": {
    "from": "draft",
    "to": "validated"
  }
}
```

Allowed action values (Phase 1):

* created
* updated
* archived
* unarchived (include only if unarchive is available in Phase 1)
* planning_state_changed

Rules:

* The event stream is append-only.
* Events must be scoped to the organization.

### 5.2 Audit Event Filtering

Audit event listing supports filtering:

* entity_type (required)
* entity_id (required)
* since (optional ISO timestamp)
* until (optional ISO timestamp)

Invalid filters return 422 validation_error.

## 6. Endpoints

Base path: `/api/phase1`

### 6.1 Create Snapshot

* POST `/orgs/{org_id}/snapshots`

Request body:

```json
{
  "client_request_id": "req-900",
  "scope": {
    "type": "project",
    "project_id": "proj-1"
  },
  "label": "pre-freeze review"
}
```

Response:

* 201 Created with Snapshot DTO.

Idempotency:

* Follows Step 05 idempotency scope per (org_id, resource_type=snapshot, client_request_id).
* Replay with identical payload returns the same snapshot and 201.
* Payload mismatch returns 409 conflict.

### 6.2 List Snapshots

* GET `/orgs/{org_id}/snapshots?page=1&page_size=20&sort=-created_at&filter=scope_type:project`

Rules:

* Pagination bounds follow Step 05 (page>=1, page_size 1-100).
* filter uses Step 05 syntax (comma-delimited field:value pairs).

Allowed filter fields:

* scope_type
* project_id (only when scope_type=project)
* mission_id (only when scope_type=mission)

Response 200:

```json
{
  "items": ["<Snapshot DTO>", "..."],
  "page": 1,
  "page_size": 20,
  "total": 42
}
```

### 6.3 Get Snapshot Metadata

* GET `/orgs/{org_id}/snapshots/{snapshot_id}`

Response 200: Snapshot DTO.

### 6.4 Get Snapshot Content

* GET `/orgs/{org_id}/snapshots/{snapshot_id}/content`

Response 200: Snapshot Content DTO.

### 6.5 List Audit Events

* GET `/orgs/{org_id}/audit/events?entity_type=mission&entity_id=msn-1&page=1&page_size=50&sort=-at`

Rules:

* Pagination bounds follow Step 05.
* entity_type and entity_id are required.
* since/until optional.

Response 200:

```json
{
  "items": ["<AuditEvent DTO>", "..."],
  "page": 1,
  "page_size": 50,
  "total": 10
}
```

## 7. Standard Errors

Error contract remains Step 04.

### 7.1 validation_error (bad scope)

Response 422:

```json
{
  "code": "validation_error",
  "message": "unknown scope.type: team",
  "details": {"scope.type": "unsupported"},
  "trace_id": "req-801"
}
```

### 7.2 conflict (idempotency mismatch)

Response 409:

```json
{
  "code": "conflict",
  "message": "client_request_id already used with different payload",
  "details": {"client_request_id": "req-900"},
  "trace_id": "req-802"
}
```

### 7.3 forbidden (cross-organization)

Response 403:

```json
{
  "code": "forbidden",
  "message": "org access denied",
  "details": {"org_id": "org-999"}
}
```

## 8. Test Matrix

| Test ID             | Endpoint                    | Scenario                       | Precondition    | Request                      | Expected Status | Notes                  |
| ------------------- | --------------------------- | ------------------------------ | --------------- | ---------------------------- | --------------- | ---------------------- |
| SNP-CREATE-01       | POST /snapshots             | Create project snapshot        | project exists  | valid body                   | 201             | returns Snapshot DTO   |
| SNP-CREATE-IDEMP-01 | POST /snapshots             | Idempotent replay same payload | none            | same client_request_id twice | 201             | same snapshot returned |
| SNP-CREATE-IDEMP-02 | POST /snapshots             | Idempotency payload mismatch   | first recorded  | same id diff label/scope     | 409             | conflict               |
| SNP-LIST-VAL-01     | GET /snapshots              | Pagination bounds              | snapshots exist | page_size=0                  | 422             | validation_error       |
| SNP-GET-404         | GET /snapshots/{id}         | Missing snapshot in org        | none            | bad id                       | 404             | not_found              |
| SNP-CONTENT-200     | GET /snapshots/{id}/content | Content deterministic ordering | snapshot exists | GET twice                    | 200             | stable ordering        |
| AUD-LIST-REQ-01     | GET /audit/events           | Missing required filters       | none            | entity_type missing          | 422             | validation_error       |
| AUD-LIST-200        | GET /audit/events           | List events sorted desc        | events exist    | sort=-at                     | 200             | stable sort            |
| AUD-403             | GET /audit/events           | Cross-org blocked              | caller org-123  | org-999                      | 403             | forbidden              |

## 9. Self-Audit

* Scope: Planning-only snapshot and audit contracts; no code.
* Authority: Aligned with Steps 01-07; status codes and idempotency aligned with Step 05.
* Determinism: Ordering rules specified for snapshot content and event lists.
* Decision required: None.

## 10. Next Authorized Step

Phase 1 - Step 09: API Indexing and Cross-Doc Registration (Indexes, Roadmap Linking)
