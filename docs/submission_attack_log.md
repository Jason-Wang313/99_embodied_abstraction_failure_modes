# Submission Attack Log

Paper: 99 `embodied_abstraction_failure_modes`

Version: v5-expanded

## Attack 1: This is just worse TAMP with extra labels.

Result: Fatal. `physics_aware_tamp` reaches 0.67262 hard success while the proposed v5 method reaches 0.28708.

## Attack 2: The abstraction audit is less safe than grounded planning.

Result: Fatal. Proposed v5 has 0.45955 mechanical violation and 0.37043 damage, compared with 0.16450 violation and 0.13935 damage for `physics_aware_tamp`.

## Attack 3: The cost and risk machinery does not improve planning utility.

Result: Fatal. Proposed v5 has 0.63815 regret and -0.33399 robust utility, compared with 0.06982 regret and 0.30626 robust utility for `physics_aware_tamp`.

## Attack 4: The proposed components are not necessary.

Result: Fatal. `failure_classifier_only`, `grounded_tamp_only`, `monitor_only`, `no_calibration`, `no_cost_model`, `no_mechanics_taxonomy`, `no_predicate_refinement`, `no_recovery_feasibility_gate`, and `v4_abstraction_audit_rules` all match or beat full v5 on at least one decisive objective.

## Attack 5: Maximum-stress and fixed-risk deployment reverse the claim.

Result: Fatal. Maximum-stress robust utility is dominated by `physics_aware_tamp`, and fixed-damage-budget deployment is dominated by `grounded_geometric_tamp` or lacks useful coverage.

## Attack 6: Diagnostics do not equal robot performance.

Result: Fatal. Diagnostic evidence does not translate into closed-loop success, safety, regret, or robust utility.

## Attack 7: No real robot or high-fidelity validation exists.

Result: Fatal for main-conference readiness. This remains true even if the local surrogate had been positive.

## Terminal Action

Mark `KILL_ARCHIVE`. Do not submit as an ICLR-main paper. The 2026-06-22 expanded v5 audit strengthens the negative terminal decision.
