# Paper 99 Terminal Audit - 2026-06-15

Paper: `99_embodied_abstraction_failure_modes`

Final decision: KILL_ARCHIVE

## What Was Rechecked

- A paper-specific ICLR-main readiness execution plan was written before rerunning experiments.
- `src/run_experiment.py` compiled successfully.
- The full benchmark reran successfully with seven seeds and saved a continuation log.
- CSV, table, figure, summary, and paper artifacts were regenerated.
- The terminal decision in `results/summary.txt` was re-audited against the predeclared gates.

## Why It Is Not Submission Ready

The fresh rerun shows that the proposed abstraction-failure audit is diagnostically useful but not decisive as an embodied-planning method.

- `grounded_geometric_tamp` has higher combined-stress task success than the proposed method: 0.603 vs 0.552.
- The proposed method has false refinement alarm rate 1.000.
- `minus_predicate_refinement` beats full ablation success and regret: 0.586 success and 0.074 regret vs full 0.523 success and 0.126 regret.
- `geometric_tamp_only` and `minus_cost_model` also match or beat full on success or regret.
- No real robot, high-fidelity simulator, learned checkpoint, or external embodied-planning benchmark validation exists.

## Artifact Policy

- Canonical PDF: `C:/Users/wangz/Downloads/99.pdf`.
- Visible Desktop PDF copy: prohibited.
- GitHub repository: https://github.com/Jason-Wang313/99_embodied_abstraction_failure_modes

## Terminal Action

Keep Paper 99 archived unless a future project produces new high-fidelity or real-robot evidence showing that the full abstraction-failure audit beats grounded TAMP, LLM-TAMP failure reasoning, active relational abstraction, and runtime monitoring on closed-loop task success, safety, and regret.
