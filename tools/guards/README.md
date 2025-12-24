# Guard Scripts Placeholder

Phase 0 requires guard entry points but defers implementation. Scripts will enforce ASCII, roadmap binding, and scope checks.

- Guard scope: repository-wide safety rules per [AGENT.md](../../AGENT.md).
- Status: placeholders only; logic to be added in later steps.
- Roadmap: [roadmap/phase-0/step-000.md](../../roadmap/phase-0/step-000.md)

## Phase 0 stop notes
- Treat guard invocations as immediate stop checks: do not continue when any global stop condition applies.
- Stop conditions to honor during Phase 0: failing CI, any guard error, missing required indexes, absent roadmap linkage, or non-ASCII output.
- Keep guard scripts non-executable beyond emitting placeholder messaging (see `PS1/guards.ps1`). Actual enforcement is deferred until Phase 0 hardening completes.
