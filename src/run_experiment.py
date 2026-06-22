import csv
import hashlib
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 699589046
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

METRIC_FIELDS = [
    "task_success",
    "mechanical_violation_rate",
    "damage_unsafe_rate",
    "abstraction_failure_accuracy",
    "mechanics_retention_recall",
    "early_warning_recall",
    "false_refinement_alarm_rate",
    "planning_cost",
    "planning_regret_to_oracle",
    "robust_utility",
    "intervention_rate",
    "deployment_coverage",
]


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
    Task("articulated_fixture_assembly", 0.29, 0.72, 0.47, 0.67, 0.45, 0.69),
]

FAILURES = [
    FailureFamily("erased_contact_force", True, 0.58, 0.67, 0.71, 0.70, 0.08),
    FailureFamily("hidden_support_relation", True, 0.62, 0.52, 0.66, 0.74, 0.10),
    FailureFamily("clearance_tolerance_collapse", True, 0.69, 0.61, 0.50, 0.86, 0.09),
    FailureFamily("friction_state_aliasing", True, 0.48, 0.46, 0.56, 0.62, 0.13),
    FailureFamily("deformable_constraint_erasure", True, 0.64, 0.75, 0.63, 0.54, 0.12),
    FailureFamily("temporal_precondition_loss", False, 0.30, 0.28, 0.44, 0.38, 0.17),
    FailureFamily("tool_affordance_misabstraction", True, 0.57, 0.59, 0.67, 0.67, 0.11),
    FailureFamily("compliance_recovery_erasure", True, 0.54, 0.64, 0.60, 0.58, 0.14),
]
FAILURE_NAMES = [failure.name for failure in FAILURES]
FAILURE_INDEX = {name: idx for idx, name in enumerate(FAILURE_NAMES)}

SPLITS = [
    Split("nominal_abstraction", 0.00, 0.00, 0.00, 0.00, 0.00, 0.05),
    Split("language_ambiguity_shift", 0.34, 0.15, 0.03, 0.05, 0.04, 0.40),
    Split("predicate_noise_shift", 0.14, 0.34, 0.07, 0.07, 0.04, 0.43),
    Split("geometry_tolerance_shift", 0.05, 0.10, 0.35, 0.08, 0.05, 0.46),
    Split("mechanics_ood_shift", 0.09, 0.12, 0.11, 0.36, 0.07, 0.54),
    Split("object_affordance_transfer", 0.23, 0.18, 0.15, 0.18, 0.09, 0.58),
    Split("recovery_cost_pressure", 0.18, 0.20, 0.16, 0.22, 0.34, 0.64),
    Split("combined_adversarial_abstraction", 0.32, 0.30, 0.32, 0.38, 0.22, 0.78),
]
SPLIT_BY_NAME = {split.name: split for split in SPLITS}
HARD_SPLITS = {
    "mechanics_ood_shift",
    "object_affordance_transfer",
    "recovery_cost_pressure",
    "combined_adversarial_abstraction",
}

METHODS = [
    Method("language_symbolic_planner", 0.18, 0.050, 0.20, -0.12, 0.015),
    Method("vla_direct_policy", 0.31, 0.090, 0.16, -0.05, 0.045),
    Method("neuro_symbolic_predicate_planner", 0.47, 0.100, 0.12, 0.00, 0.075),
    Method("active_relational_abstraction", 0.61, 0.140, 0.11, 0.02, 0.105),
    Method("llm_tamp_failure_reasoning", 0.56, 0.115, 0.12, 0.03, 0.120),
    Method("runtime_monitor_replanner", 0.40, 0.080, 0.13, 0.05, 0.090),
    Method("grounded_geometric_tamp", 0.44, 0.070, 0.09, 0.02, 0.125),
    Method("physics_aware_tamp", 0.50, 0.060, 0.08, 0.01, 0.145),
    Method("affordance_graph_planner", 0.52, 0.090, 0.10, 0.015, 0.110),
    Method("learned_failure_classifier_tamp", 0.66, 0.125, 0.105, 0.015, 0.135),
    Method("semantic_model_predictive_planner", 0.58, 0.085, 0.095, 0.00, 0.140),
    Method("proposed_abstraction_failure_audit_v4", 0.76, 0.165, 0.10, 0.035, 0.135),
    Method("risk_bounded_abstraction_failure_audit_v5", 0.79, 0.155, 0.095, -0.015, 0.160),
    Method("oracle_mechanics_preserving_planner", 0.985, 0.010, 0.025, -0.010, 0.050),
]
METHOD_BY_NAME = {method.name: method for method in METHODS}
NON_ORACLE_METHODS = [method.name for method in METHODS if method.name != "oracle_mechanics_preserving_planner"]
PROPOSED = "risk_bounded_abstraction_failure_audit_v5"
V4 = "proposed_abstraction_failure_audit_v4"
ORACLE = "oracle_mechanics_preserving_planner"

ABLATIONS = [
    "full_risk_bounded_abstraction_failure_audit_v5",
    "v4_abstraction_audit_rules",
    "no_mechanics_taxonomy",
    "no_predicate_refinement",
    "no_calibration",
    "no_cost_model",
    "no_recovery_feasibility_gate",
    "monitor_only",
    "grounded_tamp_only",
    "failure_classifier_only",
]

STRESS_METHODS = [
    "active_relational_abstraction",
    "llm_tamp_failure_reasoning",
    "runtime_monitor_replanner",
    "grounded_geometric_tamp",
    "physics_aware_tamp",
    "semantic_model_predictive_planner",
    V4,
    PROPOSED,
    ORACLE,
]
FIXED_RISK_METHODS = [
    "llm_tamp_failure_reasoning",
    "runtime_monitor_replanner",
    "grounded_geometric_tamp",
    "physics_aware_tamp",
    "semantic_model_predictive_planner",
    "learned_failure_classifier_tamp",
    V4,
    PROPOSED,
]

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
    "recovery_feasibility",
]
MECHANICS_FEATURE_START = 2

FEATURE_TEMPLATES = {
    "erased_contact_force": np.array([0.30, 0.74, 0.90, 0.36, 0.30, 0.42, 0.24, 0.24, 0.22, 0.36]),
    "hidden_support_relation": np.array([0.38, 0.78, 0.34, 0.91, 0.38, 0.24, 0.28, 0.30, 0.22, 0.42]),
    "clearance_tolerance_collapse": np.array([0.24, 0.72, 0.30, 0.42, 0.92, 0.28, 0.24, 0.20, 0.28, 0.38]),
    "friction_state_aliasing": np.array([0.33, 0.70, 0.42, 0.26, 0.32, 0.91, 0.22, 0.24, 0.22, 0.34]),
    "deformable_constraint_erasure": np.array([0.36, 0.68, 0.36, 0.30, 0.36, 0.25, 0.92, 0.22, 0.26, 0.31]),
    "temporal_precondition_loss": np.array([0.55, 0.74, 0.22, 0.30, 0.24, 0.24, 0.22, 0.91, 0.30, 0.46]),
    "tool_affordance_misabstraction": np.array([0.48, 0.76, 0.38, 0.28, 0.32, 0.29, 0.25, 0.30, 0.92, 0.40]),
    "compliance_recovery_erasure": np.array([0.42, 0.72, 0.45, 0.40, 0.34, 0.38, 0.48, 0.36, 0.34, 0.91]),
}

ACTION_NAMES = ["proceed", "refine_predicate", "query_mechanics", "switch_tamp", "monitor_replan", "recover", "abstain"]
PROCEED, REFINE, QUERY, SWITCH_TAMP, MONITOR, RECOVER, ABSTAIN = range(len(ACTION_NAMES))
HEAVY_ACTIONS = {REFINE, QUERY, SWITCH_TAMP, RECOVER, ABSTAIN}


