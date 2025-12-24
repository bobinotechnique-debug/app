# Phase 1 - Step 04: API Planning Contracts

## 1. Purpose and Scope
- Establish the authoritative planning-only API contract for Phase 1 CRUD around organization, project, mission, assignment, and collaborator resources.
- Reaffirm that Phase 1 planning artifacts (Step 01) remain the single source of truth; API contracts inherit the domain boundaries and invariants from Step 02 and must satisfy UX surface needs from Step 03.
- Explicitly excluded concerns: execution tracking, time logging, delivery automation, contracts, payroll, billing, invoicing, payments, notifications, messaging, analytics, forecasting, reporting, deployment/runtime considerations, identity federation or directory sync, and any database schema or persistence design.

## 2. Global Conventions
- Base path and versioning: All endpoints are exposed under `/api/phase1`. No other versions are permitted in Phase 1 planning.
- Resource naming: `orgs/{org_id}`, `projects`, `missions`, `assignments`, `collaborators`. IDs are opaque strings (UUID-format recommended) supplied by the planning source; no surrogate or cross-organization IDs are allowed.
- Pagination, sorting, filtering: List endpoints MUST support optional `page` (>=1), `page_size` (1-100), `sort` (field name prefixed with `-` for descending), and `filter` (field-equals string filters limited to listed fields per endpoint). Requests outside limits MUST return `validation_error`.
- Timestamps: When present, timestamps MUST be ISO 8601 strings in UTC (`YYYY-MM-DDThh:mm:ssZ`). Timestamps are planning metadata only; no execution or scheduling semantics.
- Idempotency: POST create requests MAY include `client_request_id` (string, <=128 chars) to ensure idempotent creation within an organization scope. Servers MUST treat repeated `client_request_id` submissions with identical payloads as the same operation; mismatched payloads MUST return `conflict`.

## 3. Auth and Tenancy Contract (Planning Boundary)
- Every request is scoped to exactly one organization, expressed in the path as `/orgs/{org_id}/...`.
- The `{org_id}` path parameter MUST match the authenticated organization context; cross-organization access MUST return `forbidden`.
- Resources MUST NOT be created, read, or updated outside their owning organization. Any attempt to reference a project, mission, assignment, or collaborator from another organization MUST return `forbidden`.

## 4. Canonical Schemas (Planning DTOs)
All DTOs inherit Phase 1 invariants: no entity may cross organization boundaries; mission belongs to one project; assignment belongs to one mission; collaborator belongs to one organization. Derived or aggregated fields beyond those defined here are forbidden in Phase 1.

### Organization DTO
- `id` (string, required): Organization identifier; immutable.
- `name` (string, required): 1-140 characters; planning display name.
- `description` (string, optional): 0-500 characters; planning context only.
- `created_at` (string, required): ISO 8601 UTC.
- `updated_at` (string, required): ISO 8601 UTC.
- Invariants: organization is the security boundary; no cross-organization relationships (Step 02).

### Project DTO
- `id` (string, required): Project identifier; immutable.
- `organization_id` (string, required): MUST match the enclosing org path; immutable after creation.
- `name` (string, required): 1-140 characters.
- `purpose` (string, optional): 0-500 characters describing planning intent.
- `notes` (string, optional): 0-2000 characters for planning details; no execution status allowed.
- `state` (string, required): `active` or `archived` (planning visibility only); default `active`.
- `created_at` (string, required): ISO 8601 UTC.
- `updated_at` (string, required): ISO 8601 UTC.
- Invariants: project belongs to exactly one organization; must not move across organizations (Step 02).

### Mission DTO
- `id` (string, required): Mission identifier; immutable.
- `project_id` (string, required): MUST reference a project under the same organization; immutable after creation.
- `organization_id` (string, required): Derived from the project; MUST equal org path; read-only.
- `name` (string, required): 1-140 characters.
- `objective` (string, optional): 0-500 characters capturing mission intent.
- `scope_signals` (string, optional): 0-2000 characters; planning-only descriptors; MUST NOT express execution tracking.
- `state` (string, required): `active` or `archived`; default `active`; archived missions MUST NOT accept new assignments.
- `created_at` (string, required): ISO 8601 UTC.
- `updated_at` (string, required): ISO 8601 UTC.
- Invariants: mission belongs to exactly one project and inherits its organization; must not own collaborators directly (Step 02).

