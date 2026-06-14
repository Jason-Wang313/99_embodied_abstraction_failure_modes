# Submission Attack Log

Paper: 99 `embodied_abstraction_failure_modes`

Version: v4

## Attack 1: This is just TAMP with extra labels.

Result: Fatal. `grounded_geometric_tamp` reaches 0.603 combined-stress success while the proposed method reaches 0.552.

## Attack 2: Predicate refinement is expensive and unnecessary.

Result: Fatal. `minus_predicate_refinement` beats full on success and regret.

## Attack 3: The cost model is doing harm.

Result: Fatal. `minus_cost_model` matches or beats full on success/regret.

## Attack 4: Monitoring or TAMP handles failures without a mechanics taxonomy.

Result: Mixed. Monitor-only is weak, but geometric TAMP is strong enough to undermine the proposed mechanism.

## Attack 5: Diagnostics do not equal robot performance.

Result: Fatal. The proposed method has best failure accuracy and recall, but loses task success to grounded TAMP.

## Attack 6: No real robot or high-fidelity validation exists.

Result: Still true. This prevents main-conference readiness even if the local result had been positive.

## Terminal Action

Mark `KILL_ARCHIVE`. Do not submit as an ICLR-main paper.