def stable_int(*parts: object) -> int:
    payload = "::".join(str(part) for part in parts).encode("utf-8")
    return int(hashlib.sha256(payload).hexdigest()[:16], 16)


def rng_for(*parts: object) -> np.random.Generator:
    return np.random.default_rng((BASE_SEED + stable_int(*parts)) % (2**32 - 1))


def clamp01(values: np.ndarray | float) -> np.ndarray | float:
    return np.clip(values, 0.001, 0.999)


def sigmoid(values: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-values))


def safe_mean(values: list[float]) -> float:
    return float(np.mean(values)) if values else 0.0


def ci95(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    arr = np.asarray(values, dtype=float)
    return float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr)))


def fmt(value: object) -> object:
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.6f}"
    if isinstance(value, (int, np.integer)):
        return int(value)
    return value


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: fmt(value) for key, value in row.items()})


def open_writer(path: Path, fieldnames: list[str]) -> tuple[object, csv.DictWriter]:
    handle = path.open("w", newline="", encoding="utf-8")
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    return handle, writer


def generate_episodes(
    seed: int,
    task: Task,
    failure: FailureFamily,
    split: Split,
    episodes: int,
    stress_override: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = rng_for("episodes", seed, task.name, failure.name, split.name, stress_override)
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
            split.recovery_cost_shift + 0.04 * (1.0 - task.recovery_margin),
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
            -2.12
            + 1.28 * failure.violation_hazard
            + 0.90 * task.base_difficulty
            + 0.52 * split.mechanics_shift
            + 0.36 * split.geometry_shift
            + 0.24 * features[:, FEATURE_NAMES.index("contact_force")]
            + 0.25 * features[:, FEATURE_NAMES.index("support_relation")]
            + 0.24 * features[:, FEATURE_NAMES.index("clearance")]
            + 0.22 * features[:, FEATURE_NAMES.index("tool_affordance")]
            + 0.18 * abstraction_confidence
            + rng.normal(0.0, 0.12 + 0.04 * stress, size=episodes)
        )
    )
    damage_risk = clamp01(
        sigmoid(
            -2.42
            + 1.18 * failure.damage_hazard
            + 0.74 * task.damage_sensitivity
            + 0.39 * split.mechanics_shift
            + 0.31 * features[:, FEATURE_NAMES.index("deformation")]
            + 0.20 * features[:, FEATURE_NAMES.index("friction")]
            + 0.18 * features[:, FEATURE_NAMES.index("clearance")]
            + 0.16 * features[:, FEATURE_NAMES.index("recovery_feasibility")]
            + rng.normal(0.0, 0.11 + 0.035 * stress, size=episodes)
        )
    )
    return features, violation_risk, damage_risk


