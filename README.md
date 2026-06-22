# 99 Embodied Abstraction Failure Modes

Submission-hardening version: v5-expanded.

Terminal decision: KILL_ARCHIVE for ICLR main.

This repository is the expanded hostile-review audit for the claim that symbolic or language robot abstractions should be audited for erased action-critical mechanics before planning. The v5 rebuild is paper-specific, executable, CPU-only, RAM-light, and deliberately adversarial: it tests whether a mechanics-aware abstraction-failure audit survives strong grounded planning, physics-aware TAMP, LLM-TAMP, semantic MPC, monitoring, ablations, stress sweeps, and fixed-risk deployment budgets.

The honest answer is no. The v5 audit improves diagnostic labeling in some settings, but closed-loop planning is dominated by grounded/physics-aware planners and the full mechanism is contradicted by ablations.

## Evidence Summary

The v5 runner builds a deterministic embodied-abstraction benchmark with:

- 6 robot task families.
- 8 abstraction-failure families.
- 8 train/test/stress splits.
- 14 methods including language planning, VLA direct policy, neuro-symbolic predicates, active relational abstraction, LLM-TAMP failure reasoning, runtime monitoring, grounded geometric TAMP, physics-aware TAMP, affordance graph planning, learned failure-classifier TAMP, semantic MPC, v4 audit rules, v5 risk-bounded audit, and an oracle.
- 10 seeds and 6 episodes per seed/task/failure/split/method cell.
- 322,560 main rollout rows, 115,200 ablation rows, 259,200 stress rows, 138,240 fixed-risk rows, 96 hard paired tests, and 24 representative negative cases.
- Hard aggregate tables, paired statistics, ablations, stress curves, fixed-risk deployment budgets, negative-case tables, generated figures, and a 29-page archive manuscript.

The strongest non-oracle reference is `physics_aware_tamp`, which beats `risk_bounded_abstraction_failure_audit_v5` on every decisive hard-aggregate planning objective:

- Success: 0.67262 vs 0.28708.
- Mechanical violation: 0.16450 vs 0.45955.
- Damage: 0.13935 vs 0.37043.
- Regret: 0.06982 vs 0.63815.
- Robust utility: 0.30626 vs -0.33399.

The v5 audit also fails the diagnostic, ablation, maximum-stress, fixed-risk, and scope gates. All planned ablations match or beat the full method on at least one decisive objective, and no real robot, high-fidelity simulator, external benchmark, or trained-model checkpoint evidence is claimed.

## Reproduce

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
python scripts\validate_submission_artifacts.py
```

Primary evidence files:

- `results/summary.txt`
- `results/dataset_summary.csv`
- `results/rollouts.csv`
- `results/main_group_metrics.csv`
- `results/main_seed_metrics.csv`
- `results/metrics.csv`
- `results/hard_aggregate_metrics.csv`
- `results/hard_aggregate_seed_metrics.csv`
- `results/pairwise_stats.csv`
- `results/ablation_metrics.csv`
- `results/stress_sweep.csv`
- `results/fixed_risk_metrics.csv`
- `results/failure_cases.csv`

## Build Archive PDF

```powershell
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Copy-Item -LiteralPath main.pdf -Destination C:\Users\wangz\Downloads\99.pdf -Force
cd ..
python scripts\validate_submission_artifacts.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/99.pdf`

PDF SHA256: `3D54F7894471FA1642ECF0F408F29F1CDAAA66C2663EDCA32D7FF656ABD48E09`

PDF pages: 29.

The manuscript uses bright boxed clickable citations. No PDF should be copied to the visible Desktop.
