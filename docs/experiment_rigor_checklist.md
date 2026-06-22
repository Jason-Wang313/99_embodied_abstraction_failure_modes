# Experiment Rigor Checklist

## v5 Completed

- [x] Paper-specific embodied-abstraction benchmark rather than a generic scaffold.
- [x] Pre-execution expanded submission plan.
- [x] CPU-only and RAM-light execution.
- [x] 6 task families.
- [x] 8 abstraction-failure families.
- [x] 8 splits.
- [x] 14 methods, including grounded geometric TAMP, physics-aware TAMP, LLM-TAMP failure reasoning, semantic MPC, monitoring, and oracle references.
- [x] 10 seeds.
- [x] 322,560 main rollout rows.
- [x] 115,200 ablation rollout rows.
- [x] 259,200 stress rollout rows.
- [x] 138,240 fixed-risk rollout rows.
- [x] Seed-level uncertainty and paired comparisons.
- [x] Mechanical violation, damage, cost, regret, diagnostic, warning, false-alarm, robust-utility, and deployment-coverage metrics.
- [x] Mechanism ablations.
- [x] Maximum-stress sweep.
- [x] Fixed-risk deployment budgets.
- [x] Representative negative cases.
- [x] Generated figures and LaTeX result tables.
- [x] Explicit terminal gate in `results/summary.txt`.
- [x] Generated 29-page manuscript with bright boxed clickable citations.
- [x] Validated Downloads-only PDF and absence of Desktop PDF copy.

## ICLR Main Bar Not Met

- [ ] Real robot validation.
- [ ] Accepted high-fidelity simulator benchmark.
- [ ] Trained learned model checkpoint.
- [ ] External embodied-planning benchmark comparison.
- [ ] Evidence that full v5 beats grounded TAMP, physics-aware TAMP, LLM-TAMP failure reasoning, semantic MPC, and runtime monitoring.
- [ ] Evidence that the mechanics taxonomy, predicate refinement, calibration, cost model, and recovery-feasibility gate are necessary rather than harmful.
- [ ] Fixed-risk deployment coverage under strict violation or damage budgets.

Decision: fail ICLR-main empirical-rigor gate; archive.
