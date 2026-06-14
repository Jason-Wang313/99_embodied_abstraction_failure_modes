# Hostile Reviewer Response

Paper: 99 Embodied Abstraction Failure Modes

## Strongest Technical Threats

- VLA agents with integrated motion planning.
- Embodied active learning of relational abstractions.
- Neuro-symbolic predicate learning for robot planning.
- VLA surveys and structured taxonomies.
- LLM task-and-motion planning with motion failure reasoning.
- Corrective LLM planning.
- Runtime monitoring of generative-policy consistency.
- Foundation-model-driven robust task planning and failure recovery.

## Hostile Review

A hostile reviewer would ask whether mechanics-aware abstraction auditing improves planning beyond grounded TAMP or LLM-TAMP failure reasoning. The v4 evidence says no for this audit: the proposed method has higher abstraction-failure accuracy but lower combined-stress success than grounded geometric TAMP, and ablations that remove predicate refinement or use geometric TAMP only match or beat full on success/regret.

## Honest Response

We accept the rejection. The evidence suggests that erased mechanics matter, but the full predicate-refinement audit is not the decisive ingredient. The paper should remain an archive unless future hardware or high-fidelity experiments show the full mechanism beating grounded planning and failure-reasoning baselines.
