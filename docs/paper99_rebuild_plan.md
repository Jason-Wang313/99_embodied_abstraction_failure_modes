# Paper 99 Rebuild Plan: Embodied Abstraction Failure Modes

Timestamp: 2026-06-14 22:01:20 +01:00

## Starting Point

Paper 99 is currently a v3 archive. The original research bet is:

> Find where symbolic or language abstractions erase action-critical mechanics.

The current repo contains a generic synthetic probability scaffold, not an embodied abstraction-failure benchmark. Hostile prior work is strong: VLA agents with motion planning, embodied active learning of relational abstractions, neuro-symbolic predicates for robot planning, VLA surveys/taxonomies, failure-demonstration hierarchies, cross-environment failure reasoning, LLM task-and-motion planning with motion-failure reasoning, AGENTSAFE, corrective LLM planning, runtime monitoring of generative-policy consistency, and foundation-model-driven failure recovery already cover much of the obvious space. The rebuild cannot claim novelty from "language abstractions can fail" or "add a monitor." It must test whether a mechanics-aware abstraction-failure audit changes planning outcomes beyond strong baselines.

## Rebuilt Claim Under Test

The strongest defensible claim is:

> Symbolic or language abstractions should be audited for erased mechanics before planning. A planner should identify when predicates hide contact force, support, clearance, friction, deformation, temporal preconditions, or tool-use mechanics, then preserve or refine those mechanics in the plan state.

This is a local evidence audit, not hardware validation.

## Benchmark Design

I will replace the generic scaffold with a deterministic embodied-abstraction benchmark. Each episode samples a task, a hidden mechanics failure, abstraction noise, language/predicate confidence, geometry tolerances, and action costs. Methods must decide whether the abstraction is safe, whether to refine predicates, query mechanics, switch to TAMP, monitor/replan, or proceed. The benchmark measures whether the proposed abstraction-failure audit improves task success, mechanical violations, safety, calibration, and regret.

Tasks:

1. `tabletop_manipulation_with_support`
2. `tool_use_with_hidden_leverage`
3. `container_insertion_clearance`
4. `deformable_object_packing`
5. `mobile_manipulation_with_occlusion`

Failure families:

1. `erased_contact_force`
2. `hidden_support_relation`
3. `clearance_tolerance_collapse`
4. `friction_state_aliasing`
5. `deformable_constraint_erasure`
6. `temporal_precondition_loss`
7. `tool_affordance_misabstraction`

Splits:

1. `nominal_abstraction`
2. `language_ambiguity_shift`
3. `geometry_tolerance_shift`
4. `mechanics_ood_shift`
5. `combined_abstraction_stress`

## Methods To Compare

Strong baselines:

1. `language_symbolic_planner`
2. `vla_direct_policy`
3. `neuro_symbolic_predicate_planner`
4. `active_relational_abstraction`
5. `llm_tamp_failure_reasoning`
6. `runtime_monitor_replanner`
7. `grounded_geometric_tamp`
8. `proposed_abstraction_failure_audit`
9. `oracle_mechanics_preserving_planner`

## Metrics

Diagnostic metrics:

1. Abstraction-failure classification accuracy.
2. Mechanics-retention recall.
3. False refinement/alarm rate.
4. Calibration error.
5. Predicate refinement informativeness.

Closed-loop metrics:

1. Task success.
2. Mechanical violation rate.
3. Damage/unsafe action rate.
4. Recovery/replan success.
5. Planning/refinement cost.
6. Planning regret to oracle.

Statistics:

1. Seven deterministic seeds.
2. Per-task and per-failure-family means with 95 percent confidence intervals.
3. Paired seed/task/family comparison against the strongest non-oracle baseline.
4. Explicit terminal decision in `results/summary.txt`.

## Ablations

The full method must beat stripped variants:

1. `full_abstraction_failure_audit`
2. `minus_mechanics_taxonomy`
3. `minus_predicate_refinement`
4. `minus_calibration`
5. `minus_cost_model`
6. `monitor_only`
7. `geometric_tamp_only`

If stripped variants match or beat full on task success, mechanical violations, damage, or regret, the mechanism is not supported.

## Stress Tests

Stress axes:

1. Language ambiguity.
2. Predicate/scene-graph noise.
3. Geometry tolerance.
4. Out-of-distribution mechanics.
5. Recovery/refinement cost.
6. Combined maximum stress.

The stress sweep must show whether abstraction-failure auditing remains useful when active relational abstraction, LLM-TAMP failure reasoning, runtime monitoring, and grounded geometric TAMP degrade.

## Paper Rewrite Requirements

After experiments:

1. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative evidence audit.
2. Replace template claims with measured claims only.
3. Include tables for combined stress, ablations, pairwise decision, and failure cases.
4. Include figures for abstraction diagnostics, closed-loop outcomes, cost/regret, ablations, and stress curves.
5. Update README, child status, claims, final audit, and submission-readiness docs.
6. Build only `C:/Users/wangz/Downloads/99.pdf`; do not copy anything to Desktop.
7. Commit and push to `https://github.com/Jason-Wang313/99_embodied_abstraction_failure_modes`.

## Terminal Gate

Mark `STRONG_REVISE` only if all of the following are true:

1. `proposed_abstraction_failure_audit` beats the strongest non-oracle baseline on combined-stress task success.
2. It also reduces mechanical violations and damage against the safest/most grounded baseline.
3. It improves mechanics-retention recall or failure classification without excessive false refinements or planning cost.
4. Core ablations degrade in expected directions.
5. Maximum-stress curves do not reverse in favor of active relational abstraction, LLM-TAMP failure reasoning, runtime monitoring/replanning, or grounded geometric TAMP.
6. The paper honestly states that the evidence is local/simulated and not robot hardware validation.

Otherwise mark `KILL_ARCHIVE`. An abstraction-failure audit that is matched or beaten by TAMP/failure reasoning, runtime monitoring, active relational abstraction, or grounded geometric planning is not ICLR-main ready.

## Execution Result

Executed on 2026-06-14. The rebuilt benchmark produced a terminal `KILL_ARCHIVE` decision. The proposed abstraction-failure audit improved abstraction-failure accuracy and mechanics-retention recall but did not beat `grounded_geometric_tamp` on combined-stress task success (0.552 vs 0.603), had excessive false refinement alarms, and was undermined by `geometric_tamp_only`, `minus_cost_model`, and `minus_predicate_refinement` ablations that matched or beat full on success/regret.
