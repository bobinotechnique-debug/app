# Phase 1 - Step 03: UX Surface Contracts

## 1. Purpose
- Define the authoritative UX surfaces for Phase 1 planning so that downstream UX, API, and implementation efforts align with approved planning artifacts.
- Reaffirm that planning records from Phase 1 Step 01 remain the single source of truth; this document inherits and applies the domain boundaries and invariants locked in Phase 1 Step 02.

## 2. Planning Surfaces (Read/Plan Only)
Each surface is limited to planning visibility and intent capture. No execution tracking, finance, notifications, or analytics may appear.

### Organization Overview (projects list)
- **User intent**: View an organization’s planning footprint and start or select projects for planning.
- **Visible entities**: Organization context with its projects; collaborator count is organizationally scoped and non-aggregated beyond listing affiliations.
- **Allowed planning actions**: Create a project within the current organization; edit project planning metadata (name, purpose); reorder project listings for planning clarity; link to project-level planning views.
- **Explicitly forbidden actions**: Cross-organization project creation; displaying or editing execution status; exposing billing, contracts, payroll, or analytics; assigning collaborators directly from this surface; any API or data operations beyond planning definitions.

### Project Planning View
- **User intent**: Plan missions and assignments within a single project while maintaining organization alignment.
- **Visible entities**: Project details; missions under the project; assignments grouped under missions; collaborators linked to this project’s missions or assignments; organization context.
- **Allowed planning actions**: Create or edit missions within the project; create or edit assignments within a mission; reorder missions or assignments for planning clarity; link collaborators to missions or assignments within the same organization; navigate to mission- or assignment-level planning surfaces.
- **Explicitly forbidden actions**: Moving missions or assignments across projects or organizations; showing execution progress, time tracking, or alerts; modifying collaborator organization membership; any financial or contractual controls; initiating API calls or database operations.

### Mission Planning View
- **User intent**: Define a mission’s planning scope and organize its assignments.
- **Visible entities**: Mission details; parent project and organization context; assignments under the mission; collaborators attached to those assignments.
- **Allowed planning actions**: Edit mission planning attributes (objective, scope signals); create, edit, or reorder assignments within the mission; link collaborators to assignments within the same organization; link back to project or assignment planning views.
- **Explicitly forbidden actions**: Associating the mission with another project or organization; tracking execution state, timelines, or effort; initiating notifications; adjusting collaborator organization scope; any financial or analytics displays.

### Assignment Planning View
- **User intent**: Capture planning details for a single assignment under its mission.
- **Visible entities**: Assignment planning details; parent mission, project, and organization context; collaborators linked to this assignment.
- **Allowed planning actions**: Edit assignment planning attributes (intent, expected acceptance signals); link or relink collaborators within the same organization; reorder the assignment within its mission for planning purposes; navigate to mission or collaborator planning views.
- **Explicitly forbidden actions**: Moving the assignment outside its mission or project; recording execution status, time, or delivery metrics; issuing notifications or approvals; displaying contracts, payroll, or analytics; altering collaborator organization membership.

### Collaborator Planning View
- **User intent**: Review and plan collaborator participation within their single organization.
- **Visible entities**: Collaborator profile within the organization; linked projects, missions, and assignments (planning references only); organization context.
- **Allowed planning actions**: Edit collaborator planning attributes (role expectations, availability signals within planning scope); link or unlink collaborator to missions or assignments inside the same organization; reorder linked work references for clarity; navigate to related project, mission, or assignment planning views.
- **Explicitly forbidden actions**: Associating the collaborator with another organization; assigning execution status or time tracking; triggering notifications; showing payroll, contracts, or analytics; editing mission or assignment ownership outside planning scope.

## 3. Cross-Surface Invariants
- Every project shown or edited belongs to exactly one organization; navigation must never imply cross-organization links.
- Every mission is anchored to exactly one project and inherits that project’s organization; surfaces must block any action that would detach or duplicate that relationship.
- Every assignment belongs to exactly one mission and inherits the mission’s project and organization; reordering remains within the mission only.
- Every collaborator is scoped to exactly one organization; links to missions or assignments must never span organizations.
- Planning artifacts remain the governing reference; surfaces display and edit planning data only when it aligns with approved Phase 1 planning records from Steps 01 and 02.

## 4. Forbidden UX States
- Displaying a project without an owning organization.
- Showing a mission attached to multiple projects or to none.
- Presenting an assignment outside a single mission or linked to multiple missions.
- Representing a collaborator as shared across organizations or attached to work outside their organization.
- Any surface that bypasses or contradicts the approved planning artifacts from Phase 1 Steps 01 and 02.

## 5. Deferred UX Concerns (Out of Phase 1 Scope)
- Execution status or delivery tracking of any kind.
- Time tracking, effort logging, or scheduling automation.
- Notifications, alerts, or messaging flows.
- Contracts, payroll, billing, or finance displays or controls.
- Analytics, reporting, or forecasting beyond planning records.

## 6. Dependency Declaration
All future UX, API, database, and implementation work must conform to these Phase 1 UX surface contracts and the planning invariants from Steps 01 and 02. Deviations require an approved amendment to the planning record.

## 7. Self Audit
- Scope respected: UX planning surfaces only; no execution, finance, notifications, or implementation detail introduced.
- Authority respected: Aligned with AGENT.md, Phase 1 Step 01 (planning as source of truth), and Phase 1 Step 02 (domain boundaries and invariants).
- No leakage: Deferred concerns and forbidden states explicitly block execution, financial, notification, and analytics topics.
