# Experiment Rigor Checklist

## v4.1 Completed

- [x] Paper-specific embodied-abstraction benchmark rather than the old generic branch scaffold.
- [x] Multiple seeds.
- [x] Strong non-oracle baselines.
- [x] Ablations.
- [x] Stress splits and maximum-stress sweep.
- [x] Uncertainty/calibration metrics.
- [x] Mechanical violation, damage, cost, and regret metrics.
- [x] Pairwise seed/task/family comparisons.
- [x] Failure cases.
- [x] Generated figures and LaTeX result tables.
- [x] Explicit terminal gate in `results/summary.txt`.
- [x] Fresh 2026-06-15 continuation rerun logged at `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/99_embodied_abstraction_failure_modes_continuation_rerun_20260615.log`.

## ICLR Main Bar Not Met

- [ ] Real robot validation.
- [ ] High-fidelity simulator benchmark.
- [ ] Trained learned model checkpoint.
- [ ] External embodied-planning benchmark comparison.
- [ ] Evidence that full method beats grounded TAMP and LLM-TAMP failure reasoning.
- [ ] Evidence that predicate refinement and cost modeling are necessary rather than harmful.

Decision: fail ICLR-main empirical-rigor gate; archive.
