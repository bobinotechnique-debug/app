# Phase 1 - Step 10: API Error Taxonomy and Problem Details Registry (Planning-only)

## 1. Purpose and Scope

- Consolidate a planning-only error taxonomy and problem-details registry that aligns with the Step 04 error envelope and Step 05 examples without changing behavior.
- Provide a checklist to keep error codes, HTTP status usage, and detail shapes consistent across future Phase 1 documentation updates.
- Maintain cross-document alignment for error handling while deferring any implementation or runtime behavior decisions.

## 2. Authority

- Subordinate to Phase 1 Steps 01-09; does not supersede any previously locked contracts.
- Bound to the Step 04 error envelope and Step 05 status-code clarifications; no new status codes or behaviors are introduced.
- Follows the indexing and cross-doc registration rules locked in Step 09 and the roadmap binding rule in AGENT.md.

## 3. Definitions

- **Error envelope (Phase 1 canonical)**: `{ code, message, details, trace_id? }` as defined in Step 04 and exemplified in Step 05.
- **Problem-details registry**: The planning-only list of allowed error codes, their canonical meanings, and required HTTP status pairings for Phase 1 artifacts.

## 4. Requirements / Checklist

- Maintain the canonical envelope fields without additions: `code` (machine-readable), `message` (human-readable summary), `details` (field or context map), optional `trace_id`.
- Allowed error codes and status pairings (planning-only, unchanged from prior steps):
  - `validation_error` → `422 Unprocessable Entity` for schema/constraint violations, including pagination, immutability, archive misuse, and validation endpoints.
  - `bad_request` → `400 Bad Request` only for malformed JSON or unsupported content types.
  - `unauthorized` → `401 Unauthorized` for missing/invalid authentication.
  - `forbidden` → `403 Forbidden` for cross-organization access attempts.
  - `not_found` → `404 Not Found` for missing resources within the caller organization.
  - `conflict` → `409 Conflict` for idempotency key mismatches, immutable relationship moves, and archived-parent blocks.
- Keep error code namespace closed for Phase 1. Any proposal for new codes or status mappings requires a `DECISION REQUIRED` note and a downstream phase change request; do not invent interim codes.
- Preserve deterministic error structures in examples and matrices: keys sorted, codes lower_snake_case, and details mapping to stable field names.
- Ensure every API doc that references errors links back to this registry or Step 04/05 without duplicating or diverging definitions.
- Document traceability: when an index or spec references an error code, include a relative link to this step or the originating step (04 or 05) to prevent drift.

## 5. Drift Detection Notes

- If an API doc introduces an error code or status not listed above, halt and raise `DECISION REQUIRED` before merging.
- If the envelope shape diverges (extra or missing fields), normalize to the canonical four-field structure or document the exception rationale in a future phase request.
- Cross-check indexes: all Phase 1 API steps should reference the same error code spellings and status pairings; mismatches must be reconciled by updating the relevant docs to match this registry.

## 6. Self-Audit

- Scope respected: Documentation-only; no application code or runtime behavior altered.
- Authority respected: Bound to Steps 01-09 and AGENT.md; uses Step 04/05 contracts without extension.
- No new behavior introduced: Error codes and mappings are restated, not expanded.
- Indexing updated: API and roadmap indexes include this step with canonical paths.

## 7. Next Authorized Step

- Phase 1 - Step 11: TBD (DECISION REQUIRED for title and scope).
