# Phase 1 Freeze 1.0.0

- **Version:** 1.0.0
- **Date:** 2025-12-25
- **Authority:** AGENT.md (root) → Docs governance → This freeze record

## Scope of Freeze
- Phase 1 documentation across roadmap, specs, and API artifacts is SEALED as a planning-only baseline.
- All Phase 1 identifiers, lifecycle rules, invariants, and taxonomy remain unchanged until a formal amendment.
- Index entries that reference Phase 1 must preserve existing titles, paths, and linkage.

## Explicitly Excluded
- Non-Phase 1 materials remain governed by their respective phases.
- Runtime code, infrastructure, and UX implementation remain out of scope for this freeze (Phase 1 is documentation-only).

## Governance and Modification Rules
- Phase 1 is SEALED. No further edits are allowed without a formal decision document.
- Any change to Phase 1 requires:
  - A new decision document under `docs/decisions/` that explicitly references this freeze (`phase1_freeze_1.0.0`).
  - An explicit unfreeze or amendment reference inside that decision.
- Silent edits are forbidden; modifications without a decision record are invalid.
- Authorities must restate the roadmap/spec/API linkage to Phase 1 before approving any amendment.

## Relationship to Phase 2
- Phase 2 may build on the frozen Phase 1 baseline but cannot alter Phase 1 artifacts without an approved unfreeze/amendment decision.
- Phase 2 planning must cite this freeze when referencing Phase 1 contracts or invariants.

## Validation Checklist
- Phase 1 planning is locked; guards and reviews must reject edits lacking a `docs/decisions/` amendment reference.
- Roadmap/specs/API Phase 1 documents display the freeze marker: `FROZEN by phase1_freeze_1.0.0`.
- Freeze status and authority chain are visible from Phase 1 indexes and steps.
