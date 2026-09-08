# Prioritization, sequencing, dependencies, and roadmaps

## Investment judgment

Separate “worth doing” from “ready to do” and “able to do with available capacity.” Compare a bounded set of alternatives, including defer, stop, combine, buy, reuse or a smaller learning investment. Identify mandatory constraints before ranking; an unfulfilled mandatory control is not compensated for by a high value score.

| Consideration | Evidence to request | Effect on judgment |
|---|---|---|
| Strategic outcome / user impact | Problem severity, reach, baseline, sponsor and strategy link | Is the outcome worth pursuing? |
| Time criticality | Actual deadline source, cost of delay, expiring opportunity | What happens if it waits? |
| Readiness / feasibility | Data/access, evaluation, integration, ownership and known constraints | Is delivery or learning the next sensible investment? |
| Effort / capacity | Team estimate range, scarce skills, operating burden | What would be displaced? |
| Risk / controls | Required controls, uncertainty and reversibility | Which conditions bound the choice? |
| Platform contribution | Credible demand, avoided duplicate effort, onboarding improvement | Does sharing add net value? |
| Dependency unlock | Confirmed consumers and prerequisites | What becomes feasible after this work? |
| Learning value | Decision-changing uncertainty and experiment cost | Can a small step prevent a larger bad investment? |

Default to `high`, `medium`, `low`, or `unknown` priority with a written rationale and separate confidence. These are not universal meanings: explain relative to the current portfolio. Do not average missing data into neutral scores. If the user supplies a scoring method, use it transparently, show assumptions and sensitivity, and retain hard constraints outside the weighted sum.

For a recommendation, state the selected investment, alternative displaced, main tradeoff, evidence gap and condition that could change the order. Avoid double counting one benefit as business value, reuse value and dependency-unlock value.

## Capacity and portfolio balancing

Identify the bottleneck by team/skill, not just total headcount. Ask whether capacity is confirmed, estimated or unavailable. Include discovery, integration, governance support, operating work, and migration obligations when they consume the constrained resource. Do not invent team velocity or assume parallel work is free.

Use ranges when estimates support them. If capacity is unknown, provide a conditional sequence and a capacity question; do not present a feasible schedule. Portfolio balance across near-term outcomes, platform foundations, learning and maintenance should follow strategy and constraints, not a fixed percentage rule.

## Dependencies

Canonical direction: `dependent_id` requires `prerequisite_id`. A record pointing UC-001 to CAP-001 means UC-001 depends on CAP-001. Each edge has a reason, type, strength, confirmation state, owner if known, and evidence. Mere co-occurrence or a capability-demand link is not a confirmed blocking dependency.

Types include capability, data/access, governance, technical, operational, capacity and external. Strength is `hard` or `soft`. Status is `hypothesized`, `confirmed`, `resolved` or `rejected`. “Confirmed” means the relationship is confirmed, not that the prerequisite is complete. “Resolved” means this dependency is satisfied or no longer blocks for a recorded reason; preserve its history.

Ask whether the prerequisite must be fully complete or only meet an interface/readiness condition. Where a tactical route bypasses a target-service dependency, record the conditions and revise the active edges. Do not simply hide the blocker.

Review hard confirmed unresolved edges for cycles. A cycle can reveal incompatible sequencing, a coarse capability decomposition, or work that must be jointly planned. Return the path and ask which edge can be relaxed, split or handled with a temporary contract. Do not manufacture a topological ordering of a cyclic graph.

## Sequencing

Sequence by confirmed prerequisites, bottleneck capacity, readiness, learning opportunities and urgency. A lower-priority enabling capability may happen before a higher-value use case. A high-value but low-readiness use case may receive a small discovery allocation rather than full delivery capacity.

Select a proving ground by representativeness, manageable risk, accessible data, committed consumer, feedback speed and ability to expose contract differences. The easiest demo may not be the best proving ground.

Describe branches when key facts remain uncertain: “If service readiness is confirmed, reuse; otherwise evaluate the bounded tactical path.” Use critical-path language only if durations, calendars and resource assumptions support it; otherwise describe dependency chains and timing risks.

## Roadmap construction

Roadmaps communicate why and what should change. A roadmap item may represent an outcome, capability increment, strategic bet, learning step, migration or retirement. Tasks such as “write test cases” belong in delivery plans unless the investment itself is a material quality capability.

Default horizons:

- `now`: selected current attention/investment with explicit conditions and capacity assumptions.
- `next`: plausible subsequent work whose readiness or capacity is not yet committed.
- `later`: directional intent or option, with an evidence/trigger condition.

Use quarter-based, outcome-based or maturity-based labels if supplied. `horizon_detail` can hold the organization's labels. A now item is not automatically committed. Dates need `date_kind` (`forecast` or `commitment`), source and uncertainty; a commitment must come from authorized evidence, not inference.

For each meaningful item show: title, intended outcome, capability/use-case links, horizon, priority/rationale, confidence, success metric, known owner, readiness/exit condition, dependency implications and status. Use links to risks/decisions rather than reproducing them. A missing metric may be a next action, not a reason to invent one.

## Views from one state

| View | Selection and emphasis |
|---|---|
| Product | Use cases in a product area; user outcomes, target experience and learning |
| Platform | Shared/candidate capabilities; consumers, adoption, service maturity and dependencies |
| Portfolio | Investments by outcome/horizon; capacity tradeoffs, risk, stop/combine choices |
| Executive | Selected themes/outcomes, meaningful progress/value, material uncertainty and decisions |
| Target state | Current/tactical/target choices and their transition triggers |

These are generated views, not separate editable roadmap registers. Every output includes source snapshot/as-of, filter scope, and whether coverage is partial. Do not count a shared roadmap item several times when rolling up consumer views.

## Replanning

Reassess when strategy, demand, evidence, service readiness, capacity or risk changes. Preserve previous decisions and explain the changed premise. Compare before/after for moved items, added/deferred/stopped work, dependencies and outcome consequences. Avoid churn from cosmetic priority changes that would not change action.