### Assignment DTO
- `id` (string, required): Assignment identifier; immutable.
- `mission_id` (string, required): MUST reference a mission under the same project and organization; immutable after creation.
- `project_id` (string, required): Derived from the mission; read-only; MUST equal the mission’s project.
- `organization_id` (string, required): Derived from project; read-only; MUST equal org path.
- `title` (string, required): 1-140 characters.
- `intent` (string, optional): 0-500 characters describing planning intent.
- `acceptance_criteria` (string, optional): 0-2000 characters; planning expectations only; MUST NOT include execution tracking signals.
- `collaborator_id` (string, optional): MUST reference a collaborator within the same organization; null means unassigned in planning.
- `state` (string, required): `active` or `archived`; default `active`; archived assignments MUST NOT be reassigned.
- `created_at` (string, required): ISO 8601 UTC.
- `updated_at` (string, required): ISO 8601 UTC.
- Invariants: assignment belongs to exactly one mission; inherits project and organization; collaborator links cannot cross organizations (Step 02).

### Collaborator DTO
- `id` (string, required): Collaborator identifier; immutable.
- `organization_id` (string, required): MUST match org path; immutable.
- `name` (string, required): 1-140 characters.
- `role` (string, optional): 0-120 characters describing planning role expectations.
- `availability_notes` (string, optional): 0-2000 characters; planning-only signals; no scheduling or time tracking allowed.
- `state` (string, required): `active` or `archived`; default `active`; archived collaborators MUST NOT receive new assignments.
- `created_at` (string, required): ISO 8601 UTC.
- `updated_at` (string, required): ISO 8601 UTC.
- Invariants: collaborator belongs to exactly one organization; cannot be shared across organizations (Step 02).

## 5. Endpoints (Planning CRUD only)
All endpoints inherit global conventions, auth/tenancy rules, and error contract. Updates use PATCH (partial) to avoid forcing unrelated planning fields and to align with UX editing patterns; PUT is forbidden. Archive operations use a soft-archive PATCH that sets `state` to `archived`.

### Organization
#### Get Organization
- **Method + Path**: GET `/api/phase1/orgs/{org_id}`
- **Purpose**: Retrieve planning details for a single organization.
- **Response**: Organization DTO.
- **Status Codes**: 200, 401 (`unauthorized`), 403 (`forbidden`), 404 (`not_found`).
- **Validation**: `org_id` required; must match authenticated org.
- **Forbidden States Prevented**: Cross-organization access blocked.
- **Example Response**:
```
{
  "id": "org-123",
  "name": "Northwind Ops",
  "description": "Planning workspace",
  "created_at": "2024-10-01T12:00:00Z",
  "updated_at": "2024-10-05T09:30:00Z"
}
```

### Projects
#### List Projects
- **Method + Path**: GET `/api/phase1/orgs/{org_id}/projects`
- **Purpose**: List projects within an organization with pagination and optional filtering by `state`.
- **Response**: `{ "items": [Project DTO], "page": number, "page_size": number, "total": number }`
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: `org_id` required; `page` >=1; `page_size` 1-100; `sort` limited to `name`, `state`, `created_at`.
- **Forbidden States Prevented**: Projects from other organizations MUST NOT appear.
- **Example Response**:
```
{
  "items": [
    {"id": "proj-1", "organization_id": "org-123", "name": "Migration", "state": "active", "purpose": "Move services", "notes": null, "created_at": "2024-10-02T08:00:00Z", "updated_at": "2024-10-04T08:00:00Z"},
    {"id": "proj-2", "organization_id": "org-123", "name": "Launch", "state": "archived", "purpose": "Retrospective", "notes": "Completed", "created_at": "2024-09-01T12:00:00Z", "updated_at": "2024-09-15T12:00:00Z"}
  ],
  "page": 1,
  "page_size": 20,
  "total": 2
}
```

#### Get Project
- **Method + Path**: GET `/api/phase1/orgs/{org_id}/projects/{project_id}`
- **Purpose**: Retrieve a single project scoped to the organization.
- **Response**: Project DTO.
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: `project_id` must belong to `{org_id}`.
- **Forbidden States Prevented**: Cross-organization access blocked.
- **Example Response**:
```
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
```

