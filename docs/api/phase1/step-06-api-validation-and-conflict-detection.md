# Phase 1 - Step 06: API Validation and Conflict Detection

## 1. Purpose and Scope

* Define the planning-only API contract for validating planning data and detecting conflicts.
* Extend Phase 1 Steps 01-05 without introducing execution, payroll, or contract issuance semantics.
* Provide deterministic, side-effect-free endpoints that return validation reports for:
  * Organization scope
  * Project scope
  * Mission scope
  * Collaborator scope

OUT OF SCOPE:

* Any mutation or auto-fix of planning data.
* Execution-time constraints.
* Financial, payroll, or legal compliance checks.

## 2. Authority

* Planning remains the source of truth (Phase 1 Step 01).
* Domain boundaries and invariants remain authoritative (Phase 1 Step 02).
* API resource boundaries and error contract remain authoritative (Phase 1 Step 04).
* Examples and status-code decisions remain authoritative (Phase 1 Step 05).

## 3. Locked Decisions

### 3.1 Read-only and Deterministic

* All validation endpoints are read-only.
* Same input planning state MUST yield the same output (deterministic).
* Validation endpoints MUST NOT mutate resources, create derived resources, or enqueue actions.

### 3.2 Status Codes

* 200 OK for successful validation responses (even if invalid).
* 404 not_found for missing resources within caller org.
* 403 forbidden for cross-organization access or linkage attempts.
* 422 validation_error for invalid query params (pagination, filters, enums).
* 400 bad_request only for malformed JSON or unsupported content type.

### 3.3 Validation Result Semantics

* Validation returns a report with:
  * status: VALID or INVALID
  * blocking_errors: list
  * warnings: list
* INVALID means at least one blocking error.
* Warnings never change status to INVALID.

### 3.4 Versioning

* Validation rules are versioned as a simple string.
* The API returns rule_version in every report.
* rule_version changes are allowed without changing endpoint paths.

## 4. Validation Domain (API View)

### 4.1 Validation Item

A validation item is a structured, traceable finding.

Fields:

* id: stable identifier within the report (string)
* level: BLOCKING or WARNING
* category: STRUCTURAL | TEMPORAL | OVERLAP | LOAD | REST
* message: human-readable
* entity_type: organization | project | mission | assignment | collaborator
* entity_id: string
* related: optional list of related entities (entity_type/entity_id)
* time_range: optional {"start": "...", "end": "..."} for time-based findings

### 4.2 Deterministic Sorting

* blocking_errors and warnings MUST be returned in deterministic order:
  * by category
  * then by entity_type
  * then by entity_id
  * then by start timestamp if present
  * then by id

## 5. Validation Report Contract

Response body for all validation endpoints:

```json
{
  "scope": {
    "type": "project",
    "organization_id": "org-123",
    "project_id": "proj-1"
  },
  "status": "INVALID",
  "rule_version": "phase1.v1",
  "blocking_errors": [
    {
      "id": "E-001",
      "level": "BLOCKING",
      "category": "OVERLAP",
      "message": "collaborator has overlapping assignments",
      "entity_type": "collaborator",
      "entity_id": "collab-1",
      "related": [
        {"entity_type": "assignment", "entity_id": "asn-1"},
        {"entity_type": "assignment", "entity_id": "asn-2"}
      ],
      "time_range": {"start": "2024-10-10T08:00:00Z", "end": "2024-10-10T12:00:00Z"}
    }
  ],
  "warnings": [
    {
      "id": "W-001",
      "level": "WARNING",
      "category": "REST",
      "message": "rest time below threshold",
      "entity_type": "collaborator",
      "entity_id": "collab-1",
      "related": [{"entity_type": "assignment", "entity_id": "asn-3"}]
    }
  ]
}
```

Notes:

* scope.type is one of: organization | project | mission | collaborator
* The scope object includes only the relevant ids.

## 6. Endpoints

Base path: `/api/phase1`

### 6.1 Validate Organization

* GET `/orgs/{org_id}/validate`

Semantics:

* Validates all planning entities within the organization.
* Returns a single report.

Example:

* Request: `GET /api/phase1/orgs/org-123/validate`
* Response 200: validation report with scope.type=organization

### 6.2 Validate Project

* GET `/orgs/{org_id}/projects/{project_id}/validate`

Semantics:

* Validates project, its missions, assignments, and collaborators linked within the project.
* Includes overlap checks across missions within the same project.

Example:

* Request: `GET /api/phase1/orgs/org-123/projects/proj-1/validate`
* Response 200: validation report with scope.type=project

### 6.3 Validate Mission

