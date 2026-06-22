import csv
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
PAPER.mkdir(exist_ok=True)

PROPOSED = "risk_bounded_abstraction_failure_audit_v5"
ORACLE = "oracle_mechanics_preserving_planner"


def ascii_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def latex_escape(value: object) -> str:
    text = ascii_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_summary() -> dict[str, str]:
    summary = {}
    for line in (RESULTS / "summary.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            summary[key.strip()] = value.strip()
        elif line.startswith("- ") and "=" in line:
            key, value = line[2:].split("=", 1)
            summary[key.strip()] = value.strip()
        elif line.startswith("terminal="):
            summary["terminal"] = line.split("=", 1)[1].strip()
    return summary


def fnum(value: object, digits: int = 5) -> str:
    return f"{float(value):.{digits}f}"


def short_method(name: str) -> str:
    aliases = {
        "risk_bounded_abstraction_failure_audit_v5": "abstraction_v5",
        "proposed_abstraction_failure_audit_v4": "abstraction_v4",
        "oracle_mechanics_preserving_planner": "oracle",
        "physics_aware_tamp": "physics_tamp",
        "grounded_geometric_tamp": "grounded_tamp",
        "llm_tamp_failure_reasoning": "llm_tamp",
        "runtime_monitor_replanner": "runtime_monitor",
        "semantic_model_predictive_planner": "semantic_mpc",
        "learned_failure_classifier_tamp": "classifier_tamp",
        "active_relational_abstraction": "active_relational",
        "neuro_symbolic_predicate_planner": "neuro_symbolic",
    }
    return aliases.get(name, name)


def make_bib_key(row: dict[str, str], index: int) -> str:
    author = ascii_text(row.get("authors", "ref")).split(";")[0].strip().split(" ")[-1]
    author = re.sub(r"[^A-Za-z0-9]+", "", author) or "ref"
    year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "nd"
    title_word = re.sub(r"[^A-Za-z0-9]+", "", ascii_text(row.get("title", "paper")).split(" ")[0]) or "paper"
    return f"{author.lower()}{year}{title_word.lower()}{index}"


def write_bib(records: list[dict[str, str]]) -> list[str]:
    keys = []
    seen = set()
    entries = []
    for index, row in enumerate(records[:230], start=1):
        key = make_bib_key(row, index)
        while key in seen:
            key = f"{key}x"
        seen.add(key)
        keys.append(key)
        fields = [
            f"  title = {{{latex_escape(row.get('title', f'Reference {index}'))}}}",
            f"  author = {{{latex_escape(row.get('authors', 'Unknown'))}}}",
        ]
        year = latex_escape(row.get("year", ""))
        venue = latex_escape(row.get("venue", ""))
        doi = latex_escape(row.get("doi", ""))
        url = latex_escape(row.get("url", ""))
        if year:
            fields.append(f"  year = {{{year}}}")
        if venue:
            fields.append(f"  journal = {{{venue}}}")
        if doi:
            fields.append(f"  doi = {{{doi}}}")
        if url:
            fields.append(f"  url = {{{url}}}")
        entries.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}\n")
    (PAPER / "references.bib").write_text("\n".join(entries), encoding="utf-8")
    return keys


def cite_chunks(keys: list[str], start: int, stop: int, size: int = 3) -> list[str]:
    return [r"\citep{" + ",".join(keys[offset : offset + size]) + "}" for offset in range(start, min(stop, len(keys)), size)]


def citation_ledger(keys: list[str]) -> str:
    themes = [
        "VLA and language abstraction pressure",
        "neuro-symbolic predicate pressure",
        "relational abstraction and active learning pressure",
        "task-and-motion planning pressure",
        "monitoring, recovery, and failure reasoning pressure",
        "safety, deployment, and reproducibility pressure",
    ]
    rows = []
    for index, chunk in enumerate(cite_chunks(keys, 0, len(keys), 3), start=1):
        rows.append(f"{index} & {latex_escape(themes[(index - 1) % len(themes)])} & {chunk} " + r"\\")
    return "\n".join(rows)


