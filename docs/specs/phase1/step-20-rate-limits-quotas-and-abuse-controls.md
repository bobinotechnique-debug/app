# Phase 1 - Step 20: Rate Limits, Quotas, and Abuse Controls (Planning-only)
_FROZEN by phase1_freeze_1.0.0_

## 1. Purpose and Scope

This step defines planning-only contracts for rate limiting, quotas, and abuse controls in Phase 1.

Goals:

* Provide consistent client-visible semantics when limits are reached
* Standardize headers and problem details mapping for throttling
* Define quota concepts per organization/project and per operation type
* Define bulk safety limits aligned to Step 19
* Provide retry/backoff guidance without prescribing implementation

This document is declarative. It does not mandate specific enforcement mechanisms (API gateway, middleware), storage, or monitoring systems.

In scope:

* Rate limit semantics and response headers
* Quotas and limits per scope (organization/project) and per operation type
* Bulk operation limits and payload constraints
* Abuse controls and request validation constraints
* Error mapping aligned to Step 10

Out of scope:

* Billing tiers, pricing, subscription logic
* WAF rules, bot mitigation services
* DDoS protection infrastructure
* Detailed observability and metrics pipelines (covered elsewhere)

## 2. Authority and Precedence

* Step 01 planning-as-source-of-truth: limits do not change planning meaning.
* Step 04 API contracts: limit semantics apply to those endpoints.
* Step 10 error taxonomy: throttling and quota errors must map to problem details.
* Step 16 retry/idempotency: safe retries and backoff must align.
* Step 19 bulk semantics: bulk limits must be compatible with batch envelopes.

If any limits require product policy decisions (exact numbers, tiering), STOP and escalate to governance before proceeding.

## 3. Definitions

### 3.1 Rate Limit

A rate limit constrains the frequency of requests over time.

Examples:

* requests per minute per caller
* writes per second per organization

### 3.2 Quota

A quota constrains the amount of a resource or operation over a longer horizon.

Examples:

* maximum missions per project
* maximum collaborators per organization
* maximum exports per day

### 3.3 Abuse Controls

Abuse controls are protective limits and validations to prevent misuse:

* payload size limits
* burst limits
* invalid request rejection (Step 15 extra=forbid intent)

## 4. Client-Visible Rate Limit Semantics

### 4.1 HTTP Status

When throttled, the response MUST use:

* HTTP 429 Too Many Requests

### 4.2 Retry-After

When possible, throttling responses SHOULD include:

* Retry-After: <seconds>

### 4.3 Rate Limit Headers

Phase 1 recommends the following headers (names may vary by standard, but semantics must be consistent):

* RateLimit-Limit: maximum requests in window
* RateLimit-Remaining: remaining requests in window
* RateLimit-Reset: seconds until window resets OR absolute timestamp

If these are not used, equivalent headers may be provided.

### 4.4 Idempotency and Retries

* Clients may retry after Retry-After.
* For retryable writes, clients SHOULD use Idempotency-Key (Step 16) to prevent duplicate effects.

## 5. Quota Model (Planning-only)

Quotas are policy-defined and may depend on:

* organization
* project
* caller role (Step 11), without specifying enforcement
* operation type

Quota types (illustrative):

* max_projects_per_org
* max_missions_per_project
* max_assignments_per_mission
* max_collaborators_per_org
* max_exports_per_day
* max_import_rows_per_day

Exact numeric thresholds are product policy and are not set in Phase 1.

## 6. Bulk Limits (Step 19 Integration)

Bulk operations must be bounded to protect the system.

Recommended bulk limits (policy placeholders):

* max_items_per_batch: 100
* max_payload_bytes: 5 MB
* max_nested_expansions: aligns to Step 15 depth constraints

Rules:

* If a batch exceeds limits, the request MUST be rejected.
* For partial mode, limits apply to the entire batch, not per item.

## 7. Abuse Controls and Validation Constraints

### 7.1 Payload Size

Requests SHOULD be rejected when:

* body exceeds a configured size limit

### 7.2 Parameter Explosion

Requests SHOULD be rejected when:

* include/expand lists exceed a configured count
* conflict_type lists exceed a configured count

### 7.3 Write Burst Controls

Write operations (create/update/transition/import) may have stricter rate limits than reads.

Phase 1 declares:

* reads and writes may have separate rate limit buckets

## 8. Error Mapping (Step 10 Integration)

Rate limit and quota errors MUST map to Step 10 problem details.

Suggested semantic codes (must exist in Step 10 registry):

* planning.rate_limited
* planning.quota_exceeded
* planning.request_too_large
* planning.batch_limit_exceeded
* planning.query_limit_exceeded (already referenced in Step 15)

Notes:

* HTTP status mapping remains in Step 10. For rate limiting, status SHOULD be 429.
* Problem details may include:

  * retry_after_seconds
  * limit scope (organization/project)
  * limit type (read/write/bulk)

## 9. Backoff Guidance (Non-Normative)

Clients should:

* honor Retry-After when present
* use exponential backoff with jitter when Retry-After is missing
* avoid retry storms by capping retries

This is guidance only; no algorithm is mandated.

## 10. Validation Checklist

Before implementation work proceeds:

* 429 semantics and Retry-After guidance do not contradict Step 16 idempotency.
* Bulk limit semantics align with Step 19 envelopes.
* Query limit errors align with Step 15.
* Error codes referenced here exist in Step 10 registry.
