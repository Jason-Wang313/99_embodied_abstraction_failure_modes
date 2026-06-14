# ICLR Main Gate

Paper: 99 `embodied_abstraction_failure_modes`

Version: v4

Gate verdict: KILL_ARCHIVE

## Required Gate

The proposed abstraction-failure audit had to beat the strongest non-oracle baseline on combined-stress task success, reduce mechanical violations and damage against the safest/most grounded baseline, improve mechanics-retention diagnostics without excessive false refinements or cost, and survive ablations.

## Measured Outcome

- Best non-oracle success baseline: `grounded_geometric_tamp`, 0.603 task success.
- Proposed method: 0.552 task success.
- Proposed method damage/unsafe rate: 0.150.
- Proposed method false refinement alarm rate: 1.000.
- Ablations matching or beating full: `geometric_tamp_only`, `minus_cost_model`, `minus_predicate_refinement`.

## Verdict

The proposed mechanism is not submission-ready. It improves diagnostics, but grounded mechanics-aware planning does better on the closed-loop success objective and the ablation pattern contradicts the full predicate-refinement claim.
