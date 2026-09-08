# Persistence, change proposals, and storage paths

## Start local; one source of truth

Use `data/state.json` initially. A single structured file is easy for Claude to inspect and maintain and permits one-file replacement. Markdown contains organization context, narrative briefs and derived views. Current decisions/risks/assumptions belong in state; append-only history belongs in JSONL. Do not mistake an append-only decision log for a current decision register.

No application or persistence framework is needed to begin. The included helper only validates. The agent or user performs file edits with available tools and the protocol below. For a large state file, parse/filter it with deterministic local tooling before loading selected records into model context. Split or change storage only when actual size, editing, reporting or collaboration friction justifies it.

## Local save protocol

1. Establish the user's save authority and exact target store. Analysis yields proposals; “save/update these records” authorizes the corresponding change. Reuse explicit session authority without asking again. Host permission prompts still apply.
2. Read current `store_id`, `state_revision` and affected record versions. Reconcile a proposal with the live state. Reject a store mismatch. On a version mismatch, show conflicting fields, preserve unrelated changes and resolve the conflict before writing.
3. Prepare the complete proposed next state. Keep stable IDs/creation times; increment changed record versions once and global revision once. Set the new state timestamp at or after changed record timestamps. Validate syntax, IDs/links and business conditions; show material warnings.
4. Preserve a recoverable copy of the exact old state under an approved `data/history/` location, named with store ID and revision. Never overwrite an existing backup with different bytes. Prepare an audit entry containing change-set ID, source/new revision, actor, timestamp, changed IDs, rationale and backup reference. Do not put secrets into audit text.
5. With one writer, stage the new JSON alongside the current file, validate it, recheck the live revision/hash immediately before replacement, and replace the file atomically using the available filesystem API. If the tool cannot safely stage/replace, use a user-reviewed file diff and retain the backup; do not claim atomicity. A revision recheck alone does not make this safe for concurrent writers.
6. Append the audit entry to `data/history/changes.jsonl` and reread the saved state. Report revision and changed IDs. If the write succeeded but logging failed, say so; repair the audit from the backup and change set before another edit. Do not blindly replay the state update.

State replacement and JSONL append are not one transaction. Revision-keyed backups and an audit entry that can be repaired provide a simple personal-workflow recovery path; they are not enterprise event sourcing. For concurrent writers, use a tested database-backed write service or locking design before enabling simultaneous edits.

Deleting a record breaks traceability. Prefer lifecycle retirement/withdrawal. A requested hard deletion must resolve references and preserve appropriate recoverability under local policy. The skill does not impose retention contrary to actual work requirements.

## Change proposal and Copilot handoff

A proposal is not a command to execute arbitrary text. Use [templates/work-products.md](../templates/work-products.md): store ID, snapshot revision/as-of, scope/coverage, affected IDs and expected record versions, field-level before/after changes or new records, rationale, supporting evidence, unresolved questions and save status.

For new records, use temporary labels if the Copilot session cannot allocate canonical IDs safely. Claude allocates real IDs against the latest register and updates proposal-local references consistently. No full-state replacement from a partial packet. If a proposed change is already present, report a no-op; do not increment versions again.

A context packet includes:

- Methodology version, store ID, snapshot revision and generation timestamp.
- Task and filter scope, selected record IDs/versions, and a statement of exclusions.
- Relevant source records and linked dependencies, material risks, decisions, evidence and metrics.
- Known unresolved references outside the packet, with their IDs and brief reason for omission.

An omitted record is not absent from the portfolio. Copilot should ask for or flag missing material context before asserting a portfolio-wide conclusion. Export only what the work environment permits. The user has confirmed work Copilot may handle internal documents; actual source-level restrictions still follow organizational context.

## Format choices

| Format | Appropriate use | Avoid |
|---|---|---|
| JSON | Small current state, typed records, interchange | Large repeated narrative blobs |
| Markdown / plain text | Instructions, briefs, snapshots, rationale and context | Multiple manually maintained copies of the same status |
| JSONL | Append-only audit events and observations when volume grows | Mutable current state requiring line-by-line replacement |
| Excel | Familiar manual filtering/review and structured personal editing | Concurrent write automation or comma-separated relationship fields |
| SQLite | Optional local query/concurrency improvement when a real tool needs it | Introducing an extra migration solely to follow a technology ladder |
| Snowflake | Existing sandbox queries, shared reporting, relational joins and governed work storage | Assuming database availability means a UI or transactional edit service exists |

