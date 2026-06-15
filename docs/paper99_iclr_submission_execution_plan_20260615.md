# Paper 99 ICLR-Main Submission-Readiness Execution Plan

Timestamp: 2026-06-15

Paper: `99_embodied_abstraction_failure_modes`

Repository: `C:/Users/wangz/robotics_massive_pool_paper_factory/99_embodied_abstraction_failure_modes`

GitHub target: https://github.com/Jason-Wang313/99_embodied_abstraction_failure_modes

PDF target: `C:/Users/wangz/Downloads/99.pdf`

Desktop policy: do not copy a PDF or paper artifact to the visible Desktop.

## Goal

Rebuild Paper 99 as if it were being considered for an ICLR main-conference submission, but only mark it submission-ready if the fresh evidence supports that decision. The work must begin from the current negative v4 audit, rerun the evidence pipeline, verify every CSV/table/figure/PDF artifact, and then update claims honestly.

## Non-Negotiable Evidence Rule

The paper may be upgraded to `STRONG_REVISE` only if the freshly rerun benchmark clears all predeclared gates below. If any decisive gate fails, the correct terminal state remains `KILL_ARCHIVE`, even if the paper is polished, better explained, or more readable.

## Step 1: Baseline State Audit

1. Confirm the child repository is clean or identify unrelated local changes before editing.
2. Confirm `origin` points to the public GitHub repository.
3. Inspect current `README.md`, `child_status.md`, `paper/main.tex`, `docs/*decision*`, `docs/*gate*`, and `results/summary.txt`.
4. Record the current root-ledger state in `GLOBAL_POOL_STATUS.md`, `BATCH_STATUS.md`, `SUBMISSION_STATUS.md`, `MASTER_REPORT.md`, and `MASTER_SUBMISSION_REPORT.md`.
5. Confirm the current `C:/Users/wangz/Downloads/99.pdf` exists, and confirm no visible Desktop copy exists.

## Step 2: Fresh Experiment Rerun

Run the full paper-specific evidence pipeline without reducing rigor:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\99_embodied_abstraction_failure_modes_continuation_rerun_20260615.log
```

Expected scope:

1. Five robot task families.
2. Seven abstraction-failure families.
3. Five stress splits.
4. Nine methods.
5. Seven deterministic seeds.
6. Ablations, paired comparisons, stress sweep, failure cases, figures, LaTeX tables, and `results/summary.txt`.

## Step 3: CSV And Artifact Integrity Gates

Verify row counts and coverage after the rerun:

1. `results/metrics.csv`: expected combined method/split coverage.
2. `results/per_task_family_metrics.csv`: expected task/failure/method/split aggregation.
3. `results/seed_task_family_metrics.csv`: expected seed/task/failure/method/split coverage.
4. `results/pairwise_stats.csv`: paired seed/task/family comparisons against relevant baselines.
5. `results/ablation_metrics.csv` and `results/ablation_seed_metrics.csv`: full and stripped variants.
6. `results/stress_sweep.csv` and `results/stress_sweep_seed_metrics.csv`: stress robustness.
7. `results/failure_cases.csv`: concrete negative examples.
8. `figures/*.png` and `results/*table.tex`: regenerated and referenced by the paper.

Any missing, stale, or internally inconsistent artifact blocks submission readiness.

## Step 4: ICLR-Main Empirical Gates

The proposed method, `proposed_abstraction_failure_audit`, must pass all gates:

1. Success gate: beat the strongest non-oracle baseline on combined-stress task success using paired statistics.
2. Safety gate: reduce mechanical violation rate and damage/unsafe rate against the safest grounded baseline.
3. Diagnostic gate: improve abstraction-failure accuracy or mechanics-retention recall without merely increasing interventions.
4. False-alarm gate: keep false refinement/alarm rate below the predeclared acceptable range, with no saturation behavior.
5. Ablation gate: full method must beat `minus_mechanics_taxonomy`, `minus_predicate_refinement`, `minus_calibration`, `minus_cost_model`, `monitor_only`, and `geometric_tamp_only` on the claimed mechanism metrics.
6. Stress gate: maximum-stress curves must not reverse in favor of grounded geometric TAMP, LLM-TAMP failure reasoning, active relational abstraction, or runtime monitoring.
7. Scope gate: the paper must state that the evidence is local/executable and not robot hardware validation.

## Step 5: Claim And Paper Rewrite

If all empirical gates pass:

1. Rewrite the paper as an ICLR-main `STRONG_REVISE` submission candidate.
2. State only measured claims.
3. Include decisive baselines, ablations, confidence intervals, paired statistics, stress behavior, and limitations.
4. Keep novelty bounded against VLA, neuro-symbolic, relational-abstraction, LLM-TAMP, monitoring, and grounded TAMP prior work.

If any decisive empirical gate fails:

1. Keep or rewrite the paper as a negative evidence audit.
2. Preserve the `KILL_ARCHIVE` decision.
3. Explain exactly which gate failed and why that blocks ICLR-main readiness.
4. Do not inflate claims, hide failed ablations, or imply hardware/external validation.

## Step 6: PDF Build And Log Verification

Build the paper from `paper/` and copy only the numbered PDF to Downloads:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Copy-Item -LiteralPath main.pdf -Destination C:\Users\wangz\Downloads\99.pdf -Force
```

Then verify:

1. LaTeX exits cleanly.
2. BibTeX has no real missing citation or undefined-reference warnings.
3. Only harmless rerunfilecheck metadata remains, if present.
4. `C:/Users/wangz/Downloads/99.pdf` exists with a fresh hash.
5. No `99.pdf` exists on the visible Desktop.

## Step 7: Repository And Root Ledger Update

After the decision and PDF are final:

1. Update `README.md`, `child_status.md`, `docs/claims.md`, `docs/final_audit.md`, `docs/iclr_main_gate.md`, `docs/submission_readiness_decision.md`, `docs/submission_version_log.md`, and any stale review/attack docs.
2. Commit all Paper 99 changes in the child repository.
3. Push to `origin/main`.
4. Verify local and remote child commits match.
5. Verify the GitHub repository is public.
6. Update the root status files so Paper 99 is marked as continuation re-audited on 2026-06-15 with the final decision, PDF path, SHA, and public GitHub URL.

## Final Acceptance Checklist

Paper 99 is complete only when all of the following are true:

1. Fresh experiment log exists in the root `logs/` directory.
2. CSVs, figures, tables, summary, paper, and docs all reflect the same decision.
3. `C:/Users/wangz/Downloads/99.pdf` is the only final PDF copy requested by this workflow.
4. The child repo is clean after commit and push.
5. Local commit equals `origin/main`.
6. GitHub visibility is public.
7. Root ledgers are updated through Paper 99.
8. The final decision is either evidence-backed `STRONG_REVISE` or evidence-backed `KILL_ARCHIVE`; no cosmetic submission-ready label is allowed.
