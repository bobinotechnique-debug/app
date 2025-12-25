# Phase 2 - Step 02: Data Architecture Lock
Status: Architecture Lock - DONE

## Purpose
- Define data persistence baselines for Phase 2 without introducing product logic.
- Govern schema evolution, migration discipline, and forbidden database behaviors.
- Require deviations to be documented in docs/decisions/ with impact analysis.

## Persistence Baseline
- Primary database: PostgreSQL 15+ as the authoritative store.
- Migration tooling: Alembic manages all schema changes with versioned revisions committed to the repository.
- Access patterns: SQLAlchemy ORM and Core used through infrastructure repositories; direct SQL outside repositories is discouraged and must remain read-only when necessary.

## Migration Rules
- Every schema change requires an Alembic revision with clear upgrade and downgrade paths; manual database edits are prohibited.
- Migrations must be idempotent within their revision scope and avoid destructive operations without explicit safeguards.
- Production migrations must be backwards compatible with the running application until deployment is complete; breaking changes require staged rollouts and documented decisions.
- Data backfills or transformations must be explicit in migrations with logging hooks; silent data modification is forbidden.
- Migration ordering must respect dependency graph; out-of-order revision merges must be resolved by new revisions rather than editing history.

## Schema Evolution Boundaries
- Columns, constraints, and indexes must include rationale in migration descriptions; removal of columns requires a deprecation window and explicit data handling plan.
- Default values must be deterministic and avoid server-side randomization; timezone handling must remain explicit (UTC only).
- UUID primary keys are preferred; composite or natural keys require justification and a DECISION entry.
- Audit fields (created_at, updated_at) must be added through migrations and kept consistent across tables.

## Forbidden Items in Phase 2
- Database-level business logic such as triggers, stored procedures implementing domain rules, or cascading actions beyond referential integrity.
- Silent schema drift from applying local changes without Alembic revisions.
- Unmanaged extensions that introduce side effects or hidden state (e.g., cron-based jobs) without documented decisions.
- Automatic schema synchronization from ORM metadata at runtime in production environments.

## Tables vs Views Policy
- Base tables capture authoritative domain records; naming must be explicit and singular per entity boundary.
- Database views are allowed only as read-only projections for reporting or API optimization; materialized views require refresh strategies documented with performance budgets.
- Views must not hide business logic or enforce validation; they expose derived projections only.
- Any new view or materialized view must include dependency mapping in its migration and avoid breaking consumers when refreshed.

## Testing Strategy Boundaries
- Migration tests must run against ephemeral PostgreSQL instances and validate both upgrade and downgrade paths.
- Repository and data access integration tests must cover transactional behavior and isolation levels where relevant.
- Data fixtures used in tests must map to documented schemas; implicit schema assumptions are forbidden.

## Enforcement and Deviations
- Schema changes and migrations are subject to code review with architecture alignment checks.
- Any deviation from these data architecture rules requires a DECISION under docs/decisions/ including rollback and monitoring plans.
