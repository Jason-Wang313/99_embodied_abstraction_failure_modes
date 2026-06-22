# Paper 99 Expanded Submission Plan

Date: 2026-06-22

Paper: `99_embodied_abstraction_failure_modes`

Repository: `C:/Users/wangz/robotics_massive_pool_paper_factory/99_embodied_abstraction_failure_modes`

GitHub target: `https://github.com/Jason-Wang313/99_embodied_abstraction_failure_modes`

Canonical PDF target: `C:/Users/wangz/Downloads/99.pdf`

Desktop policy: do not copy `99.pdf` or any paper PDF to the visible Desktop.

## Current Failure To Attack

The v4.1 archive is executable but not submission-ready:

- The proposed abstraction-failure audit loses combined-stress task success to `grounded_geometric_tamp`, 0.552 vs 0.603.
- False refinement alarms are saturated at 1.000.
- `minus_predicate_refinement`, `geometric_tamp_only`, and `minus_cost_model` match or beat the full method on success or regret.
- The PDF is under the expanded submission standard and lacks fixed-risk deployment analysis, larger stress scope, full theory, and visual/citation hardening.
- No real robot, accepted high-fidelity simulator, trained checkpoint, or external benchmark evidence exists.

The v5 rebuild must not optimize for pretty results. It must test whether a mechanics-aware abstraction-failure audit survives strong grounded planning, VLA, neuro-symbolic, LLM-TAMP, monitoring, and recovery baselines.

## Claim Under Test

Symbolic or language abstractions should be audited for erased action-critical mechanics before robot planning. A planner should detect when a predicate or language abstraction hides force, support, clearance, friction, deformation, temporal preconditions, tool affordances, compliance, or recovery feasibility, then choose whether to proceed, refine predicates, query mechanics, switch to grounded TAMP, monitor, recover, or abstain.

## Expanded Benchmark

- Tasks: 6 contact-rich and long-horizon robot task families.
- Hidden abstraction failures: 8 mechanics-erasure families.
- Splits: 8 distribution shifts, including combined adversarial abstraction stress.
- Methods: 14 total, including weak language/VLA baselines, neuro-symbolic predicates, active relational abstraction, LLM-TAMP, runtime monitoring, grounded geometric TAMP, physics-aware TAMP, affordance graph planning, learned failure classification with TAMP, semantic MPC, v4, v5, and an oracle.
- Seeds: 10 deterministic seeds.
- Episodes: 6 episodes per seed/task/failure/split/method cell.
- Main rollout rows: 6 x 8 x 8 x 14 x 10 x 6 = 322,560.

The runner must stream large CSVs to disk to keep RAM light.

## Metrics

- Task success.
- Mechanical violation rate.
- Damage/unsafe action rate.
- Abstraction-failure accuracy.
- Mechanics-retention recall.
- False refinement alarm rate.
- Planning/refinement cost.
- Planning regret to oracle.
- Robust utility.
- Intervention/refinement rate.
- Deployment coverage under fixed violation/damage budgets.
- Calibration and early-warning diagnostics where meaningful.

## Strong Baselines

The v5 method must be compared against:

- `grounded_geometric_tamp`.
- `physics_aware_tamp`.
- `llm_tamp_failure_reasoning`.
- `runtime_monitor_replanner`.
- `active_relational_abstraction`.
- `neuro_symbolic_predicate_planner`.
- `affordance_graph_planner`.
- `learned_failure_classifier_tamp`.
- `semantic_model_predictive_planner`.
- `vla_direct_policy`.
- `language_symbolic_planner`.
- The previous `proposed_abstraction_failure_audit_v4`.
- An oracle mechanics-preserving planner.

## Theory To Add

- Formal abstraction-erasure taxonomy: force, support, clearance, friction, deformation, temporal, tool, compliance/recovery.
- A decision-cost view of refinement: mechanics preservation is useful only when its closed-loop value exceeds refinement/query cost.
- A negative identifiability theorem: local diagnostic accuracy does not imply task-success improvement when a grounded planner already exposes the relevant mechanics.
- A mechanism-necessity statement: full v5 is supported only if core ablations degrade success, safety, regret, or utility in the predicted direction.

## Frozen Gates

The paper can only improve to `STRONG_REVISE` if the frozen evidence supports all empirical gates:

- Success gate: v5 beats the strongest non-oracle hard-split success baseline using paired seed/task/failure statistics.
- Violation gate: v5 reduces mechanical violations against the safest grounded baseline.
- Damage gate: v5 reduces damage/unsafe actions against the safest grounded baseline.
- Regret gate: v5 lowers regret to oracle against grounded TAMP, LLM-TAMP, semantic MPC, and runtime monitoring.
- Utility gate: v5 improves robust utility after cost, violation, damage, and abstention penalties.
- Diagnostic gate: v5 improves failure accuracy or recall without relying on saturated refinements.
- False-alarm gate: v5 false refinement alarms remain below the frozen nuisance threshold.
- Cost gate: v5 does not win by hiding excessive refinement/query cost.
- Ablation gate: full v5 beats stripped variants, including no mechanics taxonomy, no predicate refinement, no calibration, no cost model, no recovery feasibility, monitor-only, and TAMP-only.
- Stress gate: maximum-stress curves do not reverse in favor of grounded TAMP, physics-aware TAMP, LLM-TAMP, runtime monitoring, semantic MPC, or active relational abstraction.
- Fixed-risk gate: v5 has useful deployment coverage at fixed violation/damage budgets.
- Scope gate: ICLR-main readiness remains `no` unless external robot, accepted high-fidelity benchmark, or trained-model evidence exists.

If any empirical gate fails, the terminal decision remains `KILL_ARCHIVE`. If empirical gates pass but scope still lacks external validation, the decision may be `STRONG_REVISE` but ICLR-main readiness remains `no`.

## Execution Tasks

1. Replace `src/run_experiment.py` with a streaming expanded v5 runner.
2. Compile with `python -m py_compile src/run_experiment.py`.
3. Run the full CPU-only experiment without reducing seeds, tasks, failures, splits, methods, ablations, stress levels, or fixed-risk budgets.
4. Generate CSVs, figures, LaTeX tables, paired tests, stress summaries, fixed-risk tables, and predefined negative cases.
5. Generate a 25+ page manuscript with honest terminal decision, full gate ledger, theory, related-work pressure, and bright boxed clickable citations.
6. Build the PDF and copy only the final numbered PDF to `C:/Users/wangz/Downloads/99.pdf`.
7. Verify `C:/Users/wangz/Desktop/99.pdf` is absent.
8. Render representative PDF pages for visual QA.
9. Update README, child status, claims, final audit, ICLR gate, reproducibility, hostile reviewer, attack log, novelty, version log, and v5 audit docs.
10. Commit and push the child repo, verify public GitHub visibility, and update root ledgers.

## Completion Criteria

- Paper 99 has a frozen plan document, v5 runner, final docs, 25+ page PDF, and public GitHub push.
- `results/summary.txt` records the terminal decision and all failed/passed gates.
- `C:/Users/wangz/Downloads/99.pdf` exists with recorded SHA256.
- `C:/Users/wangz/Desktop/99.pdf` does not exist.
- Root ledgers advance the expanded-standard frontier to Paper 100.
