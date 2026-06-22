# Submission Readiness Audit v5

Paper: 99 `embodied_abstraction_failure_modes`

Audit date: 2026-06-22

Decision: KILL_ARCHIVE

ICLR main readiness: no

## Fresh Rerun

Command sequence:

```powershell
python -m py_compile src\run_experiment.py scripts\generate_manuscript.py scripts\validate_submission_artifacts.py
python src\run_experiment.py
python scripts\generate_manuscript.py
python scripts\validate_submission_artifacts.py
```

The rerun completed successfully and printed `Paper 99 expanded v5 evidence audit complete: KILL_ARCHIVE`.

## Coverage

- `dataset_summary.csv`: 23,040 rows.
- `rollouts.csv`: 322,560 rows.
- `main_group_metrics.csv`: 53,760 rows.
- `main_seed_metrics.csv`: 1,120 rows.
- `metrics.csv`: 112 rows.
- `hard_aggregate_seed_metrics.csv`: 140 rows.
- `hard_aggregate_metrics.csv`: 14 rows.
- `pairwise_stats.csv`: 96 rows.
- `ablation_rollouts.csv`: 115,200 rows.
- `ablation_seed_metrics.csv`: 100 rows.
- `ablation_metrics.csv`: 10 rows.
- `stress_sweep_raw.csv`: 259,200 rows.
- `stress_sweep_seed_metrics.csv`: 900 rows.
- `stress_sweep.csv`: 90 rows.
- `fixed_risk_raw.csv`: 138,240 rows.
- `fixed_risk_seed_metrics.csv`: 480 rows.
- `fixed_risk_metrics.csv`: 48 rows.
- `fixed_risk_pairwise_stats.csv`: 56 rows.
- `failure_cases.csv`: 24 rows.
- Seeds: 0 through 9.
- Tasks: `tabletop_manipulation_with_support`, `container_insertion_clearance`, `deformable_object_packing`, `tool_use_with_hidden_leverage`, `mobile_manipulation_with_occlusion`, `bimanual_contact_rich_assembly`.
- Failure families: `erased_contact_force`, `hidden_support_relation`, `clearance_tolerance_collapse`, `friction_state_aliasing`, `deformable_constraint_erasure`, `temporal_precondition_loss`, `tool_affordance_misabstraction`, `recovery_feasibility_erasure`.

## Hard-Aggregate Gate Evidence

- `physics_aware_tamp`: success 0.67262, violation 0.16450, damage 0.13935, regret 0.06982, utility 0.30626.
- `grounded_geometric_tamp`: success 0.60103, violation 0.21321, damage 0.18006, regret 0.13974, utility 0.20214.
- `llm_tamp_failure_reasoning`: success 0.57402, violation 0.20738, damage 0.17587, regret 0.13391, utility 0.18206.
- `semantic_model_predictive_planner`: success 0.56528, violation 0.21518, damage 0.18131, regret 0.14943, utility 0.15941.
- `proposed_abstraction_failure_audit_v4`: success 0.54907, violation 0.19701, damage 0.16822, regret 0.13168, utility 0.17247.
- `risk_bounded_abstraction_failure_audit_v5`: success 0.28708, violation 0.45955, damage 0.37043, regret 0.63815, utility -0.33399.

## Failed Gates

- Success gate failed: v5 does not beat `physics_aware_tamp`.
- Violation gate failed: v5 has higher mechanical violation than `physics_aware_tamp`.
- Damage gate failed: v5 has higher damage than `physics_aware_tamp`.
- Regret gate failed: v5 has higher regret than `physics_aware_tamp`.
- Utility gate failed: v5 has lower robust utility than `physics_aware_tamp`.
- Diagnostic gate failed: v5 does not clear the frozen accuracy, early-warning, and false-alarm criterion.
- Ablation gate failed: all planned ablations match or beat full v5 on at least one decisive objective.
- Stress gate failed: maximum-stress robust utility is dominated by `physics_aware_tamp`.
- Fixed-risk gate failed: fixed-damage-budget deployment is dominated by `grounded_geometric_tamp` or has insufficient coverage.
- Scope gate failed: no real robot, accepted high-fidelity benchmark, external benchmark, or trained checkpoint evidence exists.

## PDF And Artifact Audit

- Canonical PDF: `C:/Users/wangz/Downloads/99.pdf`.
- PDF pages: 29.
- PDF SHA256: `3D54F7894471FA1642ECF0F408F29F1CDAAA66C2663EDCA32D7FF656ABD48E09`.
- Citation behavior: bright boxed clickable in-text citations route to the reference section.
- Visible Desktop PDF copy: absent and prohibited.
- Public GitHub target: https://github.com/Jason-Wang313/99_embodied_abstraction_failure_modes

## Gate Outcome

The paper remains a useful negative evidence audit, not an ICLR-main-ready submission. The correct terminal state is `KILL_ARCHIVE`.
