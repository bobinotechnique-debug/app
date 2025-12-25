# Phase 1 - Step 17: Export and Import Contracts (Planning-only)
_FROZEN by phase1_freeze_1.0.0_

## 1. Purpose and Scope

This step defines planning-only contracts for exporting and importing planning data in Phase 1.

Goals:

* Provide a consistent way to extract planning state for review, backup, sharing, or offline analysis
* Support safe re-import with validation and predictable outcomes
* Allow dry-run import validation without mutating planning state
* Ensure exports can be tied to snapshots (Step 08) for reproducibility

This step is declarative. It does not mandate specific endpoint URLs, storage backends, streaming implementations, or file delivery mechanisms.

In scope:

* Export formats (JSON, CSV) and versioning
* Snapshot-based export semantics
* Import semantics: create/update mapping, conflict handling, idempotency, dry-run
* Validation and error mapping aligned to Step 10

Out of scope:

* Data migrations across major domain revisions
* Execution data exports (time tracking, payroll)
* Third-party integrations and connectors
* Encryption, signing, or transport security

## 2. Authority and Precedence

* Step 01 planning-as-source-of-truth: exports derive solely from planning artifacts.
* Step 02 invariants: imports must never violate invariants.
* Step 04 API contracts: resources are the canonical shapes; export/import aligns to them.
* Step 08 snapshots: exports SHOULD reference snapshot_id for reproducibility.
* Step 10 errors: validation and import errors must map to the registry.
* Step 11 authorization: only permitted roles may export/import (enforcement out of scope).
* Step 12 lifecycle: imports must respect state models.
* Step 13 conflicts: imports may surface conflicts; block conflicts cannot be overridden by import.
* Step 16 concurrency/idempotency: imports should be safe to retry.

If policy decisions are required (e.g., whether import can update existing resources), STOP and escalate to governance before proceeding.

## 3. Export Contract

### 3.1 Export Types

Supported export types:

* snapshot_export: full planning export for a scope at a point in time
* delta_export (optional): changes since a snapshot or timestamp

Phase 1 requires snapshot_export; delta_export is optional.

Export before purge is mandatory; purge workflows must capture a snapshot_export for the affected scope first.

### 3.2 Export Scope

Exports MUST be scoped to exactly one of:

* organization_id
* project_id

Rules:

* project export includes all missions, assignments, and collaborators referenced within that project scope.
* organization export includes projects and associated entities, subject to policy limits.

### 3.3 Snapshot Alignment

Snapshot export MUST include:

* snapshot_id (Step 08) if available
* exported_at timestamp
* scope descriptor

If snapshot_id is not available, export MUST include a computed_at timestamp and a stable planning revision token if available.

### 3.4 Export Formats

#### 3.4.1 JSON (Required)

A JSON export is the canonical export format.

Top-level structure:

* format_version
* exported_at
* snapshot_id (optional)
* scope: { organization_id | project_id }
* resources: { organizations, projects, missions, assignments, collaborators }
* references: optional lookup tables (roles, qualification keys)

Rules:

* Resources are arrays of canonical resource documents aligned to Step 04.
* Resource identifiers must be preserved.
* Order of resources is not semantically meaningful.

#### 3.4.2 CSV (Optional)

CSV export is a convenience format for offline analysis.

Minimum required CSV tables for project scope:

* projects.csv
* missions.csv
* assignments.csv
* collaborators.csv

Rules:

* CSV is a projection and may omit nested fields.
* A CSV export MUST include a manifest.json describing:

  * format_version
  * exported_at
  * scope
  * file list + columns

## 4. Export Versioning

* format_version is required.
* Phase 1 recommends semantic versions:

  * 1.0 for the initial contract
  * minor bumps for additive changes
  * major bumps for breaking changes

Clients MUST treat unknown major versions as unsupported.

## 5. Import Contract

### 5.1 Import Modes

* dry_run: validate and compute effects without applying changes
* apply: perform mutations if validation passes

### 5.2 Import Scope

Import requests MUST declare scope:

* organization_id or project_id

Rules:

* Imported resources must belong to the declared scope.
* Cross-scope references are rejected.

### 5.3 Import Strategies

Supported strategies (policy-defined; Phase 1 declares the options):

* create_only: create new resources; reject if ids already exist
* upsert: create or update by id

Phase 1 only allows create_only and upsert; merge_by_key is forbidden.

### 5.4 Idempotency and Safety

Imports SHOULD support:

* Idempotency-Key (Step 16)

Rules:

* For apply mode, repeating the same import payload with same Idempotency-Key must be safe.
* If import uses upsert, concurrent modifications must be protected by If-Match or a bulk revision token when feasible.

## 6. Validation Rules

Imports MUST be validated against:

* Step 04 schemas (shape)
* Step 02 invariants (domain constraints)
* Step 12 lifecycle transitions (state legality)
* Step 13 conflict blocking rules (block conflicts cannot be imported into a confirmed/locked state)

Validation output in dry_run mode MUST include:

* counts of resources to create/update
* list of detected conflicts by type/severity
* list of invalid items with reasons and references

## 7. Conflict Handling During Import

Rules:

* If import would introduce any block conflict, apply mode MUST fail unless the payload is adjusted.
* warn conflicts may be imported only when they are not marked override-required, OR when an explicit override record is included and permitted.
* info conflicts are allowed.

Importing override records is not allowed in Phase 1; overrides must be recorded manually after import where permitted.

## 8. Import Result Model

The import result MUST provide stable, machine-readable output.

Minimum fields:

* mode: dry_run | apply
* format_version
* scope
* created: map[resource_type -> int]
* updated: map[resource_type -> int]
* skipped: map[resource_type -> int]
* conflicts: list[conflict_record_summary]
* errors: list[item_error]

Where:

* conflict_record_summary aligns to Step 13 taxonomy (type, severity, status)
* item_error includes: resource_type, resource_id or row number, code, message

## 9. Error Mapping (Step 10 Integration)

Import/export failures MUST map to Step 10 problem details.

Suggested semantic codes (must exist in Step 10 registry):

* planning.export_unsupported_format
* planning.export_scope_invalid
* planning.import_invalid_format_version
* planning.import_strategy_not_allowed
* planning.import_validation_failed
* planning.import_conflict_blocking
* planning.import_dry_run_only

## 10. Audit and Traceability (Step 08)

* Export events may be recorded as audit events (optional) with scope and snapshot_id.
* Import apply mode MUST record an audit event summarizing:

  * counts created/updated
  * actor
  * timestamp
  * import reference (e.g., filename or external correlation id)

Dry-run MUST NOT create audit events.

## 11. Validation Checklist

Before implementation work proceeds:

* JSON export schema is aligned to Step 04 resource contracts.
* Export includes snapshot attribution (snapshot_id or computed_at + revision).
* Import dry_run semantics are fully specified and do not mutate state.
* Import validation references Steps 02/12/13.
* Error codes referenced here exist in Step 10 registry.
* Idempotency guidance aligns with Step 16.
