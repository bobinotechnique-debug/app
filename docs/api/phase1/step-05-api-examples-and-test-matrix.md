# Phase 1 - Step 05: API Examples and Test Matrix

## 1. Purpose and Scope
- Convert Step 04 API planning contracts into actionable request/response examples and a minimal validation-focused test matrix.
- Remain planning-only: no implementation detail, database design, or execution semantics.
- Apply Phase 1 boundaries from Steps 01-04 without expanding scope; clarify ambiguities only where Step 04 left multiple options.

## 2. Contract Decisions (Locked)
- **Validation status codes**: Use `422 Unprocessable Entity` for all validation_error responses (lengths, bounds, immutability, pagination, archived-parent rules). Reserve `400 Bad Request` only for malformed JSON or unsupported content type. (Step 04 clarification)
- **Archive mechanism**: Archive operations use dedicated `PATCH .../archive` endpoints only. Generic PATCH endpoints MUST NOT change `state`; attempts to do so return `422 validation_error`. This removes the duplicate state-change path implied in Step 04 PATCH examples. (Step 04 clarification)
- **Filter syntax**: `filter` query parameter accepts a comma-delimited list of `field:value` pairs (AND semantics). Values are exact-match, case-sensitive strings. Allowed fields per list endpoint:
  - Projects: `state`, `name`.
  - Missions: `state`, `name`.
  - Assignments: `state`, `collaborator_id` (nullable matches use `collaborator_id:null`).
  - Collaborators: `state`, `role`.
  Pagination (`page>=1`, `page_size 1-100`) and `sort` (field name, prefix `-` for descending) apply alongside filters; out-of-bounds inputs return `422 validation_error`.
- **Cross-organization behavior**: Any attempt to access or link resources across organizations returns `403 forbidden` (not 404). `404 not_found` is reserved for missing resources within the caller org. (Step 04 clarification)
- **Idempotency scope**: Idempotency key applies per `(org_id, resource_type, client_request_id)`. Replay with identical payload returns the existing resource and `201 Created` (or `200 OK` for POST-initiated replays if implementation prefers), while a payload mismatch returns `409 conflict` without side effects. Keys do not cross resource types or organizations. Duplicate keys expire per server policy (not defined in Phase 1). (Step 04 clarification)
- **Archived parent and immutability**: Archived parents reject new children with `409 conflict`; archived children cannot be reassigned or moved. Organization, project, mission linkage is immutable after creation; attempts to move return `409 conflict`.

## 3. Standard Error Examples
All errors use the Step 04 single error contract:
```json
{
  "code": "validation_error",
  "message": "page_size must be between 1 and 100",
  "details": {"page_size": "must be between 1 and 100"},
  "trace_id": "req-001"
}
```
Other codes: `forbidden` (cross-org), `not_found` (missing in org), `conflict` (idempotency collision or move attempt), `unauthorized` (missing auth). Trace IDs are optional.

## 4. Endpoint Examples
Examples assume base path `/api/phase1` and org `org-123`. Status codes follow the locked decisions above.

### Organization
- **Get Organization (happy path)**
  - Request: `GET /api/phase1/orgs/org-123`
  - Response 200:
```json
{
  "id": "org-123",
  "name": "Northwind Ops",
  "description": "Planning workspace",
  "created_at": "2024-10-01T12:00:00Z",
  "updated_at": "2024-10-05T09:30:00Z"
}
```
- **Cross-org forbidden example**
  - Request: `GET /api/phase1/orgs/org-999`
  - Response 403 forbidden (caller belongs to org-123):
```json
{
  "code": "forbidden",
  "message": "org access denied",
  "details": {"org_id": "org-999"}
}
```

### Projects
- **List Projects (happy path with filter/sort)**
  - Request: `GET /api/phase1/orgs/org-123/projects?page=1&page_size=20&sort=-created_at&filter=state:active`
  - Response 200:
```json
{
  "items": [
    {
      "id": "proj-1",
      "organization_id": "org-123",
      "name": "Migration",
      "purpose": "Move services",
      "notes": "Planning runbooks only",
      "state": "active",
      "created_at": "2024-10-02T08:00:00Z",
      "updated_at": "2024-10-04T08:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```
- **Create Project (happy path with idempotency)**
  - Request: `POST /api/phase1/orgs/org-123/projects`
```json
{
  "client_request_id": "req-123",
  "name": "Migration",
  "purpose": "Move services",
  "notes": "Planning runbooks only"
}
```
  - Response 201:
```json
{
  "id": "proj-1",
  "organization_id": "org-123",
  "name": "Migration",
  "purpose": "Move services",
  "notes": "Planning runbooks only",
  "state": "active",
  "created_at": "2024-10-02T08:00:00Z",
  "updated_at": "2024-10-02T08:00:00Z"
}
```
- **Create Project validation_error (name too long)**
  - Response 422:
```json
{
  "code": "validation_error",
  "message": "name must be between 1 and 140 characters",
  "details": {"name": "too long"}
}
```
- **Create Project conflict (idempotency mismatch)**
  - Same `client_request_id` with different `name` returns 409:
```json
{
  "code": "conflict",
  "message": "client_request_id already used with different payload",
  "details": {"client_request_id": "req-123"}
}
```
- **Update Project (happy path)**
  - Request: `PATCH /api/phase1/orgs/org-123/projects/proj-1`
```json
{
  "notes": "Adjusted scope per planning review"
}
```
  - Response 200 returns updated project; `state` unchanged because archive uses dedicated endpoint.
- **Update Project validation_error (state change blocked)**
  - Request body includes `state`: returns 422 with `details.state: "use /archive"`.
- **Archive Project (happy path)**
  - Request: `PATCH /api/phase1/orgs/org-123/projects/proj-1/archive`
  - Response 200:
```json
{
  "id": "proj-1",
  "organization_id": "org-123",
  "name": "Migration",
  "purpose": "Move services",
  "notes": "Planning runbooks only",
  "state": "archived",
  "created_at": "2024-10-02T08:00:00Z",
  "updated_at": "2024-10-06T10:00:00Z"
}
```
- **Archive Project conflict (archived parent blocks new mission)**
  - Subsequent `POST /api/phase1/orgs/org-123/projects/proj-1/missions` returns 409 conflict with `details.project_id: "archived"`.

### Missions
- **List Missions (happy path)**
  - Request: `GET /api/phase1/orgs/org-123/projects/proj-1/missions?page=1&page_size=10&filter=state:active`
  - Response 200 with mission list and pagination metadata.
- **Create Mission (happy path)**
  - Request: `POST /api/phase1/orgs/org-123/projects/proj-1/missions`
```json
{
  "client_request_id": "req-456",
  "name": "Audit",
  "objective": "Map services",
  "scope_signals": "Planning-only checklist"
}
```
  - Response 201 Mission DTO with `state` default `active`.
- **Create Mission conflict (project archived)**
  - Response 409 with `code: "conflict"` and `details.project_id: "archived"` when parent project archived.
- **Update Mission (happy path)**
  - Request: `PATCH /api/phase1/orgs/org-123/projects/proj-1/missions/msn-1`
```json
{
  "scope_signals": "Updated planning checklist"
}
```
  - Response 200 returns updated mission with immutable project/org linkage.
- **Update Mission conflict (attempted move)**
  - Including `project_id` or `organization_id` returns 409 conflict.
- **Archive Mission (happy path)**
  - Request: `PATCH /api/phase1/orgs/org-123/projects/proj-1/missions/msn-1/archive`
  - Response 200 Mission DTO with `state`=`archived`.
- **Archive Mission conflict (child creation blocked)**
  - Subsequent assignment creation under archived mission returns 409 conflict with `details.mission_id: "archived"`.

