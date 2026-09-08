# Optional lightweight PM tool — UI specification

Status: design brief for a future requested build. This is separate from the operational skill and is not a deployed application. Build only views that solve demonstrated recurring friction. Framework, hosting and integration choices remain open until the work environment and requested scope are known.

## Product intent and user

Primary user: a portfolio manager coordinating investment, reuse and production decisions across several teams. The tool should make the authoritative state easier to inspect, compare and update, while preserving the skill's decision semantics. Success is less repeated preparation, faster access to rationale and fewer reconciliation errors, not a larger dashboard.

A useful first build is a read-only portfolio/roadmap view plus record detail and a context-packet export. Add editing only when the user asks and the write/validation boundary exists. A conversational assistant remains optional; deterministic browsing, filtering and exports must work without an LLM call.

## Information architecture

```text
Workspace
  Overview / review queue
  Portfolio → Use-case detail
  Capabilities → Capability detail / consumer comparison
  Roadmap → Item detail
  Decisions & issues → Record detail / history
  Views & export → Scope preview / context packet
```

Desktop-first, responsive for reading on smaller screens. Persistent context: workspace/store, source revision/as-of, active filters and data freshness. Distinguish derived views from editable fields. Default selection should be useful with ten records and scale through filtering rather than loading thousands into a giant grid.

## Screen specifications

| View | User job / content | Actions if in scope | Data source |
|---|---|---|---|
| Overview / review queue | See meaningful changes, unresolved decisions, confirmed blockers, fired revisit triggers, unknown/stale evidence requiring attention | Open record, filter review scope, export review packet | Current records and history; trigger checks must explain basis |
| Portfolio | Compare use cases by outcome, lifecycle, owner, evidence/readiness and linked roadmap horizon | Filter/search, compare selected investments, open intake/detail | USE_CASES, links, roadmap, metrics, decisions/risks |
| Use-case detail | Understand problem, users, outcome, source evidence, capability needs, dependencies, current decisions and value | View sources/history, propose edits, create linked record | UC plus related records; never duplicate shared capability status |
| Capabilities | See consumer demand, classification, maturity, support ownership and reuse choices | Compare consumer requirements, inspect target/tactical state | CAP and demand links; separate hypothesized, confirmed and adopted demand |
| Capability detail | Evaluate shared contract, current/tactical/target, adoption, economics and service health | Open consumer comparison, decision/history, propose reclassification | CAP, LNK, MET, DEP, DEC, RISK |
| Roadmap | Understand outcome/capability/learning investments across Now/Next/Later | Filter by scope/owner/kind; inspect conditions; propose horizon move | RM plus links and relevant blockers/decisions |
| Decisions & issues | Find pending choices, provisional revisits, accepted exposures and decision history | Open memo, propose adoption/supersession/response | DEC, ASM, RISK and evidence |
| Views & export | Produce an executive view or assistant context packet with provenance | Preview, choose scope, export; no implicit external sending | Deterministic projection of selected current state |

## Core interactions

Intake: start with problem, users and intended outcome. Show optional fields progressively. Search existing use cases/capabilities before creating duplicates. Saving a draft cannot label it approved/funded. Surface unknown owner/evidence as unresolved, not as fabricated defaults.

Capability comparison: select consumers and show common/unique contract, source/access, quality and support differences side by side. A demand count is descriptive, not a platformization score. Show actual adopted consumers separately. A shared classification change should include rationale and ownership/readiness implications.

Dependency inspection: show “A requires B” with confirmation, strength, reason and satisfaction condition. A small graph is optional; the accessible dependency table remains available. Highlight cycles and unresolved prerequisites without treating soft/hypothesized edges as hard facts.

Roadmap move: dragging an item, if implemented, creates a proposed field change. Display old/new horizon, affected dependencies, capacity assumption and any commitment implications. Apply within the user's editing authority using version checks; never alter dates or unrelated sequence automatically. Provide keyboard controls equivalent to drag.

