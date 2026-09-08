# Decisions, evidence, risks, assumptions, and value

## Decision records

Record choices whose rationale matters later: investment/stop, platformization, build/buy/reuse, tactical exception, target-state change, material sequencing or accepted risk. Routine wording changes need only revision history.

A useful decision contains context, question, considered options (including do nothing when relevant), chosen option or proposal, rationale, evidence, assumptions, consequences, owner/authority, reversibility, date if adopted, affected IDs and revisit trigger. Distinguish `proposed`, `adopted`, `superseded` and `withdrawn`. An adopted decision can be provisional; set `provisional: true` and define its revisit trigger.

Do not mark a recommendation adopted unless an authorized person actually made the choice. Preserve the original rationale when new evidence leads to a different decision. Create a successor decision, link `supersedes_id`, and update the old decision's status/version. Reopening a decision is justified by a trigger or changed premise, not by the assistant preferring different phrasing.

## Evidence and uncertainty

Evidence is a traceable observation or source supporting a bounded claim. Capture source location, observed date, claim, relevant scope, strength/limitations and affected records. Distinguish:

- Direct observation: measured or observed in a defined context.
- Reported statement: user or stakeholder account; useful but not independent verification.
- Inference: interpretation from supplied facts; label it as such.

Avoid a rigid evidence ladder: an interview may be strong evidence of a workflow problem and weak evidence of achievable savings. Reliability depends on the claim. Do not call an inaccessible document verified; record it as a supplied reference with an access limitation. Record contradictory evidence and freshness explicitly.

Use assumptions for testable propositions that materially affect choices. Each has a statement, owner if known, test/revisit trigger, linked evidence, impact if false, and status (`open`, `validated`, `invalidated`, `retired`). “Validated” is bounded by the test and date; it does not imply universal truth. Embed minor assumptions in the relevant rationale instead of filling the register.

## Risks and issues

Frame risk as cause → uncertain event → consequence. Record likelihood, impact, exposure, response, owner, trigger and affected work. Use `unknown` when severity cannot be assessed. Avoid meaningless multiplied scores based on arbitrary labels.

An issue has already occurred; use `kind: issue` within the same risk register. Responses include mitigate, avoid, transfer/share where feasible, or accept by the appropriate owner. An assistant may recommend acceptance; it cannot invent an authorized acceptance. `accepted` requires an owner and rationale; `closed` requires a closure basis. Unowned risks remain visible.

Review tactical debt, unsupported dependencies, model/data changes, consumer adoption, operating ownership and platform bottlenecks when relevant. Do not create a universal enterprise-policy checklist; derive actual requirements from organization sources and responsible owners.

## Measurement design

Separate four layers:

| Layer | Example measure | Interpretation limit |
|---|---|---|
| Business outcome | Time to resolve a case, quality-adjusted throughput, avoided loss | Needs baseline, scope and attribution |
| User adoption / experience | Eligible users using the workflow, successful completion, satisfaction | Activity alone is not business value |
| Capability / platform health | Onboarding effort, successful consumers, latency, reliability | More consumers may increase support cost |
| Economics / controls | Cost per successful task, incident burden, material error rate | Cost reduction can trade off quality or risk |

Each metric needs a definition/formula, unit, source, cadence, direction, owner if known, and baseline/target/current values with dates when available. Do not enter zero for unknown. Record denominator and cohort for rates. Targets should have a basis or be labeled proposed. Keep observations dated so current values do not erase learning history.

For savings, distinguish capacity released from realized financial benefit. For revenue, avoid attributing all growth to the AI use case without a comparison. For a shared capability, avoid summing duplicated savings across consumers and the platform. Where causality is uncertain, report observed association and the evidence needed to improve attribution.

## Experiments and learning gates

Represent an experiment as a `learning` roadmap item with `experiment` details: hypothesis, method, cohort, success criteria, stopping rule and decision implication. Link the uncertain assumption, evidence and metrics. Specify both positive and negative results that change action. Avoid endless pilots without a scale/stop decision.

For AI evaluation, choose task-representative cases, error categories and end-to-end acceptance criteria. Include unacceptable failure modes where relevant. A model benchmark score is not automatically a user-workflow acceptance criterion. Human review cost and unsuccessful attempts belong in unit economics.

## Value and lifecycle decisions

At review, compare actual outcomes with baseline and target, explain data limitations, and choose continue, improve, expand, pause, consolidate or retire. An implementation can be technically successful and commercially/operationally weak. A shared platform capability can be technically reusable yet lack adoption; examine onboarding friction and competing alternatives before funding more features.

Use the smallest measurement plan that can influence a decision. Where telemetry is not yet available, begin with a bounded manual observation and record its limitations. Do not build a metrics pipeline solely to fill this system's fields.
