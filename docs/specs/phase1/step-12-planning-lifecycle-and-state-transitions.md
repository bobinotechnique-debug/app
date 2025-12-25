# Phase 1 - Step 12: Planning Lifecycle and State Transitions (Planning-Only)

## 1. Purpose and Scope

This step defines the planning-only lifecycle and state transition rules for Phase 1 planning artifacts. It formalizes:

- Canonical lifecycle states per resource
- Allowed transitions, including terminal states
- Cross-resource transition constraints (e.g., project vs missions)
- Validation expectations for state changes, without implementation detail

This document is declarative and must not prescribe runtime behavior, workflows, automation, or infrastructure.

In scope:

- Lifecycle states for: organization, project, mission, assignment, collaborator (planning identity)
- Transition rules and invariants
- Required error categorization for invalid transitions (aligned to Step 10)

Out of scope:

- Execution lifecycle (time tracking, payroll, billing, accounting)
- Notifications, accept/decline flows, or contract execution
- AuthN/AuthZ enforcement (Step 11 defines roles; Step 12 defines states)
- Automation policies (auto-archive, auto-close)

## 2. Authority and Precedence

- Step 01 (Planning Core) defines planning-as-source-of-truth; Step 12 must preserve it.
- Step 02 (Domain Boundaries) defines invariants; Step 12 must not relax them.
- Step 04 (API Planning Contracts) provides resource shapes; Step 12 defines legal state moves.
- Step 10 (Errors) defines problem details; Step 12 specifies which errors apply.
- Step 11 (Authorization) defines who may act; Step 12 defines what transitions are allowed.

If any conflict requires product policy decisions (e.g., archival semantics), STOP and mark DECISION REQUIRED.

## 3. Lifecycle Conventions (Planning-only)

### 3.1 No Hard Deletes

Phase 1 planning artifacts are not deleted. Lifecycle progression uses:

- active states
- archived states
- canceled states

### 3.2 Immutability Boundaries

- A state transition is a discrete event that must be auditable (Step 08) and attributable.
- Terminal states are immutable: once reached, only unarchive or reopen transitions may exist if explicitly allowed.

### 3.3 Consistent Terminology

- active: usable for planning and downstream references
- archived: retained but excluded from default planning views
- canceled: explicitly invalidated due to plan change; retained for audit

## 4. Canonical State Models

### 4.1 Organization Lifecycle

States:

- active
- archived

Allowed transitions:

- active -> archived
- archived -> active (unarchive)

Constraints:

- Organization cannot be archived if it owns any active projects.

Terminal notes:

- archived is not terminal because unarchive is allowed.

### 4.2 Project Lifecycle

States:

- draft
- active
- closed
- archived

Allowed transitions:

- draft -> active
- active -> closed
- closed -> active (reopen)
- draft -> archived
- active -> archived
- closed -> archived
- archived -> active (unarchive)

Constraints:

- A project in draft may contain missions, but missions must not be scheduled outside explicit date bounds if those bounds are not yet set.
- A project cannot be closed if it contains any missions not in a terminal mission state.

Terminal notes:

- closed is not terminal (reopen allowed).
- archived is not terminal (unarchive allowed).

### 4.3 Mission Lifecycle

States:

- draft
- planned
- locked
- canceled
- archived

Allowed transitions:

- draft -> planned
- planned -> locked
- locked -> planned (unlock)
- draft -> canceled
- planned -> canceled
- locked -> canceled
- draft -> archived
- planned -> archived
- canceled -> archived
- archived -> planned (unarchive)

Constraints:

- A mission must have a project and valid time window before reaching planned.
- A locked mission may only allow limited field edits (non-time, non-scope) by policy; Phase 1 does not define field-level enforcement, only the intent.
- A mission cannot be locked if it has any assignment in a non-terminal assignment state.

Terminal notes:

- canceled is terminal with respect to planning intent but may be archived.
- archived may be unarchived.

### 4.4 Assignment Lifecycle

Assignments represent planning commitments within a mission.

States:

- proposed
- confirmed
- released
- canceled
- archived

Allowed transitions:

- proposed -> confirmed
- confirmed -> released
- proposed -> canceled
- confirmed -> canceled
- released -> confirmed (rebook)
- proposed -> archived
- canceled -> archived
- archived -> proposed (unarchive)

Constraints:

- An assignment cannot be confirmed if it violates domain invariants (Step 02), including time overlap rules when those are defined.
- An assignment cannot be released if its mission is locked, unless release is part of a lock-breaking workflow; Phase 1 does not define workflows, so default is: release allowed only when mission is not locked.

Terminal notes:

- canceled is terminal but may be archived.

### 4.5 Collaborator (Planning) Lifecycle

Collaborator is a planning identity within an organization.

States:

- invited
- active
- suspended
- archived

Allowed transitions:

- invited -> active
- active -> suspended
- suspended -> active
- invited -> archived
- active -> archived
- archived -> active (unarchive)

Constraints:

- A suspended collaborator remains readable for audit but cannot receive new assignments by policy.
- Archiving a collaborator must not delete historical assignment references.

## 5. Cross-Resource Transition Constraints

### 5.1 Organization vs Projects

- Organization archived implies no projects can be active.
- Unarchiving an organization does not automatically activate projects.

### 5.2 Projects vs Missions

- Project draft allows mission draft only.
- Project active allows missions in any non-archived state.
- Project closed requires all missions to be terminal (canceled or archived) or locked with no open assignments.

### 5.3 Missions vs Assignments

- Mission planned allows assignments proposed/confirmed.
- Mission locked implies:
  - no new assignments can be created
  - existing assignments must be in terminal or stable states (confirmed or released by policy)
- Mission canceled implies assignments must become canceled or archived.

### 5.4 Collaborators vs Assignments

- Suspended collaborator: existing assignments remain but cannot be newly confirmed.
- Archived collaborator: existing assignments remain; no new assignments can be created.

## 6. Validation and Error Mapping

Invalid transitions must be represented using Step 10 problem details.

Minimum mapping requirements:

- Attempting a forbidden transition -> error code: planning.transition_forbidden
- Missing prerequisites for a transition -> error code: planning.transition_prerequisite_failed
- Cross-resource constraint violation -> error code: planning.transition_conflict

HTTP status mapping is defined by Step 10; this step only assigns semantic categories.

## 7. Audit Trail Requirements

Every state transition event must be auditable (see Step 08):

- actor (symbolic; enforcement out of scope)
- timestamp
- previous state
- new state
- optional reason

## 8. Forward Compatibility Notes

Phase 2+ may introduce:

- Accept/decline flows mapped onto assignment states
- Contract generation gates tied to mission locked state
- Automatic transitions and scheduled archival

No automatic behavior is required or implied in Phase 1.

## 9. Validation Checklist

Before Phase 1 can proceed to implementation:

- Each planning resource has a declared state model.
- All state transitions referenced in any doc are included here.
- Step 04 API examples do not contradict these states.
- Step 08 audit trail schema can represent each transition.
- Step 10 registry includes codes referenced here.

## Self Audit

- Scope respected: Planning-only lifecycle and state transitions documented without runtime automation or execution semantics.
- Authority respected: Aligns with Phase 1 Steps 01-11 and the Phase 1 error taxonomy while keeping invariants from prior steps intact.
- Index and changelog updates: Roadmap and specs indexes updated to reference this step, and changelog entry added for traceability.
