# Phase 1 - Step 10: API Error Taxonomy and Problem Details Registry (Planning-only)
_FROZEN by phase1_freeze_1.0.0_

## 1. Purpose and Scope

- Consolidate a planning-only error taxonomy and problem-details registry that aligns with the Step 04 error envelope and Step 05 examples without changing behavior.
- Provide a checklist to keep error codes, HTTP status usage, and detail shapes consistent across future Phase 1 documentation updates.
- Maintain cross-document alignment for error handling while deferring any implementation or runtime behavior decisions.

## 2. Authority

- Subordinate to Phase 1 Steps 01-09; does not supersede any previously locked contracts.
- Defines the complete locked Phase 1 error code registry; the codes listed below are the allowed set for Phase 1.
- Bound to the Step 04 error envelope and Step 05 status-code clarifications; this document consolidates the locked registry and preserves the status mappings recorded here. Any new code or status mapping change requires governance approval and a downstream phase change request.
- Follows the indexing and cross-doc registration rules locked in Step 09 and the roadmap binding rule in AGENT.md.

## 3. Definitions

- **Error envelope (Phase 1 canonical)**: `{ code, message, details, trace_id? }` as defined in Step 04 and exemplified in Step 05.
- **Problem-details registry**: The planning-only list of allowed error codes, their canonical meanings, and required HTTP status pairings for Phase 1 artifacts.

## 4. Requirements / Checklist

- Maintain the canonical envelope fields without additions: `code` (machine-readable), `message` (human-readable summary), `details` (field or context map), optional `trace_id`.
- Allowed error codes and status pairings (planning-only):
  - Base envelope codes:
    - `validation_error` → `422 Unprocessable Entity` for schema/constraint violations, including pagination, immutability, archive misuse, and validation endpoints.
    - `bad_request` → `400 Bad Request` only for malformed JSON or unsupported content types.
    - `unauthorized` → `401 Unauthorized` for missing/invalid authentication.
    - `forbidden` → `403 Forbidden` for cross-organization access attempts and purge disallowed.
    - `not_found` → `404 Not Found` for missing resources within the caller organization.
    - `conflict` → `409 Conflict` for idempotency key mismatches, immutable relationship moves, and archived-parent blocks.
  - Lifecycle and conflict (Steps 12-13):
    - `planning.transition_forbidden` → `409 Conflict` (illegal transition)
    - `planning.transition_prerequisite_failed` → `422 Unprocessable Entity` (missing fields for transition)
    - `planning.transition_conflict` → `409 Conflict` (cross-resource constraint violation)
    - `planning.conflict_blocking` → `409 Conflict` (blocked by conflict)
    - `planning.override_not_allowed` → `409 Conflict` (override attempted on block conflict)
    - `planning.conflict_prerequisite_failed` → `422 Unprocessable Entity` (missing data to compute conflicts)
  - Derived views (Step 14):
    - `planning.derived_view_unavailable` → `422 Unprocessable Entity`
  - Query (Step 15):
    - `planning.query_invalid_parameter` → `422 Unprocessable Entity`
    - `planning.query_invalid_value` → `422 Unprocessable Entity`
    - `planning.query_invalid_range` → `422 Unprocessable Entity`
    - `planning.query_scope_required` → `422 Unprocessable Entity`
    - `planning.query_limit_exceeded` → `422 Unprocessable Entity`
  - Concurrency and idempotency (Step 16):
    - `planning.concurrency_etag_required` → `428 Precondition Required`
    - `planning.concurrency_mismatch` → `412 Precondition Failed`
    - `planning.idempotency_key_invalid` → `422 Unprocessable Entity`
    - `planning.idempotency_replay_conflict` → `409 Conflict`
  - Export/import (Step 17):
    - `planning.export_unsupported_format` → `422 Unprocessable Entity`
    - `planning.export_scope_invalid` → `422 Unprocessable Entity`
    - `planning.import_invalid_format_version` → `422 Unprocessable Entity`
    - `planning.import_strategy_not_allowed` → `409 Conflict`
    - `planning.import_validation_failed` → `422 Unprocessable Entity`
    - `planning.import_conflict_blocking` → `409 Conflict`
    - `planning.import_dry_run_only` → `409 Conflict`
  - External references (Step 18):
    - `planning.external_ref_invalid` → `422 Unprocessable Entity`
    - `planning.external_ref_duplicate` → `409 Conflict`
    - `planning.external_ref_scope_violation` → `422 Unprocessable Entity`
    - `planning.merge_by_key_not_allowed` → `409 Conflict`
    - `planning.merge_conflict` → `409 Conflict`
  - Bulk (Step 19):
    - `planning.batch_invalid` → `422 Unprocessable Entity`
    - `planning.batch_failed` → `409 Conflict`
    - `planning.batch_scope_violation` → `403 Forbidden`
    - `planning.batch_duplicate_item_id` → `422 Unprocessable Entity`
    - `planning.batch_dependency_unsatisfied` → `409 Conflict`
    - `planning.batch_concurrency_mismatch` → `409 Conflict`
    - `planning.batch_partial_not_allowed` → `409 Conflict`
    - `planning.batch_limit_exceeded` → `413 Payload Too Large`
  - Rate limits and quotas (Step 20):
    - `planning.rate_limited` → `429 Too Many Requests`
    - `planning.quota_exceeded` → `429 Too Many Requests`
    - `planning.request_too_large` → `413 Payload Too Large`
  - Retention (Step 22):
    - `planning.retention_not_expired` → `409 Conflict`
    - `planning.purge_not_allowed` → `403 Forbidden`
    - `planning.legal_hold_active` → `403 Forbidden`
    - `planning.resource_purged` → `410 Gone`
- The codes listed above are the allowed set for Phase 1. Any proposal for new codes or status mappings requires governance approval and a downstream phase change request; do not invent interim codes.
- Preserve deterministic error structures in examples and matrices: keys sorted, codes lower_snake_case, and details mapping to stable field names.
- Ensure every API doc that references errors links back to this registry or Step 04/05 without duplicating or diverging definitions.
- Document traceability: when an index or spec references an error code, include a relative link to this step or the originating step (04 or 05) to prevent drift.

## 5. Drift Detection Notes

- If an API doc introduces an error code or status not listed above, halt and escalate to governance before merging.
- If the envelope shape diverges (extra or missing fields), normalize to the canonical four-field structure or document the exception rationale in a future phase request.
- Cross-check indexes: all Phase 1 API steps should reference the same error code spellings and status pairings; mismatches must be reconciled by updating the relevant docs to match this registry.

## 6. Self-Audit

- Scope respected: Documentation-only; no application code or runtime behavior altered.
- Authority respected: Bound to Steps 01-09 and AGENT.md; uses Step 04/05 contracts without extension.
- Locked registry restated: Error codes and mappings are documented for Phase 1 without implying runtime behavior changes.
- Indexing updated: API and roadmap indexes include this step with canonical paths.

## 7. Next Authorized Step

- Phase 1 - Step 11: TBD (title and scope to be confirmed).
