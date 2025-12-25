# Phase 2 - Step 02: Backend Architecture Lock
Status: Architecture Lock - DONE

## Purpose
- Establish the backend architecture baseline for Phase 2 so implementation teams share consistent boundaries and dependencies.
- Codify non-business technical contracts for FastAPI, SQLAlchemy, Alembic, and Redis usage.
- Prevent drift by requiring any deviations to be captured in docs/decisions/.

## Stack Baseline
- Language and framework: Python 3.11+ with FastAPI for HTTP interfaces and dependency injection.
- Persistence: PostgreSQL 15+ accessed through SQLAlchemy ORM and Core.
- Migrations: Alembic for schema migrations with revision history committed to version control.
- Caching and async coordination: Redis 7+ for ephemeral caching, locks, and background coordination primitives when required.
- Observability hooks: structured logging and metrics emitters must be initialized in the infrastructure layer and injected downward without coupling to handlers.

## Layering and Boundaries
- **api/**: FastAPI routers, request/response models, and endpoint wiring only. No direct database access, ORM session management, or caching calls.
- **services/**: Application orchestration and coordination across domain operations. Services may call repositories, caches, and external gateways but must not encode business rules; they compose domain behaviors and manage transactional scope.
- **domain/**: Domain entities, value objects, and domain services. Pure logic with no framework imports or I/O concerns. Domain must not depend on api/, services/, or infrastructure code.
- **infra/**: Adapters for persistence, cache, messaging, HTTP clients, and settings loaders. Infrastructure provides repositories and gateway implementations consumed by services.
- Cross-layer interactions must travel downward through well-defined interfaces; lateral dependencies across peer layers are forbidden.

## Dependency Rules
- Domain depends on nothing outside its own module; all imports into domain must be standard library or domain-local utilities.
- Services may depend on domain and infrastructure abstractions but never import FastAPI route objects or HTTP request objects.
- API layer depends on services and DTO mappers; it must not instantiate database sessions directly or manipulate ORM entities beyond mapping to DTOs.
- Infrastructure may depend on external libraries (SQLAlchemy, Redis clients, HTTP clients) but must not reach into api/.
- Circular dependencies across domain, services, and infrastructure are forbidden; dependency direction is api -> services -> domain and api -> services -> infra -> db/cache.

## Configuration and Settings Contract
- Centralized settings module loads environment variables once at process startup, producing immutable configuration objects shared via dependency injection.
- Environment variable names must be explicit, documented, and prefixed for clarity (e.g., SAMU_DB_URL, SAMU_REDIS_URL, SAMU_ENV).
- Secrets (database URLs, API keys) are loaded from environment variables or secret managers only; configuration files must not hardcode secrets.
- Settings resolution order: defaults -> environment variables -> optional .env override for local development; runtime mutation of settings is forbidden.
- Components receive configuration through constructor parameters or FastAPI dependency injection; global mutable state for configuration is prohibited.

## Testing Strategy Boundaries
- Unit tests target domain logic and service orchestration with in-memory collaborators or fakes; no database or network access.
- Integration tests cover API endpoints, database migrations, repository adapters, and cache interactions using ephemeral Postgres/Redis instances.
- Alembic migration tests must validate forward and backward application against the current schema snapshot.
- Contract tests for infrastructure gateways should stub external systems at the boundary without embedding business rules.
- Tests must respect layering rules: API tests assert response contracts, service tests assert orchestration outcomes, and domain tests assert pure logic invariants.

## Enforcement and Deviations
- Architecture guardrails must be checked during code review and CI; infrastructure or service shortcuts that bypass domain contracts are rejected.
- Any deviation from these boundaries requires a documented DECISION under docs/decisions/ with rationale and rollback plan.
