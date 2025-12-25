# Phase 1 - Step 13: Conflict Detection and Resolution Rules (Planning-only)

## 1. Purpose and Scope

This step defines the planning-only conflict model for Phase 1. It standardizes:

* What constitutes a planning conflict
* How conflicts are detected (declaratively)
* How conflicts are represented, classified, and resolved (as planning decisions)
* Which conflicts must block state transitions (Step 12)

This step remains declarative. It must not introduce implementation behavior, solver logic, optimization algorithms, or automated decision-making.

In scope:

* Conflict taxonomy (types, severity)
* Detection rules (inputs required, constraints)
* Resolution patterns (manual decisions, override rationale)
* UX-facing expectations at contract level (labels, counts), without UI design
* API-facing expectations at contract level (fields, error mapping), without endpoints

Out of scope:

* Automatic scheduling / optimization
* Real-time execution constraints (time tracking, payroll)
* Notification/accept/decline workflows (Phase 2+)
* Runtime policy engines

## 2. Authority and Precedence

* Step 01 planning-as-source-of-truth governs all decisions.
* Step 02 domain invariants are non-negotiable; conflicts must not override invariants.
* Step 04 API contracts define resource shapes; Step 13 only adds conflict semantics.
* Step 08 audit trail requirements apply to conflict resolutions and overrides.
* Step 10 error taxonomy defines problem details; Step 13 maps conflicts to those categories.
* Step 11 defines who can resolve conflicts.
* Step 12 defines lifecycle transitions that conflicts may block.

If conflict rules require product policy choices, STOP and escalate to governance before proceeding.

## 3. Definitions

### 3.1 Planning Conflict

A planning conflict is a condition where the current planning state violates a constraint or expectation such that:

* the plan is inconsistent, risky, or ambiguous
* the plan may be allowed with an explicit override
* or the plan must be blocked until corrected

Conflicts are computed from planning artifacts only (missions, assignments, collaborators, projects).

### 3.2 Conflict Record

A conflict is represented as a record with:

* conflict_id (stable identifier)
* type
* severity
* scope (organization, project, mission, assignment, collaborator)
* involved_entities (references)
* detected_at
* status: open | acknowledged | resolved | overridden
* resolution (optional): resolution_kind + actor + timestamp + rationale

Conflict records are append-only for audit; the current status is derived from the latest event.

## 4. Conflict Taxonomy

Conflicts are grouped by category. Each conflict type MUST specify default severity and whether it blocks transitions.

Severities:

* info: may be displayed; never blocks
* warn: requires attention; may block depending on rule
* block: must block designated transitions

### 4.1 Temporal Conflicts

1. collaborator_time_overlap

* Description: A collaborator has overlapping assignments in time.
* Severity: block
* Blocks: assignment.confirmed, mission.locked

2. mission_time_overlap_same_resource

* Description: A mission overlaps another mission within a rule-defined exclusivity scope (e.g., same venue, same stage).
* Severity: warn
* Blocks: none (non-blocking in Phase 1)

3. assignment_outside_mission_window

* Description: Assignment start/end is outside mission start/end.
* Severity: block
* Blocks: assignment.confirmed, mission.planned, mission.locked

4. invalid_time_window

* Description: start >= end for mission or assignment.
* Severity: block
* Blocks: any transition requiring a valid window

### 4.2 Capacity and Load Conflicts

5. collaborator_capacity_exceeded

* Description: A collaborator exceeds declared capacity within a window (hours/day, hours/week).
* Severity: warn
* Blocks: assignment.confirmed (requires explicit override to proceed)
* Note: Warn-only by default; override_required when used to confirm assignments.

6. mission_staffing_below_minimum

* Description: Mission lacks required minimum staffing (role counts).
* Severity: warn
* Blocks: mission.locked (default)

7. mission_staffing_above_maximum

* Description: Mission staffing exceeds declared maximum.
* Severity: info
* Blocks: none

### 4.3 Role and Qualification Conflicts

8. collaborator_missing_qualification

* Description: Collaborator does not meet a required qualification for an assignment role.
* Severity: warn
* Blocks: assignment.confirmed (default)

9. collaborator_role_mismatch

* Description: Collaborator role category is incompatible with assignment role.
* Severity: warn
* Blocks: assignment.confirmed (default)

### 4.4 Availability Conflicts

