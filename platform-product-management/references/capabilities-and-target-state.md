# Capabilities, platformization, and target state

Use for capability mapping, reuse decisions, target-state reasoning, and build/buy/reuse/defer choices.

## Decompose by consumer ability

Name a capability as an enduring ability: “retrieve authorized source material” or “evaluate task-specific response quality.” A product feature is a particular user-facing expression; an implementation is the code/vendor/service that realizes the ability. “Vector database” is an implementation category, not enough of a capability proposition.

For each use case, walk the user workflow and ask what abilities are necessary to create its outcome. Identify inputs, outputs, consumers, quality expectations, data/access boundaries, and failure behavior. Stop decomposition when the unit can be independently reasoned about for reuse, ownership or roadmap decisions. Do not decompose to coding tasks.

Compare candidate overlaps across these dimensions:

| Dimension | Questions that can change the reuse decision |
|---|---|
| Consumer outcome | Do consumers need the same ability or only use the same terminology? |
| Semantics | Are business meanings, source freshness and permitted uses compatible? |
| Contract | Can inputs, outputs and error behavior be stable across consumers? |
| Quality / service | Are latency, accuracy, availability and scale requirements compatible? |
| Controls | Can identity, authorization, retention and audit requirements coexist? |
| Change cadence | Can one service evolve without blocking its consumers? |
| Ownership | Who funds, operates, supports and changes the shared capability? |

Record meaningful consumer-specific requirements on the use-case/capability relationship, not in a duplicated capability definition for every consumer.

## Capability classification

Use one primary classification; record alternatives as a decision or note:

- `use_case_specific`: specialized outcome or constraints; independent implementation is reasonable.
- `reusable`: an implementation or pattern can be reused, but it is not yet a supported shared service.
- `shared_platform`: a supported capability has a shared consumer contract and operating model.
- `enterprise_shared_service`: an existing enterprise-owned service outside this portfolio's direct control.
- `commodity_external`: an externally supplied capability whose integration and exit still need ownership.
- `candidate_standardization`: promising overlap that needs evidence before committing to shared ownership.

Classification is distinct from maturity (`candidate`, `piloting`, `available`, `deprecated`, `retired`) and implementation state. A proposed target service is not available just because its design is approved.

## Platformization decision

Recommend sharing when demand, structural compatibility, economics/risk reduction, and an operating owner jointly support it. Do not use a fixed minimum number of consumers as the sole gate. One strategic consumer may justify a foundational service with credible future demand; several incompatible consumers may not.

Test:

1. Demand: named consumer problems, evidence strength, adoption intent and timing.
2. Compatibility: shared contract versus consumer-specific adapters; identify differences that would make the common layer unstable.
3. Value: avoided duplicate effort, reduced risk, faster onboarding or improved quality; subtract shared overhead, migration and coordination costs.
4. Readiness: interface stability, service ownership, support capacity, policy constraints, and credible proving ground.
5. Dependency consequences: does the platform become a bottleneck or single point of failure? Can consumers proceed independently where necessary?
6. Reversibility: what can be learned cheaply now, and what becomes expensive to unwind?

Possible conclusions: reuse an existing service; publish a reusable pattern; pilot a shared slice; fund a supported platform service; buy; retain specialized implementations; defer. Document the choice and what evidence would change it.

## Platform as a product

Define the platform's consumers, onboarding path, documentation, support promise, compatibility expectations, and adoption feedback. Measure time to first successful use, integration effort, repeat adoption, supported-consumer satisfaction and service health. Count actual consumers rather than speculative use-case links.

Funding and support matter: who pays for the shared service, who prioritizes conflicting requests, and who carries incident burden? Prefer showback and transparent cost drivers initially; formal chargeback is an organizational choice. Avoid rewarding a platform for adoption that adds no net consumer value.

## Tactical versus target implementation

For a material capability choice, capture current implementation, tactical choice, target hypothesis, transition steps, owner, dependencies, reversibility, expected lifespan if known, and trigger for review/migration. Use narrative fields and linked decision records; do not demand a full architecture model.

Compare these options explicitly when relevant:

| Option | Good reason to choose | Key question |
|---|---|---|
| Reuse existing | Meets necessary needs at acceptable integration cost | Is it actually available and supported for this use? |
| Buy | Commodity fit and acceptable economics/control/exit | What must be verified in the current offering and contract? |
| Build now | Differentiated need or no feasible existing option | Can scope stay small and production ownership be clear? |
| Temporary implementation | Target service timing conflicts with justified delivery | What limits exposure and triggers reassessment? |
| Thin boundary / adapter | A likely change can be isolated cheaply | Which concrete volatility does this isolate? |
| Defer | Weak demand, constraint, or better opportunity elsewhere | What new evidence or capacity would change the choice? |
| Platformize later | Shared potential exists but the contract is still learning | What will the proving ground teach? |

Do not mandate an abstraction layer merely for theoretical portability. Compare its cost to expected change and exit costs.

## Target service unavailable

Establish the business urgency, required production controls, actual target-service readiness evidence, and the cost of waiting. Recommend a bounded tactical path only if it can satisfy necessary controls and support requirements. Identify any requirements it cannot meet. Do not waive governance because delivery is urgent.

Create two separate choices when appropriate: authorize a tactical investment now; revisit convergence later when the target meets specified functional/service criteria and migration value exceeds cost. The target's availability triggers evaluation, not automatic migration. Preserve the decision if the temporary solution becomes the preferred long-term choice.

## Debt and deprecation

Record material debt as a risk, decision consequence, or roadmap item according to whether it is an exposure, accepted tradeoff, or funded work. Avoid duplicate debt registries. For deprecation, identify actual consumers, communication owner, supported transition path, compatibility limits and exit evidence. Never mark a shared capability retired while knowingly leaving supported consumers without an accepted transition.
