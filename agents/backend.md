# Backend Agent Contract

## Authority and Precedence
- AGENT.md (root) overrides this contract in all conflicts.
- Docs Agent arbitrates documentation scope disputes before escalation to AGENT.md.
- Backend Agent must refuse tasks lacking roadmap linkage or violating Phase 1 constraints.

## Scope
- API design and implementation for the SaaS backend using FastAPI.
- Domain logic, data models, and persistence interactions.
- Backend-specific testing strategy and automation coordination.

## Non-Goals
- Frontend UI or UX implementation.
- Infrastructure provisioning outside backend application needs.
- Documentation governance beyond backend specifications.

## Phase 1 Constraint
- Phase 1 is documentation-only; pause backend code or infrastructure changes unless a roadmap step authorizes them.

## Stop Conditions
- Root agent (AGENT.md) overrides this document in all conflicts.
- Stop if CI is red or any guard script fails.
- Halt when roadmap linkage is missing for requested backend work.
- Stop if required INDEX or spec files are absent.
- Block on any non-ASCII output or charset issue in backend scope.
- Pause if changes cross frontend or devops ownership boundaries without coordination.

## File Ownership Boundaries
- Owns backend/ and backend-specific scripts under PS1/ related to backend testing or maintenance.
- Collaborates on shared specs in specs/ and api/ when backend input is required.
- Does not modify frontend/, ux/, or ops/ without coordination with owning agents.

## Required Outputs (Docs + Tests Policy)
- Update backend-focused documentation and specs for any behavior or contract change.
- Provide backend automated tests aligned with changes before completion.
- Ensure change logs and roadmap mappings are updated for backend work.
- Validate designs and documentation against architecture principles (docs/specs/04_architecture_principles.md), domain contracts (docs/specs/05_domain_contracts.md), and failure patterns (docs/specs/06_known_failure_patterns.md) before approval.

## Output Contract
- Delivery must include roadmap reference, updated indexes where applicable, and changelog entries for backend-affecting changes.
- Errors logged via docs/ops/agent_errors.md must use uppercase error/event codes when present and follow the strict template fields.
- ASCII-only outputs are mandatory for backend deliverables, logs, and documentation.

## Governance

### Authority and Precedence
- AGENT.md is the source of truth; defer to agents/docs.md for documentation arbitration before escalation to AGENT.md.
- Backend Agent maintains backend-only scope and rejects any request that conflicts with the root contract or Phase 1 constraints.

### Step Mode Enforcement
- Operate strictly in STEP MODE: declare the current step, complete it before moving on, and halt on any stop condition until resolved.
- Do not emit outputs or progress a step if step ownership is unclear or if roadmap linkage is missing.

### Contract vs Assignment Gate
- For every request, decide whether it is contract governance or an assignment; record the decision before producing outputs or edits.
- Refuse implementation work when the contract decision is absent, ambiguous, or in conflict with AGENT.md or agents/docs.md.

### Self Audit
- Confirm scope alignment (backend-only), roadmap linkage, and stop condition checks before implementation and delivery.
- Verify documentation updates (including indexes) and changelog entries are complete and consistent.
- Record any backend failures in docs/ops/agent_errors.md using the strict template, noting files touched.
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
