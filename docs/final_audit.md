# Final Audit

1. Paper: 99 `embodied_abstraction_failure_modes`.
2. Submission-hardening version: v5-expanded.
3. Last audit timestamp: 2026-06-22 09:46:59 +08:00.
4. Thesis tested: mechanics-aware auditing for symbolic/language abstraction failures.
5. Evidence produced: 6 tasks x 8 abstraction-failure families x 8 splits x 14 methods x 10 seeds, 322,560 main rollout rows, 23,040 dataset-summary rows, 53,760 main group rows, 1,120 main seed-metric rows, 112 aggregate metric rows, 140 hard seed rows, 14 hard aggregate rows, 96 hard paired-test rows, 115,200 ablation rows, 259,200 stress rows, 138,240 fixed-risk rows, and 24 negative cases.
6. Terminal decision: KILL_ARCHIVE.
7. Main empirical reason: `physics_aware_tamp` beats `risk_bounded_abstraction_failure_audit_v5` on hard success, 0.67262 vs 0.28708.
8. Safety reason: `physics_aware_tamp` has lower mechanical violation, 0.16450 vs 0.45955, and lower damage, 0.13935 vs 0.37043.
9. Utility reason: `physics_aware_tamp` has lower regret, 0.06982 vs 0.63815, and higher robust utility, 0.30626 vs -0.33399.
10. Mechanism reason: all planned ablations match or beat full v5 on at least one decisive objective.
11. Stress reason: maximum-stress robust utility is dominated by `physics_aware_tamp`.
12. Fixed-risk reason: fixed-damage-budget deployment is dominated by `grounded_geometric_tamp` or lacks useful coverage.
13. Scope reason: no real robot, accepted high-fidelity simulator, external benchmark, or trained checkpoint evidence exists.
14. Reproducibility: `python src/run_experiment.py` regenerated all v5 CSVs, tables, figures, and summary text.
15. Manuscript: `python scripts/generate_manuscript.py` generated a 29-page ICLR-style archive with bright boxed clickable citations.
16. Validation: `python scripts/validate_submission_artifacts.py` verified `C:/Users/wangz/Downloads/99.pdf`.
17. Exact Downloads PDF path: `C:/Users/wangz/Downloads/99.pdf`.
18. PDF SHA256: `3D54F7894471FA1642ECF0F408F29F1CDAAA66C2663EDCA32D7FF656ABD48E09`.
19. GitHub URL: https://github.com/Jason-Wang313/99_embodied_abstraction_failure_modes
20. Desktop policy: no visible Desktop PDF copy should be made.
