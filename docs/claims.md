# Claims

## Claim Under Test

Symbolic or language abstractions should be audited for erased mechanics before robot planning. The audit should detect when predicates hide contact force, support, clearance, friction, deformation, temporal preconditions, or tool-use mechanics, then preserve or refine those mechanics in the plan state.

## Supported By The v4 Audit

- The executable benchmark tests five robot task families, seven abstraction-failure families, five stress splits, nine methods, seven seeds, ablations, stress sweeps, and failure cases.
- The proposed method improves abstraction-failure accuracy over non-oracle baselines on combined stress.
- The proposed method reduces damage/unsafe actions relative to several weaker baselines.

## Not Supported

- The proposed method does not beat `grounded_geometric_tamp` on combined-stress task success: 0.552 vs 0.603.
- False refinement alarms are excessive on low-risk temporal/nuisance cases.
- `minus_predicate_refinement`, `geometric_tamp_only`, and `minus_cost_model` match or beat the full method on success or regret.
- No real robot or high-fidelity simulator validation is available.

## Submission Claim

The paper is not ICLR-main ready. The correct terminal label is `KILL_ARCHIVE`.
