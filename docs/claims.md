# Claims

## Claim Under Test

Symbolic or language abstractions should be audited for erased mechanics before robot planning. The audit should detect when predicates hide contact force, support, clearance, friction, deformation, temporal preconditions, tool affordances, compliance, or recovery feasibility, then choose whether to proceed, refine predicates, query mechanics, switch to grounded TAMP, monitor, recover, or abstain.

## Supported By The v5 Audit

- The benchmark now tests 6 robot task families, 8 abstraction-failure families, 8 splits, 14 methods, 10 seeds, 322,560 main rollout rows, ablations, stress sweeps, fixed-risk deployment budgets, paired tests, negative cases, and generated manuscript tables/figures.
- Erased mechanics can be diagnosed as a real failure mode in the local surrogate benchmark.
- Brightly reporting negative evidence is valuable: the expanded audit prevents overstating a mechanism that fails under stronger grounded baselines.

## Not Supported

- `risk_bounded_abstraction_failure_audit_v5` does not beat `physics_aware_tamp` on hard success: 0.28708 vs 0.67262.
- It does not reduce mechanical violations: 0.45955 vs 0.16450 for `physics_aware_tamp`.
- It does not reduce damage: 0.37043 vs 0.13935 for `physics_aware_tamp`.
- It does not lower regret: 0.63815 vs 0.06982 for `physics_aware_tamp`.
- It does not improve robust utility: -0.33399 vs 0.30626 for `physics_aware_tamp`.
- It fails the diagnostic gate under the frozen accuracy, warning, and false-alarm thresholds.
- Every planned ablation matches or beats full v5 on at least one decisive objective.
- Maximum-stress robust utility is dominated by `physics_aware_tamp`.
- Fixed-damage-budget deployment is dominated by `grounded_geometric_tamp` or has insufficient useful coverage.
- No real robot, high-fidelity simulator, external benchmark, or trained-model checkpoint evidence is available.

## Submission Claim

The paper is not ICLR-main ready. The correct terminal label is `KILL_ARCHIVE`.
