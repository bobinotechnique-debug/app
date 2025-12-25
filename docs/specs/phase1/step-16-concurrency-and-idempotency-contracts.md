# Phase 1 - Step 16: Concurrency and Idempotency Contracts (Planning-only)

## 1. Purpose and Scope

This step defines planning-only contracts for concurrency control and idempotency across Phase 1 write operations. The goal is to prevent lost updates, ensure safe retries, and provide consistent client expectations.

This document is declarative. It defines contract-level requirements (headers/fields, semantics, error mapping) without prescribing storage engines, locking mechanisms, queues, or infrastructure.

In scope:

* Optimistic concurrency control contracts (revision tokens, ETags, If-Match)
* Idempotency contracts for create and transition actions (Idempotency-Key)
* Retry safety rules and response consistency
* Error mapping aligned to Step 10

Out of scope:

* Database-level locking details
* Distributed transactions
* Background jobs and async processing
* Exactly-once delivery guarantees

## 2. Authority and Precedence

* Step 01: planning-as-source-of-truth; concurrency protects planning integrity.
* Step 02: invariants remain authoritative; concurrency does not override validation.
* Step 04: API contracts define writes; Step 16 defines shared safety semantics.
* Step 08: audit trail requires deterministic attribution of state changes.
* Step 10: error taxonomy defines problem details and HTTP mapping.
* Step 12: lifecycle transitions are writes and must be concurrency safe.

If any rule requires product policy choices (e.g., which endpoints require idempotency), STOP and mark DECISION REQUIRED.

## 3. Core Concepts

### 3.1 Resource Revision Token

A revision token is an opaque value representing the current version of a resource.

Properties:

* opaque string
* changes whenever the resource changes
* may be exposed as:

  * HTTP ETag header
  * a field such as revision

Phase 1 does not mandate token format.

### 3.2 Optimistic Concurrency

Optimistic concurrency requires the client to prove it is updating the latest known revision.

Mechanisms:

* If-Match with ETag
* if_match with revision token in body or query (less preferred)

### 3.3 Idempotency

Idempotency ensures that repeating the same request (e.g., due to retries) results in:

* the same effect applied once
* and a consistent response payload

Idempotency is scoped to a caller + key + endpoint + request shape.

## 4. Concurrency Contracts

### 4.1 ETag Exposure (Recommended)

Read responses SHOULD include:

* ETag: <revision_token>

If ETag is not used, the revision token MUST be returned in the resource body.

### 4.2 If-Match for Writes

Writes that update an existing resource SHOULD require:

* If-Match: <revision_token>

Semantics:

* If-Match matches current revision -> proceed with validation and apply change
* If-Match missing -> policy-defined; Phase 1 recommends rejecting for safety
* If-Match does not match -> reject with concurrency error

Applies to:

* update resource (PATCH/PUT)
* state transitions (e.g., mission planned -> locked)
* archive/unarchive

DECISION REQUIRED if some writes are allowed without If-Match.

### 4.3 Precondition Semantics

* If-Match uses strong comparison semantics (opaque equality).
* Wildcard If-Match: * is not supported in Phase 1 unless explicitly added.

### 4.4 Read-After-Write Consistency

When a write succeeds, the response MUST include:

* the updated resource body (or canonical representation)
* the new revision token (ETag or body field)

This ensures clients can chain subsequent writes safely.

## 5. Idempotency Contracts

### 5.1 Idempotency-Key Header

For retryable writes, clients MAY provide:

* Idempotency-Key: <opaque string>

Server behavior:

* The first request with a new key is processed normally.
* Subsequent requests with the same key MUST return the same outcome.

### 5.2 Which Requests Require Idempotency

Phase 1 recommends Idempotency-Key support for:

* POST create operations (organization, project, mission, assignment, collaborator)
* POST actions that cause state transitions (if modeled as actions)

For PATCH/PUT, idempotency is usually achieved via If-Match plus deterministic bodies; Idempotency-Key is optional.

### 5.3 Response Consistency

For an idempotent replay:

* If the original request succeeded, return the same status code and body (or a semantically equivalent canonical body) and same resource identifier.
* If the original request failed due to validation, return the same problem details category.
* If the original request failed due to concurrency, return the same concurrency error.

### 5.4 Key Scope and TTL

* Key scope is per endpoint and per authenticated caller (auth out of scope, but caller identity is assumed).
* Keys SHOULD expire after a TTL.

DECISION REQUIRED for TTL duration; Phase 1 suggests 24 hours.

### 5.5 Safety Constraints

Idempotency MUST NOT bypass:

* authorization (Step 11)
* validation/invariants (Step 02)
* conflict blocking rules (Step 13)

Idempotency is about replay safety, not about granting new outcomes.

## 6. Optimistic Locking Patterns

### 6.1 Update Pattern

Client flow:

1. GET resource -> receives ETag
2. PATCH with If-Match: ETag
3. On success -> receives new ETag
4. On mismatch -> client re-GET and re-apply intent

### 6.2 Transition Pattern (Step 12)

State transitions must be treated as updates:

* require If-Match
* validate prerequisites and blocking conflicts
* apply transition event (auditable)

## 7. Retry Semantics

Clients may retry when:

* network timeouts occur
* 5xx errors occur

Clients SHOULD NOT blindly retry on:

* validation errors
* conflict blocking errors
* concurrency mismatch errors

When Idempotency-Key is used, safe retry is enabled for creates and actions.

## 8. Error Mapping (Step 10 Integration)

Concurrency and idempotency errors MUST map to Step 10 problem details.

Suggested semantic codes (must exist in Step 10 registry):

* planning.concurrency_etag_required (If-Match missing)
* planning.concurrency_mismatch (If-Match does not match)
* planning.idempotency_key_invalid (bad key)
* planning.idempotency_replay_conflict (same key, different request shape)

Notes:

* HTTP status mapping remains in Step 10.
* Problem details may include the current revision token (non-normative) to assist clients.

## 9. Interaction with Snapshots and Audit (Step 08)

* Each successful write creates an audit event.
* The audit event should include:

  * prior revision token
  * new revision token

This supports replay and traceability.

## 10. Validation Checklist

Before implementation work proceeds:

* All update and transition surfaces in Step 04 reference If-Match / revision semantics.
* Idempotency-Key is documented for creates and any action-style transitions.
* Error codes referenced here exist in Step 10 registry.
* Retry guidance does not contradict conflict blocking rules (Step 13).
* Audit expectations align with Step 08.