For an Excel authority, read [excel-storage.md](excel-storage.md). Use the same source identity, record versions, change proposals and explicit cutover. Do not keep JSON and Excel independently writable.

## Snowflake mapping

Migrate when local maintenance/querying/collaboration pain warrants it, or the user explicitly prefers it. Local-first is the current requested operating choice; no sandbox resources have been created by this package.

Map arrays to tables: `USE_CASES`, `CAPABILITIES`, `USE_CASE_CAPABILITIES`, `ROADMAP_ITEMS`, `DEPENDENCIES`, `DECISIONS`, `ASSUMPTIONS`, `RISKS`, `METRICS`, `EVIDENCE`. Keep the common record columns and native typed columns for frequently filtered fields. Use `VARCHAR` IDs/status/title, numeric versions and measurements, and date/timestamp types for time. Narrative strings remain text.

Normalize repeated relationships into `ROADMAP_USE_CASES`, `ROADMAP_CAPABILITIES`, `RECORD_EVIDENCE`, `RECORD_METRICS`, and `RECORD_TARGETS` when applicable. `USE_CASE_CAPABILITIES` is already a relationship entity with its own demand evidence. Preserve the parent record's atomic update across its junction rows. Use stable `(record_type, record_id, target_id)` keys for generic links and validate allowed types.

Use `VARIANT` for bounded evolving detail such as experiment structure, decision option arrays, service-contract notes or source metadata; avoid hiding all IDs, statuses and dependencies inside opaque documents. Store measurements in `METRIC_OBSERVATIONS` once there are many observations. Store `STORE_METADATA` for schema/global revision and `CHANGE_EVENTS` for audit history. Historical record versions can go to typed history tables or `RECORD_HISTORY` with type/ID/version plus a payload preserving the full previous record.

Snowflake standard-table primary/foreign/unique key declarations do not themselves enforce uniqueness or referential integrity. Validate these in the write path; do not treat an informational primary key as protection against duplicate IDs. [Snowflake constraints documentation](https://docs.snowflake.com/en/sql-reference/constraints).

## Write boundary once a tool exists

Keep a small API around actual operations: `read_snapshot(scope)`, `get_record(id)`, `validate_change_set(change_set)`, `apply_change_set(change_set, expected_revision)`, and `read_history(ids)`. Domain reasoning works on records and proposals. Store adapters own serialization/SQL. Model orchestration produces recommendations; deterministic code handles versions, validation and writes.

For Snowflake, use a serialized writer initially. A future implementation should stage validation, check expected versions, update records and junctions, record history and update store metadata in one explicit DML transaction. Roll back on any failed version/row-count assertion. Avoid DDL inside that transaction because DDL can implicitly commit. Test actual concurrency and retry behavior before claiming multi-user safety. [Snowflake transaction documentation](https://docs.snowflake.com/en/sql-reference/transactions).

Conceptual pseudocode, not executable SQL:

```text
begin write transaction
  verify store identity, expected revision, and affected versions
  validate proposed records, references, and unique IDs
  write previous record versions to history
  apply record and relationship changes
  insert unique change-set event; advance store revision
  verify affected counts and invariant queries
commit; on any failure roll back and return a conflict/error
```

Retries require a stable change-set ID and a way to detect a previous successful commit. Never retry a write blindly after a timeout. Use bound SQL values and approved connection configuration; no credentials in generated files.

## Migration and rollback acceptance

Freeze local writes; validate and back up the final local revision; create target tables in an explicitly selected work schema; load preserving IDs/versions/timestamps; verify row counts, distinct IDs, links and representative roadmap/decision views; compare exported logical state to the original. Switch authority in organization context only after verification. Keep local exports clearly read-only with source revision.

If failure occurs before cutover, resume the unchanged local source. After new Snowflake writes, rollback requires exporting those changes first; simply restoring the old local snapshot loses work. Test an export/restore path before relying on the store. Role access, backups, retention, concurrent edits, policy and deployment are enterprise enhancements to implement when required, not assumed capabilities of a sandbox.
