# Phase 1 - Step 07: Planning State Transitions (Draft, Validated, Frozen)

## 1. Purpose and Scope

* Define the authoritative Phase 1 planning state machine and allowed transitions.
* Ensure state transitions are consistent with:
  * Planning-as-source-of-truth (Step 01)
  * Domain boundaries and invariants (Step 02)
  * UX surface expectations (Step 03)
  * API planning contracts (Step 04)
  * API examples and test matrix (Step 05)
  * Validation and conflict detection endpoints (Step 06)

Planning-only: no execution, payroll, invoicing, or contract issuance semantics.

**Lifecycle Authority Alignment (DEC-P1-LIFECYCLE-001)**

* Specs Step 12 is authoritative for lifecycles per entity (organization, project, mission, assignment, collaborator).
* The `planning_state` values in this document are a compatibility overlay for API consumers and must be derived from the canonical entity lifecycles, not treated as an independent lifecycle model.
* Organization lifecycle coverage follows Specs Step 12 (active/archived) and is **not** expressed through `planning_state` endpoints.

## 2. Entities with Planning State

Phase 1 planning state applies to the following entities as a derived view over their canonical lifecycles:

* Project
* Mission
* Assignment
* Collaborator

Notes:

* Organization lifecycle is governed directly by Specs Step 12 (active/archived) and uses lifecycle-aware endpoints rather than `planning_state` transitions.
* "Archived" remains a separate axis controlled by dedicated /archive endpoints per Step 05. This step does not redefine archive semantics.
* `planning_state` is read-only with respect to Specs Step 12 authority: transitions exposed here MUST NOT contradict or bypass lifecycle constraints.

## 3. State Definitions

### 3.1 DRAFT

* Default state for new planning entities.
* Editable subject to general immutability rules (org/project/mission linkage immutability from Steps 04-05).
* May contain validation warnings or blocking errors.

### 3.2 VALIDATED

* Planning entity has been validated against the Step 06 rule set.
* VALIDATED means: validation report has zero blocking_errors at the time of transition.
* Warnings may exist.

### 3.3 FROZEN

* Planning entity is locked against further edits (except archival).
* Intended for "ready to execute later" while still within planning scope.
* No automatic downstream artifacts are created in Phase 1.

## 4. Transition Rules

### 4.1 Allowed Transitions

* DRAFT -> VALIDATED
* VALIDATED -> DRAFT (explicit revert)
* VALIDATED -> FROZEN
* FROZEN -> VALIDATED (explicit unfreeze)

Disallowed:

* DRAFT -> FROZEN (must validate first)
* FROZEN -> DRAFT (must unfreeze to VALIDATED first)

### 4.2 Preconditions

DRAFT -> VALIDATED requires:

* Latest validation report for the entity scope contains zero blocking_errors.
* Cross-entity constraints apply (see 5.2) so the entity cannot be validated while its required parent scope is invalid.

VALIDATED -> FROZEN requires:

* Latest validation report contains zero blocking_errors.
* Entity is not archived.

VALIDATED -> DRAFT requires:

* Explicit operator intent (no implicit revert).
* No validation prerequisite.

FROZEN -> VALIDATED requires:

* Explicit operator intent (no implicit unfreeze).
* No validation prerequisite at transition time (but subsequent edits are allowed only after unfreeze).

## 5. Hierarchy and Dependency Constraints

### 5.1 Planning Hierarchy

* Project contains Missions.
* Mission contains Assignments.
* Collaborator may be linked to Assignments.

### 5.2 Validation Dependency (Parent Gating)

The following gating rules apply for transitions into VALIDATED or FROZEN:

* A Mission cannot transition to VALIDATED or FROZEN unless its parent Project is at least VALIDATED.
* An Assignment cannot transition to VALIDATED or FROZEN unless its parent Mission is at least VALIDATED.

Rationale:

* Prevent "locally validated" children inside globally invalid parent scopes.

### 5.3 Freeze Propagation (No Auto-Prop in Phase 1)

