# DEC-P1-LIFECYCLE-001: Phase 1 Lifecycle Authority

status: accepted
scope: phase 1 planning lifecycle governance (planning-only)
date: 2026-01-15

## Context
A Phase 1 audit identified a collision between API Step 07 (planning_state draft/validated/frozen) and Specs Step 12 (canonical entity lifecycles). Phase 1 is entity-centric and requires a single lifecycle authority.

## Decision
- Specs Phase 1 Step 12 is the authoritative source for lifecycle taxonomy and transitions for organization, project, mission, assignment, and collaborator.
- API-facing `planning_state` values (draft, validated, frozen) are permitted only as a derived compatibility projection over the Step 12 lifecycles; they are not an independent lifecycle model.
- Organization lifecycle remains active/archived per Step 12 and is not expressed through `planning_state` endpoints.

## Consequences
- Documentation must reference Specs Step 12 for lifecycle definitions and transitions.
- API Step 07 must describe planning_state solely as a derivation from canonical lifecycles and avoid claiming lifecycle authority.
- Audits track DEC-P1-LIFECYCLE-001 as the resolution to the lifecycle collision flagged in Phase 1.
