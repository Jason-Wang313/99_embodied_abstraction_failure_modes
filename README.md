# 99 Embodied Abstraction Failure Modes

Submission-hardening version: v4

Terminal decision: KILL_ARCHIVE for ICLR main.

This repository is the v4 evidence audit for the claim that symbolic or language robot abstractions should be audited for erased action-critical mechanics before planning. The audit is paper-specific and executable, but it does not support an ICLR-main submission.

## Evidence Summary

The runner builds a deterministic embodied-abstraction benchmark with:

- 5 robot task families.
- 7 abstraction-failure families.
- 5 stress splits.
- 9 methods including language symbolic planning, VLA direct policy, neuro-symbolic predicates, active relational abstraction, LLM-TAMP failure reasoning, runtime monitoring/replanning, grounded geometric TAMP, the proposed abstraction-failure audit, and an action oracle.
- 7 seeds and 84 episodes per seed/task/family/method group.
- Ablations, pairwise tests, failure cases, calibration/safety metrics, and stress sweeps.

The proposed method improves abstraction-failure accuracy and mechanics-retention recall, but it does not clear the submission gate. On combined stress, `grounded_geometric_tamp` has higher task success than the proposed method, false refinement alarms are excessive, and ablations that remove predicate refinement or use geometric TAMP only match or beat the full method on success or regret.

## Reproduce

```powershell
python src\run_experiment.py
```

Primary evidence files:

- `results/summary.txt`
- `results/metrics.csv`
- `results/pairwise_stats.csv`
- `results/ablation_metrics.csv`
- `results/stress_sweep.csv`
- `results/failure_cases.csv`

## Build Archive PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/99.pdf`

No PDF should be copied to the visible Desktop.