* Freezing does not automatically freeze children.
* However, edits to children may be blocked by parent freeze (see 6.2).

## 6. Editability Matrix

### 6.1 Editable Fields by State

* DRAFT: editable (subject to base immutability rules and archived rules).
* VALIDATED: editable, but edits SHOULD trigger re-validation in UX flows.
* FROZEN: not editable, except via explicit unfreeze (FROZEN -> VALIDATED) and subject to lifecycle limits in Specs Step 12.

### 6.2 Parent Freeze Impact

If a parent is FROZEN:

* Creating new children under that parent is blocked.
* Updating existing children under that parent is blocked.

Examples:

* If Project is FROZEN, cannot create or update Missions under it.
* If Mission is FROZEN, cannot create or update Assignments under it.

Blocking errors use 409 conflict with details indicating parent is frozen.

## 7. API Contract (Planning-only)

Base path: /api/phase1

### 7.1 Read State

* State is returned on all relevant DTOs as `planning_state`.
* planning_state is one of: draft, validated, frozen.
* planning_state values are derived from canonical lifecycle states defined in Specs Step 12 and serve as a compatibility layer for Phase 1 API consumers.

#### 7.1.1 planning_state Derivation from Entity Lifecycles (Specs Step 12)

| Entity | Lifecycle states (Specs Step 12) | Derived planning_state | Notes |
| --- | --- | --- | --- |
| Organization | active, archived | _n/a_ | Organization lifecycle is surfaced through lifecycle-aware endpoints; `planning_state` is not emitted. |
| Project | draft | draft | Pre-activation planning; not yet validated. |
| Project | active | validated | Active planning with validated scope. |
| Project | closed, archived | frozen | Planning is locked; unarchive or reopen drives changes to lifecycle before planning_state can move. |
| Mission | draft | draft | Mission not yet planned. |
| Mission | planned | validated | Planned and ready for validation-bound editing. |
| Mission | locked, canceled, archived | frozen | Locked or terminal mission states expose `planning_state=frozen`; cancel/archive do not bypass lock semantics. |
| Assignment | proposed | draft | Draft commitment pending validation. |
| Assignment | confirmed, released | validated | Confirmed or released commitments remain editable within validation rules. |
| Assignment | canceled, archived | frozen | Terminal or archived assignments surface as frozen. |
| Collaborator | invited | draft | Pending onboarding. |
| Collaborator | active | validated | Active collaborator eligible for assignments. |
| Collaborator | suspended, archived | frozen | Suspended/archived collaborators block new assignments and surface as frozen. |

API implementations MUST evaluate lifecycle transitions first; `planning_state` transitions are allowed only when they do not conflict with the lifecycle state machine or constraints defined in Specs Step 12.

### 7.2 Transition Endpoints

Transitions use dedicated endpoints (to avoid generic PATCH ambiguity, aligned with Step 05 archive pattern).

Project:

* POST /orgs/{org_id}/projects/{project_id}/validate_state
* POST /orgs/{org_id}/projects/{project_id}/revert_to_draft
* POST /orgs/{org_id}/projects/{project_id}/freeze
* POST /orgs/{org_id}/projects/{project_id}/unfreeze

Mission:

* POST /orgs/{org_id}/projects/{project_id}/missions/{mission_id}/validate_state
* POST /orgs/{org_id}/projects/{project_id}/missions/{mission_id}/revert_to_draft
* POST /orgs/{org_id}/projects/{project_id}/missions/{mission_id}/freeze
* POST /orgs/{org_id}/projects/{project_id}/missions/{mission_id}/unfreeze

Assignment:

* POST /orgs/{org_id}/projects/{project_id}/missions/{mission_id}/assignments/{assignment_id}/validate_state
* POST /orgs/{org_id}/projects/{project_id}/missions/{mission_id}/assignments/{assignment_id}/revert_to_draft
* POST /orgs/{org_id}/projects/{project_id}/missions/{mission_id}/assignments/{assignment_id}/freeze
* POST /orgs/{org_id}/projects/{project_id}/missions/{mission_id}/assignments/{assignment_id}/unfreeze

