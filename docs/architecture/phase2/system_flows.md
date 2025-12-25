# Phase 2 - Step 02: System Flows
Status: Architecture Lock - DONE

## Purpose
- Describe the end-to-end technical flow for Phase 2 requests without defining product behaviors.
- Clarify validation, error handling, and cross-layer responsibilities.
- Require any deviations to be documented in docs/decisions/.

## System Request Flow
1. **Frontend**: Pages and components compose requests using the centralized API client; client-side validation covers input formatting and required fields only.
2. **API Layer**: FastAPI routers accept requests, perform schema validation with Pydantic models, and map HTTP inputs to service calls. API handlers must not access the database directly.
3. **Services**: Coordinate domain operations, manage transactions, and call repositories or gateways. Services apply orchestration logic and invoke domain behaviors but do not introduce new business rules.
4. **Domain**: Executes pure business rules and invariants using domain entities and value objects. No I/O or framework dependencies are allowed here.
5. **Infrastructure**: Repositories and adapters translate domain and service requests into persistence or integration calls (PostgreSQL via SQLAlchemy, Redis, external HTTP). Infrastructure enforces data access policies and returns results without leaking driver specifics upward.
6. **Database/Cache**: PostgreSQL stores authoritative data; Redis handles ephemeral cache or coordination state as configured by infrastructure.

## Validation Placement
- Client-side validation covers presentation-level constraints (required fields, simple formatting) only.
- API layer performs request shape validation, type checks, and tenancy/scope assertions based on configuration.
- Domain enforces invariants and rule evaluation; validation failures return structured errors to services for mapping.
- Services ensure cross-component consistency (e.g., ensuring dependencies are loaded) and consolidate validation results from domain and infrastructure.

## Error Mapping and Propagation
- Services convert domain and infrastructure errors into standardized application errors before returning to the API layer.
- API layer maps standardized errors into the established error envelope and problem detail contracts defined in Phase 1 (Step 10) without reinterpreting codes.
- Frontend API client normalizes error envelopes into UI-consumable shapes; components display errors without altering codes or retry semantics beyond documented client behavior.

## Anti-Patterns and Forbidden Flows
- API routes bypassing services to access repositories or ORM sessions directly.
- Domain logic reaching into infrastructure (database sessions, Redis clients, HTTP clients) or into API request objects.
- Services embedding business rules that belong in domain entities or applying validation rules inconsistently with domain outcomes.
- Infrastructure emitting HTTP responses or shaping error envelopes; only API layer handles HTTP concerns.
- Frontend components issuing ad hoc fetch calls or mutating shared state outside approved providers.
- Implicit cross-organization or cross-project data access paths; all access must travel through validated service boundaries.

## Observability and Tracing Placement
- Request identifiers and correlation metadata originate at the API edge and propagate through services, domain calls, and infrastructure adapters.
- Infrastructure adapters emit database and cache telemetry, while services emit orchestration-level logs and metrics.
- Frontend propagates correlation headers provided by the API client and records client-side navigation metrics without embedding business semantics.