* GET `/orgs/{org_id}/projects/{project_id}/missions/{mission_id}/validate`

Semantics:

* Validates mission and its assignments.
* Includes overlap checks for collaborators within the mission.

Example:

* Request: `GET /api/phase1/orgs/org-123/projects/proj-1/missions/msn-1/validate`
* Response 200: validation report with scope.type=mission

### 6.4 Validate Collaborator

* GET `/orgs/{org_id}/collaborators/{collaborator_id}/validate`

Semantics:

* Validates collaborator planning load and conflicts across assignments within the organization.
* Includes overlap checks across all missions/projects where the collaborator is assigned.

Example:

* Request: `GET /api/phase1/orgs/org-123/collaborators/collab-1/validate`
* Response 200: validation report with scope.type=collaborator

## 7. Optional Query Parameters

### 7.1 Include Filters

All validate endpoints MAY accept:

* `include=blocking,warnings` (default both)

Rules:

* If include excludes warnings, warnings array is empty.
* If include excludes blocking, blocking_errors array is empty.
* Invalid include values return 422 validation_error.

### 7.2 Category Filters

All validate endpoints MAY accept:

* `categories=STRUCTURAL,TEMPORAL,OVERLAP,LOAD,REST` (comma-delimited)

Rules:

* Restricts findings to listed categories.
* Unknown categories return 422 validation_error.

## 8. Standard Error Examples

Error contract remains the Step 04 single error contract.

### 8.1 Validation error (bad categories)

Response 422:

```json
{
  "code": "validation_error",
  "message": "unknown category: COSTING",
  "details": {"categories": "unsupported value COSTING"},
  "trace_id": "req-002"
}
```

### 8.2 Forbidden cross-org

Response 403:

```json
{
  "code": "forbidden",
  "message": "org access denied",
  "details": {"org_id": "org-999"}
}
```

### 8.3 Not found within org

Response 404:

```json
{
  "code": "not_found",
  "message": "mission not found",
  "details": {"mission_id": "msn-404"}
}
```

## 9. API Contract Test Matrix (Validation)
| Test ID        | Endpoint                            | Scenario                                | Precondition                  | Request                         | Expected Status | Expected Error Code/Notes       |
| -------------- | ----------------------------------- | --------------------------------------- | ----------------------------- | ------------------------------- | --------------- | ------------------------------- |
| VAL-ORG-200    | GET /orgs/{org_id}/validate         | Org validation returns report           | Org exists                    | GET /orgs/org-123/validate      | 200             | status VALID/INVALID allowed    |
| VAL-ORG-403    | GET /orgs/{org_id}/validate         | Cross-org blocked                       | Caller org-123                | GET /orgs/org-999/validate      | 403             | forbidden                       |
| VAL-PRJ-404    | GET /projects/{project_id}/validate | Missing project in org                  | none                          | GET /projects/proj-404/validate | 404             | not_found                       |
| VAL-PRJ-200    | GET /projects/{project_id}/validate | Project validation deterministic        | Project exists                | GET twice                       | 200             | Same output ordering            |
| VAL-MSN-200    | GET /missions/{mission_id}/validate | Mission validation includes assignments | Mission has assignments       | GET validate                    | 200             | Findings reference assignments  |
| VAL-COL-200    | GET /collaborators/{id}/validate    | Collaborator overlap detected           | Overlapping assignments exist | GET validate                    | 200             | blocking_errors include OVERLAP |
| VAL-INCLUDE-01 | Any validate                        | include filters warnings out            | Findings include warnings     | include=blocking                | 200             | warnings empty                  |
| VAL-INCLUDE-02 | Any validate                        | include invalid value                   | none                          | include=foo                     | 422             | validation_error                |
| VAL-CAT-01     | Any validate                        | categories filter restricts output      | Multiple categories exist     | categories=OVERLAP              | 200             | Only OVERLAP findings           |
| VAL-CAT-02     | Any validate                        | categories invalid                      | none                          | categories=COSTING              | 422             | validation_error                |

## 10. Self-Audit

* Scope: Documentation-only within docs/api/phase1; no code changes.
* Authority: Aligned with Phase 1 Steps 01-05; uses the existing error contract and status decisions.
* Planning-only: No execution, payroll, or contract issuance semantics introduced.
* Determinism: Sorting and rule_version specified to ensure stable outputs.
* Indexing: Ensure Step 06 is registered in applicable API and roadmap indexes.
* DECISION REQUIRED: None.

## 11. Next Authorized Step

Phase 1 - Step 07: Planning State Transitions (Draft, Validated, Frozen)
