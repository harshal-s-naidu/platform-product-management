# Operating model, strategy, and discovery

Use for onboarding, strategy, intake, discovery, product briefs, and responsibility boundaries. These are operating recommendations, not organizational policy.

## Responsibilities and boundaries

| Discipline | Primary question | Record or output |
|---|---|---|
| Portfolio management | Which investments advance strategy under capacity and risk constraints? | Investment recommendation, capacity tradeoff, portfolio roadmap |
| Product management | Whose problem matters, what outcome improves, and what should the product become? | Use-case/product brief, discovery evidence, outcome roadmap |
| Platform product management | Which consumer needs justify a shared capability and a supported interface? | Capability proposition, adoption plan, platform roadmap |
| Architecture | Which technical options meet constraints with acceptable tradeoffs? | Linked option/decision and architecture source |
| Program management | How are cross-team milestones and dependencies coordinated? | Delivery links, dependency owners, decision dates |
| Delivery management | How does a team execute and release safely? | Existing team backlog, execution plan, operational readiness evidence |

One person can participate in several disciplines. Label the decision being made rather than classifying the person. Do not recast a mandatory governance or operational requirement as optional merely because it is outside product ownership.

The PM owns the coherence of the investment narrative, facilitates choices, and makes decisions within their authority. Business owners validate the outcome and change adoption; governance owners interpret required controls; data science owns evaluation methods and model limitations; engineering estimates delivery and technical feasibility; platform owners define service contracts and support; operators accept production responsibilities. Actual authority comes from organization context, not this generic allocation.

## Onboarding without a long questionnaire

First establish: the decision the user needs to make, who consumes the output, the scope, and where current facts live. Ask for one representative use case or existing roadmap. If context is missing, proceed provisionally with explicit unknowns.

Create organization context only in the approved work environment. Record the authoritative store and source ownership before persisting live records. The initial default is a single local state file; Snowflake availability does not force a database setup.

Within the first useful session:

1. Capture a use case's user, problem, outcome, owner if known, and evidence.
2. Identify its smallest meaningful capabilities and relevant existing services.
3. Identify confirmed constraints and uncertain dependencies separately.
4. Recommend the next investment or learning step, with rationale and a roadmap implication.
5. Save only if asked; otherwise return a proposed record change. End with a resumable handoff.

Do not ask the user to prepopulate the whole portfolio, choose every future UI view, or name every stakeholder before producing value.

## Strategy and opportunity framing

A useful strategy states target users, important problems, desired outcomes, strategic choices, constraints, and what will not be pursued. A technology inventory is not a strategy. An aspiration such as “become AI-enabled” needs an observable outcome and a boundary before it can rank investments.

Keep objectives/outcomes in organization context or linked use-case/roadmap fields initially. Use a separate objective registry only when shared ownership, reporting, or explicit OKR rollups justify it. If OKRs are used, distinguish the objective from measurable key results and from initiatives. Do not make initiative completion itself a business key result without explaining why it represents value.

An opportunity is a plausible user problem with a potential outcome, not a commitment to a solution. Capture it as a use case in `idea` or `discovery` status. Assess:

- Who experiences the problem, in what workflow, at what frequency and consequence?
- What do people do today, including manual work, workarounds and existing non-AI tools?
- Which outcome would improve, and who cares enough to sponsor adoption?
- Why AI, rather than workflow change, rules, search, analytics, training, or no investment?
- What evidence exists, what contradicts the proposal, and what is still assumed?
- Which data, operating and control constraints could invalidate the idea?

Segment when needs materially differ: internal builders versus end users; frequent versus occasional users; high-risk versus low-risk actions; new versus existing consumers. Avoid creating a formal segmentation model if one sentence captures the meaningful difference.

## Discovery and experiments

Identify the riskiest assumption that can change an investment decision. It may concern demand, data rights, workflow adoption, accuracy, integration effort, economics, or operational ownership. Design the cheapest credible learning step: interview, workflow observation, data feasibility sample, offline evaluation, technical spike, or bounded pilot.

Each learning step needs a question, method, relevant cohort/data, success/failure criteria, owner if known, and a decision it will inform. Record that detail on a learning roadmap item and linked assumption/evidence; no standalone experiment registry is required. A successful demo is evidence of a bounded technical capability, not proof of production fit or value.

For AI, distinguish offline model quality, end-to-end workflow usefulness, and production outcomes. Consider task-specific error costs, human review, failure/abstention behavior, data access, monitoring, support, and changes in models or source data. Request actual policy from the responsible owner; never invent a governance approval or compliance checklist as universal law.

## Product vision and lifecycle

A product brief should explain the user problem, value proposition, current alternatives, target experience, measurable success, scope/non-goals, capability needs, constraints, and next learning or delivery step. Treat a use case as the smallest outcome-bearing investment unit; several use cases may contribute to a product or platform named in `product_area` without creating more entity types.

Lifecycle: idea → discovery → candidate → active → production → retired. `paused` and `stopped` are legitimate decisions. An active use case means an investment is being worked; it does not imply release approval. A production use case should have an actual service owner, required readiness evidence, support path and measurement plan, proportionate to its context.

During production, continue reviewing adoption, value, cost, reliability, quality and user friction. Scale only when evidence supports it. Retire or consolidate when demand disappears, a superior service replaces it, or its cost/risk is unjustified. Record consumer impact and migration/support obligations before retirement.

## Product-system health

After several review cycles, ask whether the system reduced repeated preparation, clarified decisions, surfaced important dependencies, and stayed current. Remove fields and outputs that are not used. Add structure only after repeated questions reveal a need. Improving this methodology is separate from rewriting historical decisions to appear consistent with today's view.
