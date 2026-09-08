# Context, continuity, and usage discipline

This method works in conversational assistants with pasted files and in file-capable coding agents. Available tools, context limits and usage allowances belong in organization context. An allowance is not a reliable conversion to prompts or tokens; actual consumption depends on the configured service/model and workload. Do not invent a cost forecast.

## Loading policy

| Load tier | Content | Guidance |
|---|---|---|
| Entry | SKILL.md plus the active adapter | Load once at session/task entry where the host permits; avoid repeating identical text in each prompt |
| Working context | Small relevant slice of organization context and task scope | Keep actual facts with source/as-of; do not load all internal documents |
| Task method | Workflow contract plus one or two relevant reference modules | Expand when the task crosses domains; completeness matters more than an arbitrary token ceiling |
| Current state | Relevant records and linked blockers, decisions, risks, assumptions, evidence and metrics | Query/filter before sending; include material cross-scope dependencies |
| History | Decisions or observations relevant to a changed premise | Retrieve by IDs, dates and revisit triggers |
| Rare | Full master specification, all examples, schema, UI/builder docs | Load for design review, record validation, training, or requested implementation only |

Budget goals, not hard limits: runtime entry roughly 1,000–2,000 tokens; each focused method module usually 600–1,500; task facts sized to the actual question. Copilot's compact edition includes enough method to work alone and can be somewhat larger. Token estimates are approximate and model-dependent. Structure eliminates repetition and supports retrieval; JSON is not intrinsically smaller than concise prose.

## Retrieval procedure

1. Identify task, scope and relevant IDs from user input or a small index/list query.
2. Read selected records and expand to linked capabilities/use cases, active prerequisites, material risks, affected decisions and supporting evidence/metrics.
3. For portfolio questions, inspect the complete relevant candidate set or clearly label the comparison partial. Do not select only previously favored records and call the result a portfolio ranking.
4. Retrieve source excerpts sufficient to evaluate key claims; source links alone do not prove their contents.
5. Emit only needed fields with ID, version and provenance. For integrity checks, deterministic code may read the full state without printing it to the model.

## Session memory

At the end of substantial work, maintain a short `context/session-handoff.md` if the user authorized saving. Include task, source store/revision, decisions saved, proposals pending, unresolved facts and next action. It is a navigation aid, not a second authoritative state. On resume, reread current state before relying on old handoff facts.

If the host offers persistent instructions/skills, use its verified mechanism. Do not promise persistent model memory. If a file isn't loaded or accessible, say so and use the compact principles with the available facts. Copilot can use an explicitly supplied instruction block and context without native skill registration.

## Usage discipline

Avoid reading the master at each turn, replaying whole chats, generating every mode output, repeatedly rewriting unchanged files, or calling a model to compute deterministic counts. Batch related PM questions when they share context. Use Python/SQL for filtering, validation, counts and relationship checks when available. Do not launch background model loops, embeddings, auto-summarization jobs or delegated agents just because the package exists.

After a representative week, compare actual usage, review-preparation effort and output quality. Adjust context breadth before reducing substantive reasoning on important choices. An optional usage log can record session purpose and observed consumption; do not create an additional tracking burden unless it helps manage a real allowance.

## Methodology updates

Edit canonical reference modules and entry points, increment the package version for meaningful changes, then regenerate assembled editions with `scripts/build_editions.py`. That script uses an explicit allowlist and excludes real work context/state/history. Never re-export the whole working folder as a portable public methodology after it contains internal facts. Upgrades preserve work records; schema changes require explicit migration.