def classify_failure(
    method: Method,
    seed: int,
    task: Task,
    failure: FailureFamily,
    split: Split,
    features: np.ndarray,
    stress_override: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    rng = rng_for("classify", method.name, seed, task.name, failure.name, split.name, stress_override)
    stress = split.stress if stress_override is None else stress_override
    mechanics_features = features[:, MECHANICS_FEATURE_START:]
    sorted_features = np.sort(mechanics_features, axis=1)
    gap = sorted_features[:, -1] - sorted_features[:, -2]
    correct_prob = (
        method.failure_acc
        - method.stress_penalty * stress
        - failure.classifier_hardness
        - 0.045 * task.language_ambiguity
        - 0.045 * split.predicate_noise
        + 0.15 * gap
    )
    if method.name in {"grounded_geometric_tamp", "physics_aware_tamp"}:
        correct_prob += 0.04 * (features[:, FEATURE_NAMES.index("clearance")] + features[:, FEATURE_NAMES.index("support_relation")] - 1.0)
    if method.name == ORACLE:
        correct_prob = np.full(len(features), 0.985 - 0.01 * stress)
    correct_prob = clamp01(correct_prob)
    correct = rng.random(len(features)) < correct_prob

    scores = mechanics_features + rng.normal(0.0, 0.12 + 0.06 * stress, size=mechanics_features.shape)
    if method.name in {"language_symbolic_planner", "vla_direct_policy", "neuro_symbolic_predicate_planner"}:
        scores += rng.normal(0.0, 0.20, size=scores.shape)
    predicted = np.argmax(scores, axis=1)
    predicted[correct] = FAILURE_INDEX[failure.name]
    if method.name == ORACLE:
        predicted[:] = FAILURE_INDEX[failure.name]
        correct[:] = True
    return predicted, correct


def predict_failure_risk(
    method: Method,
    seed: int,
    task: Task,
    split: Split,
    violation_risk: np.ndarray,
    damage_risk: np.ndarray,
    features: np.ndarray,
    stress_override: float | None = None,
) -> np.ndarray:
    rng = rng_for("risk", method.name, seed, task.name, split.name, stress_override)
    stress = split.stress if stress_override is None else stress_override
    true_failure = clamp01(0.56 * violation_risk + 0.44 * damage_risk)
    predicted = (
        true_failure
        + method.risk_bias
        + 0.07 * split.predicate_noise
        + 0.05 * task.language_ambiguity
        + 0.09 * (features[:, FEATURE_NAMES.index("language_ambiguity")] - 0.45)
        + rng.normal(0.0, method.risk_noise + 0.035 * stress, size=len(true_failure))
    )
    if method.name == ORACLE:
        predicted = true_failure + rng.normal(0.0, 0.018 + 0.01 * stress, size=len(true_failure))
    return clamp01(predicted)


def choose_actions(
    method_name: str,
    seed: int,
    predicted_failure: np.ndarray,
    predicted_risk: np.ndarray,
    features: np.ndarray,
    stress: float,
    damage_budget: float | None = None,
) -> np.ndarray:
    rng = rng_for("actions", method_name, seed, float(np.mean(predicted_risk)), stress, damage_budget)
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
    compliance = names == "compliance_recovery_erasure"
    actionable = ~temporal

    if method_name == "language_symbolic_planner":
        actions[very_high] = MONITOR
    elif method_name == "vla_direct_policy":
        actions[high_risk & (features[:, FEATURE_NAMES.index("language_ambiguity")] > 0.62)] = MONITOR
        actions[very_high] = RECOVER
    elif method_name == "neuro_symbolic_predicate_planner":
        actions[contact | support | tool] = REFINE
        actions[high_risk & (clearance | deform | compliance)] = SWITCH_TAMP
        actions[very_high] = MONITOR
    elif method_name == "active_relational_abstraction":
        actions[contact | support | temporal | tool] = REFINE
        actions[clearance | deform | compliance | high_risk] = QUERY
        actions[very_high] = SWITCH_TAMP
    elif method_name == "llm_tamp_failure_reasoning":
        actions[high_risk | clearance | support | tool] = SWITCH_TAMP
        actions[contact | deform | compliance] = QUERY
        actions[very_high] = RECOVER
    elif method_name == "runtime_monitor_replanner":
        actions[high_risk | temporal | friction] = MONITOR
        actions[very_high | clearance] = RECOVER
    elif method_name == "grounded_geometric_tamp":
        actions[clearance | support | contact | high_risk] = SWITCH_TAMP
        actions[deform | tool | compliance] = QUERY
        actions[very_high] = RECOVER
    elif method_name == "physics_aware_tamp":
        actions[clearance | support | contact | deform | friction | high_risk] = SWITCH_TAMP
        actions[tool | compliance] = QUERY
        actions[very_high] = RECOVER
    elif method_name == "affordance_graph_planner":
        actions[support | tool | compliance] = QUERY
        actions[clearance | high_risk] = SWITCH_TAMP
        actions[very_high] = RECOVER
    elif method_name == "learned_failure_classifier_tamp":
        actions[actionable & high_risk] = QUERY
        actions[clearance | support | very_high] = SWITCH_TAMP
        actions[very_high & (deform | compliance)] = RECOVER
    elif method_name == "semantic_model_predictive_planner":
        actions[high_risk | clearance | support | compliance] = SWITCH_TAMP
        actions[contact | deform | tool] = QUERY
        actions[very_high] = RECOVER
    elif method_name == V4:
        actions[contact | support | deform | tool | compliance] = REFINE
        actions[clearance] = SWITCH_TAMP
        actions[friction] = QUERY
        actions[temporal] = MONITOR
        actions[very_high] = RECOVER
        alarm = (predicted_risk > 0.52) | (features[:, FEATURE_NAMES.index("predicate_confidence")] > 0.66)
        actions[alarm & (rng.random(len(actions)) < 0.34)] = REFINE
    elif method_name == PROPOSED:
        reliable = predicted_risk > (0.61 + 0.05 * stress)
        actions[reliable & (contact | support | tool)] = REFINE
        actions[reliable & (clearance | deform | compliance)] = SWITCH_TAMP
        actions[reliable & friction] = QUERY
        actions[temporal & (predicted_risk > 0.72)] = MONITOR
        actions[very_high & actionable] = RECOVER
        abstain = (predicted_risk > 0.86) & (features[:, FEATURE_NAMES.index("recovery_feasibility")] < 0.52)
        actions[abstain] = ABSTAIN
    elif method_name == ORACLE:
        actions[contact | support | deform | tool | compliance] = REFINE
        actions[clearance] = SWITCH_TAMP
        actions[friction] = QUERY
        actions[temporal] = MONITOR
        actions[very_high] = RECOVER
    elif method_name == "full_risk_bounded_abstraction_failure_audit_v5":
        return choose_actions(PROPOSED, seed, predicted_failure, predicted_risk, features, stress, damage_budget)
    elif method_name == "v4_abstraction_audit_rules":
        return choose_actions(V4, seed, predicted_failure, predicted_risk, features, stress, damage_budget)
    elif method_name == "no_mechanics_taxonomy":
        actions[high_risk] = QUERY
        actions[very_high] = RECOVER
    elif method_name == "no_predicate_refinement":
        actions[high_risk | clearance | support | deform | compliance] = SWITCH_TAMP
        actions[contact | tool] = QUERY
        actions[very_high] = RECOVER
    elif method_name == "no_calibration":
        actions[actionable & (predicted_risk > 0.55)] = QUERY
        actions[clearance | support | very_high] = SWITCH_TAMP
    elif method_name == "no_cost_model":
        actions[contact | support | deform | tool | compliance] = REFINE
        actions[clearance | high_risk] = SWITCH_TAMP
        actions[very_high] = RECOVER
    elif method_name == "no_recovery_feasibility_gate":
        actions[actionable & high_risk] = QUERY
        actions[clearance | deform | compliance] = SWITCH_TAMP
        actions[very_high] = RECOVER
    elif method_name == "monitor_only":
        actions[high_risk | temporal | friction] = MONITOR
        actions[very_high] = RECOVER
    elif method_name == "grounded_tamp_only":
        actions[clearance | support | contact | deform | high_risk] = SWITCH_TAMP
        actions[very_high] = RECOVER
    elif method_name == "failure_classifier_only":
        actions[actionable & high_risk] = QUERY
        actions[very_high] = RECOVER
    else:
        raise ValueError(f"unknown method {method_name}")

    if damage_budget is not None:
        risk_cut = max(0.36, 0.68 - 1.7 * damage_budget)
        actions[predicted_risk > risk_cut] = np.where(predicted_risk[predicted_risk > risk_cut] > risk_cut + 0.12, ABSTAIN, RECOVER)
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
    abstain = actions == ABSTAIN

    success[proceed] = clamp01(0.95 - 0.96 * violation_risk[proceed] - 0.60 * damage_risk[proceed] - 0.06 * task.mechanics_depth)
    violation[proceed] = clamp01(violation_risk[proceed] + 0.06 * failure.violation_hazard)
    damage[proceed] = clamp01(damage_risk[proceed] + 0.06 * failure.damage_hazard)
    cost[proceed] = 0.035

    refine_bonus = 0.055 if method_name in {V4, "no_cost_model", "v4_abstraction_audit_rules"} else 0.0
    refine_bonus += 0.025 if method_name in {PROPOSED, "full_risk_bounded_abstraction_failure_audit_v5"} else 0.0
    success[refine] = clamp01(
        0.66
        + refine_bonus
        + 0.17 * failure.refinement_value
        - 0.32 * violation_risk[refine]
        - 0.19 * damage_risk[refine]
        - 0.05 * task.language_ambiguity
        - 0.05 * stress
    )
    violation[refine] = clamp01(0.46 * violation_risk[refine])
    damage[refine] = clamp01(0.50 * damage_risk[refine])
    cost[refine] = 0.18 + 0.05 * split.recovery_cost_shift

    success[query] = clamp01(
        0.70
        + 0.13 * failure.refinement_value
        + 0.04 * task.recovery_margin
        - 0.28 * violation_risk[query]
        - 0.20 * damage_risk[query]
        - 0.05 * stress
    )
    violation[query] = clamp01(0.42 * violation_risk[query])
    damage[query] = clamp01(0.45 * damage_risk[query])
    cost[query] = 0.21 + 0.06 * split.recovery_cost_shift

    tamp_bonus = 0.12 if method_name in {"grounded_geometric_tamp", "grounded_tamp_only"} else 0.0
    tamp_bonus += 0.13 if method_name == "physics_aware_tamp" else 0.0
    tamp_bonus += 0.06 if method_name == "llm_tamp_failure_reasoning" else 0.0
    tamp_bonus += 0.05 if method_name == "semantic_model_predictive_planner" else 0.0
    tamp_bonus += 0.04 if method_name == "no_predicate_refinement" else 0.0
    success[switch_tamp] = clamp01(
        0.71
        + tamp_bonus
        + 0.16 * failure.tamp_value
        - 0.23 * violation_risk[switch_tamp]
        - 0.18 * damage_risk[switch_tamp]
        - 0.04 * stress
    )
    violation_scale = 0.27 if method_name == "physics_aware_tamp" else 0.30
    damage_scale = 0.30 if method_name == "physics_aware_tamp" else 0.34
    violation[switch_tamp] = clamp01(violation_scale * violation_risk[switch_tamp])
    damage[switch_tamp] = clamp01(damage_scale * damage_risk[switch_tamp])
    cost[switch_tamp] = 0.25 + 0.08 * task.geometry_tolerance + 0.05 * split.recovery_cost_shift

    success[monitor] = clamp01(0.62 + 0.08 * task.recovery_margin - 0.38 * violation_risk[monitor] - 0.22 * damage_risk[monitor] - 0.04 * stress)
    violation[monitor] = clamp01(0.50 * violation_risk[monitor])
    damage[monitor] = clamp01(0.48 * damage_risk[monitor])
    cost[monitor] = 0.14 + 0.05 * split.recovery_cost_shift

    recover_bonus = 0.09 if method_name == "runtime_monitor_replanner" else 0.0
    recover_bonus += 0.06 if method_name == "llm_tamp_failure_reasoning" else 0.0
    recover_bonus += 0.04 if method_name in {PROPOSED, "full_risk_bounded_abstraction_failure_audit_v5"} else 0.0
    success[recover] = clamp01(0.58 + recover_bonus + 0.12 * task.recovery_margin - 0.20 * violation_risk[recover] - 0.16 * damage_risk[recover] - 0.05 * stress)
    violation[recover] = clamp01(0.24 * violation_risk[recover])
    damage[recover] = clamp01(0.28 * damage_risk[recover])
    cost[recover] = 0.30 + 0.10 * split.recovery_cost_shift

    success[abstain] = 0.001
    violation[abstain] = 0.001
    damage[abstain] = 0.001
    cost[abstain] = 0.16 + 0.05 * split.recovery_cost_shift

    overhead = METHOD_BY_NAME.get(method_name, METHOD_BY_NAME[PROPOSED]).planning_overhead
    if method_name in ABLATIONS:
        overhead = METHOD_BY_NAME[PROPOSED].planning_overhead
    if method_name == "monitor_only":
        overhead = 0.065
    if method_name in {"grounded_tamp_only", "no_predicate_refinement"}:
        overhead = 0.115
    if method_name == "no_cost_model":
        overhead = 0.100
    cost += overhead
    return clamp01(success), clamp01(violation), clamp01(damage), cost


def utility(success: np.ndarray, violation: np.ndarray, damage: np.ndarray, cost: np.ndarray, actions: np.ndarray) -> np.ndarray:
    abstention = (actions == ABSTAIN).astype(float)
    return success - 0.58 * violation - 0.72 * damage - 0.42 * cost - 0.24 * abstention


def oracle_utility(task: Task, failure: FailureFamily, split: Split, violation_risk: np.ndarray, damage_risk: np.ndarray, stress_override: float | None = None) -> np.ndarray:
    utilities = []
    for action_id in range(len(ACTION_NAMES)):
        actions = np.full(len(violation_risk), action_id, dtype=int)
        success, violation, damage, cost = expected_outcome(ORACLE, actions, task, failure, split, violation_risk, damage_risk, stress_override)
        utilities.append(utility(success, violation, damage, cost, actions))
    return np.max(np.vstack(utilities), axis=0)


def simulate_group(
    seed: int,
    task: Task,
    failure: FailureFamily,
    split: Split,
    method_name: str,
    features: np.ndarray,
    violation_risk: np.ndarray,
    damage_risk: np.ndarray,
    oracle_u: np.ndarray,
    stress_override: float | None = None,
    damage_budget: float | None = None,
    raw_writer: csv.DictWriter | None = None,
    raw_extra: dict[str, object] | None = None,
) -> dict[str, object]:
    stress = split.stress if stress_override is None else stress_override
    method = METHOD_BY_NAME.get(method_name, METHOD_BY_NAME[PROPOSED])
    predicted, correct = classify_failure(method, seed, task, failure, split, features, stress_override)
    predicted_risk = predict_failure_risk(method, seed, task, split, violation_risk, damage_risk, features, stress_override)
    actions = choose_actions(method_name, seed, predicted, predicted_risk, features, stress, damage_budget)
    success, violation, damage, cost = expected_outcome(method_name, actions, task, failure, split, violation_risk, damage_risk, stress_override)
    util = utility(success, violation, damage, cost, actions)
    regret = np.maximum(0.0, oracle_u - util)
    heavy = np.isin(actions, list(HEAVY_ACTIONS)).astype(float)
    actionable = 1.0 if failure.actionable else 0.0
    retention = heavy if failure.actionable else np.zeros(len(actions))
    early_warning = ((predicted_risk > 0.58) & (violation_risk + damage_risk > 0.68)).astype(float)
    false_alarm = heavy if not failure.actionable else np.zeros(len(actions))
    if damage_budget is None:
        coverage = ((damage < 0.18) & (violation < 0.24) & (actions != ABSTAIN)).astype(float)
    else:
        coverage = ((damage <= damage_budget) & (violation <= damage_budget + 0.08) & (actions != ABSTAIN)).astype(float)

    if raw_writer is not None:
        extra = raw_extra or {}
        for episode_idx in range(len(actions)):
            row = {
                **extra,
                "seed": seed,
                "task": task.name,
                "failure_family": failure.name,
                "split": split.name,
                "episode": episode_idx,
                "method": method_name,
                "action": ACTION_NAMES[int(actions[episode_idx])],
                "predicted_failure": FAILURE_NAMES[int(predicted[episode_idx])],
                "predicted_risk": predicted_risk[episode_idx],
                "task_success": success[episode_idx],
                "mechanical_violation_rate": violation[episode_idx],
                "damage_unsafe_rate": damage[episode_idx],
                "abstraction_failure_accuracy": float(correct[episode_idx]),
                "mechanics_retention_recall": retention[episode_idx],
                "early_warning_recall": early_warning[episode_idx],
                "false_refinement_alarm_rate": false_alarm[episode_idx],
                "planning_cost": cost[episode_idx],
                "planning_regret_to_oracle": regret[episode_idx],
                "robust_utility": util[episode_idx],
                "intervention_rate": float(actions[episode_idx] != PROCEED),
                "deployment_coverage": coverage[episode_idx],
            }
            raw_writer.writerow({key: fmt(value) for key, value in row.items()})

    return {
        "seed": seed,
        "task": task.name,
        "failure_family": failure.name,
        "split": split.name,
        "method": method_name,
        "n": len(actions),
        "actionable_failure": actionable,
        "task_success": float(np.mean(success)),
        "mechanical_violation_rate": float(np.mean(violation)),
        "damage_unsafe_rate": float(np.mean(damage)),
        "abstraction_failure_accuracy": float(np.mean(correct)),
        "mechanics_retention_recall": float(np.mean(retention)),
        "early_warning_recall": float(np.mean(early_warning)),
        "false_refinement_alarm_rate": float(np.mean(false_alarm)),
        "planning_cost": float(np.mean(cost)),
        "planning_regret_to_oracle": float(np.mean(regret)),
        "robust_utility": float(np.mean(util)),
        "intervention_rate": float(np.mean(actions != PROCEED)),
        "deployment_coverage": float(np.mean(coverage)),
    }


def aggregate(rows: list[dict[str, object]], keys: list[str]) -> list[dict[str, object]]:
    grouped: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    output = []
    for key_values, group in grouped.items():
        out = {key: value for key, value in zip(keys, key_values)}
        out["n"] = len(group)
        for metric in METRIC_FIELDS:
            values = [float(row[metric]) for row in group]
            out[metric] = safe_mean(values)
            out[f"ci95_{metric}"] = ci95(values)
        output.append(out)
    output.sort(key=lambda row: tuple(str(row[key]) for key in keys))
    return output


def pairwise(seed_rows: list[dict[str, object]], proposed_name: str, baselines: list[str], metrics: list[tuple[str, str]]) -> list[dict[str, object]]:
    by_seed_method = {(int(row["seed"]), row["method"]): row for row in seed_rows}
    output = []
    for baseline in baselines:
        if baseline == proposed_name:
            continue
        for metric, direction in metrics:
            diffs = []
            proposed_vals = []
            baseline_vals = []
            for seed in SEEDS:
                p = by_seed_method.get((seed, proposed_name))
                b = by_seed_method.get((seed, baseline))
                if not p or not b:
                    continue
                pv = float(p[metric])
                bv = float(b[metric])
                proposed_vals.append(pv)
                baseline_vals.append(bv)
                diffs.append(pv - bv)
            mean_diff = safe_mean(diffs)
            diff_ci = ci95(diffs)
            if direction == "higher":
                winner = proposed_name if mean_diff > diff_ci else baseline if mean_diff < -diff_ci else "statistical_tie"
            else:
                winner = proposed_name if mean_diff < -diff_ci else baseline if mean_diff > diff_ci else "statistical_tie"
            output.append(
                {
                    "baseline": baseline,
                    "metric": metric,
                    "direction": direction,
                    "v5_mean": safe_mean(proposed_vals),
                    "baseline_mean": safe_mean(baseline_vals),
                    "mean_diff_v5_minus_baseline": mean_diff,
                    "ci95_diff": diff_ci,
                    "winner": winner,
                    "paired_seeds": len(diffs),
                }
            )
    return output


def run_main() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    dataset_fields = [
        "seed",
        "task",
        "failure_family",
        "split",
        "episode",
        *FEATURE_NAMES,
        "violation_risk",
        "damage_risk",
    ]
    rollout_fields = [
        "seed",
        "task",
        "failure_family",
        "split",
        "episode",
        "method",
        "action",
        "predicted_failure",
        "predicted_risk",
        *METRIC_FIELDS,
    ]
    dataset_handle, dataset_writer = open_writer(RESULTS / "dataset_summary.csv", dataset_fields)
    rollout_handle, rollout_writer = open_writer(RESULTS / "rollouts.csv", rollout_fields)
    group_rows = []
    try:
        for seed in SEEDS:
            for task in TASKS:
                for failure in FAILURES:
                    for split in SPLITS:
                        features, violation_risk, damage_risk = generate_episodes(seed, task, failure, split, EPISODES_PER_CELL)
                        oracle_u = oracle_utility(task, failure, split, violation_risk, damage_risk)
                        for episode_idx in range(EPISODES_PER_CELL):
                            dataset_writer.writerow(
                                {
                                    "seed": seed,
                                    "task": task.name,
                                    "failure_family": failure.name,
                                    "split": split.name,
                                    "episode": episode_idx,
                                    **{name: fmt(features[episode_idx, idx]) for idx, name in enumerate(FEATURE_NAMES)},
                                    "violation_risk": fmt(violation_risk[episode_idx]),
                                    "damage_risk": fmt(damage_risk[episode_idx]),
                                }
                            )
                        for method in METHODS:
                            group_rows.append(
                                simulate_group(seed, task, failure, split, method.name, features, violation_risk, damage_risk, oracle_u, raw_writer=rollout_writer)
                            )
    finally:
        dataset_handle.close()
        rollout_handle.close()

    main_seed = aggregate(group_rows, ["method", "split", "seed"])
    metrics = aggregate(main_seed, ["method", "split"])
    per_task_family = aggregate(group_rows, ["method", "split", "task", "failure_family"])
    hard_group = [row for row in group_rows if row["split"] in HARD_SPLITS]
    hard_seed = aggregate(hard_group, ["method", "seed"])
    hard_metrics = aggregate(hard_seed, ["method"])
    return group_rows, main_seed, metrics, per_task_family, hard_seed, hard_metrics


def run_ablations() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    fields = ["seed", "task", "failure_family", "split", "episode", "method", "action", "predicted_failure", "predicted_risk", *METRIC_FIELDS]
    handle, writer = open_writer(RESULTS / "ablation_rollouts.csv", fields)
    rows = []
    hard_splits = [split for split in SPLITS if split.name in HARD_SPLITS]
    try:
        for ablation in ABLATIONS:
            for seed in SEEDS:
                for task in TASKS:
                    for failure in FAILURES:
                        for split in hard_splits:
                            features, violation_risk, damage_risk = generate_episodes(seed, task, failure, split, EPISODES_PER_CELL)
                            oracle_u = oracle_utility(task, failure, split, violation_risk, damage_risk)
                            rows.append(simulate_group(seed, task, failure, split, ablation, features, violation_risk, damage_risk, oracle_u, raw_writer=writer))
    finally:
        handle.close()
    seed_rows = aggregate(rows, ["method", "seed"])
    return seed_rows, aggregate(seed_rows, ["method"])


def run_stress() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    fields = ["stress_level", "seed", "task", "failure_family", "split", "episode", "method", "action", "predicted_failure", "predicted_risk", *METRIC_FIELDS]
    handle, writer = open_writer(RESULTS / "stress_sweep_raw.csv", fields)
    seed_rows = []
    split = SPLIT_BY_NAME["combined_adversarial_abstraction"]
    stress_levels = [round(value, 2) for value in np.linspace(0.0, 1.0, 10)]
    try:
        for stress in stress_levels:
            for method_name in STRESS_METHODS:
                for seed in SEEDS:
                    group_rows = []
                    for task in TASKS:
                        for failure in FAILURES:
                            features, violation_risk, damage_risk = generate_episodes(seed, task, failure, split, EPISODES_PER_CELL, stress)
                            oracle_u = oracle_utility(task, failure, split, violation_risk, damage_risk, stress)
                            group_rows.append(
                                simulate_group(
                                    seed,
                                    task,
                                    failure,
                                    split,
                                    method_name,
                                    features,
                                    violation_risk,
                                    damage_risk,
                                    oracle_u,
                                    stress_override=stress,
                                    raw_writer=writer,
                                    raw_extra={"stress_level": stress},
                                )
                            )
                    row = aggregate(group_rows, ["method", "seed"])[0]
                    row["stress_level"] = stress
                    seed_rows.append(row)
    finally:
        handle.close()
    summary = aggregate(seed_rows, ["method", "stress_level"])
    return seed_rows, summary


def run_fixed_risk() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    fields = ["damage_budget", "seed", "task", "failure_family", "split", "episode", "method", "action", "predicted_failure", "predicted_risk", *METRIC_FIELDS]
    handle, writer = open_writer(RESULTS / "fixed_risk_raw.csv", fields)
    seed_rows = []
    split = SPLIT_BY_NAME["combined_adversarial_abstraction"]
    budgets = [0.0, 0.02, 0.05, 0.08, 0.10, 0.15]
    try:
        for budget in budgets:
            for method_name in FIXED_RISK_METHODS:
                for seed in SEEDS:
                    group_rows = []
                    for task in TASKS:
                        for failure in FAILURES:
                            features, violation_risk, damage_risk = generate_episodes(seed, task, failure, split, EPISODES_PER_CELL)
                            oracle_u = oracle_utility(task, failure, split, violation_risk, damage_risk)
                            group_rows.append(
                                simulate_group(
                                    seed,
                                    task,
                                    failure,
                                    split,
                                    method_name,
                                    features,
                                    violation_risk,
                                    damage_risk,
                                    oracle_u,
                                    damage_budget=budget,
                                    raw_writer=writer,
                                    raw_extra={"damage_budget": budget},
                                )
                            )
                    row = aggregate(group_rows, ["method", "seed"])[0]
                    row["damage_budget"] = budget
                    seed_rows.append(row)
    finally:
        handle.close()
    metrics = aggregate(seed_rows, ["method", "damage_budget"])
    budget_seed_rows = [row for row in seed_rows if abs(float(row["damage_budget"]) - 0.05) < 1e-9]
    pairs = pairwise(
        budget_seed_rows,
        PROPOSED,
        [method for method in FIXED_RISK_METHODS if method != PROPOSED],
        [
            ("task_success", "higher"),
            ("mechanical_violation_rate", "lower"),
            ("damage_unsafe_rate", "lower"),
            ("planning_regret_to_oracle", "lower"),
            ("robust_utility", "higher"),
            ("deployment_coverage", "higher"),
            ("planning_cost", "lower"),
            ("intervention_rate", "lower"),
        ],
    )
    return seed_rows, metrics, pairs


def negative_cases(group_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    selected = [
        row
        for row in group_rows
        if row["split"] in HARD_SPLITS
        and row["method"] == PROPOSED
        and (
            float(row["task_success"]) < 0.48
            or float(row["damage_unsafe_rate"]) > 0.24
            or float(row["mechanical_violation_rate"]) > 0.30
            or float(row["planning_regret_to_oracle"]) > 0.30
        )
    ]
    selected.sort(key=lambda row: (-float(row["planning_regret_to_oracle"]), -float(row["damage_unsafe_rate"]), float(row["task_success"])))
    cases = []
    for idx, row in enumerate(selected[:24], start=1):
        family = row["failure_family"]
        if family == "temporal_precondition_loss":
            reason = "risk-bounded auditing still spends effort on a mostly temporal nuisance"
        elif family in {"clearance_tolerance_collapse", "hidden_support_relation"}:
            reason = "grounded or physics-aware TAMP captures the mechanics with lower regret"
        elif family == "deformable_constraint_erasure":
            reason = "deformation risk remains high despite detecting the erased mechanics"
        elif family == "compliance_recovery_erasure":
            reason = "recovery feasibility is too uncertain for reliable deployment coverage"
        else:
            reason = "mechanics detection does not offset refinement/query cost"
        cases.append(
            {
                "case_id": idx,
                "split": row["split"],
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


def table_escape(value: object) -> str:
    text = str(value)
    return text.replace("_", "\\_")


def make_latex_table(path: Path, rows: list[dict[str, object]], columns: list[tuple[str, str]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write("\\begin{tabular}{" + "l" * len(columns) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            handle.write(" & ".join(table_escape(fmt(row[key])) for key, _ in columns) + " \\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")


def plot_figures(hard_metrics: list[dict[str, object]], ablations: list[dict[str, object]], stress: list[dict[str, object]], fixed: list[dict[str, object]]) -> None:
    non_oracle = [row for row in sorted(hard_metrics, key=lambda r: float(r["task_success"]), reverse=True) if row["method"] != ORACLE]
    methods = [row["method"].replace("_", "\n") for row in non_oracle]
    x = np.arange(len(non_oracle))

    plt.figure(figsize=(13, 5))
    plt.bar(x - 0.2, [float(row["task_success"]) for row in non_oracle], width=0.2, label="success")
    plt.bar(x, [float(row["mechanical_violation_rate"]) for row in non_oracle], width=0.2, label="violation")
    plt.bar(x + 0.2, [float(row["damage_unsafe_rate"]) for row in non_oracle], width=0.2, label="damage")
    plt.xticks(x, methods, fontsize=7)
    plt.ylim(0, 1.0)
    plt.title("Hard-split closed-loop outcomes")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_v5_hard_outcomes.png", dpi=180)
    plt.close()

    plt.figure(figsize=(13, 5))
    plt.bar(x - 0.25, [float(row["abstraction_failure_accuracy"]) for row in non_oracle], width=0.25, label="failure accuracy")
    plt.bar(x, [float(row["mechanics_retention_recall"]) for row in non_oracle], width=0.25, label="retention recall")
    plt.bar(x + 0.25, [float(row["false_refinement_alarm_rate"]) for row in non_oracle], width=0.25, label="false refinement")
    plt.xticks(x, methods, fontsize=7)
    plt.ylim(0, 1.0)
    plt.title("Hard-split abstraction diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_v5_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(13, 5))
    plt.bar(x - 0.2, [float(row["planning_regret_to_oracle"]) for row in non_oracle], width=0.2, label="regret")
    plt.bar(x, [float(row["planning_cost"]) for row in non_oracle], width=0.2, label="cost")
    plt.bar(x + 0.2, [float(row["robust_utility"]) for row in non_oracle], width=0.2, label="utility")
    plt.xticks(x, methods, fontsize=7)
    plt.title("Hard-split cost, regret, and robust utility")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_v5_utility_regret.png", dpi=180)
    plt.close()

    ablation_rows = sorted(ablations, key=lambda row: float(row["task_success"]), reverse=True)
    ax = np.arange(len(ablation_rows))
    plt.figure(figsize=(12, 5))
    plt.bar(ax - 0.2, [float(row["task_success"]) for row in ablation_rows], width=0.2, label="success")
    plt.bar(ax, [float(row["planning_regret_to_oracle"]) for row in ablation_rows], width=0.2, label="regret")
    plt.bar(ax + 0.2, [float(row["robust_utility"]) for row in ablation_rows], width=0.2, label="utility")
    plt.xticks(ax, [row["method"].replace("_", "\n") for row in ablation_rows], fontsize=7)
    plt.title("V5 mechanism ablations")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_v5_ablation.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5))
    for method in [m for m in STRESS_METHODS if m != ORACLE]:
        rows = sorted([row for row in stress if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in rows], [float(row["task_success"]) for row in rows], marker="o", label=method.replace("_", " "))
    plt.xlabel("Combined stress level")
    plt.ylabel("Task success")
    plt.ylim(0, 1.0)
    plt.title("Stress sweep")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_v5_stress_sweep.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5))
    for method in FIXED_RISK_METHODS:
        rows = sorted([row for row in fixed if row["method"] == method], key=lambda row: float(row["damage_budget"]))
        plt.plot([float(row["damage_budget"]) for row in rows], [float(row["deployment_coverage"]) for row in rows], marker="o", label=method.replace("_", " "))
    plt.xlabel("Damage budget")
    plt.ylabel("Deployment coverage")
    plt.ylim(0, 1.0)
    plt.title("Fixed-damage deployment coverage")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "abstraction_v5_fixed_risk.png", dpi=180)
    plt.close()


def decision_summary(
    hard_metrics: list[dict[str, object]],
    hard_pairwise: list[dict[str, object]],
    ablations: list[dict[str, object]],
    stress_metrics: list[dict[str, object]],
    fixed_metrics: list[dict[str, object]],
) -> dict[str, object]:
    by_method = {row["method"]: row for row in hard_metrics}
    v5 = by_method[PROPOSED]
    refs = {name: row for name, row in by_method.items() if name not in {PROPOSED, ORACLE}}
    best_success_name, best_success = max(refs.items(), key=lambda item: float(item[1]["task_success"]))
    best_violation_name, best_violation = min(refs.items(), key=lambda item: float(item[1]["mechanical_violation_rate"]))
    best_damage_name, best_damage = min(refs.items(), key=lambda item: float(item[1]["damage_unsafe_rate"]))
    best_regret_name, best_regret = min(refs.items(), key=lambda item: float(item[1]["planning_regret_to_oracle"]))
    best_utility_name, best_utility = max(refs.items(), key=lambda item: float(item[1]["robust_utility"]))
    best_warning_name, best_warning = max(refs.items(), key=lambda item: float(item[1]["early_warning_recall"]))

    full = {row["method"]: row for row in ablations}["full_risk_bounded_abstraction_failure_audit_v5"]
    ablation_beats = [
        row["method"]
        for row in ablations
        if row["method"] != "full_risk_bounded_abstraction_failure_audit_v5"
        and (
            float(row["task_success"]) >= float(full["task_success"])
            or float(row["planning_regret_to_oracle"]) <= float(full["planning_regret_to_oracle"])
            or float(row["robust_utility"]) >= float(full["robust_utility"])
        )
    ]

    max_stress_rows = [row for row in stress_metrics if abs(float(row["stress_level"]) - 1.0) < 1e-9 and row["method"] != ORACLE]
    max_stress_ref = max(max_stress_rows, key=lambda row: float(row["robust_utility"]))
    fixed_budget_rows = [row for row in fixed_metrics if abs(float(row["damage_budget"]) - 0.05) < 1e-9]
    fixed_ref = max([row for row in fixed_budget_rows if row["method"] != PROPOSED], key=lambda row: float(row["deployment_coverage"]))
    fixed_v5 = [row for row in fixed_budget_rows if row["method"] == PROPOSED][0]

    gates = {
        "success_gate": float(v5["task_success"]) > float(best_success["task_success"]) + 0.01,
        "violation_gate": float(v5["mechanical_violation_rate"]) < float(best_violation["mechanical_violation_rate"]) - 0.005,
        "damage_gate": float(v5["damage_unsafe_rate"]) < float(best_damage["damage_unsafe_rate"]) - 0.005,
        "regret_gate": float(v5["planning_regret_to_oracle"]) < float(best_regret["planning_regret_to_oracle"]) - 0.005,
        "utility_gate": float(v5["robust_utility"]) > float(best_utility["robust_utility"]) + 0.005,
        "diagnostic_gate": (
            float(v5["abstraction_failure_accuracy"]) >= max(float(row["abstraction_failure_accuracy"]) for row in refs.values()) - 0.015
            and float(v5["early_warning_recall"]) >= float(best_warning["early_warning_recall"]) - 0.02
            and float(v5["false_refinement_alarm_rate"]) < 0.08
        ),
        "false_alarm_gate": float(v5["false_refinement_alarm_rate"]) < 0.08,
        "cost_gate": float(v5["planning_cost"]) <= float(best_success["planning_cost"]) + 0.08,
        "ablation_gate": not ablation_beats,
        "stress_gate": max_stress_ref["method"] == PROPOSED,
        "fixed_risk_gate": (
            float(fixed_v5["deployment_coverage"]) >= float(fixed_ref["deployment_coverage"]) + 0.02
            and float(fixed_v5["deployment_coverage"]) > 0.40
        ),
        "scope_gate": False,
    }
    empirical_gates = [value for key, value in gates.items() if key != "scope_gate"]
    decision = "STRONG_REVISE" if all(empirical_gates) else "KILL_ARCHIVE"
    reasons = []
    if not gates["success_gate"]:
        reasons.append(f"v5 hard success {float(v5['task_success']):.5f} does not beat {best_success_name} {float(best_success['task_success']):.5f}")
    if not gates["violation_gate"]:
        reasons.append(f"v5 mechanical violation {float(v5['mechanical_violation_rate']):.5f} does not improve over {best_violation_name} {float(best_violation['mechanical_violation_rate']):.5f}")
    if not gates["damage_gate"]:
        reasons.append(f"v5 damage {float(v5['damage_unsafe_rate']):.5f} does not improve over {best_damage_name} {float(best_damage['damage_unsafe_rate']):.5f}")
    if not gates["regret_gate"]:
        reasons.append(f"v5 regret {float(v5['planning_regret_to_oracle']):.5f} trails {best_regret_name} {float(best_regret['planning_regret_to_oracle']):.5f}")
    if not gates["utility_gate"]:
        reasons.append(f"v5 utility {float(v5['robust_utility']):.5f} trails {best_utility_name} {float(best_utility['robust_utility']):.5f}")
    if not gates["diagnostic_gate"]:
        reasons.append("v5 diagnostics do not clear the frozen accuracy/early-warning/false-alarm gate")
    if not gates["ablation_gate"]:
        reasons.append("ablations match or beat full: " + ", ".join(ablation_beats))
    if not gates["stress_gate"]:
        reasons.append(f"maximum-stress robust utility is dominated by {max_stress_ref['method']}")
    if not gates["fixed_risk_gate"]:
        reasons.append(f"fixed-damage budget 0.05 is dominated by {fixed_ref['method']} or has insufficient coverage")
    reasons.append("scope gate fails because no real robot, accepted high-fidelity benchmark, external benchmark, or trained checkpoint evidence exists")
    return {
        "decision": decision,
        "iclr_main_ready": "no",
        "gates": gates,
        "reasons": reasons,
        "best_success_reference": best_success_name,
        "best_violation_reference": best_violation_name,
        "best_damage_reference": best_damage_name,
        "best_regret_reference": best_regret_name,
        "best_utility_reference": best_utility_name,
        "best_warning_reference": best_warning_name,
        "max_stress_reference": max_stress_ref["method"],
        "fixed_risk_reference": fixed_ref["method"],
        "v5": v5,
    }


def write_tables(
    hard_metrics: list[dict[str, object]],
    hard_pairwise: list[dict[str, object]],
    ablations: list[dict[str, object]],
    stress_metrics: list[dict[str, object]],
    fixed_metrics: list[dict[str, object]],
    cases: list[dict[str, object]],
    decision: dict[str, object],
) -> None:
    hard_sorted = sorted(hard_metrics, key=lambda row: float(row["task_success"]), reverse=True)
    make_latex_table(
        RESULTS / "hard_aggregate_table.tex",
        hard_sorted,
        [
            ("method", "Method"),
            ("task_success", "Success"),
            ("mechanical_violation_rate", "Violation"),
            ("damage_unsafe_rate", "Damage"),
            ("early_warning_recall", "Warn"),
            ("false_refinement_alarm_rate", "False alarm"),
            ("planning_regret_to_oracle", "Regret"),
            ("robust_utility", "Utility"),
        ],
    )
    make_latex_table(RESULTS / "combined_stress_table.tex", hard_sorted, [("method", "Method"), ("task_success", "Success"), ("mechanical_violation_rate", "Violation"), ("damage_unsafe_rate", "Damage"), ("planning_regret_to_oracle", "Regret")])
    decision_pairs = [
        row
        for row in hard_pairwise
        if row["metric"] in {"task_success", "mechanical_violation_rate", "damage_unsafe_rate", "planning_regret_to_oracle", "robust_utility", "abstraction_failure_accuracy", "false_refinement_alarm_rate"}
        and row["baseline"] in {decision["best_success_reference"], decision["best_violation_reference"], decision["best_damage_reference"], decision["best_regret_reference"], decision["best_utility_reference"]}
    ]
    make_latex_table(
        RESULTS / "pairwise_decision_table.tex",
        decision_pairs[:14],
        [
            ("baseline", "Baseline"),
            ("metric", "Metric"),
            ("v5_mean", "V5"),
            ("baseline_mean", "Baseline"),
            ("mean_diff_v5_minus_baseline", "Diff"),
            ("ci95_diff", "CI95"),
            ("winner", "Winner"),
        ],
    )
    make_latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablations, key=lambda row: float(row["task_success"]), reverse=True),
        [
            ("method", "Ablation"),
            ("task_success", "Success"),
            ("damage_unsafe_rate", "Damage"),
            ("planning_regret_to_oracle", "Regret"),
            ("robust_utility", "Utility"),
            ("false_refinement_alarm_rate", "False alarm"),
        ],
    )
    make_latex_table(
        RESULTS / "stress_table.tex",
        [row for row in stress_metrics if abs(float(row["stress_level"]) - 1.0) < 1e-9],
        [("method", "Method"), ("stress_level", "Stress"), ("task_success", "Success"), ("damage_unsafe_rate", "Damage"), ("planning_regret_to_oracle", "Regret"), ("robust_utility", "Utility")],
    )
    make_latex_table(
        RESULTS / "fixed_risk_table.tex",
        [row for row in fixed_metrics if abs(float(row["damage_budget"]) - 0.05) < 1e-9],
        [("method", "Method"), ("damage_budget", "Budget"), ("task_success", "Success"), ("damage_unsafe_rate", "Damage"), ("deployment_coverage", "Coverage"), ("robust_utility", "Utility")],
    )
    make_latex_table(
        RESULTS / "negative_cases_table.tex",
        cases[:8],
        [("split", "Split"), ("task", "Task"), ("failure_family", "Failure"), ("task_success", "Success"), ("damage_unsafe_rate", "Damage"), ("planning_regret_to_oracle", "Regret"), ("failure_mode", "Failure")],
    )


def write_summary(counts: dict[str, int], hard_metrics: list[dict[str, object]], ablations: list[dict[str, object]], cases: list[dict[str, object]], decision: dict[str, object]) -> None:
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 99: embodied_abstraction_failure_modes expanded v5 evidence audit\n")
        handle.write(f"Terminal decision: {decision['decision']}\n")
        handle.write("ICLR main ready: no\n")
        handle.write("Design: 6 tasks x 8 abstraction-failure families x 8 splits x 14 methods, 10 seeds, 6 episodes per seed/task/failure/split/method cell.\n")
        handle.write("Claim under test: risk-bounded mechanics-aware abstraction auditing should improve robot planning beyond VLA, neuro-symbolic, relational-abstraction, LLM-TAMP, grounded TAMP, semantic MPC, and monitoring baselines.\n\n")
        handle.write("Row counts:\n")
        for key, value in counts.items():
            handle.write(f"- {key}: {value}\n")
        handle.write("\nHard-aggregate evidence:\n")
        for row in sorted(hard_metrics, key=lambda item: float(item["task_success"]), reverse=True):
            handle.write(
                f"- {row['method']}: success={float(row['task_success']):.5f} +/- {float(row['ci95_task_success']):.5f}, "
                f"violation={float(row['mechanical_violation_rate']):.5f}, damage={float(row['damage_unsafe_rate']):.5f}, "
                f"failure_acc={float(row['abstraction_failure_accuracy']):.5f}, warning={float(row['early_warning_recall']):.5f}, "
                f"false_alarm={float(row['false_refinement_alarm_rate']):.5f}, cost={float(row['planning_cost']):.5f}, "
                f"regret={float(row['planning_regret_to_oracle']):.5f}, utility={float(row['robust_utility']):.5f}\n"
            )
        handle.write("\nReference winners:\n")
        for key in ["best_success_reference", "best_violation_reference", "best_damage_reference", "best_regret_reference", "best_utility_reference", "best_warning_reference", "max_stress_reference", "fixed_risk_reference"]:
            handle.write(f"- {key}={decision[key]}\n")
        v5 = decision["v5"]
        handle.write(f"- v5_success={float(v5['task_success']):.5f}\n")
        handle.write(f"- v5_violation={float(v5['mechanical_violation_rate']):.5f}\n")
        handle.write(f"- v5_damage={float(v5['damage_unsafe_rate']):.5f}\n")
        handle.write(f"- v5_regret={float(v5['planning_regret_to_oracle']):.5f}\n")
        handle.write(f"- v5_utility={float(v5['robust_utility']):.5f}\n")
        handle.write("\nGate outcomes:\n")
        for key, value in decision["gates"].items():
            handle.write(f"- {key}: {value}\n")
        handle.write("\nTerminal rationale:\n")
        for reason in decision["reasons"]:
            handle.write(f"- {reason}\n")
        handle.write("\nAblation summary:\n")
        for row in sorted(ablations, key=lambda item: float(item["task_success"]), reverse=True):
            handle.write(
                f"- {row['method']}: success={float(row['task_success']):.5f}, damage={float(row['damage_unsafe_rate']):.5f}, "
                f"regret={float(row['planning_regret_to_oracle']):.5f}, utility={float(row['robust_utility']):.5f}, "
                f"false_alarm={float(row['false_refinement_alarm_rate']):.5f}\n"
            )
        handle.write("\nRepresentative negative cases:\n")
        for row in cases[:8]:
            handle.write(
                f"- {row['split']} / {row['task']} / {row['failure_family']} seed {row['seed']}: "
                f"success={float(row['task_success']):.5f}, violation={float(row['mechanical_violation_rate']):.5f}, "
                f"damage={float(row['damage_unsafe_rate']):.5f}, regret={float(row['planning_regret_to_oracle']):.5f}; {row['failure_mode']}\n"
            )
        handle.write("\nNo hardware validation is claimed; this is a local CPU-only executable surrogate audit.\n")
        handle.write(f"terminal={decision['decision']}\n")


def assert_no_nan(rows: list[dict[str, object]], name: str) -> None:
    for row in rows:
        for key, value in row.items():
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError(f"{name} has non-finite value at {key}: {row}")


def main() -> None:
    group_rows, main_seed, metrics, per_task_family, hard_seed, hard_metrics = run_main()
    hard_pairwise = pairwise(
        hard_seed,
        PROPOSED,
        [method for method in NON_ORACLE_METHODS if method != PROPOSED],
        [
            ("task_success", "higher"),
            ("mechanical_violation_rate", "lower"),
            ("damage_unsafe_rate", "lower"),
            ("planning_regret_to_oracle", "lower"),
            ("robust_utility", "higher"),
            ("abstraction_failure_accuracy", "higher"),
            ("early_warning_recall", "higher"),
            ("false_refinement_alarm_rate", "lower"),
        ],
    )
    ablation_seed, ablation_metrics = run_ablations()
    stress_seed, stress_metrics = run_stress()
    fixed_seed, fixed_metrics, fixed_pairwise = run_fixed_risk()
    cases = negative_cases(group_rows)
    decision = decision_summary(hard_metrics, hard_pairwise, ablation_metrics, stress_metrics, fixed_metrics)

    assert_no_nan(group_rows, "main_group_metrics")
    assert_no_nan(main_seed, "main_seed_metrics")
    assert_no_nan(metrics, "metrics")
    assert_no_nan(per_task_family, "per_task_family_metrics")
    assert_no_nan(hard_seed, "hard_aggregate_seed_metrics")
    assert_no_nan(hard_metrics, "hard_aggregate_metrics")
    assert_no_nan(ablation_seed, "ablation_seed_metrics")
    assert_no_nan(ablation_metrics, "ablation_metrics")
    assert_no_nan(stress_seed, "stress_sweep_seed_metrics")
    assert_no_nan(stress_metrics, "stress_sweep")
    assert_no_nan(fixed_seed, "fixed_risk_seed_metrics")
    assert_no_nan(fixed_metrics, "fixed_risk_metrics")

    write_csv(RESULTS / "main_group_metrics.csv", group_rows)
    write_csv(RESULTS / "main_seed_metrics.csv", main_seed)
    write_csv(RESULTS / "metrics.csv", metrics)
    write_csv(RESULTS / "per_task_family_metrics.csv", per_task_family)
    write_csv(RESULTS / "seed_task_family_metrics.csv", group_rows)
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", hard_seed)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics)
    write_csv(RESULTS / "pairwise_stats.csv", hard_pairwise)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed)
    write_csv(RESULTS / "stress_sweep.csv", stress_metrics)
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", fixed_seed)
    write_csv(RESULTS / "fixed_risk_metrics.csv", fixed_metrics)
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", fixed_pairwise)
    write_csv(RESULTS / "failure_cases.csv", cases)

    counts = {
        "dataset_summary_rows": len(SEEDS) * len(TASKS) * len(FAILURES) * len(SPLITS) * EPISODES_PER_CELL,
        "main_rollout_rows": len(SEEDS) * len(TASKS) * len(FAILURES) * len(SPLITS) * len(METHODS) * EPISODES_PER_CELL,
        "main_group_rows": len(group_rows),
        "main_seed_metric_rows": len(main_seed),
        "main_metric_rows": len(metrics),
        "hard_seed_rows": len(hard_seed),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(hard_pairwise),
        "ablation_rollout_rows": len(SEEDS) * len(TASKS) * len(FAILURES) * len(HARD_SPLITS) * len(ABLATIONS) * EPISODES_PER_CELL,
        "ablation_seed_rows": len(ablation_seed),
        "ablation_metric_rows": len(ablation_metrics),
        "stress_rollout_rows": len(SEEDS) * len(TASKS) * len(FAILURES) * 10 * len(STRESS_METHODS) * EPISODES_PER_CELL,
        "stress_seed_rows": len(stress_seed),
        "stress_metric_rows": len(stress_metrics),
        "fixed_risk_rows": len(SEEDS) * len(TASKS) * len(FAILURES) * 6 * len(FIXED_RISK_METHODS) * EPISODES_PER_CELL,
        "fixed_risk_seed_rows": len(fixed_seed),
        "fixed_risk_metric_rows": len(fixed_metrics),
        "fixed_risk_pairwise_rows": len(fixed_pairwise),
        "negative_cases": len(cases),
    }
    write_tables(hard_metrics, hard_pairwise, ablation_metrics, stress_metrics, fixed_metrics, cases, decision)
    plot_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics)
    write_summary(counts, hard_metrics, ablation_metrics, cases, decision)

    print(f"Paper 99 expanded v5 evidence audit complete: {decision['decision']}")
    print("ICLR main ready: no")
    print("Reasons:")
    for reason in decision["reasons"]:
        print("-", reason)
    print("Wrote results to", RESULTS)


if __name__ == "__main__":
    main()
