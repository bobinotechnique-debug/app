# Phase 1 - Step 19: Bulk Operations and Batch Semantics (Planning-only)
_FROZEN by phase1_freeze_1.0.0_

## 1. Purpose and Scope

This step defines planning-only contracts for bulk and batch operations in Phase 1.

Goals:

* Standardize request/response semantics for submitting multiple creates, updates, upserts, or transitions in one operation
* Provide predictable behavior for partial success versus atomic failure
* Define per-item validation and error reporting aligned to Step 10
* Ensure bulk operations respect concurrency (Step 16) and conflicts (Step 13)

This document is declarative. It does not mandate specific endpoints, database transaction strategies, queues, or performance guarantees.

In scope:

* Bulk create, update, upsert, and state transitions
* Atomicity policies (all-or-nothing versus partial)
* Per-item error reporting and correlation
* Idempotency and retry rules
* Concurrency requirements for bulk updates

Out of scope:

* Long-running async bulk jobs
* Streaming ingestion pipelines
* External integrations
* Optimization and scheduling solvers

## 2. Authority and Precedence

* Step 01 planning-as-source-of-truth governs all mutations.
* Step 02 invariants apply to each item and to cross-item references.
* Step 04 API contracts define canonical resources; Step 19 defines batch semantics.
* Step 08 audit applies to each applied change and to the batch summary.
* Step 10 error taxonomy governs error shapes and semantics.
* Step 11 authorization governs who may perform bulk operations.
* Step 12 lifecycle governs allowed transitions.
* Step 13 conflicts may block transitions.
* Step 16 concurrency and idempotency governs safe retries.
* Step 18 external refs may be used for merge_by_key where allowed.

If atomicity policy requires product decisions (e.g., default mode), STOP and escalate to governance before proceeding.

## 3. Terminology

* bulk: a single request containing multiple items
* item: a single mutation unit within the bulk request
* atomic: all items are applied or none are applied
* partial: some items may apply while others fail

## 4. Bulk Operation Types

Phase 1 recognizes the following bulk operation intents:

* bulk_create: create multiple resources
* bulk_update: update multiple resources by id
* bulk_upsert: create or update multiple resources (policy-defined)
* bulk_transition: apply lifecycle transitions to multiple resources
* bulk_archive: archive or unarchive multiple resources

No specific endpoint naming is mandated.

## 5. Request Envelope

A bulk request uses a canonical envelope.

Fields (illustrative):

* operation: one of the bulk operation types
* scope: { organization_id | project_id }
* mode: atomic | partial
* idempotency_key (optional): opaque string (prefer header Idempotency-Key)
* items: array of item requests

Item fields:

* item_id: client-supplied correlation id (required)
* resource_type: organization | project | mission | assignment | collaborator
* action: create | update | upsert | transition | archive | unarchive
* target_id (optional): internal id for update or transition
* match_key (optional): external ref match key for merge_by_key (Step 18)
* if_match (optional): revision token for optimistic concurrency (Step 16)
* payload: canonical resource body or patch-like object

Rules:

* item_id must be unique within the request.
* scope is required and all items must belong to that scope.

## 6. Atomicity Policy

### 6.1 Mode: atomic

* All items are validated first.
* If any item fails validation, the entire batch fails and no changes are applied.
* Response includes per-item errors.

### 6.2 Mode: partial

* Items are processed independently.
* Successful items apply; failed items do not.
* Response includes per-item results.

### 6.3 Default Mode

Default mode when omitted: atomic (all-or-nothing) for safety in Phase 1.

## 7. Processing Order and Cross-Item References

### 7.1 Order

* Phase 1 does not mandate processing order, but results must be deterministic.
* If order matters (e.g., create project then missions), the request SHOULD provide items in dependency order.

### 7.2 Temporary Client References (Optional)

To support create chains within one request, items MAY use:

* temp_id: client temporary identifier
* references within payload may use temp_id

Phase 1 forbids temp_id intra-batch references; bulk_create must be limited to resources without intra-batch references.

## 8. Validation Rules

Each item MUST be validated against:

* Step 04 shape requirements
* Step 02 invariants
* Step 12 transition legality for transition actions
* Step 13 conflict blocking rules for confirm or lock transitions
* Step 16 concurrency requirements (If-Match) where policy requires

Additionally, the batch MUST be validated for:

* scope coherence (all items within scope)
* duplicate external refs (Step 18 uniqueness) when using match_key

## 9. Concurrency and Idempotency

### 9.1 Concurrency

* For update or transition items, If-Match SHOULD be required per Step 16.
* A bulk request may include multiple items targeting the same resource id; this is discouraged.

If multiple items target the same resource:

* atomic mode: reject with a batch-level error unless explicitly allowed
* partial mode: reject to preserve determinism; clients must split requests by resource

### 9.2 Idempotency

* Bulk requests SHOULD support Idempotency-Key (Step 16).
* Replays with the same Idempotency-Key must return the same batch outcome.
* If the same key is used with a different request body, reject.

## 10. Response Envelope

A bulk response MUST be machine-readable and correlate each result to item_id.

Fields (illustrative):

* operation
* scope
* mode
* applied_count
* failed_count
* results: array of item results

Item result fields:

* item_id
* status: success | failed | skipped
* resource_type
* resource_id (if known)
* revision (new revision token if success)
* error (if failed): problem details summary aligned to Step 10

Batch-level error:

* If the entire batch fails (atomic), return a problem details envelope with:
  * code: planning.batch_failed
  * extensions: per-item errors

## 11. Error Mapping (Step 10 Integration)

Suggested semantic codes (must exist in Step 10 registry):

* planning.batch_invalid
* planning.batch_failed
* planning.batch_scope_violation
* planning.batch_duplicate_item_id
* planning.batch_dependency_unsatisfied
* planning.batch_concurrency_mismatch
* planning.batch_partial_not_allowed

Per-item errors reuse the standard codes from:

* Step 10 base registry
* Step 12 transition errors
* Step 13 conflict errors
* Step 16 concurrency and idempotency errors
* Step 18 external ref errors

## 12. Audit Requirements (Step 08)

* In partial mode, each successful item must create its own audit event.
* In atomic mode, each successful item must create its own audit event; additionally, a batch summary audit event MAY be created.
* Failed items MUST NOT create audit events.

## 13. Validation Checklist

Before implementation work proceeds:

* Bulk request and response envelopes are consistent with Step 04 and Step 10.
* Atomic versus partial semantics are explicitly declared and default decided.
* Concurrency (Step 16) requirements are enforced per item.
* Conflict blocking (Step 13) is applied to transition items.
* Error codes referenced here exist in Step 10 registry.
* Import Step 17 can reuse these batch semantics where applicable.
