# Tool adapters and compatibility

Documentation checked during package preparation on 2026-09-07. Tenant rollout, permissions and installed extensions can differ. These are integration notes, not requirements to install or buy anything.

## File-capable coding assistants

Keep model identity separate from host behavior. The portable setup is to open the package folder and explicitly attach or read `CLAUDE.md` and `SKILL.md`. Verify whether the session can read/edit files, run validation, or work with spreadsheets/databases before relying on those actions. The core methodology needs none of those tools for conversational analysis.

If the host supports native skills, register the complete folder while keeping relative references intact. Native discovery is a convenience. Explicit file loading remains the compatibility fallback. Do not make another independently maintained copy of live records.

If the host is Claude Code, its skill mechanism supports `SKILL.md` folders. Follow the installed host's current configuration rather than assuming a model name determines discovery. [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

## Optional Snowflake Cortex / CoCo host

If using Snowflake's CoCo extension, its documentation describes workspace references using `@`, file/SQL tools, and skills discoverable through `/`. Verify the installed interface and permissions before relying on them. [Snowflake VS Code documentation](https://docs.snowflake.com/en/user-guide/vscode-ext).

Snowflake's developer guide describes workspace custom skills under `.cortex/skills/`. If supported in the installed environment, register/copy the portable package there, keeping relative references intact, then verify discovery. Keep the live store in one explicitly configured location. [Snowflake CoCo VS Code guide](https://www.snowflake.com/en/developers/guides/get-started-coco-vscode-extension/).

`CLAUDE.md` remains an explicit bootstrap file; automatic support is not assumed for Cortex. Cortex, SQL and Snowflake tables are optional. Using a Claude model through Cortex does not require the PM records to live in Snowflake.

A useful setup verification prompt:

> Read the supplied entry-point files and tell me the authoritative store, the module you would load for a platformization decision, and whether this session can read and update workspace files. Do not change records or create tools during this check.

Correct behavior: local JSON state initially; capability/target-state module; tool capabilities honestly reported from the session. This checks loading without starting a large build.

## Microsoft Copilot web

Use `COPILOT_SKILL.md` as explicitly supplied instructions and a selected context packet as facts. Add relevant modules for depth or use `COPILOT_COMPLETE.md` as the full reference edition. Neither file format implies native skills, persistent memory, workspace access, Excel editing or a database connection.

Microsoft documents file support for its Copilot products, with experience-specific differences. Use the work tenant's supported format; if Markdown upload is unavailable, paste the compact instructions or supply the plain-text edition. Do not assume consumer upload limits apply to a work account. [Microsoft file-format documentation](https://support.microsoft.com/en-us/microsoft-365-copilot/file-formats-supported-by-microsoft-365-copilot).

Use work-approved context. At session end, request a versioned change proposal or executive output. Hand proposals to the authoritative writer. Generated reports and old attachments remain snapshots, not live records.

## Microsoft 365 Copilot / Copilot Studio later

When available, assess the actual need: easier discovery of work documents, persistent instruction distribution, controlled actions, or a shared user interface. Retain the domain model and methodology. Add retrieval/action adapters only for confirmed capabilities and a requested workflow. Require citations/as-of and version checks at the action boundary. Do not assume a future license or agent has access to Snowflake or can safely reconcile updates.

## Optional storage and usage tools

Local JSON is the default. Excel is a supported alternative using [excel-storage.md](excel-storage.md); a database is a later option. An assistant may work with any store only when the host actually provides the necessary access and the store has been selected as authoritative.

Ordinary state validation and local filtering need no LLM call. Use approved connections for SQL and keep credentials outside the package. This package neither calls a model nor measures usage. Configure any later usage reporting against the actual service used; do not treat a credit allowance as a model-independent token budget.
