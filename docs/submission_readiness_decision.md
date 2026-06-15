# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

## Evidence

The v4.1 continuation rerun re-executed the executable embodied-abstraction audit on 2026-06-15. The audit includes strong baselines, ablations, stress tests, uncertainty/calibration metrics, pairwise seed/task/family comparisons, and failure cases.

Combined-stress headline:

- `grounded_geometric_tamp`: task success 0.603, regret 0.099.
- `llm_tamp_failure_reasoning`: task success 0.582, regret 0.094.
- `proposed_abstraction_failure_audit`: task success 0.552, regret 0.091.
- `oracle_mechanics_preserving_planner`: task success 0.616, regret 0.000.

The proposed method has the best non-oracle abstraction-failure accuracy, but the diagnostic advantage does not translate into decisive closed-loop performance.

Failed gates:

- Success gate: `proposed_abstraction_failure_audit` loses to `grounded_geometric_tamp` on combined-stress task success, 0.552 vs 0.603.
- False-alarm gate: false refinement alarm rate is 1.000.
- Ablation gate: `minus_predicate_refinement`, `geometric_tamp_only`, and `minus_cost_model` match or beat full on success or regret.

## Terminal Reason

The idea is killed because the fresh continuation evidence is negative for the main claim. A paper arguing that abstraction-failure auditing improves embodied planning cannot be ICLR-main-target when grounded geometric TAMP has higher success and predicate-refinement/geometric/cost-model ablations match or beat full on success/regret.

## Revival Condition

Revival would require real robot or high-fidelity simulator validation and evidence that the full mechanics-aware abstraction audit beats grounded geometric TAMP, LLM-TAMP failure reasoning, active relational abstraction, and runtime monitoring on task success, mechanical violations, damage, and regret.
