# Final Audit

1. Paper: 99 `embodied_abstraction_failure_modes`.
2. Submission-hardening version: v4.
3. Last audit timestamp: 2026-06-14 22:25:02 +01:00.
4. Thesis tested: mechanics-aware auditing for symbolic/language abstraction failures.
5. Evidence produced: 5 tasks x 7 abstraction-failure families x 5 splits x 9 methods, seven seeds, ablations, stress sweep, pairwise tests, and failure cases.
6. Terminal decision: KILL_ARCHIVE.
7. Main empirical reason: `grounded_geometric_tamp` beats the proposed method on combined-stress task success, 0.603 vs 0.552.
8. Mechanism reason: false refinement alarms are excessive and multiple ablations match or beat full on success/regret.
9. Hostile prior-work pressure: VLA agents, neuro-symbolic predicates, active relational abstraction, LLM-TAMP failure reasoning, runtime monitoring, and grounded TAMP already cover the obvious novelty space.
10. Reproducibility: `python src/run_experiment.py` regenerates all v4 CSVs, LaTeX tables, figures, and summary text.
11. Exact Downloads PDF path: `C:/Users/wangz/Downloads/99.pdf`.
12. GitHub URL: https://github.com/Jason-Wang313/99_embodied_abstraction_failure_modes
13. Desktop policy: no visible Desktop PDF copy should be made.
