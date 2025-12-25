# Phase 1 - Step 11: Authorization and Access Control (Planning-Only)
_FROZEN by phase1_freeze_1.0.0_

## 1. Purpose and Scope
- Define the planning-only authorization and access control model for Phase 1 without introducing runtime enforcement or authentication.
- Cover declarative roles and permissions over planning resources: organization, project, mission, assignment, and collaborator.
- Out of scope: authentication mechanisms, runtime enforcement, execution-time access control, and any infrastructure concerns.

## 2. Authority and Precedence
- Inherits authority from Phase 1 Step 01 (Planning Core) and must remain consistent with Step 02 domain boundaries.
- Must not contradict API planning contracts (Step 04) or the error taxonomy (Step 10).
- Advisory and declarative only; no implementation behavior is mandated in Phase 1.

## 3. Planning Authorization Principles
### 3.1 Planning-Only Access
- Authorization rules apply exclusively to planning artifacts: organization, project, mission, assignment, and collaborator.
- No rule defined here applies to execution, payroll, accounting, or operational systems.

### 3.2 Least Authority by Default
- Access is denied by default unless explicitly granted by role.
- Read access does not imply write access.
- Write access does not imply delete or archive access.

### 3.3 Scope Containment
- Organization-level authority does not automatically grant project-level write rights.
- Project-level authority does not escape its parent organization.

## 4. Canonical Planning Roles
### 4.1 Organization Owner
- Scope: organization; intended actor: legal or administrative owner.
- Permissions: read/write organization metadata; create and archive projects; manage organization members and their project roles.
- Restrictions: cannot bypass domain invariants; cannot directly edit execution or accounting data.

### 4.2 Organization Planner
- Scope: organization; intended actor: senior planner or administrator.
- Permissions: read organization; create and edit projects; assign project-level roles.
- Restrictions: cannot delete organization; cannot override project-level ownership.

### 4.3 Project Owner
- Scope: project; intended actor: producer or project lead.
- Permissions: read/write project metadata; create, edit, and archive missions; assign collaborators to missions.
- Restrictions: cannot modify organization-level settings.

### 4.4 Project Planner
- Scope: project; intended actor: planning coordinator.
- Permissions: read project; create and edit missions; propose assignments.
- Restrictions: cannot archive project; cannot manage organization members.

### 4.5 Collaborator (Planning)
- Scope: self plus assigned missions; intended actor: technician, artist, or staff contributor.
- Permissions: read own assignments; view mission details where assigned.
- Restrictions: cannot create or edit missions; cannot assign other collaborators.

## 5. Resource vs Permission Matrix (Planning-Only)
| Resource     | Read           | Create          | Update          | Archive       |
| ------------ | -------------- | --------------- | --------------- | ------------- |
| Organization | Owner, Planner | Owner           | Owner           | Owner         |
| Project      | Owner, Planner | Owner, Planner  | Owner           | Owner         |
| Mission      | Project roles  | Project roles   | Project roles   | Project Owner |
| Assignment   | Project roles  | Project Planner | Project Planner | Project Owner |
| Collaborator | Self, Planners | Org Owner       | Org Owner       | Org Owner     |

Notes:
- Archive is a planning concept; no deletion occurs in Phase 1.
- Self access is limited to the authenticated collaborator identity (authentication is out of scope here).

## 6. Authorization Invariants
- A collaborator cannot be assigned to a mission they cannot read.
- A planner cannot modify artifacts outside their declared scope.
- Organization ownership is singular per organization.
- Project ownership is singular per project.
- Violations of these invariants are planning errors aligned to the Phase 1 error taxonomy (Step 10).

## 7. Interaction with API Planning Contracts
- Authorization failures are represented as planning errors, not security breaches.
- API examples may reference roles symbolically but must not enforce them in runtime behavior.
- Error shapes must align with the Problem Details registry defined in Step 10.

## 8. Forward Compatibility Notes
- This step defers Phase 2+ concerns such as mapping roles to authentication identities, runtime policy engines (RBAC/ABAC), and cross-organization delegation.
- No Phase 2 behavior is implied or required by this document.

## 9. Validation Checklist
- All planning resources reference an explicit scope (organization or project).
- All mutations in API examples can be traced to a permitted role.
- No document introduces authorization rules outside this step.

## Self Audit
- Scope respected: Planning-only authorization and access control documented without runtime enforcement or authentication behavior.
- Authority respected: Aligns with Phase 1 Steps 01-10 and the Phase 1 error taxonomy for planning errors.
- Index and changelog updates: Roadmap and specs indexes updated to reference this step, and changelog entry added for traceability.
