# Phase 1 - Step 18: Interop Keys and External References (Planning-only)

## 1. Purpose and Scope

This step defines planning-only interoperability keys and external reference contracts for Phase 1. It standardizes how planning resources can be linked to identifiers from other systems (or prior exports) without changing planning-as-source-of-truth.

Goals:

* Allow stable linking to external systems (HR, venue systems, spreadsheets) without embedding execution behavior
* Support deduplication and merge strategies during import (Step 17)
* Provide consistent semantics for external identifiers and correlation ids

This document is declarative. It does not mandate integrations, sync engines, or data pipelines.

In scope:

* External identifier fields and constraints
* source_system naming
* external reference objects (multiple keys)
* Deduplication rules and merge semantics (planning-only)
* Error mapping aligned to Step 10

Out of scope:

* Real-time synchronization
* Conflict resolution automation
* Data ownership transfer to external systems
* Authentication/authorization federation

## 2. Authority and Precedence

* Step 01 planning-as-source-of-truth: external keys are metadata, not authority.
* Step 02 invariants: external keys cannot bypass domain constraints.
* Step 04 resource contracts: external reference fields extend shapes as optional metadata.
* Step 08 audit: changes to external keys are auditable.
* Step 10 errors: invalid external refs map to registry.
* Step 15 query filters may include external ids.
* Step 17 import uses these semantics for merge_by_key.

If any rule requires product policy (e.g., whether external keys are mutable), STOP and escalate to governance before proceeding.

## 3. Core Concepts

### 3.1 External Reference

An external reference links a planning resource to an identifier in another system.

Canonical structure:

* source_system: string
* external_id: string
* external_type (optional): string
* issued_at (optional): ISO 8601 timestamp

A resource may have zero or more external references.

### 3.2 Source System

source_system is a stable namespace identifying the origin system.

Rules:

* lowercase slug recommended: e.g., hr_sirh, venue_bobino, csv_import
* must be ASCII
* must be stable over time

### 3.3 External Id

external_id is an opaque identifier string.

Rules:

* treated as case-sensitive
* must be ASCII
* length limits are policy-defined

## 4. Field Placement and Resource Coverage

External references may be applied to the following Phase 1 resources:

* organization
* project
* mission
* assignment
* collaborator

Recommended field shape (illustrative):

* external_refs: list[ExternalRef]

Alternative simplified fields may exist for legacy cases:

* external_id
* source_system

If both exist, external_refs is authoritative.

## 5. Uniqueness and Constraints

### 5.1 Uniqueness Within Scope

An external reference tuple (source_system, external_id, external_type) MUST be unique within the declared scope.

Scope rules:

* organization, project, collaborator: unique within the organization
* mission, assignment: unique within the project

### 5.2 Mutability

External references are mutable via add/remove only; updating an existing tuple requires remove + add.

### 5.3 Deletion

Removing external refs does not delete the resource.

## 6. Deduplication Semantics

Deduplication is relevant for:

* import merge_by_key (Step 17)
* manual linking of resources to external ids

### 6.1 Match Keys

A match key is:

* (source_system, external_id, external_type)

If external_type is not present, match key is:

* (source_system, external_id)

### 6.2 Dedup Outcomes

When an incoming item matches an existing item by match key:

* create_only strategy: reject as duplicate
* upsert strategy: update existing item by internal id only; match key alone is not sufficient
* merge_by_key strategy: treat as upsert target and update existing item

### 6.3 Merge Safety

Merge_by_key MUST NOT:

* re-parent resources across organizations/projects
* override lifecycle terminal states without explicit policy
* bypass concurrency requirements (Step 16) when applicable

## 7. Merge Semantics (Planning-only)

### 7.1 Field-Level Rules

Phase 1 does not define field-by-field merge rules for every resource. Instead, it defines safe defaults:

Default merge behavior (recommended):

* scalar fields: incoming overwrites existing if non-null unless marked merge-immutable
* lists: replace by default (unless list elements have stable ids)
* external_refs: union by match key

Merge-immutable fields (never overwritten by merge):

* lifecycle_state
* parent references (org_id, project_id)

### 7.2 Lifecycle Merge

By default:

* lifecycle_state is not overwritten by import merge unless the import explicitly requests a state transition and that transition is legal (Step 12).

### 7.3 Audit

Every merge that changes a resource must be auditable (Step 08), including:

* which external match key caused the merge
* before/after snapshots of changed fields (non-normative)

## 8. Query and Filtering (Step 15 Integration)

Standard filters:

* source_system
* external_id
* external_type

Rules:

* filtering by external_id MUST require source_system to avoid ambiguity.

## 9. Error Mapping (Step 10 Integration)

External reference errors MUST map to Step 10 problem details.

Suggested semantic codes (must exist in Step 10 registry):

* planning.external_ref_invalid
* planning.external_ref_duplicate
* planning.external_ref_scope_violation
* planning.merge_by_key_not_allowed
* planning.merge_conflict

## 10. Forward Compatibility Notes

Phase 2+ may introduce:

* sync status fields (last_synced_at, sync_errors)
* bidirectional connectors
* mapping tables and reconciliation workflows

No sync behavior is required or implied in Phase 1.

## 11. Validation Checklist

Before implementation work proceeds:

* External reference fields are optional metadata and do not change source-of-truth.
* Uniqueness scope decisions are recorded and traceable.
* Import Step 17 merge_by_key references this step.
* Query filters align with Step 15.
* Error codes referenced here exist in Step 10 registry.
