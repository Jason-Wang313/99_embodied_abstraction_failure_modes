import csv
import hashlib
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 699589046
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84
STRESS_EPISODES_PER_GROUP = 48

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

FAILURE_NAMES = [
    "erased_contact_force",
    "hidden_support_relation",
    "clearance_tolerance_collapse",
    "friction_state_aliasing",
    "deformable_constraint_erasure",
    "temporal_precondition_loss",
    "tool_affordance_misabstraction",
]
FAILURE_INDEX = {name: idx for idx, name in enumerate(FAILURE_NAMES)}

FEATURE_NAMES = [
    "language_ambiguity",
    "predicate_confidence",
    "contact_force",
    "support_relation",
    "clearance",
    "friction",
    "deformation",
    "temporal_order",
    "tool_affordance",
]

ACTION_NAMES = ["proceed", "refine_predicate", "query_mechanics", "switch_tamp", "monitor_replan", "recover"]
PROCEED, REFINE, QUERY, SWITCH_TAMP, MONITOR, RECOVER = range(len(ACTION_NAMES))


@dataclass(frozen=True)
class Task:
    name: str
    base_difficulty: float
    mechanics_depth: float
    language_ambiguity: float
    geometry_tolerance: float
    recovery_margin: float
    damage_sensitivity: float


@dataclass(frozen=True)
class FailureFamily:
    name: str
    actionable: bool
    violation_hazard: float
    damage_hazard: float
    refinement_value: float
    tamp_value: float
    classifier_hardness: float


@dataclass(frozen=True)
class Split:
    name: str
    language_shift: float
    predicate_noise: float
    geometry_shift: float
    mechanics_shift: float
    recovery_cost_shift: float
    stress: float


@dataclass(frozen=True)
class Method:
    name: str
    failure_acc: float
    stress_penalty: float
    risk_noise: float
    risk_bias: float
    planning_overhead: float


TASKS = [
    Task("tabletop_manipulation_with_support", 0.23, 0.64, 0.44, 0.55, 0.62, 0.58),
    Task("tool_use_with_hidden_leverage", 0.27, 0.78, 0.52, 0.48, 0.50, 0.70),
    Task("container_insertion_clearance", 0.26, 0.69, 0.36, 0.86, 0.47, 0.66),
    Task("deformable_object_packing", 0.30, 0.74, 0.42, 0.62, 0.42, 0.77),
    Task("mobile_manipulation_with_occlusion", 0.24, 0.59, 0.68, 0.57, 0.66, 0.55),
]

FAILURES = [
    FailureFamily("erased_contact_force", True, 0.58, 0.67, 0.71, 0.70, 0.08),
    FailureFamily("hidden_support_relation", True, 0.62, 0.52, 0.66, 0.74, 0.10),
    FailureFamily("clearance_tolerance_collapse", True, 0.69, 0.61, 0.50, 0.86, 0.09),
    FailureFamily("friction_state_aliasing", True, 0.48, 0.46, 0.56, 0.62, 0.13),
    FailureFamily("deformable_constraint_erasure", True, 0.64, 0.75, 0.63, 0.54, 0.12),
    FailureFamily("temporal_precondition_loss", False, 0.30, 0.28, 0.44, 0.38, 0.17),
    FailureFamily("tool_affordance_misabstraction", True, 0.57, 0.59, 0.67, 0.67, 0.11),
]
FAILURE_BY_NAME = {failure.name: failure for failure in FAILURES}

SPLITS = [
    Split("nominal_abstraction", 0.00, 0.00, 0.00, 0.00, 0.00, 0.05),
    Split("language_ambiguity_shift", 0.34, 0.15, 0.03, 0.05, 0.04, 0.40),
    Split("geometry_tolerance_shift", 0.05, 0.10, 0.35, 0.08, 0.05, 0.46),
    Split("mechanics_ood_shift", 0.09, 0.12, 0.11, 0.36, 0.07, 0.52),
    Split("combined_abstraction_stress", 0.30, 0.27, 0.31, 0.34, 0.18, 0.76),
]
SPLIT_BY_NAME = {split.name: split for split in SPLITS}

METHODS = [
    Method("language_symbolic_planner", 0.19, 0.05, 0.20, -0.12, 0.015),
    Method("vla_direct_policy", 0.31, 0.09, 0.16, -0.05, 0.045),
    Method("neuro_symbolic_predicate_planner", 0.47, 0.10, 0.12, 0.00, 0.075),
    Method("active_relational_abstraction", 0.61, 0.14, 0.11, 0.02, 0.105),
    Method("llm_tamp_failure_reasoning", 0.55, 0.12, 0.12, 0.03, 0.120),
    Method("runtime_monitor_replanner", 0.40, 0.08, 0.13, 0.05, 0.090),
    Method("grounded_geometric_tamp", 0.43, 0.07, 0.09, 0.02, 0.130),
    Method("proposed_abstraction_failure_audit", 0.75, 0.17, 0.10, 0.035, 0.135),
    Method("oracle_mechanics_preserving_planner", 0.985, 0.01, 0.025, -0.01, 0.050),
]
METHOD_BY_NAME = {method.name: method for method in METHODS}
NON_ORACLE_METHODS = [method.name for method in METHODS if method.name != "oracle_mechanics_preserving_planner"]

ABLATIONS = [
    "full_abstraction_failure_audit",
    "minus_mechanics_taxonomy",
    "minus_predicate_refinement",
    "minus_calibration",
    "minus_cost_model",
    "monitor_only",
    "geometric_tamp_only",
]

FEATURE_TEMPLATES = {
    "erased_contact_force": np.array([0.30, 0.74, 0.90, 0.36, 0.30, 0.42, 0.24, 0.24, 0.22]),
    "hidden_support_relation": np.array([0.38, 0.78, 0.34, 0.91, 0.38, 0.24, 0.28, 0.30, 0.22]),
    "clearance_tolerance_collapse": np.array([0.24, 0.72, 0.30, 0.42, 0.92, 0.28, 0.24, 0.20, 0.28]),
    "friction_state_aliasing": np.array([0.33, 0.70, 0.42, 0.26, 0.32, 0.91, 0.22, 0.24, 0.22]),
    "deformable_constraint_erasure": np.array([0.36, 0.68, 0.36, 0.30, 0.36, 0.25, 0.92, 0.22, 0.26]),
    "temporal_precondition_loss": np.array([0.55, 0.74, 0.22, 0.30, 0.24, 0.24, 0.22, 0.91, 0.30]),
    "tool_affordance_misabstraction": np.array([0.48, 0.76, 0.38, 0.28, 0.32, 0.29, 0.25, 0.30, 0.92]),
}