Decision update: proposed → adopted requires actual owner/authority, chosen option and date. Provisional choices require a revisit trigger. Changing an adopted rationale creates a new superseding decision when the choice changes; edit history preserves corrections. The UI must not treat a model recommendation as approval.

Export: preview scope, source revision, counts and known exclusions. Include linked material dependencies/risks/evidence or explicitly list omitted references. Label a filtered export partial. Downloading is separate from sending to Copilot or publishing externally.

## Edit and history behavior

Use a single validation/write boundary shared by UI, CLI and future assistant actions. On save show the affected record/field diff, not a whole-state JSON wall. Allow ordinary scoped edits under the user's established authority without a redundant confirmation dialog for every field. Material business decisions need their authority represented; destructive or externally consequential operations follow actual permissions.

On version conflict, preserve the user's draft, show current and proposed values and require reconciliation. Do not silently apply last-write-wins. On a failed write, preserve draft and explain whether anything was saved. A retry uses a stable change-set identity to prevent duplicates. History shows who/when/why, old/new versions, and linked decision/source; a view-only role cannot mutate state.

## Visual and accessibility direction

Use a restrained, readable workspace with a neutral background, clear headings, comfortable text density, and a single accent for primary actions. Status chips always include text. Distinguish “unknown,” “not applicable,” “no matching records,” and “failed to load.” Avoid decorative analytics, traffic lights without defined criteria, and dashboard numbers unsupported by data.

Tables need clear headers, keyboard navigation, visible focus, accessible labels and readable contrast. Forms need associated labels and field-level errors with a summary. Do not rely on hover or color to reveal critical meaning. Support reduced motion, text resizing and an accessible alternative for graphs. Specific conformance targets should be set against actual organizational requirements at build time.

## Empty, partial, loading and error states

- Empty live store: explain there are no records and offer “Capture first use case,” not fictional demo data presented as work facts.
- Filter has no matches: retain filters and offer clear/reset; do not suggest the portfolio is empty.
- Partial context: show scope exclusions and offer to include related records where permitted.
- Unknown value: render “Unknown”; distinguish absent baseline from numerical zero.
- Loading: preserve context and avoid displaying stale figures as current. On refresh failure, label the last available snapshot and its as-of.
- Authorization denied: preserve current read state and explain unavailable action without requesting credentials in the UI.
- Conflict/write failure: retain draft and report saved/not-saved status accurately.

## Acceptance scenarios

1. Given three candidate consumer links but no adopted demand, the capability view reports zero confirmed actual adopters and labels the candidates correctly; it does not call the service a proven platform.
2. Given a forecast date, an executive export retains its forecast meaning and source; moving a horizon cannot create a commitment.
3. Given a hypothesized hard dependency, the roadmap distinguishes it from a confirmed blocker. Given a confirmed cycle, sequence generation returns the cycle instead of a valid ordering.
4. Given a filtered portfolio, exports state the filters and unresolved out-of-scope links. Two views of a shared investment do not double count it in a rollup.
5. Given a stale record version, a save preserves the draft, refuses silent overwrite and offers field-level reconciliation.
6. Given an adopted decision that changes, the old rationale remains accessible and the successor links back to it.
7. Given a missing metric baseline, the UI shows Unknown and makes no percentage-improvement calculation. Given an actual zero baseline, it avoids undefined percent-change claims.
8. Given an inaccessible evidence link, the claim is not labeled verified; source location and access limitation remain visible.
9. Given a failed save or timeout, the UI reports the actual known outcome and supports checking change-set status before retry.
10. A keyboard-only user can filter, open a record, propose a horizon change and cancel/save within their authority without drag or hover.
11. Read-only browsing/filtering/export works with all model calls disabled. No record is sent to an external assistant as a side effect of opening a page.
12. A fresh user can complete one intake-to-roadmap review loop without constructing a database schema or filling every optional field.

## What to decide at build time

Confirm the first workflow, user count, authoritative store, installed runtime, authentication/role needs and allowed deployment location. Start from the existing schema and sample fixtures. Pick the smallest supported framework for that environment; this specification does not require a new platform, hosted service, plugin or frontend stack.