#### Create Project
- **Method + Path**: POST `/api/phase1/orgs/{org_id}/projects`
- **Purpose**: Create a project in the organization.
- **Request Body**:
```
{
  "client_request_id": "optional-idempotency-key",
  "name": "string (1-140)",
  "purpose": "string (0-500)",
  "notes": "string (0-2000)",
  "state": "active" | "archived"
}
```
- **Response**: Project DTO.
- **Status Codes**: 201, 400 (`validation_error`), 401, 403, 409 (`conflict` when idempotency key clashes), 422 (`validation_error` if constraints fail).
- **Validation**: Name required; lengths enforced; `state` defaults to `active`; organization_id derived from path and immutable.
- **Forbidden States Prevented**: Cross-organization creation; missing organization; creation outside planning scope.
- **Example Request**:
```
{
  "client_request_id": "req-123",
  "name": "Migration",
  "purpose": "Move services",
  "notes": "Planning runbooks only",
  "state": "active"
}
```
- **Example Response**: Project DTO with generated identifiers and timestamps matching the request constraints.

#### Update Project (Partial)
- **Method + Path**: PATCH `/api/phase1/orgs/{org_id}/projects/{project_id}`
- **Purpose**: Update planning fields of a project.
- **Request Body**: Any subset of `name`, `purpose`, `notes`, `state`.
- **Response**: Project DTO.
- **Status Codes**: 200, 400, 401, 403, 404, 409 (if attempting to change immutable org/project relationship).
- **Validation**: Cannot change `organization_id` or `id`; state change to `archived` MUST NOT remove organization linkage.
- **Forbidden States Prevented**: Moving project across organizations; violating length constraints.
- **Example Request**:
```
{
  "notes": "Adjusted scope per planning review",
  "state": "archived"
}
```
- **Example Response**: Updated Project DTO reflecting new notes and state while keeping identifiers unchanged.

#### Archive Project
- **Method + Path**: PATCH `/api/phase1/orgs/{org_id}/projects/{project_id}/archive`
- **Purpose**: Set project `state` to `archived` for planning visibility.
- **Response**: Project DTO with `state`=`archived`.
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: Project must belong to org; already archived MAY return 200 with unchanged state.
- **Forbidden States Prevented**: Cross-organization state changes; project deletion that would orphan missions.
- **Example Response**: Project DTO with `state` set to `archived` and unchanged identifiers.

### Missions
#### List Missions
- **Method + Path**: GET `/api/phase1/orgs/{org_id}/projects/{project_id}/missions`
- **Purpose**: List missions within a project.
- **Response**: `{ "items": [Mission DTO], "page": number, "page_size": number, "total": number }`
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: `project_id` must belong to `{org_id}`; pagination constraints; `sort` allowed on `name`, `state`, `created_at`.
- **Forbidden States Prevented**: Missions from other projects or organizations excluded.
- **Example Response**:
```
{
  "items": [
    {"id": "msn-1", "project_id": "proj-1", "organization_id": "org-123", "name": "Audit", "objective": "Map services", "scope_signals": null, "state": "active", "created_at": "2024-10-03T08:00:00Z", "updated_at": "2024-10-04T08:00:00Z"}
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```

#### Get Mission
- **Method + Path**: GET `/api/phase1/orgs/{org_id}/projects/{project_id}/missions/{mission_id}`
- **Purpose**: Retrieve a mission within the specified project.
- **Response**: Mission DTO.
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: Mission must belong to project and organization; organization_id is derived, not supplied by client.
- **Forbidden States Prevented**: Cross-project or cross-organization access.
- **Example Response**:
```
{
  "id": "msn-1",
  "project_id": "proj-1",
  "organization_id": "org-123",
  "name": "Audit",
  "objective": "Map services",
  "scope_signals": null,
  "state": "active",
  "created_at": "2024-10-03T08:00:00Z",
  "updated_at": "2024-10-04T08:00:00Z"
}
```

