# Experiment Rigor Checklist

## v4 Completed

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

## ICLR Main Bar Not Met

- [ ] Real robot validation.
- [ ] High-fidelity simulator benchmark.
- [ ] Trained learned model checkpoint.
- [ ] External embodied-planning benchmark comparison.
- [ ] Evidence that full method beats grounded TAMP and LLM-TAMP failure reasoning.

Decision: fail ICLR-main empirical-rigor gate; archive.
