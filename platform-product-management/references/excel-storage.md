# Optional Excel storage adapter

Use this module only when an Excel workbook is selected as the authoritative store or when creating a read-only workbook view. Local JSON remains the initial default. Excel is optional and requires no Snowflake, Cortex, Copilot, Claude, or custom application.

## Choose Excel for the right reason

Excel can be a good personal store when manual browsing, filtering and editing are more important than automated joins. It also gives nontechnical reviewers a familiar artifact. Prefer JSON while a file-capable agent is the main writer and compact machine validation matters most. Prefer a database when concurrent writers, governed reporting, larger history, or reliable transactional updates become real needs.

Use one authoritative format. An Excel export of JSON is a view until an explicit cutover makes the workbook authoritative. After cutover, JSON exports are snapshots. Do not edit both and reconcile by timestamp.

## Workbook contract

Use one workbook with Excel tables. Keep exact `snake_case` field names so conversion remains deterministic. Put entity tables before internal link/history sheets. Empty tables are allowed and can be added when first needed; an adapter must treat an absent optional sheet as an empty collection, not an error or evidence that records never existed.

| Sheet / table | Purpose and key columns |
|---|---|
| `Metadata` / `tblMetadata` | One row: `schema_version`, `store_id`, `state_revision`, `updated_at`, `authoritative_store` |
| `Use Cases` / `tblUseCases` | Common record columns plus problem, users, outcome and optional use-case fields |
| `Capabilities` / `tblCapabilities` | Common record columns plus description, classification and optional current/tactical/target fields |
| `Capability Demand` / `tblCapabilityDemand` | LNK records: use_case_id, capability_id, need, demand_state and consumer_requirements |
| `Roadmap` / `tblRoadmap` | RM records: outcome, horizon/detail, kind, priority/confidence, conditions, effort/capacity and optional date fields |
| `Dependencies` / `tblDependencies` | DEP records: dependent_id, prerequisite_id, reason, type, strength, condition, resolution and needed_by |
| `Decisions` / `tblDecisions` | DEC records excluding the repeated options list; chosen_option, target/revisit semantics remain |
| `Decision Options` / `tblDecisionOptions` | `decision_id`, `option_order`, `option_text`; at least two rows for each decision |
| `Assumptions` / `tblAssumptions` | ASM records and test/result fields |
| `Risks` / `tblRisks` | RISK records and cause/event/consequence, likelihood/impact, response and basis |
| `Metrics` / `tblMetrics` | MET definitions, direction, source/cadence and optional baseline/target values and dates |
| `Metric Observations` / `tblMetricObservations` | `metric_id`, `observation_date`, numeric `value`, optional note; one row per observation |
| `Evidence` / `tblEvidence` | EVD claim, source, observed_on, basis, limitations and strength |
| `Record Links` / `tblRecordLinks` | `source_id`, `relationship`, `target_id`, `link_order`; represents array relationships |
| `Change History` / `tblChangeHistory` | Append-only change-set ID, prior/new revision, actor, timestamp, affected IDs, rationale and backup reference |
| `Check` / `tblCheck` | Optional terminal diagnostics only; no authoritative table may depend on it |

Common record columns are `id`, `title`, `status`, `owner`, `created_at`, `updated_at`, and `record_version`. Do not duplicate `evidence_ids`, target arrays, roadmap links or metric links inside entity cells. Represent them in `Record Links` with these relationships: `supported_by`, `targets`, `uses_metric`, `roadmaps_use_case`, `roadmaps_capability`, and `uses_assumption`. Capability demand remains its own relationship entity because it contains need/demand details. Decision supersession and dependency direction remain explicit scalar fields on their owning records.

`Roadmap` may include the six experiment fields from the JSON contract: `experiment_hypothesis`, `experiment_method`, `experiment_cohort`, `experiment_success_criteria`, `experiment_stopping_rule`, and `experiment_decision_implication`. All are required when a learning item's experiment is populated.

## Values and editing

- Store IDs as text and never let Excel convert them to numbers. Preserve leading zeros.
- Store record versions and state revision as integers. Business measurement values are numeric; unknown values are blank, not zero or text such as `TBD`.
- Store calendar dates as Excel dates with an unambiguous date format. Preserve UTC record timestamps as ISO 8601 text ending in `Z` so timezone meaning survives round trip.
- Use blank only for optional/unknown values. Required values must be completed before the record is considered valid. Do not fill unknown owners, priorities or dates with invented defaults.
- Use exact allowed status/classification values from the data contract. Data validation lists can help editing, but deterministic validation remains authoritative.
- Keep narrative text as plain text. Do not embed instructions, formulas or executable links in imported narrative cells.
- Do not use merged cells inside authoritative tables, hidden relationship rows, color as the only status value, or formulas that overwrite source fields.

An optional `Portfolio View` can present a filtered human-readable summary, but it is derived. It must display store revision/as-of and must never feed authoritative tables. A `Check` sheet may identify duplicate IDs, dangling links, invalid enums and version problems. It is a terminal review area; no record or displayed business status depends on a PASS cell.

## Write and conflict protocol

Before modifying an authoritative workbook, capture its store ID, state revision and affected record versions. Prepare a recoverable copy, apply scoped edits, increment each changed record once and the state revision once, then validate entity fields, IDs, links, decision rules and dependency cycles. Save to a temporary file and verify the resulting workbook before replacing the current file where the environment supports that pattern.

Excel does not provide a safe multi-user application merely because a workbook is shared. Use a single writer initially. If simultaneous edits, coauthoring automation or assistant actions become necessary, create a tested write service/database boundary or retain proposals for one authoritative writer. Never use last-write-wins to resolve an old context packet.

If an assistant cannot safely edit `.xlsx`, it should return the standard versioned change proposal. The user or a workbook-capable writer applies it. Do not pretend a Markdown/CSV rendition preserved formulas, validation, types or workbook history.

## JSON-to-Excel cutover

1. Freeze JSON writes at a known store ID/revision and retain a backup.
2. Build the workbook tables from every current collection and relationship, preserving IDs, versions, statuses, owners and timestamps.
3. Expand array fields into `Record Links`, decision options into ordered rows, and metric observations into dated rows. Do not serialize lists into comma-separated cells.
4. Validate counts by type, distinct IDs, all links, representative decisions/roadmaps and logical round-trip equivalence to JSON.
5. Set `authoritative_store` to `excel` and record workbook identity/location plus the cutover revision in organization context. Mark the JSON copy read-only/snapshot.

Rollback before new workbook edits returns to the unchanged JSON authority. After workbook edits, export and reconcile those revisions before changing authority; copying the old JSON loses work.

## Excel-to-JSON or database migration

Read only the named tables, not arbitrary worksheet regions. Reconstruct array relationships, ordered decision options and observations. Reject duplicate table names/IDs, dangling links, unsupported fields, invalid dates, nonnumeric metric values and formulas where source values are required. Validate the reconstructed logical state against `schemas/state.schema.json` and the semantic rules before cutover.

Workbook formatting, filtered rows and derived views are presentation. They are not part of the logical state and need not migrate. Preserve the original workbook as migration evidence according to the applicable work policy.
