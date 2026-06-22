# Reproducibility Checklist

## Reproduces Locally

- [x] `python -m py_compile src\run_experiment.py scripts\generate_manuscript.py scripts\validate_submission_artifacts.py`
- [x] `python src\run_experiment.py`
- [x] `python scripts\generate_manuscript.py`
- [x] `python scripts\validate_submission_artifacts.py`
- [x] `results/summary.txt`
- [x] `results/dataset_summary.csv`
- [x] `results/rollouts.csv`
- [x] `results/main_group_metrics.csv`
- [x] `results/main_seed_metrics.csv`
- [x] `results/metrics.csv`
- [x] `results/hard_aggregate_metrics.csv`
- [x] `results/hard_aggregate_seed_metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/ablation_rollouts.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/ablation_seed_metrics.csv`
- [x] `results/stress_sweep_raw.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/stress_sweep_seed_metrics.csv`
- [x] `results/fixed_risk_raw.csv`
- [x] `results/fixed_risk_metrics.csv`
- [x] `results/fixed_risk_seed_metrics.csv`
- [x] `results/fixed_risk_pairwise_stats.csv`
- [x] `results/failure_cases.csv`
- [x] Generated LaTeX tables in `results/`.
- [x] v5 figures in `figures/`.
- [x] `paper/main.tex`
- [x] `paper/references.bib`
- [x] `paper/main.pdf`
- [x] Canonical PDF target: `C:/Users/wangz/Downloads/99.pdf`
- [x] PDF SHA256: `3D54F7894471FA1642ECF0F408F29F1CDAAA66C2663EDCA32D7FF656ABD48E09`
- [x] Canonical PDF pages: 29
- [x] Visible Desktop PDF copy absent.

## Does Not Reproduce

- [ ] Real robot runs.
- [ ] High-fidelity simulator rollouts.
- [ ] Learned model checkpoints.
- [ ] External embodied-planning benchmark comparisons.

This is reproducible as a negative local v5 evidence audit, not as a deployable robotics system paper.