### Assignments
- **List Assignments (happy path with filter)**
  - Request: `GET /api/phase1/orgs/org-123/missions/msn-1/assignments?page=1&page_size=10&filter=state:active,collaborator_id:null`
  - Response 200 with assignment list.
- **Create Assignment (happy path)**
  - Request: `POST /api/phase1/orgs/org-123/missions/msn-1/assignments`
```json
{
  "client_request_id": "req-789",
  "title": "Draft checklist",
  "intent": "Capture tasks",
  "acceptance_criteria": "Has sections"
}
```
  - Response 201 Assignment DTO with derived `project_id` and `organization_id`.
- **Create Assignment forbidden (cross-org collaborator)**
  - Using `collaborator_id` from another org returns 403 forbidden with `details.collaborator_id`.
- **Update Assignment (happy path)**
  - Request: `PATCH /api/phase1/orgs/org-123/missions/msn-1/assignments/asn-1`
```json
{
  "collaborator_id": "collab-1"
}
```
  - Response 200 Assignment DTO with collaborator linked.
- **Update Assignment conflict (move attempt)**
  - Including `mission_id` or `project_id` returns 409 conflict with immutable linkage note.
- **Archive Assignment (happy path)**
  - Request: `PATCH /api/phase1/orgs/org-123/missions/msn-1/assignments/asn-1/archive`
  - Response 200 Assignment DTO with `state`=`archived`.
- **Archive Assignment conflict (reassign blocked)**
  - PATCH with `collaborator_id` after archive returns 409 conflict (`details.collaborator_id: "archived assignment"`).

### Collaborators
- **List Collaborators (happy path)**
  - Request: `GET /api/phase1/orgs/org-123/collaborators?page=1&page_size=20&filter=state:active`
  - Response 200 list of collaborators with pagination metadata.
- **Create Collaborator (happy path)**
  - Request: `POST /api/phase1/orgs/org-123/collaborators`
```json
{
  "client_request_id": "req-321",
  "name": "Sam Analyst",
  "role": "Planner",
  "availability_notes": "Q4 only"
}
```
  - Response 201 Collaborator DTO with `state` default `active`.
- **Create Collaborator validation_error (name missing)**
  - Response 422 with `details.name: "required"`.
- **Update Collaborator (happy path)**
  - Request: `PATCH /api/phase1/orgs/org-123/collaborators/collab-1`
```json
{
  "availability_notes": "Q1-Q2 only"
}
```
  - Response 200 Collaborator DTO with updated notes.
- **Update Collaborator conflict (org move attempt)**
  - Including `organization_id` returns 409 conflict.
- **Archive Collaborator (happy path)**
  - Request: `PATCH /api/phase1/orgs/org-123/collaborators/collab-1/archive`
  - Response 200 Collaborator DTO with `state`=`archived`.
- **Archive Collaborator forbidden (cross-org)**
  - Archiving a collaborator from another org returns 403 forbidden with `details.organization_id`.

