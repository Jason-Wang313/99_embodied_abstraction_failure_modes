# Hostile Reviewer Response

Paper: 99 Embodied Abstraction Failure Modes

## Strongest Technical Threats

- Physics-aware task-and-motion planning.
- Grounded geometric TAMP.
- LLM task-and-motion planning with failure reasoning.
- Semantic model-predictive planning.
- Runtime monitoring and replanning.
- VLA agents with integrated motion planning.
- Embodied active learning of relational abstractions.
- Neuro-symbolic predicate learning for robot planning.
- Foundation-model-driven robust task planning and failure recovery.

## Hostile Review

A hostile reviewer would ask whether mechanics-aware abstraction auditing improves planning beyond grounded or physics-aware planners. The v5 evidence says no. `physics_aware_tamp` reaches 0.67262 hard success, 0.16450 violation, 0.13935 damage, 0.06982 regret, and 0.30626 robust utility. The proposed `risk_bounded_abstraction_failure_audit_v5` reaches 0.28708 hard success, 0.45955 violation, 0.37043 damage, 0.63815 regret, and -0.33399 robust utility.

The reviewer would also ask whether the proposed parts are necessary. The v5 ablation evidence says no: all planned ablations match or beat full v5 on at least one decisive objective, including `no_predicate_refinement`, `grounded_tamp_only`, `no_cost_model`, `no_mechanics_taxonomy`, and `v4_abstraction_audit_rules`.

## Honest Response

We accept the rejection. The evidence suggests that erased mechanics matter as a diagnostic category, but this full risk-bounded abstraction audit is not the decisive planning ingredient. The paper should remain an archive unless future hardware, high-fidelity, or external benchmark evidence shows the full mechanism beating grounded planning and failure-reasoning baselines on success, safety, regret, utility, and fixed-risk deployment coverage.
