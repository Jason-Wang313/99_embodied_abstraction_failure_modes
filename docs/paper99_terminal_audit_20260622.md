# Paper 99 Terminal Audit 2026-06-22

Final decision: KILL_ARCHIVE

ICLR main readiness: no

## What Was Completed

- A paper-specific expanded v5 plan was written before editing or running the final audit.
- `src/run_experiment.py`, `scripts/generate_manuscript.py`, and `scripts/validate_submission_artifacts.py` compiled successfully.
- The full CPU-only/RAM-light benchmark reran successfully with 10 seeds.
- The runner generated 322,560 main rows, 115,200 ablation rows, 259,200 stress rows, 138,240 fixed-risk rows, 96 hard paired rows, and 24 negative cases.
- The manuscript generator produced `paper/main.tex` and `paper/references.bib`.
- LaTeX/BibTeX produced a 29-page PDF.
- `C:/Users/wangz/Downloads/99.pdf` was validated with SHA256 `3D54F7894471FA1642ECF0F408F29F1CDAAA66C2663EDCA32D7FF656ABD48E09`.
- Representative PDF pages were visually inspected, including citation boxes and bibliography routing style.
- No visible Desktop PDF copy was made.

## Why It Is Killed

- `risk_bounded_abstraction_failure_audit_v5` hard success is 0.28708; `physics_aware_tamp` hard success is 0.67262.
- v5 mechanical violation is 0.45955; `physics_aware_tamp` mechanical violation is 0.16450.
- v5 damage is 0.37043; `physics_aware_tamp` damage is 0.13935.
- v5 regret is 0.63815; `physics_aware_tamp` regret is 0.06982.
- v5 robust utility is -0.33399; `physics_aware_tamp` robust utility is 0.30626.
- Diagnostics do not clear the frozen gate.
- All planned ablations match or beat full v5 on at least one decisive objective.
- Maximum-stress robust utility and fixed-risk deployment tests reverse against stronger grounded baselines.
- No real robot, high-fidelity simulator, external benchmark, or trained checkpoint evidence is claimed.

## Terminal Instruction

Keep Paper 99 archived unless a future project produces new real-robot, high-fidelity, or external benchmark evidence showing that the full mechanics-aware abstraction audit beats grounded TAMP, physics-aware TAMP, LLM-TAMP failure reasoning, semantic MPC, active relational abstraction, and runtime monitoring on closed-loop task success, safety, regret, robust utility, and fixed-risk deployment coverage.
