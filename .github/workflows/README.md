# GitHub Actions Workflows (Phase 0 Placeholder)

Phase 0 tracks workflow wiring only. Implement CI jobs after Phase 0 hardening.

- Scope: guard and validation workflows as defined in AGENT.md.
- Status: placeholders only; no jobs defined yet.
- Roadmap: [roadmap/phase-0/step-000.md](../../roadmap/phase-0/step-000.md)

## Phase 0 stop notes
- Workflows are non-executable stubs (`backend.yml`, `frontend.yml`, `docs.yml`, and `validate.yml`) with jobs disabled to respect Phase 0 stop conditions.
- Do not add steps or business logic until guards are implemented and Phase 0 exits.
- If a workflow is manually triggered, it should short-circuit immediately per the stub configuration and point contributors back to the roadmap entry.
