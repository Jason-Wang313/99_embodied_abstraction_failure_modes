# ICLR Main Gate

Paper: 99 `embodied_abstraction_failure_modes`

Version: v5-expanded

Gate verdict: KILL_ARCHIVE

ICLR main readiness: no

## Required Gate

The proposed abstraction-failure audit had to beat the strongest non-oracle hard-split baseline on task success, reduce mechanical violations and damage against the safest grounded baseline, lower regret to the oracle, improve robust utility, provide useful diagnostics without pathological warnings, survive mechanism ablations, remain competitive at maximum stress, offer fixed-risk deployment coverage, and have enough external or high-fidelity validation to support an ICLR-main robotics claim.

## Measured Outcome

- Best non-oracle success baseline: `physics_aware_tamp`, 0.67262 hard success.
- Proposed v5 method: 0.28708 hard success.
- Best violation baseline: `physics_aware_tamp`, 0.16450 violation.
- Proposed v5 violation: 0.45955.
- Best damage baseline: `physics_aware_tamp`, 0.13935 damage.
- Proposed v5 damage: 0.37043.
- Best regret baseline: `physics_aware_tamp`, 0.06982 regret.
- Proposed v5 regret: 0.63815.
- Best utility baseline: `physics_aware_tamp`, 0.30626 robust utility.
- Proposed v5 utility: -0.33399.
- Ablations matching or beating full v5: `failure_classifier_only`, `grounded_tamp_only`, `monitor_only`, `no_calibration`, `no_cost_model`, `no_mechanics_taxonomy`, `no_predicate_refinement`, `no_recovery_feasibility_gate`, and `v4_abstraction_audit_rules`.
- Fresh v5 rerun status: completed on 2026-06-22.
- PDF status: 29 pages, Downloads-only, bright boxed clickable citations, SHA256 `3D54F7894471FA1642ECF0F408F29F1CDAAA66C2663EDCA32D7FF656ABD48E09`.

## Verdict

The proposed mechanism is not submission-ready. Stronger grounded and physics-aware planning does better on closed-loop planning objectives, the ablation pattern contradicts the claimed mechanism, stress/fixed-risk gates fail, and the paper lacks real robot or high-fidelity external validation.