#### Create Mission
- **Method + Path**: POST `/api/phase1/orgs/{org_id}/projects/{project_id}/missions`
- **Purpose**: Create a mission under the project.
- **Request Body**:
```
{
  "client_request_id": "optional-idempotency-key",
  "name": "string (1-140)",
  "objective": "string (0-500)",
  "scope_signals": "string (0-2000)",
  "state": "active" | "archived"
}
```
- **Response**: Mission DTO.
- **Status Codes**: 201, 400, 401, 403, 404, 409, 422.
- **Validation**: Project must exist within org; name required; mission inherits organization_id and project_id from path; state defaults to `active`.
- **Forbidden States Prevented**: Missions outside project; missions across organizations; archived project MAY reject new missions with `conflict`.
- **Example Request**:
```
{
  "client_request_id": "req-456",
  "name": "Audit",
  "objective": "Map services",
  "scope_signals": "Planning-only checklist",
  "state": "active"
}
```
- **Example Response**: Mission DTO reflecting provided fields with generated identifiers and timestamps.

#### Update Mission (Partial)
- **Method + Path**: PATCH `/api/phase1/orgs/{org_id}/projects/{project_id}/missions/{mission_id}`
- **Purpose**: Update planning fields of a mission.
- **Request Body**: Any subset of `name`, `objective`, `scope_signals`, `state`.
- **Response**: Mission DTO.
- **Status Codes**: 200, 400, 401, 403, 404, 409 (if attempting to move mission).
- **Validation**: `project_id` and `organization_id` immutable; archiving prevents new assignments.
- **Forbidden States Prevented**: Moving mission to another project; violating invariants; adding collaborators directly to missions.
- **Example Request**:
```
{
  "scope_signals": "Updated planning checklist",
  "state": "archived"
}
```
- **Example Response**: Updated Mission DTO reflecting new scope signals and archived state.

#### Archive Mission
- **Method + Path**: PATCH `/api/phase1/orgs/{org_id}/projects/{project_id}/missions/{mission_id}/archive`
- **Purpose**: Set mission `state` to `archived`.
- **Response**: Mission DTO with `state`=`archived`.
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: Mission must belong to project and organization; archived mission MUST NOT allow new assignments.
- **Forbidden States Prevented**: Cross-project state changes; orphaned assignments without mission context.
- **Example Response**: Mission DTO with `state` set to `archived` and unchanged identifiers.

### Assignments
#### List Assignments
- **Method + Path**: GET `/api/phase1/orgs/{org_id}/missions/{mission_id}/assignments`
- **Purpose**: List assignments under a mission.
- **Response**: `{ "items": [Assignment DTO], "page": number, "page_size": number, "total": number }`
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: Mission must belong to org; pagination constraints; `sort` allowed on `title`, `state`, `created_at`.
- **Forbidden States Prevented**: Assignments from other missions or organizations excluded.
- **Example Response**:
```
{
  "items": [
    {"id": "asn-1", "mission_id": "msn-1", "project_id": "proj-1", "organization_id": "org-123", "title": "Draft checklist", "intent": "Capture tasks", "acceptance_criteria": "Has sections", "collaborator_id": null, "state": "active", "created_at": "2024-10-03T10:00:00Z", "updated_at": "2024-10-04T11:00:00Z"}
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```

#### Get Assignment
- **Method + Path**: GET `/api/phase1/orgs/{org_id}/missions/{mission_id}/assignments/{assignment_id}`
- **Purpose**: Retrieve an assignment under a mission.
- **Response**: Assignment DTO.
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: Assignment must belong to mission and organization.
- **Forbidden States Prevented**: Cross-mission or cross-organization access.
- **Example Response**:
```
{
  "id": "asn-1",
  "mission_id": "msn-1",
  "project_id": "proj-1",
  "organization_id": "org-123",
  "title": "Draft checklist",
  "intent": "Capture tasks",
  "acceptance_criteria": "Has sections",
  "collaborator_id": null,
  "state": "active",
  "created_at": "2024-10-03T10:00:00Z",
  "updated_at": "2024-10-04T11:00:00Z"
}
```

