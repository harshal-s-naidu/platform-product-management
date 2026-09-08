# Platform Product Management — start here

Package version: 1.0.1. Methodology and data contract version: 1.0.0.

This is a complete conversational operating system for an AI Portfolio Manager with a platform product-management focus. Use it to run intake, discovery, strategy, investment choices, capability reuse, sequencing, roadmaps, decisions, production-readiness conversations, value measurement, and recurring reviews. No application, database, or custom agent is required to begin.

## Your first session with a file-capable assistant

1. Copy this entire folder into an approved work location and open it in VS Code. Keep internal information inside your work environment.
2. Give your assistant this prompt, using its file attachment or workspace reference feature if necessary:

   > Read CLAUDE.md and SKILL.md in this folder. Use this platform product-management system for my work. Start with onboarding, then help me capture my first use case. Keep data/state.json as the initial source of truth. Do not build an application, workbook, or database yet. Ask only for context needed for the next useful decision.

3. The agent should read the onboarding section in references/operating-model.md, create `context/organization.md` from the supplied template, and populate `data/state.json` as you supply facts. Unknowns remain explicit. You do not need to complete every template or field to start.
4. Ask for a useful output immediately: “Assess this use case, identify reusable capabilities and unresolved dependencies, and recommend its next step.”
5. When you want records updated, say so: “Save this intake and the agreed decision.” Analysis alone produces proposed changes. An explicit save/update instruction authorizes the scoped update; no repeated approval ceremony is needed.

Explicitly asking the agent to read these files is the portable fallback. `CLAUDE.md` is a bootstrap file, not a promise of automatic discovery by every model or editor. Optional host-specific setup is described in [references/tool-adapters.md](references/tool-adapters.md).

## Your first session in Copilot web

Paste [COPILOT_SKILL.md](COPILOT_SKILL.md) into a new conversation, or attach it and explicitly ask Copilot to use it as instructions. Add your relevant work context, then ask the task in plain language. For deeper work, attach the relevant reference module from the routing table. If managing several attachments is awkward, [COPILOT_COMPLETE.md](COPILOT_COMPLETE.md) is a self-contained, larger reference edition. You need only one edition at a time.

Example opening:

> Use the attached platform product-management instructions. Assess the use cases in this context packet and recommend Now / Next / Later. Distinguish confirmed constraints from assumptions. Show tradeoffs and proposed record changes. Do not invent owners, dates, benefits, or dependencies.

Copilot's replies are proposals until saved to your authoritative records. At the end, ask: “Produce a handoff using the change-proposal template, retaining the source snapshot ID and record versions.” Give that handoff to your authoritative writer to reconcile and apply. If you have no file tools in a session, copying the revised records into your work files manually is sufficient; verify the changes before replacing the state.

## What to read and when

| File | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Shared runtime instructions and task routing; main entry point |
| [CLAUDE.md](CLAUDE.md) | Workspace behavior for Claude or another file-capable assistant |
| [COPILOT_SKILL.md](COPILOT_SKILL.md) | Compact, usable Copilot instructions |
| [DESIGN_REVIEW.md](DESIGN_REVIEW.md) | Independent assessment and architecture decisions |
| [MASTER_SPECIFICATION.md](MASTER_SPECIFICATION.md) | Full assembled specification for offline review; not routine context |
| [references/operating-model.md](references/operating-model.md) | Onboarding, responsibilities, strategy and operating practice |
| [references/workflows.md](references/workflows.md) | Task inputs, methods, outputs and applicability |
| [references/capabilities-and-target-state.md](references/capabilities-and-target-state.md) | Reuse, platformization, build/buy and tactical choices |
| [references/prioritization-and-roadmaps.md](references/prioritization-and-roadmaps.md) | Investment, capacity, sequencing and roadmap rules |
| [references/decisions-evidence-and-value.md](references/decisions-evidence-and-value.md) | Decisions, risks, assumptions, experiments and measurement |
| [references/reviews-and-communication.md](references/reviews-and-communication.md) | Review cadence and executive outputs |
| [references/data-contract.md](references/data-contract.md) | Record definitions, relationships and state transitions |
| [references/persistence-and-handoffs.md](references/persistence-and-handoffs.md) | Saving, history, Copilot handoff, Snowflake migration |
| [references/excel-storage.md](references/excel-storage.md) | Optional Excel workbook mapping and cutover rules |
| [references/context-policy.md](references/context-policy.md) | Selective loading, continuity and credit discipline |
| [templates/work-products.md](templates/work-products.md) | Copyable PM outputs and change proposals |
| [examples/worked-examples.md](examples/worked-examples.md) | Five connected, fictional operating examples |
| [optional/UI_SPECIFICATION.md](optional/UI_SPECIFICATION.md) | Future lightweight tool views and acceptance criteria |
| [optional/BUILDER_BRIEF.md](optional/BUILDER_BRIEF.md) | Instructions for asking Claude to build tools later |

## Starting records and upkeep

`data/state.json` is intentionally empty. It is the initial canonical state. You may later cut over to an Excel workbook using [references/excel-storage.md](references/excel-storage.md), or to another supported store. Keep only one writable authority. The fictional dataset in `examples/sample-state.json` is separate and must never be merged into real work automatically. `context/organization.template.md` contains blank configuration prompts, not organizational facts.

Use one writer initially. Keep a dated backup before replacing state. Read [persistence and handoffs](references/persistence-and-handoffs.md) before the first save. The included validator is optional operational support, not a prerequisite application:

```sh
python3 scripts/validate_state.py data/state.json
```

It uses the Python standard library, validates this package's schema subset and cross-record relationships, and reports readiness warnings. It does not establish business truth or certify organizational approval.

Useful recurring requests:

- “Review what's changed since the last portfolio review. What should I act on this week?”
- “Compare these investment options under the capacity available. Show what gets displaced.”
- “Challenge this proposed shared capability. What evidence would justify platformizing it?”
- “The target service is delayed. Recommend a production path and a revisit trigger.”
- “Create an executive roadmap from the current state, including uncertainty and decisions required.”
- “Measure whether this production use case and its shared capabilities are delivering value.”

## What is included versus deferred

The full methodology, portable instructions, data contract, starter records, templates, examples, JSON/Excel/Snowflake storage guidance, and UI specification are included. There is no deployed UI, live workbook, database connection, production table creation, background scheduler, external-system integration, or live work data. Those are later implementation choices, not missing requirements for conversational use.

See [VALIDATION.md](VALIDATION.md) for checks performed and practical limits. Preserve your filled work context and records when upgrading the portable methodology.
