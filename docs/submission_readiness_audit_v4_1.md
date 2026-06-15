# Submission Readiness Audit v4.1

Paper: 99 `embodied_abstraction_failure_modes`

Audit date: 2026-06-15

Decision: KILL_ARCHIVE

ICLR main readiness: no

## Fresh Rerun

Command sequence:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\99_embodied_abstraction_failure_modes_continuation_rerun_20260615.log
```

The rerun completed successfully and printed `Paper 99 evidence audit complete: KILL_ARCHIVE`.

## Coverage

- `metrics.csv`: 45 rows.
- `per_task_family_metrics.csv`: 1,575 rows.
- `seed_task_family_metrics.csv`: 11,025 rows.
- `pairwise_stats.csv`: 35 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 1,715 rows.
- `stress_sweep.csv`: 36 rows.
- `stress_sweep_seed_metrics.csv`: 252 rows.
- `failure_cases.csv`: 12 rows.
- Seeds: 0 through 6.
- Tasks: `container_insertion_clearance`, `deformable_object_packing`, `mobile_manipulation_with_occlusion`, `tabletop_manipulation_with_support`, `tool_use_with_hidden_leverage`.
- Failure families: `clearance_tolerance_collapse`, `deformable_constraint_erasure`, `erased_contact_force`, `friction_state_aliasing`, `hidden_support_relation`, `temporal_precondition_loss`, `tool_affordance_misabstraction`.

## Combined-Stress Gate Evidence

- `grounded_geometric_tamp`: success 0.603 +/- 0.013, violation 0.220, damage 0.168, regret 0.099.
- `llm_tamp_failure_reasoning`: success 0.582 +/- 0.011, violation 0.208, damage 0.165, regret 0.094.
- `proposed_abstraction_failure_audit`: success 0.552 +/- 0.009, violation 0.205, damage 0.150, failure accuracy 0.506, recall 1.000, false alarm 1.000, regret 0.091.
- `active_relational_abstraction`: success 0.546 +/- 0.008, violation 0.233, damage 0.166, regret 0.096.

## Failed Gates

- Success gate failed: `proposed_abstraction_failure_audit` does not beat `grounded_geometric_tamp` on combined-stress task success.
- False-alarm gate failed: proposed false refinement alarm rate is 1.000.
- Ablation gate failed: `minus_predicate_refinement`, `geometric_tamp_only`, and `minus_cost_model` match or beat the full audit on success or regret.

## Gate Outcome

The paper remains a useful negative evidence audit, not an ICLR-main-ready submission. The correct terminal state is `KILL_ARCHIVE`.
