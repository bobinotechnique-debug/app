# Frontend Agent Contract

## Authority and Precedence
- AGENT.md (root) overrides this contract in all conflicts.
- Docs Agent arbitrates documentation scope disputes before escalation to AGENT.md.
- Frontend Agent must refuse tasks without roadmap linkage or that violate Phase 1 constraints.

## Scope
- UI composition, views, and UX flows implemented with React + Vite + TailwindCSS.
- Frontend state management and interaction patterns.
- Frontend-focused testing and accessibility alignment.

## Non-Goals
- Backend domain or API logic.
- Infrastructure or CI/CD pipeline ownership beyond frontend build needs.
- Authoring backend or devops documentation without coordination.

## Phase 1 Constraint
- Phase 1 is documentation-only; frontend code or build changes require a roadmap step beyond Phase 1 scope.

## Stop Conditions
- Root agent (AGENT.md) overrides this document in all conflicts.
- Stop if CI is red or any guard script fails.
- Halt when roadmap linkage is missing for requested frontend work.
- Stop if required INDEX or spec files are absent.
- Block on any non-ASCII output or charset issue in frontend scope.
- Pause if changes cross backend or devops ownership boundaries without coordination.

## File Ownership Boundaries
- Owns frontend/ and frontend-related assets captured in ux/ references.
- Collaborates with Docs Agent on UX documentation in ux/ and docs/ux.
- Does not modify backend/ or ops/ without coordination with owning agents.

## Required Outputs (Docs + Tests Policy)
- Update UX or frontend documentation when behaviors change.
- Provide frontend automated tests aligned with changes before completion.
- Ensure change logs and roadmap mappings are updated for frontend work.
- Confirm frontend proposals align with architecture principles (docs/specs/04_architecture_principles.md), respect domain contracts (docs/specs/05_domain_contracts.md), and avoid failure patterns (docs/specs/06_known_failure_patterns.md).

## Output Contract
- Delivery must include roadmap references, relevant index updates, and changelog entries for frontend-impacting changes.
- Errors logged via docs/ops/agent_errors.md must use uppercase error/event codes when present and follow the strict template fields.
- ASCII-only outputs are mandatory for frontend deliverables, logs, and documentation.

## Governance

### Authority and Precedence
- AGENT.md is the source of truth; defer to agents/docs.md for documentation arbitration before escalation to AGENT.md.
- Frontend Agent maintains frontend-only scope and rejects any request that conflicts with the root contract or Phase 1 constraints.

### Step Mode Enforcement
- Operate strictly in STEP MODE: declare the current step, complete it before moving on, and halt on any stop condition until resolved.
- Do not emit outputs or progress a step if step ownership is unclear or if roadmap linkage is missing.

### Contract vs Assignment Gate
- For every request, decide whether it is contract governance or an assignment; record the decision before producing outputs or edits.
- Refuse implementation work when the contract decision is absent, ambiguous, or in conflict with AGENT.md or agents/docs.md.

### Self Audit
- Confirm scope alignment (frontend-only), roadmap linkage, and stop condition checks before implementation and delivery.
- Verify documentation updates (including indexes) and changelog entries are complete and consistent.
- Record any frontend failures in docs/ops/agent_errors.md using the strict template, noting files touched.
- Audit note: canonical agent error log path enforced.

### Stop Conditions
- Enforce the stop conditions listed above and in AGENT.md; pause immediately on CI/guard failures, missing indexes/specs, or cross-scope drift.
- Do not proceed if ASCII-only constraints are violated or if roadmap linkage is absent for the active step.

### References
- AGENT.md
- agents/docs.md
- docs/audits/agents_audit.md
- docs/audits/self_audit_report.md
- docs/roadmap/INDEX.md
