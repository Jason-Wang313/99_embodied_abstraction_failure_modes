# Reproducibility Checklist

## Reproduces Locally

- [x] `python src/run_experiment.py`
- [x] `results/summary.txt`
- [x] `results/metrics.csv`
- [x] `results/seed_task_family_metrics.csv`
- [x] `results/per_task_family_metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/ablation_seed_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/stress_sweep_seed_metrics.csv`
- [x] `results/failure_cases.csv`
- [x] `results/combined_stress_table.tex`
- [x] `results/ablation_table.tex`
- [x] `results/pairwise_decision_table.tex`
- [x] Figures in `figures/`
- [x] `paper/main.tex`
- [x] Canonical PDF target: `C:/Users/wangz/Downloads/99.pdf`
- [x] 2026-06-15 continuation log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/99_embodied_abstraction_failure_modes_continuation_rerun_20260615.log`

## Does Not Reproduce

- [ ] Real robot runs.
- [ ] High-fidelity simulator rollouts.
- [ ] Learned model checkpoints.
- [ ] External embodied-planning benchmark comparisons.

This is reproducible as a negative local v4.1 evidence audit, not as a deployable robotics system paper.
