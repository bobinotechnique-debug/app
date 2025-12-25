# Phase 1 - Step 22: Data Retention and Archival Policies (Planning-only)

## 1. Purpose and Scope

This step defines planning-only data retention, archival, and purge policies for Phase 1. It establishes how long planning data is retained, how archival affects accessibility, and under what conditions data may be purged, while preserving auditability and legal obligations.

This document is declarative. It does not mandate storage engines, backup systems, legal tooling, or automated purge jobs.

In scope:

* Retention periods by data category
* Archival semantics and access rules
* Purge policies and safeguards
* Legal hold behavior
* Export obligations prior to purge
* Error mapping aligned to Step 10

Out of scope:

* Jurisdiction-specific legal advice
* Encryption/key management
* Backup implementation details
* Operational disaster recovery procedures

## 2. Authority and Precedence

* Step 01 planning-as-source-of-truth: retention must not change planning meaning while data exists.
* Step 04 API contracts: access behavior reflects archival state.
* Step 08 audit: audit trail retention has special rules.
* Step 10 error taxonomy: access to purged data must map to problem details.
* Step 12 lifecycle: archived states are distinct from purged data.
* Step 17 export/import: exports support compliance prior to purge.
* Step 21 observability: retention affects logs/metrics correlation windows.

If retention durations or purge permissions require product/legal decisions, STOP and escalate to governance before proceeding.

## 3. Definitions

### 3.1 Retention

Retention is the period during which data is stored and accessible according to its access rules.

### 3.2 Archival

Archival is a reversible lifecycle state (Step 12) that limits default visibility and mutation but preserves data.

### 3.3 Purge (Deletion)

Purge is irreversible removal of data such that it is no longer retrievable via the system.

### 3.4 Legal Hold

A legal hold suspends purge for specified data due to legal, regulatory, or investigative requirements.

## 4. Data Categories

The following categories are recognized for Phase 1:

* Planning resources: organization, project, mission, assignment, collaborator
* Derived views and caches (Step 14)
* Audit events (Step 08)
* Import/export artifacts (Step 17)
* Observability data (logs, metrics, traces) (Step 21)

## 5. Retention Periods (Policy Placeholders)

Retention durations are product policy and may vary by tenant. Phase 1 defines categories and defaults as placeholders.

Retention defaults:

* Planning resources (active/archived): retain indefinitely until explicit purge is requested
* Audit events: retain indefinitely
* Import/export artifacts: retain for 90 days
* Derived caches: ephemeral; recomputable; no retention guarantee
* Observability data:

  * logs: 30 days
  * metrics: 180 days
  * traces: 7 days

## 6. Archival Semantics

### 6.1 Access Rules

When a resource is archived:

* It is excluded from default lists and aggregations.
* It remains readable when explicitly requested.
* Mutations are restricted according to Step 12.

Archival does not change retention clocks for purge eligibility unless policy specifies otherwise.

### 6.2 Cascade Considerations

Archiving a parent (e.g., project) implies children (missions, assignments) are effectively archived for access, but their data remains intact.

## 7. Purge Policy

### 7.1 Eligibility

A resource may be eligible for purge only if:

* It is archived.
* It has exceeded its retention period.
* It is not under legal hold.
* No dependent records require its presence for audit integrity (see 7.3).

### 7.2 Scope of Purge

Purge may apply to:

* Entire projects or organizations (policy-defined)
* Individual resources

Partial purge within a resource (field-level deletion) is out of scope.

### 7.3 Audit Integrity

Audit events MUST NOT be purged in a way that breaks referential meaning.

Options (policy-defined):

* Retain audit events with redacted resource payloads
* Replace purged resource references with tombstone identifiers (Phase 1 default; no silent reference deletion)

### 7.4 Irreversibility

Once purged:

* The resource cannot be restored.
* Importing the same external refs (Step 18) creates a new resource.

## 8. Legal Hold

### 8.1 Application

A legal hold may be applied to:

* organization scope
* project scope
* specific resources

### 8.2 Effects

When a legal hold is active:

* Purge operations MUST be blocked.
* Archival remains allowed unless policy forbids it.

### 8.3 Visibility

Legal hold status SHOULD be visible to authorized roles (Step 11), but details may be restricted.

## 9. Export Obligations Prior to Purge

Before purge, the system SHOULD allow:

* snapshot export (Step 17) of the affected scope
* confirmation that export has completed or been offered

Export is mandatory before purge; purge operations must be preceded by an offered or completed export for the affected scope.

## 10. Error Mapping (Step 10 Integration)

Retention and purge errors MUST map to Step 10 problem details.

Suggested semantic codes (must exist in Step 10 registry):

* planning.retention_not_expired
* planning.purge_not_allowed
* planning.legal_hold_active
* planning.resource_purged

Accessing purged data SHOULD result in a not-found or gone semantics as defined in Step 10.

## 11. Audit and Observability

* Archival actions MUST create audit events (Step 08).
* Purge actions MUST create a terminal audit event summarizing scope and timestamp.
* Observability events SHOULD record purge attempts and outcomes without exposing sensitive data.

## 12. Validation Checklist

Before implementation work proceeds:

* Retention categories and defaults are explicitly decided.
* Archival vs purge semantics are not conflated.
* Legal hold behavior is defined and blocks purge.
* Export obligations prior to purge are clarified.
* Error codes referenced here exist in Step 10 registry.
