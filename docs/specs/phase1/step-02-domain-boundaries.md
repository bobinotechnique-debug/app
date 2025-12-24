# Phase 1 - Step 02: Domain Boundaries and Invariants

## 1. Purpose
- Lock the Phase 1 domain boundaries now to prevent scope drift before UX, API, or implementation work begins.
- All boundaries and invariants extend and depend on Phase 1 Step 01 (Planning Core), which remains the planning-as-source-of-truth for every downstream artifact.

## 2. Canonical Domain Entities
- **Organization**: Owns the security and tenancy boundary; accountable for the policies that govern all projects and collaborators within it.
- **Project**: Owns planning cohesion within an organization; responsible for grouping missions and assignments under a single purpose and timeline.
- **Mission**: Owns a discrete project-scoped objective; responsible for articulating outcomes and aligning assignments to that objective.
- **Assignment**: Owns a specific unit of work under a mission; responsible for clear scope, ownership, and acceptance expectations.
- **Collaborator**: Owns participation commitments within a single organization; responsible for executing or overseeing missions and assignments to which they are attached.

## 3. Domain Boundaries
- **Organization**
  - Responsible for: defining governance, access, and policy context for its projects and collaborators.
  - Must not: share collaborators, projects, missions, or assignments across organizations; delegate security boundaries to any project.
- **Project**
  - Responsible for: maintaining planning coherence for missions and assignments within its organization; ensuring alignment to the project purpose.
  - Must not: exist outside an organization; contain missions or assignments that span multiple organizations or projects; override organization-level policies; redefine organization-level governance.
- **Mission**
  - Responsible for: expressing a project-scoped objective and aligning assignments to that objective, using planning inputs approved in Phase 1 Step 01.
  - Must not: exist outside a single project; own collaborators directly; redefine organization or project scope; create independent planning artifacts.
- **Assignment**
  - Responsible for: a singular, actionable work commitment under one mission with explicit ownership and acceptance expectations.
  - Must not: belong to multiple missions or projects; bypass mission objectives; exist without assigned ownership within its organization.
- **Collaborator**
  - Responsible for: fulfilling or overseeing missions and assignments within one organization according to project context.
  - Must not: participate across organizations; create or modify projects, missions, or assignments outside their organization’s governance; operate without project alignment when attached to missions or assignments.

## 4. Core Invariants (Non-Negotiable)
- Every project is owned by exactly one organization.
- Every mission belongs to exactly one project, which belongs to exactly one organization.
- Every assignment belongs to exactly one mission and inherits that mission’s project and organization context.
- Every collaborator is scoped to exactly one organization and cannot be shared across organizations.
- Planning artifacts remain the authoritative source for domain relationships; downstream UX, API, and data models must trace to approved planning records from Phase 1 Step 01.
- Cross-organization relationships between any entities are forbidden by design.
- Domain relationships are immutable without a planning change: organization and project ownership cannot be altered by downstream systems without revising the Phase 1 planning record.

## 5. Forbidden States
- A project without an owning organization.
- A mission linked to multiple projects or to no project.
- An assignment linked to multiple missions, to no mission, or to a mission outside the project’s organization.
- A collaborator associated with more than one organization or attached to missions or assignments outside their organization.
- Any domain relationship that bypasses planning artifacts approved in Phase 1 Step 01.

## 6. Deferred Concerns (Out of Phase 1 Scope)
- Execution tracking, time logging, and delivery status automation.
- Payroll, billing, contracts, invoicing, or financial reconciliation.
- Notifications, messaging, or alerting pipelines.
- Access provisioning automation, identity federation, or directory sync.
- Analytics, reporting, or forecasting beyond planning records.
- Deployment, runtime orchestration, or performance optimizations.

## 7. Dependency Declaration
- All future UX, API, database, and backend steps depend on this document for domain boundaries and invariants; changes must explicitly reference and align with this specification.

## Self Audit
- Scope respected: Documentation-only change defining domain boundaries and invariants for Phase 1.
- Authority respected: Aligned with AGENT.md and Phase 1 Step 01 planning contract as the source of truth.
- No leakage: Deferred concerns and forbidden states prevent Phase 2+ topics or implementation details.