#### Create Assignment
- **Method + Path**: POST `/api/phase1/orgs/{org_id}/missions/{mission_id}/assignments`
- **Purpose**: Create a planning assignment under the mission.
- **Request Body**:
```
{
  "client_request_id": "optional-idempotency-key",
  "title": "string (1-140)",
  "intent": "string (0-500)",
  "acceptance_criteria": "string (0-2000)",
  "collaborator_id": "string or null",
  "state": "active" | "archived"
}
```
- **Response**: Assignment DTO.
- **Status Codes**: 201, 400, 401, 403, 404, 409, 422.
- **Validation**: Mission must belong to org; title required; collaborator_id if provided MUST belong to the same organization; state defaults to `active`; archived mission MUST reject new assignments with `conflict`.
- **Forbidden States Prevented**: Assignments outside mission; cross-organization collaborator links; creation when mission archived.
- **Example Request**:
```
{
  "client_request_id": "req-789",
  "title": "Draft checklist",
  "intent": "Capture tasks",
  "acceptance_criteria": "Has sections",
  "collaborator_id": null,
  "state": "active"
}
```
- **Example Response**: Assignment DTO reflecting provided fields with generated identifiers and timestamps.

#### Update Assignment (Partial)
- **Method + Path**: PATCH `/api/phase1/orgs/{org_id}/missions/{mission_id}/assignments/{assignment_id}`
- **Purpose**: Update planning fields of an assignment.
- **Request Body**: Any subset of `title`, `intent`, `acceptance_criteria`, `collaborator_id`, `state`.
- **Response**: Assignment DTO.
- **Status Codes**: 200, 400, 401, 403, 404, 409 (if attempting to move assignment).
- **Validation**: `mission_id`, `project_id`, `organization_id` immutable; collaborator_id if provided MUST belong to same organization; archived assignments MUST NOT be reassigned.
- **Forbidden States Prevented**: Moving assignment to another mission; cross-organization collaborator links; violating archival rules.
- **Example Request**:
```
{
  "collaborator_id": "collab-9",
  "state": "archived"
}
```
- **Example Response**: Updated Assignment DTO with collaborator linked and `state` archived while preserving identifiers.

#### Archive Assignment
- **Method + Path**: PATCH `/api/phase1/orgs/{org_id}/missions/{mission_id}/assignments/{assignment_id}/archive`
- **Purpose**: Set assignment `state` to `archived`.
- **Response**: Assignment DTO with `state`=`archived`.
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: Assignment must belong to mission and organization; archived assignments MUST NOT accept collaborator changes.
- **Forbidden States Prevented**: Cross-mission state changes; breaking mission/project/organization linkage.
- **Example Response**: Assignment DTO with `state` set to `archived` and unchanged mission/project/org linkage.

### Collaborators
#### List Collaborators
- **Method + Path**: GET `/api/phase1/orgs/{org_id}/collaborators`
- **Purpose**: List collaborators within an organization.
- **Response**: `{ "items": [Collaborator DTO], "page": number, "page_size": number, "total": number }`
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: Pagination constraints; `sort` allowed on `name`, `state`, `created_at`; filters MAY include `state`.
- **Forbidden States Prevented**: Cross-organization collaborator visibility.
- **Example Response**:
```
{
  "items": [
    {"id": "collab-1", "organization_id": "org-123", "name": "Sam Analyst", "role": "Planner", "availability_notes": "Q4 only", "state": "active", "created_at": "2024-10-01T08:00:00Z", "updated_at": "2024-10-02T08:00:00Z"}
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```

#### Get Collaborator
- **Method + Path**: GET `/api/phase1/orgs/{org_id}/collaborators/{collaborator_id}`
- **Purpose**: Retrieve a collaborator within an organization.
- **Response**: Collaborator DTO.
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: Collaborator must belong to organization.
- **Forbidden States Prevented**: Cross-organization access.
- **Example Response**:
```
{
  "id": "collab-1",
  "organization_id": "org-123",
  "name": "Sam Analyst",
  "role": "Planner",
  "availability_notes": "Q4 only",
  "state": "active",
  "created_at": "2024-10-01T08:00:00Z",
  "updated_at": "2024-10-02T08:00:00Z"
}
```