## 5. API Contract Test Matrix
| Test ID | Endpoint | Scenario | Precondition | Request | Expected Status | Expected Error Code/Notes |
| --- | --- | --- | --- | --- | --- | --- |
| ORG-GET-403 | GET /orgs/{org_id} | Cross-org access blocked | Caller authenticated to org-123 | GET /orgs/org-999 | 403 | forbidden |
| PRJ-LIST-VAL-01 | GET /projects | Pagination bounds | org has projects | page_size=0 | 422 | validation_error (page_size range) |
| PRJ-FILTER-01 | GET /projects | Filter by state | org has active/archived projects | filter=state:archived | 200 | Items only archived |
| PRJ-CREATE-IDEMP-01 | POST /projects | Idempotent replay same payload | none | POST with client_request_id=req-123 twice | 201 second replay | Same body returned |
| PRJ-CREATE-IDEMP-02 | POST /projects | Idempotency payload mismatch | first request recorded | POST with same key different name | 409 | conflict (idempotency mismatch) |
| PRJ-PATCH-IMMUT-01 | PATCH /projects/{project_id} | State change via PATCH rejected | project active | body includes state=archived | 422 | validation_error (use /archive) |
| PRJ-ARCHIVE-CHILD-01 | PATCH /projects/{project_id}/archive | Archived project blocks mission create | project archived | POST mission under project | 409 | conflict (project archived) |
| MSN-LIST-VAL-01 | GET /projects/{project_id}/missions | Pagination bounds | project exists | page=0 | 422 | validation_error (page>=1) |
| MSN-CREATE-CONFLICT-01 | POST /projects/{project_id}/missions | Parent archived | project archived | POST mission | 409 | conflict (project archived) |
| MSN-PATCH-IMMUT-01 | PATCH /missions/{mission_id} | Move mission forbidden | mission active | body includes project_id other | 409 | conflict (immutable linkage) |
| MSN-ARCHIVE-CHILD-01 | PATCH /missions/{mission_id}/archive | Archived mission blocks assignment create | mission archived | POST assignment | 409 | conflict (mission archived) |
| ASN-LIST-VAL-01 | GET /missions/{mission_id}/assignments | Filter null collaborator | assignments exist | filter=collaborator_id:null | 200 | Only unassigned returned |
| ASN-CREATE-FORBID-01 | POST /missions/{mission_id}/assignments | Cross-org collaborator rejected | mission org-123 | body collaborator_id from org-999 | 403 | forbidden |
| ASN-CREATE-CONFLICT-01 | POST /missions/{mission_id}/assignments | Parent archived | mission archived | POST assignment | 409 | conflict |
| ASN-PATCH-IMMUT-01 | PATCH /assignments/{assignment_id} | Attempt move to new mission | mission active | body includes mission_id other | 409 | conflict (immutable linkage) |
| ASN-ARCHIVE-IMMUT-01 | PATCH /assignments/{assignment_id}/archive | Archived assignment reassignment blocked | assignment archived | PATCH collaborator_id | 409 | conflict |
| COL-LIST-FILTER-01 | GET /collaborators | Filter by state | org has mixed states | filter=state:active | 200 | Only active returned |
| COL-CREATE-VAL-01 | POST /collaborators | Missing name | none | body missing name | 422 | validation_error |
| COL-PATCH-IMMUT-01 | PATCH /collaborators/{collaborator_id} | Org move rejected | collaborator active | body includes organization_id | 409 | conflict |
| COL-ARCHIVE-FORBID-01 | PATCH /collaborators/{collaborator_id}/archive | Cross-org archive blocked | collaborator in other org | archive request | 403 | forbidden |
| IDEMP-SCOPE-01 | POST create (any) | Idempotency scoped per org/resource | org-123 project create already used key in org-456 | POST same key in org-456 | 201 | Independent success (no collision) |
| PAG-SORT-01 | List endpoints | Sort descending works | items exist | sort=-created_at | 200 | Items sorted desc |
| FILTER-VAL-01 | List endpoints | Unsupported filter field | any list endpoint | filter=unknown:val | 422 | validation_error (unsupported filter) |
| JSON-400-01 | Any endpoint | Malformed JSON | n/a | invalid JSON body | 400 | validation_error (malformed JSON) |

## 6. Self-Audit
- Scope: Documentation-only within docs/api/phase1; no code, schema, or runtime behavior introduced.
- Authority: Aligned with AGENT.md, Docs Agent, and Phase 1 Steps 01-04; clarifications noted as Step 04 clarifications without scope expansion.
- Roadmap linkage: Phase 1 Step 05 documented as continuation of API planning (Phase 1 lineage 01-04).
- Indexing: Ensure Step 05 registered in applicable API and roadmap indexes.
- Validation status: Step 05 approved for Phase 1 documentation scope.
- Stop conditions: No conflicts detected between Steps 01-04; no DECISION REQUIRED items remain after clarifications.
- DECISION REQUIRED: None.
