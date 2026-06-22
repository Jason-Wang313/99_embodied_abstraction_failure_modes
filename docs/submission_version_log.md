# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Replaced the toy experiment with seven-seed metrics, stronger synthetic baselines, ablations, stress tests, and negative cases.
- Narrowed claims to synthetic diagnostic evidence.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied the stricter ICLR-main-conference standard.
- Determined that missing real-robot/high-fidelity evidence and template-generated experiments were not enough for submission.
- Terminal decision: KILL_ARCHIVE.

## v4 - Paper-Specific Evidence Audit

- Rebuilt the runner as an embodied-abstraction failure benchmark.
- Added strong baselines: language symbolic planning, VLA direct policy, neuro-symbolic predicates, active relational abstraction, LLM-TAMP failure reasoning, runtime monitoring/replanning, grounded geometric TAMP, proposed audit, and action oracle.
- Added task/failure/split structure, calibration, mechanical violation, damage, cost, regret, ablations, pairwise comparisons, stress sweep, figures, and LaTeX result tables.
- Evidence outcome: proposed method loses to `grounded_geometric_tamp` on combined-stress success, 0.552 vs 0.603, has excessive false refinement alarms, and ablations match or beat full on success/regret.
- Terminal decision: KILL_ARCHIVE.

## v4.1 - Continuation Rerun And Submission Gate Recheck

- Added a pre-execution ICLR-main submission-readiness plan for Paper 99.
- Reran `python src/run_experiment.py` on 2026-06-15 with thread caps and saved the continuation log.
- Reconfirmed CSV coverage: 45 metric rows, 1,575 per-task/family rows, 11,025 seed/task/family rows, 35 pairwise rows, 7 ablation rows, 1,715 ablation seed rows, 36 stress-sweep rows, 252 stress-sweep seed rows, and 12 failure cases.
- Evidence outcome unchanged: proposed method loses to `grounded_geometric_tamp` on combined-stress success, 0.552 vs 0.603; false refinement alarm rate is 1.000; and `minus_predicate_refinement`, `geometric_tamp_only`, and `minus_cost_model` match or beat full on success or regret.
- Terminal decision: KILL_ARCHIVE.

## v5 - Expanded Hostile-Review Audit

- Wrote `docs/paper99_expanded_submission_plan_20260622.md` before editing or running the expanded audit.
- Rebuilt the runner into a CPU-only/RAM-light v5 benchmark with 6 tasks, 8 abstraction-failure families, 8 splits, 14 methods, 10 seeds, 322,560 main rollout rows, 115,200 ablation rows, 259,200 stress rows, 138,240 fixed-risk rows, 96 hard paired tests, and 24 negative cases.
- Added stronger references including `physics_aware_tamp`, `semantic_model_predictive_planner`, `learned_failure_classifier_tamp`, `affordance_graph_planner`, prior v4 rules, and oracle mechanics preservation.
- Added fixed-risk deployment budgets, maximum-stress robust utility, hard aggregate metrics, broader ablations, generated manuscript/tables/figures, artifact validation, and visual PDF QA.
- Built a 29-page ICLR-style archive PDF with bright boxed clickable citations at `C:/Users/wangz/Downloads/99.pdf`.
- Validated PDF SHA256 `3D54F7894471FA1642ECF0F408F29F1CDAAA66C2663EDCA32D7FF656ABD48E09` and no visible Desktop PDF copy.
- Evidence outcome: `risk_bounded_abstraction_failure_audit_v5` loses to `physics_aware_tamp` on success, violation, damage, regret, and robust utility; all planned ablations match or beat full v5 on at least one decisive objective; stress, fixed-risk, diagnostic, scope, and external-validation gates fail.
- Terminal decision: KILL_ARCHIVE.
