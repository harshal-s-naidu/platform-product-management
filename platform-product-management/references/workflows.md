# Workflow contracts

Use plain-language requests. These names are routing aliases, not commands the user must memorize. Combine workflows when it reduces handoffs; do not generate every possible output for each request. Missing inputs limit confidence, not necessarily the ability to help.

| Workflow | Minimum useful inputs | Reasoning and expected output | Do not use it to |
|---|---|---|---|
| STRATEGY | Mandate, users, intended outcomes, constraints | Identify choices and non-goals; return a concise direction, investment themes, outcome measures and open strategic decisions | Invent an approved organizational strategy |
| INTAKE | Problem description and requesting user/group | Clarify outcome, alternatives, evidence and readiness; return a use-case brief, duplicate check and next step | Treat a request as funded work |
| DISCOVERY / EXPERIMENT | Uncertain proposition and decision at stake | Select the uncertainty most likely to change the choice; design a bounded learning step with criteria and decision implications | Turn all unknowns into a research program |
| PRODUCT_BRIEF | Use case or product scope | Connect user, problem, value, target experience, scope and measures; return a brief with known constraints and next bet | Produce a full technical design |
| CAPABILITY_MAP | Use cases and current service inventory, if available | Decompose into business/consumer abilities; compare common versus unique requirements and interfaces; return a map and reuse hypotheses | Split every feature into a new shared service |
| TARGET_STATE / BUILD_BUY | Capability, constraints, current options | Compare reuse, buy, build, temporary, defer and later standardization; return a decision recommendation, transition trigger and consequences | Choose a vendor on unsupported current product claims |
| PRIORITIZE | Candidate investments, strategic outcomes, capacity/constraints | Compare value, readiness, effort, learning, leverage and opportunity cost; return ordered recommendations or tiers, reasons and displaced work | Produce a precise score from guessed numbers |
| SEQUENCE / DEPENDENCY_ANALYSIS | Candidate work and dependency evidence | Distinguish hard/soft and confirmed/hypothesized edges; assess prerequisites, proving ground and capacity; return feasible next steps and conditional branches | Claim critical-path dates without durations and calendars |
| ROADMAP / PORTFOLIO_VIEW | Scope, outcomes, capability bets, decisions and horizons | Build Now / Next / Later or supplied horizon view; show uncertainty, entry/exit criteria and tradeoffs | Generate sprint tasks or imply unapproved date commitments |
| DECISION | Choice, options, evidence, constraints and authority | Compare alternatives, identify reversibility and revisit conditions; return a decision memo and proposed/adopted status as authorized | Treat the assistant's preference as an adopted decision |
| RISK | Uncertain event, exposure and affected work | Frame cause/event/consequence, severity, likelihood, owner and response; return actions or an explicit acceptance request | Label an already occurring issue as a future risk |
| METRICS | Outcome/capability, current measures and data availability | Define baseline, target, source, attribution limits and guardrails; return a measurement plan or value assessment | Equate usage or release completion with business impact |
| ROADMAP_REVIEW / HEALTH_REVIEW | Current snapshot, changes, outcomes, decision/issue state | Inspect evidence freshness, blockers, demand, debt, adoption and choices; return changes to recommend, decisions needed and follow-through | Rewrite the whole roadmap every week |
| EXECUTIVE | Audience, purpose, authoritative scope/state | Synthesize Why, What, Progress, Value, Risk, Decisions with traceable claims | Manufacture a green status or hide uncertainty |
| SAVE / HANDOFF | Explicit update instruction or a proposal | Reconcile versions and scope; validate, preserve history, save if authorized; return revision and changed IDs | Apply an old full snapshot over current state |

## Working through incomplete inputs

For a new request, establish the decision and minimum evidence required. If the owner or baseline is missing, name it and propose a discovery step; do not fabricate it. If sequencing depends on unknown enterprise-service readiness, offer conditional paths and identify the owner who can confirm it. If a ranking lacks effort or capacity, give a value/readiness assessment and state that it is not a feasible delivery plan.

## Combining workflows

Typical intake: INTAKE → CAPABILITY_MAP → SEQUENCE → ROADMAP implication. A full portfolio reset might need STRATEGY → PRIORITIZE → SEQUENCE → ROADMAP → EXECUTIVE. Only material adopted choices become decision records; supporting thought can stay in the brief.

## Request examples

- “Here are meeting notes. Extract candidate facts, decisions and open questions; show what you would change before saving.”
- “Which of these use cases is the best proving ground for a shared retrieval service, and why?”
- “Our engineering capacity fell. Re-sequence the current roadmap and show the opportunity cost.”
- “Review this proposal as a platform PM. What should remain specialized?”
- “Record the decision we just made and regenerate the executive view.”
- “Help me define value and adoption measures before this goes into production.”

## Output depth

Compact is the default. A quick answer may need only recommendation, basis, uncertainty and next action. A material investment decision merits options, consequences and evidence. A requested comprehensive review should use all relevant modules and a complete work product, without making the user ask repeatedly for omitted scope.