#### Create Collaborator
- **Method + Path**: POST `/api/phase1/orgs/{org_id}/collaborators`
- **Purpose**: Create a collaborator scoped to the organization.
- **Request Body**:
```
{
  "client_request_id": "optional-idempotency-key",
  "name": "string (1-140)",
  "role": "string (0-120)",
  "availability_notes": "string (0-2000)",
  "state": "active" | "archived"
}
```
- **Response**: Collaborator DTO.
- **Status Codes**: 201, 400, 401, 403, 409, 422.
- **Validation**: Name required; organization derived from path; state defaults to `active`.
- **Forbidden States Prevented**: Cross-organization creation; associating collaborator with multiple organizations.
- **Example Request**:
```
{
  "client_request_id": "req-321",
  "name": "Sam Analyst",
  "role": "Planner",
  "availability_notes": "Q4 only",
  "state": "active"
}
```
- **Example Response**: Collaborator DTO reflecting provided fields with generated identifiers and timestamps.

#### Update Collaborator (Partial)
- **Method + Path**: PATCH `/api/phase1/orgs/{org_id}/collaborators/{collaborator_id}`
- **Purpose**: Update planning fields of a collaborator.
- **Request Body**: Any subset of `name`, `role`, `availability_notes`, `state`.
- **Response**: Collaborator DTO.
- **Status Codes**: 200, 400, 401, 403, 404, 409 (if attempting to change organization linkage).
- **Validation**: `organization_id` immutable; archived collaborators MUST NOT receive new assignments.
- **Forbidden States Prevented**: Moving collaborator across organizations; violating length constraints.
- **Example Request**:
```
{
  "availability_notes": "Q1-Q2 only",
  "state": "archived"
}
```
- **Example Response**: Updated Collaborator DTO reflecting new availability notes and archived state.

#### Archive Collaborator
- **Method + Path**: PATCH `/api/phase1/orgs/{org_id}/collaborators/{collaborator_id}/archive`
- **Purpose**: Set collaborator `state` to `archived`.
- **Response**: Collaborator DTO with `state`=`archived`.
- **Status Codes**: 200, 401, 403, 404.
- **Validation**: Collaborator must belong to organization; archived collaborators MUST NOT be assigned to new missions or assignments.
- **Forbidden States Prevented**: Cross-organization state changes; collaborator sharing.
- **Example Response**: Collaborator DTO with `state` set to `archived` and organization linkage unchanged.

## 6. Relationship Rules (Contract Level)
- Project belongs to exactly one organization; API paths enforce `/orgs/{org_id}/projects`.
- Mission belongs to exactly one project and inherits its organization; API paths enforce `/orgs/{org_id}/projects/{project_id}/missions`.
- Assignment belongs to exactly one mission and inherits the mission’s project and organization; API paths enforce `/orgs/{org_id}/missions/{mission_id}/assignments`.
- Collaborator belongs to exactly one organization; API paths enforce `/orgs/{org_id}/collaborators`.
- Assignment references: `collaborator_id` MAY link an assignment to one collaborator within the same organization. If collaborator linkage rules are ambiguous in future phases, further decisions are required; Phase 1 restricts to single-collaborator reference to align with Step 03 planning surfaces. Missions MUST NOT own collaborators directly.

## 7. Error Contract (Single Standard)
All error responses MUST use the following structure:
```
{
  "code": "validation_error | not_found | forbidden | conflict | unauthorized",
  "message": "human-readable summary",
  "details": { "field": "description" } | [ {"field": "description"} ],
  "trace_id": "optional string for diagnostics"
}
```
- `validation_error`: Input fails constraints (lengths, formats, immutability, pagination limits, forbidden state violations).
- `not_found`: Resource does not exist within the organization scope.
- `forbidden`: Authenticated principal lacks access or attempts cross-organization linkage.
- `conflict`: Idempotency key collision, attempts to create under archived parent, or attempts to move entities across boundaries.
- `unauthorized`: Missing or invalid authentication context (planning boundary only).

## 8. Self Audit
- Scope respected: Documentation-only under `docs/api/phase1`; planning CRUD contracts without implementation, execution, finance, or analytics topics.
- Authority respected: Aligns with AGENT.md, Phase 1 Step 01 (planning source of truth), Step 02 (domain boundaries and forbidden states), and Step 03 (UX surface expectations) without conflicts.
- Invariants enforced: Organization boundary on every endpoint; missions tied to one project; assignments tied to one mission; collaborators tied to one organization; cross-organization states blocked; archived parents prevent new children where applicable.
- No leakage: No database schema, persistence strategy, runtime behavior, or non-planning features introduced.
