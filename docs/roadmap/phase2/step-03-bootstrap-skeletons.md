# Phase 2 - Step 03: Bootstrap Skeletons
Status: Done

## Purpose
- Bootstrap backend and frontend skeleton wiring that aligns to the locked Phase 2 architecture.
- Prepare minimal scaffolds for future business logic without implementing domain behavior.

## Scope
- Backend wiring for project structure, service shells, routing placeholders, and configuration hooks without domain rules.
- Frontend wiring for page shells, routing, state containers, and theming scaffolds without product behavior.
- Smoke-test harnesses that validate wiring paths compile and run without enforcing business outcomes.
- Alignment with guards and CI enforcement to ensure skeletons respect Step 02 architecture boundaries.

## Hard Rules
- Zero domain rules or product behavior are permitted in this step.
- Use Step 02 architecture lock as the authoritative boundary for all wiring decisions.
- Follow Phase 1 locks and contracts; no changes to locked APIs, models, or UX behavior.
- Any deviation or ambiguity requires a DECISION under docs/decisions/ before proceeding.

## Definition of Done
- Documentation updated to capture skeleton wiring scope, rules, and references for future implementation prompts.
- Backend and frontend scaffolds planned with explicit alignment to Step 02 architecture lock.
- Smoke-test entry points identified for verifying skeleton compilation without domain assertions.
- Next-phase prompts can reference this document to implement wiring without redefining scope.

## Key Entry Points
- Backend app bootstrap: backend/app/main.py
- Backend router registry: backend/app/api/routes.py
- Backend service shell: backend/app/services/placeholder_service.py
- Backend infrastructure stub: backend/app/infra/database.py
- Frontend app shell and providers: frontend/src/App.tsx
- Frontend API client: frontend/src/api/client.ts

## Next Authorized Step
- Step 04: [Skeleton Hardening](step-04-skeleton-hardening.md) (Pending)

## Stop Conditions
- If any conflict arises with Phase 1 locks or Step 02 architecture boundaries, halt and request a DECISION.
- If work would introduce domain logic or product behavior, stop until a later authorized step permits it.
