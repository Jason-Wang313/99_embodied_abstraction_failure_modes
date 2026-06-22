# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

## Evidence

The v5 expanded audit re-executed the embodied-abstraction failure benchmark on 2026-06-22. The audit includes 6 tasks, 8 abstraction-failure families, 8 splits, 14 methods, 10 seeds, ablations, stress tests, fixed-risk deployment budgets, uncertainty/calibration metrics, paired comparisons, negative cases, generated figures/tables, and a 29-page archive PDF.

Hard-aggregate headline:

- `physics_aware_tamp`: success 0.67262, violation 0.16450, damage 0.13935, regret 0.06982, utility 0.30626.
- `grounded_geometric_tamp`: success 0.60103, violation 0.21321, damage 0.18006, regret 0.13974, utility 0.20214.
- `llm_tamp_failure_reasoning`: success 0.57402, violation 0.20738, damage 0.17587, regret 0.13391, utility 0.18206.
- `semantic_model_predictive_planner`: success 0.56528, violation 0.21518, damage 0.18131, regret 0.14943, utility 0.15941.
- `risk_bounded_abstraction_failure_audit_v5`: success 0.28708, violation 0.45955, damage 0.37043, regret 0.63815, utility -0.33399.

Failed gates:

- Success gate: v5 loses to `physics_aware_tamp`, 0.28708 vs 0.67262.
- Violation gate: v5 has higher violation than `physics_aware_tamp`, 0.45955 vs 0.16450.
- Damage gate: v5 has higher damage than `physics_aware_tamp`, 0.37043 vs 0.13935.
- Regret gate: v5 has higher regret than `physics_aware_tamp`, 0.63815 vs 0.06982.
- Utility gate: v5 has lower robust utility than `physics_aware_tamp`, -0.33399 vs 0.30626.
- Diagnostic gate: v5 does not clear the frozen accuracy, warning, and false-alarm criterion.
- Ablation gate: every planned ablation matches or beats full v5 on at least one decisive objective.
- Stress gate: maximum-stress robust utility is dominated by `physics_aware_tamp`.
- Fixed-risk gate: fixed-damage-budget deployment is dominated by `grounded_geometric_tamp` or lacks useful coverage.
- Scope gate: no real robot, accepted high-fidelity benchmark, external benchmark, or trained checkpoint evidence exists.

## Terminal Reason

The idea is killed for this submission because the fresh expanded evidence is negative for the main claim. A paper arguing that risk-bounded abstraction-failure auditing improves embodied planning cannot be ICLR-main-target when physics-aware TAMP has much higher success, lower violation, lower damage, lower regret, and higher robust utility, and when ablations undermine the proposed mechanism.

## Revival Condition

Revival would require new real-robot, high-fidelity simulator, or accepted external benchmark evidence showing that the full mechanics-aware abstraction audit, not merely grounded TAMP or failure reasoning, causes robust embodied-planning gains under fixed-risk deployment constraints.