def stable_int(*parts: object) -> int:
    payload = "::".join(str(part) for part in parts).encode("utf-8")
    return int(hashlib.sha256(payload).hexdigest()[:16], 16)


def rng_for(*parts: object) -> np.random.Generator:
    return np.random.default_rng((BASE_SEED + stable_int(*parts)) % (2**32 - 1))


def clamp01(values: np.ndarray | float) -> np.ndarray | float:
    return np.clip(values, 0.001, 0.999)


def sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


def safe_mean(values: list[float]) -> float:
    return float(np.mean(values)) if values else 0.0


def ci95(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    arr = np.asarray(values, dtype=float)
    return float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr)))


def ece_score(predicted: np.ndarray, failures: np.ndarray, bins: int = 8) -> float:
    edges = np.linspace(0.0, 1.0, bins + 1)
    score = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (predicted >= lo) & (predicted < hi)
        if np.any(mask):
            score += float(np.mean(mask)) * abs(float(np.mean(predicted[mask])) - float(np.mean(failures[mask])))
    return score


def generate_episodes(
    rng: np.random.Generator,
    task: Task,
    failure: FailureFamily,
    split: Split,
    episodes: int,
    stress_override: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    stress = split.stress if stress_override is None else stress_override
    shift = np.array(
        [
            split.language_shift + 0.04 * task.language_ambiguity,
            split.predicate_noise + 0.05 * stress,
            split.mechanics_shift + 0.04 * task.mechanics_depth,
            split.predicate_noise + 0.03 * task.mechanics_depth,
            split.geometry_shift + 0.05 * task.geometry_tolerance,
            split.mechanics_shift + 0.02 * task.mechanics_depth,
            split.mechanics_shift + 0.06 * task.damage_sensitivity,
            split.language_shift + 0.04 * stress,
            split.language_shift + 0.03 * task.mechanics_depth,
        ]
    )
    features = clamp01(
        FEATURE_TEMPLATES[failure.name]
        + shift
        + rng.normal(0.0, 0.075 + 0.035 * stress, size=(episodes, len(FEATURE_NAMES)))
    )
    abstraction_confidence = clamp01(
        features[:, FEATURE_NAMES.index("predicate_confidence")]
        + rng.normal(0.0, 0.05 + 0.025 * stress, size=episodes)
    )
    violation_risk = clamp01(
        sigmoid(
            -2.15
            + 1.25 * failure.violation_hazard
            + 0.95 * task.base_difficulty
            + 0.50 * split.mechanics_shift
            + 0.35 * split.geometry_shift
            + 0.24 * features[:, FEATURE_NAMES.index("contact_force")]
            + 0.23 * features[:, FEATURE_NAMES.index("support_relation")]
            + 0.24 * features[:, FEATURE_NAMES.index("clearance")]
            + 0.20 * features[:, FEATURE_NAMES.index("tool_affordance")]
            + 0.16 * abstraction_confidence
            + rng.normal(0.0, 0.12 + 0.04 * stress, size=episodes)
        )
    )
    damage_risk = clamp01(
        sigmoid(
            -2.45
            + 1.18 * failure.damage_hazard
            + 0.72 * task.damage_sensitivity
            + 0.38 * split.mechanics_shift
            + 0.29 * features[:, FEATURE_NAMES.index("deformation")]
            + 0.20 * features[:, FEATURE_NAMES.index("friction")]
            + 0.18 * features[:, FEATURE_NAMES.index("clearance")]
            + rng.normal(0.0, 0.11 + 0.035 * stress, size=episodes)
        )
    )
    return features, violation_risk, damage_risk


def classify_failure(
    rng: np.random.Generator,
    method: Method,
    task: Task,
    failure: FailureFamily,
    split: Split,
    features: np.ndarray,
    stress_override: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    stress = split.stress if stress_override is None else stress_override
    mechanics_features = features[:, 2:]
    gap = np.max(mechanics_features, axis=1) - np.partition(mechanics_features, -2, axis=1)[:, -2]
    correct_prob = (
        method.failure_acc
        - method.stress_penalty * stress
        - failure.classifier_hardness
        - 0.045 * task.language_ambiguity
        - 0.045 * split.predicate_noise
        + 0.16 * gap
    )
    if method.name == "oracle_mechanics_preserving_planner":
        correct_prob = np.full(len(features), 0.985 - 0.01 * stress)
    correct_prob = clamp01(correct_prob)
    correct = rng.random(len(features)) < correct_prob

    scores = mechanics_features + rng.normal(0.0, 0.12 + 0.06 * stress, size=mechanics_features.shape)
    if method.name in {"language_symbolic_planner", "vla_direct_policy", "neuro_symbolic_predicate_planner"}:
        scores += rng.normal(0.0, 0.20, size=scores.shape)
    predicted = np.argmax(scores, axis=1)
    predicted[correct] = FAILURE_INDEX[failure.name]
    if method.name == "oracle_mechanics_preserving_planner":
        predicted[:] = FAILURE_INDEX[failure.name]
        correct[:] = True
    return predicted, correct


def predict_failure_risk(
    rng: np.random.Generator,
    method: Method,
    task: Task,
    split: Split,
    violation_risk: np.ndarray,
    damage_risk: np.ndarray,
    features: np.ndarray,
    stress_override: float | None = None,
) -> np.ndarray:
    stress = split.stress if stress_override is None else stress_override
    true_failure = clamp01(0.58 * violation_risk + 0.42 * damage_risk)
    predicted = (
        true_failure
        + method.risk_bias
        + 0.07 * split.predicate_noise
        + 0.05 * task.language_ambiguity
        + 0.10 * (features[:, FEATURE_NAMES.index("language_ambiguity")] - 0.45)
        + rng.normal(0.0, method.risk_noise + 0.035 * stress, size=len(true_failure))
    )
    if method.name == "oracle_mechanics_preserving_planner":
        predicted = true_failure + rng.normal(0.0, 0.018 + 0.01 * stress, size=len(true_failure))
    return clamp01(predicted)


def choose_actions(
    rng: np.random.Generator,
    method_name: str,
    predicted_failure: np.ndarray,
    predicted_risk: np.ndarray,
    features: np.ndarray,
    stress: float,
) -> np.ndarray:
    actions = np.full(len(predicted_risk), PROCEED, dtype=int)
    high_risk = predicted_risk > (0.57 - 0.04 * stress)
    very_high = predicted_risk > (0.77 - 0.04 * stress)
    names = np.array([FAILURE_NAMES[idx] for idx in predicted_failure])
    contact = names == "erased_contact_force"
    support = names == "hidden_support_relation"
    clearance = names == "clearance_tolerance_collapse"
    friction = names == "friction_state_aliasing"
    deform = names == "deformable_constraint_erasure"
    temporal = names == "temporal_precondition_loss"
    tool = names == "tool_affordance_misabstraction"

    if method_name == "language_symbolic_planner":
        actions[very_high] = MONITOR
    elif method_name == "vla_direct_policy":
        actions[high_risk & (features[:, FEATURE_NAMES.index("language_ambiguity")] > 0.62)] = MONITOR
        actions[very_high] = RECOVER
    elif method_name == "neuro_symbolic_predicate_planner":
        actions[contact | support | tool] = REFINE
        actions[high_risk & (clearance | deform)] = SWITCH_TAMP
        actions[very_high] = MONITOR
    elif method_name == "active_relational_abstraction":
        actions[contact | support | temporal | tool] = REFINE
        actions[clearance | deform | high_risk] = QUERY
        actions[very_high] = SWITCH_TAMP
    elif method_name == "llm_tamp_failure_reasoning":
        actions[high_risk | clearance | support | tool] = SWITCH_TAMP
        actions[contact | deform] = QUERY
        actions[very_high] = RECOVER
    elif method_name == "runtime_monitor_replanner":
        actions[high_risk | temporal | friction] = MONITOR
        actions[very_high | clearance] = RECOVER
    elif method_name == "grounded_geometric_tamp":
        actions[clearance | support | contact | high_risk] = SWITCH_TAMP
        actions[deform | tool] = QUERY
        actions[very_high] = RECOVER
    elif method_name == "proposed_abstraction_failure_audit":
        actions[contact | support | deform | tool] = REFINE
        actions[clearance] = SWITCH_TAMP
        actions[friction] = QUERY
        actions[temporal] = MONITOR
        actions[very_high] = RECOVER
        # Conservative audit behavior: catches failures but often refines too much.
        alarm = (predicted_risk > 0.60) & (features[:, FEATURE_NAMES.index("predicate_confidence")] > 0.67)
        actions[alarm & (rng.random(len(actions)) < 0.28)] = REFINE
    elif method_name == "oracle_mechanics_preserving_planner":
        actions[contact | support | deform | tool] = REFINE
        actions[clearance] = SWITCH_TAMP
        actions[friction] = QUERY
        actions[temporal] = MONITOR
        actions[very_high] = RECOVER
    else:
        raise ValueError(f"unknown method {method_name}")
    return actions


def expected_outcome(
    method_name: str,
    actions: np.ndarray,
    task: Task,
    failure: FailureFamily,
    split: Split,
    violation_risk: np.ndarray,
    damage_risk: np.ndarray,
    stress_override: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    stress = split.stress if stress_override is None else stress_override
    success = np.zeros(len(actions), dtype=float)
    violation = np.zeros(len(actions), dtype=float)
    damage = np.zeros(len(actions), dtype=float)
    cost = np.zeros(len(actions), dtype=float)

    proceed = actions == PROCEED
    refine = actions == REFINE
    query = actions == QUERY
    switch_tamp = actions == SWITCH_TAMP
    monitor = actions == MONITOR
    recover = actions == RECOVER

    success[proceed] = clamp01(0.95 - 0.95 * violation_risk[proceed] - 0.58 * damage_risk[proceed] - 0.06 * task.mechanics_depth)
    violation[proceed] = clamp01(violation_risk[proceed] + 0.06 * failure.violation_hazard)
    damage[proceed] = clamp01(damage_risk[proceed] + 0.06 * failure.damage_hazard)
    cost[proceed] = 0.035

    refine_bonus = 0.06 if method_name in {"proposed_abstraction_failure_audit", "active_relational_abstraction"} else 0.0
    success[refine] = clamp01(
        0.67
        + refine_bonus
        + 0.18 * failure.refinement_value
        - 0.34 * violation_risk[refine]
        - 0.18 * damage_risk[refine]
        - 0.05 * task.language_ambiguity
        - 0.04 * stress
    )
    violation[refine] = clamp01(0.48 * violation_risk[refine])
    damage[refine] = clamp01(0.50 * damage_risk[refine])
    cost[refine] = 0.17 + 0.04 * split.recovery_cost_shift

    success[query] = clamp01(
        0.70
        + 0.14 * failure.refinement_value
        + 0.04 * task.recovery_margin
        - 0.28 * violation_risk[query]
        - 0.20 * damage_risk[query]
        - 0.05 * stress
    )
    violation[query] = clamp01(0.42 * violation_risk[query])
    damage[query] = clamp01(0.45 * damage_risk[query])
    cost[query] = 0.21 + 0.06 * split.recovery_cost_shift

    tamp_bonus = 0.10 if method_name == "grounded_geometric_tamp" else 0.0
    tamp_bonus += 0.06 if method_name == "llm_tamp_failure_reasoning" else 0.0
    success[switch_tamp] = clamp01(
        0.71
        + tamp_bonus
        + 0.16 * failure.tamp_value
        - 0.23 * violation_risk[switch_tamp]
        - 0.18 * damage_risk[switch_tamp]
        - 0.04 * stress
    )
    violation[switch_tamp] = clamp01(0.30 * violation_risk[switch_tamp])
    damage[switch_tamp] = clamp01(0.34 * damage_risk[switch_tamp])
    cost[switch_tamp] = 0.25 + 0.08 * task.geometry_tolerance + 0.05 * split.recovery_cost_shift

    success[monitor] = clamp01(0.62 + 0.08 * task.recovery_margin - 0.38 * violation_risk[monitor] - 0.22 * damage_risk[monitor] - 0.04 * stress)
    violation[monitor] = clamp01(0.50 * violation_risk[monitor])
    damage[monitor] = clamp01(0.48 * damage_risk[monitor])
    cost[monitor] = 0.14 + 0.05 * split.recovery_cost_shift

    recover_bonus = 0.09 if method_name == "runtime_monitor_replanner" else 0.0
    recover_bonus += 0.06 if method_name == "llm_tamp_failure_reasoning" else 0.0
    success[recover] = clamp01(0.58 + recover_bonus + 0.12 * task.recovery_margin - 0.20 * violation_risk[recover] - 0.16 * damage_risk[recover] - 0.05 * stress)
    violation[recover] = clamp01(0.24 * violation_risk[recover])
    damage[recover] = clamp01(0.28 * damage_risk[recover])
    cost[recover] = 0.30 + 0.10 * split.recovery_cost_shift

    overhead = METHOD_BY_NAME.get(method_name, METHOD_BY_NAME["proposed_abstraction_failure_audit"]).planning_overhead
    if method_name in {"full_abstraction_failure_audit", "minus_mechanics_taxonomy", "minus_predicate_refinement", "minus_calibration", "minus_cost_model"}:
        overhead = METHOD_BY_NAME["proposed_abstraction_failure_audit"].planning_overhead
    if method_name == "monitor_only":
        overhead = 0.065
    if method_name == "geometric_tamp_only":
        overhead = 0.115
    cost += overhead
    return clamp01(success), clamp01(violation), clamp01(damage), cost


def oracle_actions(
    task: Task,
    failure: FailureFamily,
    split: Split,
    violation_risk: np.ndarray,
    damage_risk: np.ndarray,
    stress_override: float | None = None,
) -> np.ndarray:
    utilities = []
    for action_id in range(len(ACTION_NAMES)):
        actions = np.full(len(violation_risk), action_id, dtype=int)
        success, violation, damage, cost = expected_outcome(
            "oracle_mechanics_preserving_planner", actions, task, failure, split, violation_risk, damage_risk, stress_override
        )
        utilities.append(success - 0.62 * cost - 0.38 * violation - 0.48 * damage)
    return np.argmax(np.vstack(utilities), axis=0)


def oracle_utility(
    task: Task,
    failure: FailureFamily,
    split: Split,
    violation_risk: np.ndarray,
    damage_risk: np.ndarray,
    stress_override: float | None = None,
) -> np.ndarray:
    utilities = []
    for action_id in range(len(ACTION_NAMES)):
        actions = np.full(len(violation_risk), action_id, dtype=int)
        success, violation, damage, cost = expected_outcome(
            "oracle_mechanics_preserving_planner", actions, task, failure, split, violation_risk, damage_risk, stress_override
        )
        utilities.append(success - 0.62 * cost - 0.38 * violation - 0.48 * damage)
    return np.max(np.vstack(utilities), axis=0)


def row_metrics(
    rng: np.random.Generator,
    method_name: str,
    actions: np.ndarray,
    correct_failure: np.ndarray,
    predicted_risk: np.ndarray,
    violation_risk: np.ndarray,
    damage_risk: np.ndarray,
    task: Task,
    failure: FailureFamily,
    split: Split,
    seed: int,
    stress_override: float | None = None,
) -> dict[str, object]:
    success_prob, violation_prob, damage_prob, cost = expected_outcome(
        method_name, actions, task, failure, split, violation_risk, damage_risk, stress_override
    )
    successes = rng.random(len(actions)) < success_prob
    violations = rng.random(len(actions)) < violation_prob
    damages = rng.random(len(actions)) < damage_prob
    failures = (~successes).astype(float)

    intervention = actions != PROCEED
    actionable = np.full(len(actions), failure.actionable, dtype=bool)
    low_risk_nonactionable = (~actionable) & ((violation_risk + damage_risk) < 0.68)
    mechanics_retained = actionable & intervention
    false_alarm = low_risk_nonactionable & intervention
    replan_attempt = np.isin(actions, [SWITCH_TAMP, MONITOR, RECOVER])
    replan_success = replan_attempt & successes
    refinement_info = np.where(
        np.isin(actions, [REFINE, QUERY]),
        failure.refinement_value * correct_failure.astype(float) + np.maximum(0.0, predicted_risk - 0.48),
        0.0,
    )

    oracle_util = oracle_utility(task, failure, split, violation_risk, damage_risk, stress_override)
    method_util = success_prob - 0.62 * cost - 0.38 * violation_prob - 0.48 * damage_prob
    regret = np.maximum(0.0, oracle_util - method_util)

    return {
        "method": method_name,
        "split": split.name,
        "seed": seed,
        "task": task.name,
        "failure_family": failure.name,
        "episodes": len(actions),
        "failure_correct_count": int(np.sum(correct_failure)),
        "actionable_count": int(np.sum(actionable)),
        "mechanics_retained_count": int(np.sum(mechanics_retained)),
        "nonactionable_count": int(np.sum(low_risk_nonactionable)),
        "false_alarm_count": int(np.sum(false_alarm)),
        "success_count": int(np.sum(successes)),
        "mechanical_violation_count": int(np.sum(violations)),
        "damage_count": int(np.sum(damages)),
        "replan_attempt_count": int(np.sum(replan_attempt)),
        "replan_success_count": int(np.sum(replan_success)),
        "cost_sum": float(np.sum(cost)),
        "regret_sum": float(np.sum(regret)),
        "refinement_info_sum": float(np.sum(refinement_info)),
        "refinement_count": int(np.sum(np.isin(actions, [REFINE, QUERY]))),
        "abstraction_failure_accuracy": float(np.mean(correct_failure)),
        "mechanics_retention_recall": float(np.sum(mechanics_retained) / max(1, np.sum(actionable))),
        "false_refinement_alarm_rate": float(np.sum(false_alarm) / max(1, np.sum(low_risk_nonactionable))),
        "calibration_error": ece_score(predicted_risk, failures),
        "predicate_refinement_informativeness": float(np.sum(refinement_info) / max(1, np.sum(np.isin(actions, [REFINE, QUERY])))),
        "task_success": float(np.mean(successes)),
        "mechanical_violation_rate": float(np.mean(violations)),
        "damage_unsafe_rate": float(np.mean(damages)),
        "recovery_replan_success": float(np.sum(replan_success) / max(1, np.sum(replan_attempt))),
        "planning_cost": float(np.mean(cost)),
        "planning_regret_to_oracle": float(np.mean(regret)),
    }


def simulate_method_group(
    seed: int,
    split: Split,
    task: Task,
    failure: FailureFamily,
    method: Method,
    episodes: int,
    stress_override: float | None = None,
) -> dict[str, object]:
    rng = rng_for("main", seed, split.name, task.name, failure.name, method.name, stress_override or "base")
    features, violation_risk, damage_risk = generate_episodes(rng, task, failure, split, episodes, stress_override)
    predicted_failure, correct = classify_failure(rng, method, task, failure, split, features, stress_override)
    predicted_risk = predict_failure_risk(rng, method, task, split, violation_risk, damage_risk, features, stress_override)
    if method.name == "oracle_mechanics_preserving_planner":
        actions = oracle_actions(task, failure, split, violation_risk, damage_risk, stress_override)
    else:
        actions = choose_actions(
            rng, method.name, predicted_failure, predicted_risk, features, split.stress if stress_override is None else stress_override
        )
    return row_metrics(rng, method.name, actions, correct, predicted_risk, violation_risk, damage_risk, task, failure, split, seed, stress_override)


def ablation_actions(
    rng: np.random.Generator,
    ablation: str,
    predicted_failure: np.ndarray,
    predicted_risk: np.ndarray,
    features: np.ndarray,
    stress: float,
) -> np.ndarray:
    if ablation == "full_abstraction_failure_audit":
        return choose_actions(rng, "proposed_abstraction_failure_audit", predicted_failure, predicted_risk, features, stress)
    if ablation == "minus_mechanics_taxonomy":
        noisy_failure = np.argmax(features[:, 2:] + rng.normal(0.0, 0.25, size=(len(features), len(FAILURE_NAMES))), axis=1)
        return choose_actions(rng, "runtime_monitor_replanner", noisy_failure, predicted_risk, features, stress)
    if ablation == "minus_predicate_refinement":
        actions = choose_actions(rng, "proposed_abstraction_failure_audit", predicted_failure, predicted_risk, features, stress)
        actions[np.isin(actions, [REFINE, QUERY])] = SWITCH_TAMP
        return actions
    if ablation == "minus_calibration":
        noisy_risk = clamp01(predicted_risk + rng.normal(0.0, 0.20 + 0.06 * stress, size=len(predicted_risk)))
        return choose_actions(rng, "proposed_abstraction_failure_audit", predicted_failure, noisy_risk, features, stress)
    if ablation == "minus_cost_model":
        actions = choose_actions(rng, "proposed_abstraction_failure_audit", predicted_failure, predicted_risk - 0.08, features, stress)
        actions[actions == RECOVER] = SWITCH_TAMP
        return actions
    if ablation == "monitor_only":
        return choose_actions(rng, "runtime_monitor_replanner", predicted_failure, predicted_risk, features, stress)
    if ablation == "geometric_tamp_only":
        return choose_actions(rng, "grounded_geometric_tamp", predicted_failure, predicted_risk, features, stress)
    raise ValueError(f"unknown ablation {ablation}")


def simulate_ablation_group(seed: int, task: Task, failure: FailureFamily, ablation: str) -> dict[str, object]:
    split = SPLIT_BY_NAME["combined_abstraction_stress"]
    method = METHOD_BY_NAME["proposed_abstraction_failure_audit"]
    rng = rng_for("ablation", seed, task.name, failure.name, ablation)
    features, violation_risk, damage_risk = generate_episodes(rng, task, failure, split, EPISODES_PER_GROUP)
    predicted_failure, correct = classify_failure(rng, method, task, failure, split, features)
    predicted_risk = predict_failure_risk(rng, method, task, split, violation_risk, damage_risk, features)
    if ablation == "minus_mechanics_taxonomy":
        correct = rng.random(len(correct)) < 0.28
    if ablation == "minus_calibration":
        predicted_risk = clamp01(predicted_risk + rng.normal(0.0, 0.22, size=len(predicted_risk)))
    actions = ablation_actions(rng, ablation, predicted_failure, predicted_risk, features, split.stress)
    row = row_metrics(rng, ablation, actions, correct, predicted_risk, violation_risk, damage_risk, task, failure, split, seed)
    row["ablation"] = ablation
    return row


def aggregate(rows: list[dict[str, object]], keys: list[str]) -> list[dict[str, object]]:
    grouped: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    output = []
    for key_values, group in sorted(grouped.items()):
        episodes = sum(int(row["episodes"]) for row in group)
        failure_correct = sum(int(row["failure_correct_count"]) for row in group)
        actionable = sum(int(row["actionable_count"]) for row in group)
        retained = sum(int(row["mechanics_retained_count"]) for row in group)
        nonactionable = sum(int(row["nonactionable_count"]) for row in group)
        false_alarm = sum(int(row["false_alarm_count"]) for row in group)
        success = sum(int(row["success_count"]) for row in group)
        violations = sum(int(row["mechanical_violation_count"]) for row in group)
        damages = sum(int(row["damage_count"]) for row in group)
        replans = sum(int(row["replan_attempt_count"]) for row in group)
        replan_success = sum(int(row["replan_success_count"]) for row in group)
        cost_sum = sum(float(row["cost_sum"]) for row in group)
        regret_sum = sum(float(row["regret_sum"]) for row in group)
        refine_info_sum = sum(float(row["refinement_info_sum"]) for row in group)
        refine_count = sum(int(row["refinement_count"]) for row in group)
        row_out: dict[str, object] = {keys[idx]: key_values[idx] for idx in range(len(keys))}
        row_out.update(
            {
                "episodes": episodes,
                "seeds": len({row["seed"] for row in group}),
                "failure_correct_count": failure_correct,
                "actionable_count": actionable,
                "mechanics_retained_count": retained,
                "nonactionable_count": nonactionable,
                "false_alarm_count": false_alarm,
                "success_count": success,
                "mechanical_violation_count": violations,
                "damage_count": damages,
                "replan_attempt_count": replans,
                "replan_success_count": replan_success,
                "cost_sum": cost_sum,
                "regret_sum": regret_sum,
                "refinement_info_sum": refine_info_sum,
                "refinement_count": refine_count,
                "abstraction_failure_accuracy": failure_correct / max(1, episodes),
                "ci95_abstraction_failure_accuracy": ci95([float(row["abstraction_failure_accuracy"]) for row in group]),
                "mechanics_retention_recall": retained / max(1, actionable),
                "ci95_mechanics_retention_recall": ci95([float(row["mechanics_retention_recall"]) for row in group if int(row["actionable_count"]) > 0]),
                "false_refinement_alarm_rate": false_alarm / max(1, nonactionable),
                "ci95_false_refinement_alarm_rate": ci95([float(row["false_refinement_alarm_rate"]) for row in group if int(row["nonactionable_count"]) > 0]),
                "calibration_error": safe_mean([float(row["calibration_error"]) for row in group]),
                "ci95_calibration_error": ci95([float(row["calibration_error"]) for row in group]),
                "predicate_refinement_informativeness": refine_info_sum / max(1, refine_count),
                "ci95_predicate_refinement_informativeness": ci95([float(row["predicate_refinement_informativeness"]) for row in group]),
                "task_success": success / max(1, episodes),
                "ci95_task_success": ci95([float(row["task_success"]) for row in group]),
                "mechanical_violation_rate": violations / max(1, episodes),
                "ci95_mechanical_violation_rate": ci95([float(row["mechanical_violation_rate"]) for row in group]),
                "damage_unsafe_rate": damages / max(1, episodes),
                "ci95_damage_unsafe_rate": ci95([float(row["damage_unsafe_rate"]) for row in group]),
                "recovery_replan_success": replan_success / max(1, replans),
                "ci95_recovery_replan_success": ci95([float(row["recovery_replan_success"]) for row in group if int(row["replan_attempt_count"]) > 0]),
                "planning_cost": cost_sum / max(1, episodes),
                "ci95_planning_cost": ci95([float(row["planning_cost"]) for row in group]),
                "planning_regret_to_oracle": regret_sum / max(1, episodes),
                "ci95_planning_regret_to_oracle": ci95([float(row["planning_regret_to_oracle"]) for row in group]),
            }
        )
        output.append(row_out)
    return output


def format_row(row: dict[str, object]) -> dict[str, object]:
    return {key: f"{value:.6f}" if isinstance(value, float) else value for key, value in row.items()}


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(format_row(row))


def pairwise_stats(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    combined = [row for row in rows if row["split"] == "combined_abstraction_stress"]
    by_key = defaultdict(dict)
    for row in combined:
        by_key[(row["seed"], row["task"], row["failure_family"])][row["method"]] = row
    proposed = "proposed_abstraction_failure_audit"
    metrics = [
        ("task_success", "higher"),
        ("mechanical_violation_rate", "lower"),
        ("damage_unsafe_rate", "lower"),
        ("planning_regret_to_oracle", "lower"),
        ("abstraction_failure_accuracy", "higher"),
    ]
    output = []
    for baseline in NON_ORACLE_METHODS:
        if baseline == proposed:
            continue
        for metric, direction in metrics:
            diffs = []
            proposed_vals = []
            baseline_vals = []
            for methods in by_key.values():
                if proposed not in methods or baseline not in methods:
                    continue
                p = float(methods[proposed][metric])
                b = float(methods[baseline][metric])
                proposed_vals.append(p)
                baseline_vals.append(b)
                diffs.append(p - b)
            mean_diff = safe_mean(diffs)
            diff_ci = ci95(diffs)
            if direction == "higher":
                winner = proposed if mean_diff > diff_ci else baseline if mean_diff < -diff_ci else "statistical_tie"
            else:
                winner = proposed if mean_diff < -diff_ci else baseline if mean_diff > diff_ci else "statistical_tie"
            output.append(
                {
                    "baseline": baseline,
                    "metric": metric,
                    "direction": direction,
                    "proposed_mean": safe_mean(proposed_vals),
                    "baseline_mean": safe_mean(baseline_vals),
                    "mean_diff_proposed_minus_baseline": mean_diff,
                    "ci95_diff": diff_ci,
                    "winner": winner,
                    "paired_groups": len(diffs),
                }
            )
    return output


def stress_sweep() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    selected = [
        "active_relational_abstraction",
        "llm_tamp_failure_reasoning",
        "runtime_monitor_replanner",
        "grounded_geometric_tamp",
        "proposed_abstraction_failure_audit",
        "oracle_mechanics_preserving_planner",
    ]
    split = SPLIT_BY_NAME["combined_abstraction_stress"]
    seed_rows = []
    for stress in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        for method_name in selected:
            method = METHOD_BY_NAME[method_name]
            for seed in SEEDS:
                rows = [
                    simulate_method_group(seed, split, task, failure, method, STRESS_EPISODES_PER_GROUP, stress_override=stress)
                    for task in TASKS
                    for failure in FAILURES
                ]
                row = aggregate(rows, ["method"])[0]
                row["stress_level"] = stress
                row["seed"] = seed
                seed_rows.append(row)
    return seed_rows, aggregate(seed_rows, ["method", "stress_level"])


def failure_cases(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    selected = [
        row
        for row in rows
        if row["split"] == "combined_abstraction_stress"
        and row["method"] == "proposed_abstraction_failure_audit"
        and (
            float(row["task_success"]) < 0.58
            or float(row["damage_unsafe_rate"]) > 0.28
            or float(row["planning_regret_to_oracle"]) > 0.12
        )
    ]
    selected.sort(key=lambda row: (-float(row["planning_regret_to_oracle"]), -float(row["damage_unsafe_rate"]), float(row["task_success"])))
    cases = []
    for idx, row in enumerate(selected[:12], start=1):
        family = row["failure_family"]
        if family == "temporal_precondition_loss":
            reason = "the audit refines a mostly temporal nuisance when monitoring would be cheaper"
        elif family in {"clearance_tolerance_collapse", "hidden_support_relation"}:
            reason = "grounded TAMP captures the mechanics with lower regret than predicate refinement"
        elif family == "deformable_constraint_erasure":
            reason = "deformation risk remains high despite detecting the erased mechanics"
        else:
            reason = "mechanics detection does not offset refinement/query cost"
        cases.append(
            {
                "case_id": idx,
                "task": row["task"],
                "failure_family": family,
                "seed": row["seed"],
                "task_success": row["task_success"],
                "mechanical_violation_rate": row["mechanical_violation_rate"],
                "damage_unsafe_rate": row["damage_unsafe_rate"],
                "planning_regret_to_oracle": row["planning_regret_to_oracle"],
                "failure_mode": reason,
            }
        )
    return cases


def make_latex_table(path: Path, rows: list[dict[str, object]], columns: list[tuple[str, str]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write("\\begin{tabular}{" + "l" * len(columns) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = [str(row[key]).replace("_", "\\_") if isinstance(row[key], str) else str(row[key]) for key, _ in columns]
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")


def plot_figures(metrics: list[dict[str, object]], ablations: list[dict[str, object]], sweep: list[dict[str, object]]) -> None:
    combined = [row for row in metrics if row["split"] == "combined_abstraction_stress"]
    methods = [row["method"] for row in combined]
    x = np.arange(len(methods))

    plt.figure(figsize=(12, 5))
    plt.bar(x - 0.2, [float(row["abstraction_failure_accuracy"]) for row in combined], width=0.2, label="failure accuracy")
    plt.bar(x, [float(row["mechanics_retention_recall"]) for row in combined], width=0.2, label="mechanics recall")
    plt.bar(x + 0.2, [float(row["false_refinement_alarm_rate"]) for row in combined], width=0.2, label="false refinement")
    plt.xticks(x, [name.replace("_", "\n") for name in methods], fontsize=7)
    plt.ylim(0, 1.0)
    plt.ylabel("Rate")
    plt.title("Combined-stress abstraction diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 5))
    plt.bar(x - 0.2, [float(row["task_success"]) for row in combined], width=0.2, label="task success")
    plt.bar(x, [float(row["mechanical_violation_rate"]) for row in combined], width=0.2, label="mechanical violation")
    plt.bar(x + 0.2, [float(row["damage_unsafe_rate"]) for row in combined], width=0.2, label="damage")
    plt.xticks(x, [name.replace("_", "\n") for name in methods], fontsize=7)
    plt.ylim(0, 1.0)
    plt.ylabel("Rate")
    plt.title("Combined-stress closed-loop outcomes")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_task_outcomes.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 5))
    plt.bar(x - 0.17, [float(row["planning_cost"]) for row in combined], width=0.34, label="planning cost")
    plt.bar(x + 0.17, [float(row["planning_regret_to_oracle"]) for row in combined], width=0.34, label="regret")
    plt.xticks(x, [name.replace("_", "\n") for name in methods], fontsize=7)
    plt.ylabel("Mean per episode")
    plt.title("Planning cost and regret")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_cost_regret.png", dpi=180)
    plt.close()

    ablation_names = [row["ablation"] for row in ablations]
    ax = np.arange(len(ablation_names))
    plt.figure(figsize=(11, 5))
    plt.bar(ax - 0.17, [float(row["task_success"]) for row in ablations], width=0.34, label="task success")
    plt.bar(ax + 0.17, [float(row["planning_regret_to_oracle"]) for row in ablations], width=0.34, label="regret")
    plt.xticks(ax, [name.replace("_", "\n") for name in ablation_names], fontsize=7)
    plt.title("Abstraction-failure audit ablations")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_ablation.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.5, 5))
    for method in [
        "active_relational_abstraction",
        "llm_tamp_failure_reasoning",
        "runtime_monitor_replanner",
        "grounded_geometric_tamp",
        "proposed_abstraction_failure_audit",
    ]:
        rows = sorted([row for row in sweep if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in rows], [float(row["task_success"]) for row in rows], marker="o", label=method.replace("_", " "))
    plt.xlabel("Combined stress level")
    plt.ylabel("Task success")
    plt.title("Stress sweep: grounded planning remains hard to beat")
    plt.ylim(0, 1.0)
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_stress_sweep.png", dpi=180)
    plt.close()


def terminal_decision(metrics: list[dict[str, object]], pairwise: list[dict[str, object]], ablations: list[dict[str, object]]) -> dict[str, object]:
    combined = {row["method"]: row for row in metrics if row["split"] == "combined_abstraction_stress"}
    proposed = combined["proposed_abstraction_failure_audit"]
    non_oracle = {name: row for name, row in combined.items() if name not in {"proposed_abstraction_failure_audit", "oracle_mechanics_preserving_planner"}}
    best_success_name, best_success_row = max(non_oracle.items(), key=lambda item: float(item[1]["task_success"]))
    safest_name, safest_row = min(non_oracle.items(), key=lambda item: float(item[1]["mechanical_violation_rate"]) + float(item[1]["damage_unsafe_rate"]))
    best_regret_name, _ = min(non_oracle.items(), key=lambda item: float(item[1]["planning_regret_to_oracle"]))
    pair_success = [row for row in pairwise if row["baseline"] == best_success_name and row["metric"] == "task_success"][0]
    pair_damage = [row for row in pairwise if row["baseline"] == safest_name and row["metric"] == "damage_unsafe_rate"][0]
    ablation_by_name = {row["ablation"]: row for row in ablations}
    full_success = float(ablation_by_name["full_abstraction_failure_audit"]["task_success"])
    full_regret = float(ablation_by_name["full_abstraction_failure_audit"]["planning_regret_to_oracle"])
    ablation_beats = [
        name
        for name, row in ablation_by_name.items()
        if name != "full_abstraction_failure_audit"
        and (float(row["task_success"]) >= full_success or float(row["planning_regret_to_oracle"]) <= full_regret)
    ]
    success_gate = pair_success["winner"] == "proposed_abstraction_failure_audit"
    safety_gate = pair_damage["winner"] == "proposed_abstraction_failure_audit"
    diagnostic_gate = float(proposed["abstraction_failure_accuracy"]) >= max(float(row["abstraction_failure_accuracy"]) for row in non_oracle.values()) - 0.015
    false_alarm_gate = float(proposed["false_refinement_alarm_rate"]) < 0.35
    ablation_gate = not ablation_beats
    decision = "STRONG_REVISE" if all([success_gate, safety_gate, diagnostic_gate, false_alarm_gate, ablation_gate]) else "KILL_ARCHIVE"
    reasons = []
    if not success_gate:
        reasons.append(f"proposed does not beat strongest success baseline {best_success_name} ({float(proposed['task_success']):.3f} vs {float(best_success_row['task_success']):.3f})")
    if not safety_gate:
        reasons.append(f"proposed does not beat safest baseline {safest_name} on damage ({float(proposed['damage_unsafe_rate']):.3f} vs {float(safest_row['damage_unsafe_rate']):.3f})")
    if not false_alarm_gate:
        reasons.append(f"false refinement alarm rate is high ({float(proposed['false_refinement_alarm_rate']):.3f})")
    if not ablation_gate:
        reasons.append("ablations match or beat full on success/regret: " + ", ".join(ablation_beats))
    if not reasons:
        reasons.append("all gates passed")
    return {
        "decision": decision,
        "best_success_baseline": best_success_name,
        "safest_baseline": safest_name,
        "best_regret_baseline": best_regret_name,
        "success_gate": success_gate,
        "safety_gate": safety_gate,
        "diagnostic_gate": diagnostic_gate,
        "false_alarm_gate": false_alarm_gate,
        "ablation_gate": ablation_gate,
        "reasons": reasons,
    }


def write_summary(metrics: list[dict[str, object]], pairwise: list[dict[str, object]], ablations: list[dict[str, object]], failures: list[dict[str, object]], decision: dict[str, object]) -> None:
    combined = [row for row in metrics if row["split"] == "combined_abstraction_stress"]
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 99: embodied_abstraction_failure_modes v4 evidence audit\n")
        handle.write("Terminal decision: " + decision["decision"] + "\n")
        handle.write(f"Design: 5 tasks x 7 abstraction-failure families x 5 splits x 9 methods, {len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes per seed/task/family/method group.\n")
        handle.write("Claim under test: mechanics-aware abstraction-failure auditing should improve robot planning beyond VLA, neuro-symbolic, relational-abstraction, TAMP, and monitoring baselines.\n\n")
        handle.write("Combined-stress evidence:\n")
        for row in sorted(combined, key=lambda item: float(item["task_success"]), reverse=True):
            handle.write(
                f"- {row['method']}: success={float(row['task_success']):.3f} +/- {float(row['ci95_task_success']):.3f}, "
                f"viol={float(row['mechanical_violation_rate']):.3f}, damage={float(row['damage_unsafe_rate']):.3f}, "
                f"failure_acc={float(row['abstraction_failure_accuracy']):.3f}, recall={float(row['mechanics_retention_recall']):.3f}, "
                f"false_alarm={float(row['false_refinement_alarm_rate']):.3f}, cost={float(row['planning_cost']):.3f}, "
                f"regret={float(row['planning_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key in ["success_gate", "safety_gate", "diagnostic_gate", "false_alarm_gate", "ablation_gate"]:
            handle.write(f"- {key}: {decision[key]}\n")
        handle.write("\nTerminal rationale:\n")
        for reason in decision["reasons"]:
            handle.write(f"- {reason}\n")
        handle.write("\nAblation summary:\n")
        for row in sorted(ablations, key=lambda item: float(item["task_success"]), reverse=True):
            handle.write(
                f"- {row['ablation']}: success={float(row['task_success']):.3f}, damage={float(row['damage_unsafe_rate']):.3f}, "
                f"regret={float(row['planning_regret_to_oracle']):.3f}, failure_acc={float(row['abstraction_failure_accuracy']):.3f}\n"
            )
        handle.write("\nRepresentative failure cases:\n")
        for row in failures[:5]:
            handle.write(f"- {row['task']} / {row['failure_family']} seed {row['seed']}: success={row['task_success']}, regret={row['planning_regret_to_oracle']}; {row['failure_mode']}\n")
        handle.write("\nPaired comparison rows: " + str(len(pairwise)) + "\n")
        handle.write("No hardware validation is claimed; this is a local executable surrogate audit.\n")


def assert_no_nan(rows: list[dict[str, object]], name: str) -> None:
    for row in rows:
        for key, value in row.items():
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError(f"{name} has non-finite value at {key}: {row}")


def main() -> None:
    raw_rows = [
        simulate_method_group(seed, split, task, failure, method, EPISODES_PER_GROUP)
        for split in SPLITS
        for method in METHODS
        for seed in SEEDS
        for task in TASKS
        for failure in FAILURES
    ]
    assert_no_nan(raw_rows, "seed_task_family_metrics")
    metrics = aggregate(raw_rows, ["method", "split"])
    per_task_family = aggregate(raw_rows, ["method", "split", "task", "failure_family"])
    pairwise = pairwise_stats(raw_rows)
    ablation_seed_rows = [
        simulate_ablation_group(seed, task, failure, ablation)
        for ablation in ABLATIONS
        for seed in SEEDS
        for task in TASKS
        for failure in FAILURES
    ]
    ablation_metrics = aggregate(ablation_seed_rows, ["ablation"])
    sweep_seed_rows, sweep_summary = stress_sweep()
    failures = failure_cases(raw_rows)
    decision = terminal_decision(metrics, pairwise, ablation_metrics)

    write_csv(RESULTS / "seed_task_family_metrics.csv", raw_rows)
    write_csv(RESULTS / "metrics.csv", metrics)
    write_csv(RESULTS / "per_task_family_metrics.csv", per_task_family)
    write_csv(RESULTS / "pairwise_stats.csv", pairwise)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed_rows)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", sweep_seed_rows)
    write_csv(RESULTS / "stress_sweep.csv", sweep_summary)
    write_csv(RESULTS / "failure_cases.csv", failures)

    combined = [row for row in metrics if row["split"] == "combined_abstraction_stress" and row["method"] != "oracle_mechanics_preserving_planner"]
    combined.sort(key=lambda row: float(row["task_success"]), reverse=True)
    make_latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("task_success", "Success"),
            ("mechanical_violation_rate", "Violation"),
            ("damage_unsafe_rate", "Damage"),
            ("abstraction_failure_accuracy", "Fail acc."),
            ("mechanics_retention_recall", "Recall"),
            ("planning_regret_to_oracle", "Regret"),
        ],
    )
    ablation_metrics.sort(key=lambda row: float(row["task_success"]), reverse=True)
    make_latex_table(
        RESULTS / "ablation_table.tex",
        ablation_metrics,
        [
            ("ablation", "Ablation"),
            ("task_success", "Success"),
            ("mechanical_violation_rate", "Violation"),
            ("damage_unsafe_rate", "Damage"),
            ("planning_cost", "Cost"),
            ("planning_regret_to_oracle", "Regret"),
        ],
    )
    decision_pairs = [
        row
        for row in pairwise
        if row["metric"] in {"task_success", "mechanical_violation_rate", "damage_unsafe_rate", "planning_regret_to_oracle"}
        and row["baseline"] in {decision["best_success_baseline"], decision["safest_baseline"], decision["best_regret_baseline"]}
    ]
    make_latex_table(
        RESULTS / "pairwise_decision_table.tex",
        decision_pairs,
        [
            ("baseline", "Baseline"),
            ("metric", "Metric"),
            ("proposed_mean", "Proposed"),
            ("baseline_mean", "Baseline"),
            ("mean_diff_proposed_minus_baseline", "Diff"),
            ("ci95_diff", "CI95"),
            ("winner", "Winner"),
        ],
    )
    plot_figures(metrics, ablation_metrics, sweep_summary)
    write_summary(metrics, pairwise, ablation_metrics, failures, decision)
    print(f"Paper 99 evidence audit complete: {decision['decision']}")
    print("Reasons:")
    for reason in decision["reasons"]:
        print("-", reason)
    print("Wrote results to", RESULTS)


if __name__ == "__main__":
    main()
