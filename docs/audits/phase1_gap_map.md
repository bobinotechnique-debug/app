# Phase 1 Gap Map (Planning-Only)

## Declared but Unused Concepts
- **Draft/Validated/Frozen lifecycle taxonomy** — DEC-P1-LIFECYCLE-001 positions these API planning_state values as a compatibility view, yet API Step 07 still presents them as the primary lifecycle while Specs Step 12 remains authoritative for entity states. Documentation needs an explicit mapping that shows Draft/Validated/Frozen deriving from entity lifecycle states to avoid orphaned interpretation.【F:docs/api/phase1/step-07-planning-state-transitions.md†L16-L140】【F:docs/specs/phase1/step-12-planning-lifecycle-and-state-transitions.md†L16-L199】

## Used but Undefined Concepts
- **Active/Closed/Locked lifecycle states** — Specs Step 12 adopts these states for projects and missions and now holds lifecycle authority, but API Step 07 has not yet incorporated these states into its planning_state framing or organization lifecycle handling, leaving API behavior undefined pending alignment documentation.【F:docs/specs/phase1/step-12-planning-lifecycle-and-state-transitions.md†L63-L178】【F:docs/api/phase1/step-07-planning-state-transitions.md†L16-L140】

## Misplaced Phase 1 Concepts
- **Organization lifecycle management** — With DEC-P1-LIFECYCLE-001 setting Specs Step 12 as the lifecycle authority, API Step 07 still omits organization lifecycle coverage. API documentation must be updated to reflect organization lifecycle governance or explicitly document derived planning_state behavior for organizations to resolve the placement gap.【F:docs/specs/phase1/step-12-planning-lifecycle-and-state-transitions.md†L65-L83】【F:docs/api/phase1/step-07-planning-state-transitions.md†L16-L28】