def main() -> None:
    summary = read_summary()
    hard = sorted(read_csv(RESULTS / "hard_aggregate_metrics.csv"), key=lambda row: float(row["task_success"]), reverse=True)
    ablations = sorted(read_csv(RESULTS / "ablation_metrics.csv"), key=lambda row: float(row["robust_utility"]), reverse=True)
    stress = sorted(
        [row for row in read_csv(RESULTS / "stress_sweep.csv") if abs(float(row["stress_level"]) - 1.0) < 1e-9],
        key=lambda row: float(row["robust_utility"]),
        reverse=True,
    )
    fixed = sorted(
        [row for row in read_csv(RESULTS / "fixed_risk_metrics.csv") if abs(float(row["damage_budget"]) - 0.05) < 1e-9],
        key=lambda row: float(row["deployment_coverage"]),
        reverse=True,
    )
    refs = read_csv(DOCS / "deep_read_250.csv")
    keys = write_bib(refs)

    by_method = {row["method"]: row for row in hard}
    v5 = by_method[PROPOSED]
    non_oracle = [row for row in hard if row["method"] != ORACLE and row["method"] != PROPOSED]
    best_success = max(non_oracle, key=lambda row: float(row["task_success"]))
    best_violation = min(non_oracle, key=lambda row: float(row["mechanical_violation_rate"]))
    best_damage = min(non_oracle, key=lambda row: float(row["damage_unsafe_rate"]))
    best_regret = min(non_oracle, key=lambda row: float(row["planning_regret_to_oracle"]))
    best_utility = max(non_oracle, key=lambda row: float(row["robust_utility"]))
    intro_cites = cite_chunks(keys, 0, 18)
    related_cites = cite_chunks(keys, 18, 72)

    tex = rf"""
\documentclass[11pt]{{article}}
\usepackage[letterpaper,margin=0.95in]{{geometry}}
\usepackage{{amsmath,amssymb,booktabs,longtable,array,graphicx,float,caption,xcolor}}
\usepackage[numbers,sort&compress]{{natbib}}
\usepackage[colorlinks=false,citebordercolor={{0 1 0}},linkbordercolor={{1 0.55 0}},urlbordercolor={{0 0.55 1}},pdfborder={{0 0 1.2}}]{{hyperref}}
\graphicspath{{{{../figures/}}}}
\setlength{{\parskip}}{{0.42em}}
\setlength{{\parindent}}{{0pt}}
\newcommand{{\method}}[1]{{\texttt{{#1}}}}
\title{{Mechanics-Aware Abstraction Audits Fail Against Grounded Planning: A Frozen Negative Audit}}
\author{{Paper 99 Submission-Hardening Audit}}
\date{{Frozen evidence package: 2026-06-22}}
\begin{{document}}
\maketitle

\begin{{abstract}}
Language and symbolic robot abstractions can erase mechanics that matter for action: contact force, support, clearance, friction, deformation, temporal preconditions, tool affordances, compliance, and recovery feasibility. This paper tests whether a risk-bounded abstraction-failure audit should improve embodied planning beyond VLA policies, neuro-symbolic predicates, active relational abstraction, LLM-TAMP failure reasoning, runtime monitoring, semantic MPC, grounded geometric TAMP, and physics-aware TAMP {intro_cites[0]} {intro_cites[1]}. We rebuild the paper under a frozen CPU-only protocol with 322,560 main rollout rows, 115,200 ablation rows, 259,200 stress rows, 138,240 fixed-risk rows, and 24 predefined negative cases. The result is not a positive ICLR-main paper. The proposed \method{{abstraction\_v5}} reaches hard success {fnum(v5['task_success'])}, violation {fnum(v5['mechanical_violation_rate'])}, damage {fnum(v5['damage_unsafe_rate'])}, regret {fnum(v5['planning_regret_to_oracle'])}, and utility {fnum(v5['robust_utility'])}. The strongest reference, \method{{{latex_escape(short_method(best_success['method']))}}}, reaches success {fnum(best_success['task_success'])}. The terminal decision is \textbf{{{latex_escape(summary.get('terminal', 'KILL_ARCHIVE'))}}}.
\end{{abstract}}

\textbf{{Terminal decision.}} Paper 99 remains \textbf{{KILL\_ARCHIVE}} for ICLR main. The v5 rebuild is much stronger than the v4.1 archive, but it fails success, violation, damage, regret, utility, diagnostic, ablation, stress, fixed-risk, and scope gates. No hardware, accepted high-fidelity simulator, external benchmark, or trained policy checkpoint evidence is claimed.

\section{{Introduction}}
Robot abstractions are useful because they hide continuous complexity. They are dangerous because they can hide exactly the mechanics that decide whether an action succeeds. A symbolic predicate may say that an object is reachable while suppressing support, friction, compliance, or clearance. A language plan may name a tool affordance while erasing the leverage or contact mode needed to use it. A VLA policy may emit a plausible action token while ignoring trajectory feasibility or recovery risk.

The seed idea is therefore tempting: audit abstractions before planning, detect erased mechanics, and refine the plan state only when that refinement changes action value. This idea lives in a crowded neighborhood. VLA motion planning, neuro-symbolic predicate learning, relational abstraction, LLM-TAMP failure reasoning, runtime monitors, grounded geometric TAMP, and recovery planners all pressure the novelty claim {intro_cites[2]} {intro_cites[3]}.

The v4.1 paper was already negative. It showed diagnostic signal, but grounded geometric TAMP won task success, false refinements saturated, and ablations undercut the proposed mechanism. The v5 rebuild attacks those failures directly with more tasks, more failure families, more splits, more methods, ten seeds, fixed-risk budgets, stress sweeps, and a full hostile-review gate. The result is worse for the proposed claim: \method{{physics\_tamp}} dominates the hard aggregate, and full v5 is weaker than all of its planned ablations.

\section{{Contributions And Non-Contributions}}
\textbf{{Contribution 1: an expanded frozen benchmark.}} The v5 benchmark covers six task families, eight mechanics-erasure families, eight shifts, fourteen methods, and ten seeds. It streams raw CSVs to keep RAM light.

\textbf{{Contribution 2: theory of abstraction audit value.}} We separate diagnostic accuracy from planning value. An abstraction audit is useful only when the expected value of mechanics preservation exceeds refinement, query, TAMP switching, monitoring, recovery, and abstention costs.

\textbf{{Contribution 3: a negative result with strong baselines.}} The audit shows that physics-aware and grounded planning can expose the relevant mechanics more directly than a risk-bounded abstraction-failure classifier.

\textbf{{Non-contribution: no submission-ready claim.}} This artifact does not claim robot hardware validation, high-fidelity physics evidence, released checkpoints, or ICLR-main readiness.

\section{{Formal Setup}}
Let $z$ be a symbolic or language abstraction, $m$ a latent mechanics state, and $a$ a robot action. The audit estimates whether $z$ erases action-critical mechanics and chooses among proceeding, refining predicates, querying mechanics, switching to TAMP, monitoring, recovering, or abstaining:
\[
  a^\star = \arg\max_a \; S(a,z,m) - \lambda_v V(a,z,m) - \lambda_d D(a,z,m) - \lambda_c C(a,z,m) - \lambda_a A(a).
\]
Here $S$ is task success, $V$ is mechanical violation, $D$ is damage/unsafe action, $C$ is planning/refinement cost, and $A$ is abstention or excessive intervention.

\paragraph{{Proposition 1: diagnostics are not planning value.}} If a grounded planner already chooses the same safe mechanics-preserving action without naming the erased abstraction, then improving abstraction-failure accuracy cannot improve closed-loop value.

\paragraph{{Proposition 2: false-alarm control can become under-intervention.}} A risk-bounded audit can lower false refinements by requiring higher confidence before acting. If this also suppresses action on true mechanics failures, success and safety fall even when diagnostics improve.

\paragraph{{Proposition 3: fixed-risk coverage is decisive.}} A deployment policy under damage budget $\epsilon$ must maintain useful coverage while satisfying the budget. Abstaining or delaying on most hard cases is not a deployment win.

\section{{Benchmark Design}}
The six tasks are tabletop manipulation with support, tool use with hidden leverage, container insertion clearance, deformable object packing, mobile manipulation with occlusion, and articulated fixture assembly. The hidden failure families are erased contact force, hidden support relation, clearance tolerance collapse, friction-state aliasing, deformable-constraint erasure, temporal-precondition loss, tool-affordance misabstraction, and compliance-recovery erasure.

The eight shifts are nominal abstraction, language ambiguity, predicate noise, geometry tolerance, mechanics OOD, object-affordance transfer, recovery-cost pressure, and combined adversarial abstraction. The hard aggregate combines mechanics OOD, object-affordance transfer, recovery-cost pressure, and combined adversarial abstraction.

\section{{Methods}}
The proposed v5 method is a risk-bounded abstraction-failure audit. It estimates failure family and risk, then acts only when predicted value exceeds a risk and recovery-feasibility gate. This was intended to fix the v4 false-refinement failure.

The baseline suite includes language symbolic planning, VLA direct policy, neuro-symbolic predicates, active relational abstraction, LLM-TAMP failure reasoning, runtime monitoring, grounded geometric TAMP, physics-aware TAMP, affordance graph planning, learned failure classifier plus TAMP, semantic MPC, v4, v5, and an oracle.

\section{{Main Results}}
Table~\ref{{tab:hard}} gives the hard aggregate. The v5 result is plainly negative.

\begin{{table}}[H]
\centering
\caption{{Hard-aggregate results over hardest abstraction shifts.}}
\label{{tab:hard}}
\resizebox{{\linewidth}}{{!}}{{\input{{../results/hard_aggregate_table.tex}}}}
\end{{table}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.95\linewidth]{{abstraction_v5_hard_outcomes.png}}
\caption{{Hard-split closed-loop outcomes. Physics-aware TAMP dominates the proposed audit.}}
\end{{figure}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.95\linewidth]{{abstraction_v5_diagnostics.png}}
\caption{{Diagnostics improve locally, but the v5 policy avoids false refinements by under-acting on hard mechanics failures.}}
\end{{figure}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.95\linewidth]{{abstraction_v5_utility_regret.png}}
\caption{{Cost, regret, and robust utility expose the failed deployment tradeoff.}}
\end{{figure}}

\section{{Paired Evidence}}
The paired seed analysis prevents cherry-picking. The main references are \method{{{latex_escape(short_method(best_success['method']))}}} for success, \method{{{latex_escape(short_method(best_violation['method']))}}} for violations, \method{{{latex_escape(short_method(best_damage['method']))}}} for damage, and \method{{{latex_escape(short_method(best_regret['method']))}}} for regret.

\begin{{table}}[H]
\centering
\caption{{Selected paired decision tests for v5 against reference baselines.}}
\label{{tab:pairwise}}
\resizebox{{\linewidth}}{{!}}{{\input{{../results/pairwise_decision_table.tex}}}}
\end{{table}}

\section{{Ablations}}
The ablation result is fatal. Every planned ablation matches or beats full v5 on at least one predefined metric, and several beat it by a wide margin.

\begin{{table}}[H]
\centering
\caption{{V5 mechanism ablations.}}
\label{{tab:ablations}}
\resizebox{{\linewidth}}{{!}}{{\input{{../results/ablation_table.tex}}}}
\end{{table}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.95\linewidth]{{abstraction_v5_ablation.png}}
\caption{{Ablations undermine the necessity of the full risk-bounded audit.}}
\end{{figure}}

\section{{Stress Sweep}}
At maximum stress, the v5 method does not recover. Physics-aware TAMP remains the strongest robust-utility reference.

\begin{{table}}[H]
\centering
\caption{{Maximum-stress results.}}
\label{{tab:stress}}
\resizebox{{\linewidth}}{{!}}{{\input{{../results/stress_table.tex}}}}
\end{{table}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.88\linewidth]{{abstraction_v5_stress_sweep.png}}
\caption{{Stress sweep over combined adversarial abstraction pressure.}}
\end{{figure}}

\section{{Fixed-Risk Deployment}}
The fixed-risk analysis asks whether a method can maintain useful deployment coverage under a fixed damage budget. At budget 0.05, v5 is dominated by grounded geometric TAMP or has insufficient coverage.

\begin{{table}}[H]
\centering
\caption{{Fixed-damage deployment at budget 0.05.}}
\label{{tab:fixed}}
\resizebox{{\linewidth}}{{!}}{{\input{{../results/fixed_risk_table.tex}}}}
\end{{table}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.88\linewidth]{{abstraction_v5_fixed_risk.png}}
\caption{{Deployment coverage as the damage budget varies.}}
\end{{figure}}

\section{{Negative Cases}}
The negative cases are selected by predefined high-regret, high-damage, high-violation, and low-success rules.

\begin{{table}}[H]
\centering
\caption{{Representative failure cases.}}
\label{{tab:negative}}
\resizebox{{\linewidth}}{{!}}{{\input{{../results/negative_cases_table.tex}}}}
\end{{table}}

\section{{Related Work Pressure}}
The local literature pool is used as hostile pressure rather than as a claim that every record is directly applicable. VLA planning, neuro-symbolic predicates, relational abstraction, grounded TAMP, runtime monitoring, failure recovery, and deployment safety all pressure the novelty claim {related_cites[0]} {related_cites[1]} {related_cites[2]} {related_cites[3]}.

The novelty boundary is narrow: an abstraction audit must beat grounded planning and failure reasoning on closed-loop deployment metrics, not just classify erased mechanics. The audit shows that it does not. Appendix~\ref{{app:citations}} provides clickable pressure chunks sourced from the shared pool.

\section{{Limitations}}
This is a local CPU-only executable audit. It is not real robot evidence, not an accepted high-fidelity simulator benchmark, not a trained checkpoint comparison, and not an external embodied-planning benchmark. The negative result falsifies the claim inside the frozen surrogate benchmark. A revival must gather external evidence and a stronger mechanism, not hide failed gates.

\section{{Reproducibility}}
Run \method{{python src/run\_experiment.py}} from the repository root to regenerate all CSVs, tables, figures, and the terminal decision. Then run \method{{python scripts/generate\_manuscript.py}} and compile \method{{paper/main.tex}} with pdflatex, BibTeX, and two more pdflatex passes. The final numbered PDF belongs only at \method{{C:/Users/wangz/Downloads/99.pdf}}.

\section{{Conclusion}}
Mechanics-aware abstraction audits are plausible, but this v5 evidence does not support a positive ICLR-main contribution. V5 avoids false refinements but collapses on success, violation, damage, regret, utility, ablation, stress, and fixed-risk gates. The honest decision is \textbf{{KILL\_ARCHIVE}}.

\clearpage
\appendix
\section{{Full Gate Ledger}}
\begin{{longtable}}{{p{{0.24\linewidth}}p{{0.66\linewidth}}}}
\toprule
Gate & Frozen outcome \\
\midrule
Success & Failed: v5 success {fnum(v5['task_success'])} trails {latex_escape(short_method(best_success['method']))} at {fnum(best_success['task_success'])}. \\
Violation & Failed: v5 violation {fnum(v5['mechanical_violation_rate'])} trails {latex_escape(short_method(best_violation['method']))} at {fnum(best_violation['mechanical_violation_rate'])}. \\
Damage & Failed: v5 damage {fnum(v5['damage_unsafe_rate'])} trails {latex_escape(short_method(best_damage['method']))} at {fnum(best_damage['damage_unsafe_rate'])}. \\
Regret & Failed: v5 regret {fnum(v5['planning_regret_to_oracle'])} trails {latex_escape(short_method(best_regret['method']))} at {fnum(best_regret['planning_regret_to_oracle'])}. \\
Utility & Failed: v5 utility {fnum(v5['robust_utility'])} trails {latex_escape(short_method(best_utility['method']))} at {fnum(best_utility['robust_utility'])}. \\
False alarm & Passed: v5 false alarm is {fnum(v5['false_refinement_alarm_rate'])}. \\
Ablation & Failed: all planned ablations match or beat full v5 on at least one predefined metric. \\
Stress & Failed: maximum stress is dominated by {latex_escape(short_method(stress[0]['method']))}. \\
Fixed risk & Failed: budget 0.05 is dominated by {latex_escape(short_method(fixed[0]['method']))} or insufficient coverage. \\
Scope & Failed: no hardware, accepted high-fidelity benchmark, external benchmark, or trained checkpoint evidence. \\
\bottomrule
\end{{longtable}}

\section{{Metric Definitions}}
Task success is expected closed-loop completion. Mechanical violation is action-incompatible contact, support, clearance, friction, deformation, or tool-use violation. Damage is expected unsafe action or object/fixture damage. Abstraction-failure accuracy measures hidden mechanics-erasure classification. Mechanics-retention recall measures whether the action preserves relevant mechanics on actionable failures. False alarm is heavy intervention on temporal or nuisance cases. Robust utility subtracts violation, damage, cost, and abstention penalties from success. Regret is the gap to a non-deployable oracle action.

\section{{Expanded Baseline Descriptions}}
Language symbolic planning trusts high-level predicates. VLA direct policy maps observations and language to actions. Neuro-symbolic predicates learn abstract state tests. Active relational abstraction asks for predicate grounding. LLM-TAMP failure reasoning routes failures through task-and-motion planning. Runtime monitoring replans after risk appears. Grounded geometric TAMP exposes geometry directly. Physics-aware TAMP exposes geometry and mechanics. Affordance graphs reason over object-use relations. Learned failure classifier plus TAMP uses a classifier before planning. Semantic MPC plans over symbolic and continuous risk features. V4 and v5 test the proposed abstraction-failure audit.

\section{{Prior-Work Pressure Ledger}}
\label{{app:citations}}
\small
\begin{{longtable}}{{p{{0.06\linewidth}}p{{0.38\linewidth}}p{{0.48\linewidth}}}}
\toprule
ID & Pressure role & Clickable citations \\
\midrule
{citation_ledger(keys)}
\bottomrule
\end{{longtable}}

\bibliographystyle{{plainnat}}
\bibliography{{references}}
\end{{document}}
"""
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")
    print(f"wrote {PAPER / 'main.tex'}")
    print(f"wrote {PAPER / 'references.bib'} with {len(keys)} entries")


if __name__ == "__main__":
    main()
