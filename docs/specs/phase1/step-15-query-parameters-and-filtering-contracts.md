# Phase 1 - Step 15: Query Parameters and Filtering Contracts (Planning-only)
_FROZEN by phase1_freeze_1.0.0_

## 1. Purpose and Scope

This step defines planning-only query, filtering, sorting, pagination, and expansion contracts used across Phase 1 read surfaces.

Goal:

* Standardize how consumers query planning resources and derived views
* Ensure consistent semantics across endpoints and future steps
* Provide a shared vocabulary for filtering by time windows, states, conflicts, and ownership scope

This document is declarative. It does not mandate endpoint URLs, database indexes, caching strategy, or performance guarantees.

In scope:

* Standard query parameters: paging, sorting, includes/expands
* Standard filters: lifecycle states, time windows, project/org scope
* Conflict filters aligned to Step 13
* Derived view selectors aligned to Step 14

Out of scope:

* Authentication and authorization enforcement (Step 11)
* Web UI behavior or specific UX designs
* Full-text search engines or ranking algorithms
* GraphQL or other alternative query languages

## 2. Authority and Precedence

* Step 01 and Step 02 define canonical artifacts and invariants.
* Step 04 defines API resource contracts; Step 15 defines shared query semantics.
* Step 10 defines errors; Step 15 maps invalid query usage to those errors.
* Step 12 lifecycle states are filterable values.
* Step 13 conflicts define filterable types and severities.
* Step 14 derived models define optional expansions/selectors.

If a query rule requires product policy (e.g., default sort), STOP and escalate to governance before proceeding.

## 3. Shared Conventions

### 3.1 Parameter Naming

* Use lower_snake_case for query keys.
* Use comma-separated lists for multi-value filters.
* Use ISO 8601 UTC timestamps for time filters.

### 3.2 Unknown Parameters

Unknown parameters MUST be rejected (extra=forbid intent), mapped to Step 10 error taxonomy.

### 3.3 Default Behavior

Unless otherwise specified:

* archived items are excluded from list results
* paging defaults to a safe limit
* sort defaults are stable and deterministic (id ascending)

Defaults are declared per resource or surface.

## 4. Pagination Contract

### 4.1 Page-Based Pagination

Supported parameters:

* page: integer >= 1
* page_size: integer in [1..200]

Constraints:

* Phase 1 max page_size is 200.

Response metadata (illustrative):

* page
* page_size
* total_items (optional)
* total_pages (optional)

### 4.2 Cursor-Based Pagination (Optional)

If used, cursor parameters are:

* cursor: opaque string
* limit: integer in [1..200]

Phase 1 allows either model, but a given list surface MUST pick one and remain consistent; mixing pagination models on the same endpoint is not allowed.

## 5. Sorting Contract

Parameters:

* sort: comma-separated list of fields

Format:

* sort=field_a,-field_b

Rules:

* Leading '-' indicates descending.
* Sort fields must be whitelisted per surface.
* When sort ties occur, a stable tiebreaker must be applied (e.g., id).

Invalid sort fields MUST be rejected.

## 6. Include/Expand Contract

### 6.1 include

Purpose: request additional derived or nested summaries without changing the primary resource shape.

Parameter:

* include: comma-separated tokens

Examples:

* include=summary
* include=conflicts
* include=staffing

Tokens are whitelisted per surface.

### 6.2 expand

Purpose: request embedding of related resources (read-only).

Parameter:

* expand: comma-separated relationship names

Examples:

* expand=project
* expand=missions
* expand=assignments

Rules:

* Expansions MUST be bounded to prevent unbounded graph loading.
* Expansions MUST NOT change authorization semantics; they are filtered by the caller's scope (Step 11 is out of scope for enforcement here).

### 6.3 depth (Optional)

If nested expansions exist:

* depth: integer in [0..D]

D is policy-defined (recommended D <= 2).

## 7. Standard Filters

### 7.1 Scope Filters

* organization_id: uuid
* project_id: uuid

Rules:

* Any resource list that is ambiguous without scope MUST require one of these filters.
* If both are provided, project_id must belong to organization_id (Step 02 boundary).

### 7.2 Lifecycle State Filters (Step 12)

* state: comma-separated states applicable to the resource

Examples:

* state=active
* state=planned,locked

Default:

* state excludes archived unless explicitly included.

### 7.3 Time Window Filters

Supported parameters:

* time_from: ISO 8601 UTC
* time_to: ISO 8601 UTC

Rules:

* time_from < time_to
* Window filtering semantics must be declared per surface:

  * overlap: include items whose window overlaps [time_from, time_to)
  * contained: include items fully contained in [time_from, time_to)

Phase 1 default for missions and assignments: overlap.

### 7.4 Actor/Ownership Filters

Planning-only filters:

* collaborator_id: uuid

Use cases:

* assignments for collaborator
* collaborator load summary windows (Step 14)

### 7.5 Text Filters (Optional)

If supported:

* q: free text

Rules:

* q is a simple contains match over whitelisted fields (e.g., name, code).
* Full-text ranking is out of scope.

## 8. Conflict Filters (Step 13)

These filters apply to conflict list surfaces or resources that embed conflict summaries.

Parameters:

* conflict_status: open,acknowledged,resolved,overridden
* conflict_severity: info,warn,block
* conflict_type: comma-separated Step 13 conflict types

Rules:

* By default, conflict_status=open,acknowledged
* conflict_type must be validated against the taxonomy

Examples:

* conflict_severity=block
* conflict_type=collaborator_time_overlap,assignment_outside_mission_window

## 9. Derived View Selectors (Step 14)

For surfaces returning summaries:

* view: token selecting a derived model projection

Examples:

* view=project_summary
* view=mission_summary
* view=collaborator_load

Rules:

* view tokens must be whitelisted.
* view may imply required scope filters (e.g., collaborator_load requires collaborator_id and time window).

## 10. Error Handling (Step 10 Integration)

Invalid query usage MUST map to Step 10 problem details.

Suggested semantic codes (must exist in Step 10 registry):

* planning.query_invalid_parameter (unknown key)
* planning.query_invalid_value (bad enum/value)
* planning.query_invalid_range (time_from >= time_to)
* planning.query_scope_required (missing required scope)
* planning.query_limit_exceeded (page_size > N)

This step assigns semantic meaning only; HTTP status mapping remains in Step 10.

## 11. Validation Checklist

Before implementation work proceeds:

* Every list/read surface in Step 04 references these query semantics.
* Lifecycle state filters match Step 12 state sets.
* Conflict filters match Step 13 taxonomy and statuses.
* Derived view selectors match Step 14 derived model names.
* Error codes referenced here exist in Step 10 registry.