Collaborator:

* POST /orgs/{org_id}/collaborators/{collaborator_id}/validate_state
* POST /orgs/{org_id}/collaborators/{collaborator_id}/revert_to_draft
* POST /orgs/{org_id}/collaborators/{collaborator_id}/freeze
* POST /orgs/{org_id}/collaborators/{collaborator_id}/unfreeze

Notes:

* These endpoints mutate only planning_state.
* Archive remains a separate endpoint family and is not affected by these transitions.

### 7.3 Responses

* 200 OK returns the updated resource DTO (with planning_state updated).
* 403 forbidden for cross-org.
* 404 not_found for missing in org.
* 409 conflict for invalid transitions or parent gating/frozen parent.
* 422 validation_error for malformed transition requests (rare; typically no body).

### 7.4 Invalid Transition Example (409)

Attempt: DRAFT -> FROZEN

```json
{
  "code": "conflict",
  "message": "invalid state transition",
  "details": {"from": "draft", "to": "frozen", "rule": "must validate before freeze"},
  "trace_id": "req-101"
}
```

### 7.5 Parent Gating Example (409)

Attempt: validate assignment while mission is draft

```json
{
  "code": "conflict",
  "message": "parent planning_state blocks transition",
  "details": {"parent_type": "mission", "parent_id": "msn-1", "parent_state": "draft"},
  "trace_id": "req-102"
}
```

### 7.6 Validate-state Success Pattern

* The server MAY internally call the Step 06 validate endpoint logic to confirm zero blocking_errors.
* The server MUST NOT auto-fix planning data.

## 8. Test Matrix (State Transitions)

| Test ID             | Entity     | Endpoint              | Scenario                    | Precondition                 | Expected Status | Notes                       |
| ------------------- | ---------- | --------------------- | --------------------------- | ---------------------------- | --------------- | --------------------------- |
| ST-PROJ-01          | Project    | POST /validate_state  | Draft -> Validated success  | Validation has zero blocking | 200             | planning_state=validated    |
| ST-PROJ-02          | Project    | POST /freeze          | Validated -> Frozen success | Project validated            | 200             | planning_state=frozen       |
| ST-PROJ-03          | Project    | POST /freeze          | Draft -> Frozen rejected    | Project draft                | 409             | must validate before freeze |
| ST-MSN-01           | Mission    | POST /validate_state  | Parent gating blocks        | Project draft                | 409             | parent_state=draft          |
| ST-ASN-01           | Assignment | POST /validate_state  | Parent gating blocks        | Mission draft                | 409             | parent_state=draft          |
| ST-ASN-02           | Assignment | POST /freeze          | Validated -> Frozen         | Assignment validated         | 200             | planning_state=frozen       |
| ST-ASN-03           | Assignment | POST /revert_to_draft | Validated -> Draft          | Assignment validated         | 200             | planning_state=draft        |
| ST-UNF-01           | Any        | POST /unfreeze        | Frozen -> Validated         | Entity frozen                | 200             | planning_state=validated    |
| ST-PARENT-FROZEN-01 | Mission    | POST create mission   | Parent frozen blocks create | Project frozen               | 409             | parent frozen               |
| ST-PARENT-FROZEN-02 | Assignment | PATCH assignment      | Parent frozen blocks update | Mission frozen               | 409             | parent frozen               |

## 9. Self-Audit

* Scope: Planning-only state machine; no execution semantics.
* Authority: Extends Steps 01-06; aligns with Step 05 pattern of dedicated endpoints for special actions.
* Consistency: Archive remains separate and unchanged.
* Determinism: Transitions are explicit and testable.
* DECISION REQUIRED: None.

## 10. Next Authorized Step

Phase 1 - Step 08: Planning Snapshots and Audit Trails (Planning-only)