10. collaborator_unavailable

* Description: Collaborator is unavailable (explicit unavailability window) during the assignment.
* Severity: warn
* Blocks: assignment.confirmed (default)

11. collaborator_suspended_or_archived

* Description: Collaborator lifecycle state prevents planning allocation (Step 12).
* Severity: block
* Blocks: assignment.proposed, assignment.confirmed

### 4.5 Integrity and Reference Conflicts

12. cross_project_assignment

* Description: Assignment references a mission or collaborator outside its project/organization boundary.
* Severity: block
* Blocks: any write creating inconsistency

13. archived_parent_reference

* Description: Active child references an archived parent (e.g., mission planned in an archived project).
* Severity: block
* Blocks: mission.planned, assignment.confirmed

## 5. Detection Rules (Declarative)

### 5.1 Inputs

Conflict detection uses only planning artifacts:

* mission time windows
* assignment time windows
* collaborator identity and lifecycle state
* declared roles/qualifications
* declared capacities and availability windows

No external systems are consulted.

### 5.2 Determinism

Given the same planning state snapshot, conflict detection must produce the same set of conflicts. This enables reproducible audits (Step 08).

### 5.3 Incremental vs Full Detection

Phase 1 does not mandate an algorithm, but the model must support:

* full recomputation for a project scope
* incremental recomputation for a single edited mission/assignment

## 6. Conflict Resolution Model

Conflict resolution is a planning decision, recorded as an auditable event.

### 6.1 Resolution Kinds

* edit_plan: change times, roles, assignments, staffing
* reassign: swap collaborator(s)
* split: split a mission or assignment window
* cancel: cancel mission or assignment
* archive: archive artifacts
* override: explicitly allow plan to proceed despite a warn conflict

### 6.2 Overrides

Overrides are allowed only for conflicts whose severity is warn or info.

Override requirements:

* rationale (free text)
* actor
* timestamp
* optional expiry (date/time) for reevaluation

Overrides MUST NOT apply to block conflicts.

### 6.3 Ownership

Who may resolve or override is governed by Step 11 roles:

* project_owner and project_planner may resolve within project scope
* organization roles may resolve across projects

## 7. Transition Blocking Rules (Step 12 Integration)

The following transitions MUST be blocked when any blocking conflicts exist in the affected scope:

* assignment: proposed -> confirmed
* mission: planned -> locked
* project: active -> closed (if any missions have open block conflicts)

Warn conflicts:

* Do not block by default unless specified per conflict type.
* Warn conflicts never block unless explicitly marked as override_required (e.g., collaborator_capacity_exceeded when confirming assignments).
* If a warn conflict is marked as override_required, the transition may proceed only when an override record exists.

## 8. Error Mapping (Step 10 Integration)

When a write attempts a transition that is blocked by conflicts:

* error code: planning.conflict_blocking
* include conflict summaries in problem details extensions (non-normative)

When a write attempts to override a block conflict:

* error code: planning.override_not_allowed

When conflict computation cannot be performed due to missing prerequisite fields:

* error code: planning.conflict_prerequisite_failed

This step defines semantic mapping only. HTTP status and envelope remain defined by Step 10.

## 9. UX and API Contract Notes (Non-UI)

The planning surface should be able to:

* show conflict count by scope (project, mission, collaborator)
* filter to conflicts by type/severity
* show whether an override exists and its rationale

API surfaces may expose:

* conflicts as a derived read model
* conflict summaries embedded into mission/assignment read models

No endpoint is mandated in Phase 1.

## 10. Audit Trail Requirements

Every conflict lifecycle event must be auditable (Step 08):

* detected event (system actor symbol permitted)
* acknowledged event
* resolved event
* overridden event

The audit trail must preserve:

* the conflict type and involved entities
* the resolution rationale where applicable

## 11. Forward Compatibility Notes

Phase 2+ may extend this model with:

* acceptance / decline conflicts
* real-time availability feeds
* optimization and auto-proposals
* policy packs per organization

Phase 1 remains manual and declarative.

## 12. Validation Checklist

Before implementation work proceeds:

* Every block conflict maps to blocked transitions in Step 12.
* Every warn conflict declares whether override is permitted and whether it is required to proceed.
* Conflict record fields are representable in Step 08 audit trail.
* Error codes referenced here exist in Step 10 registry.
