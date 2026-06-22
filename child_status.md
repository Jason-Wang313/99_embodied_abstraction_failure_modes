# Child Status 99

Current stage: expanded-standard v5 hostile-review audit complete
Last update: 2026-06-22 09:46:59 +08:00
PDF: C:/Users/wangz/Downloads/99.pdf
PDF pages: 29
PDF SHA256: 3D54F7894471FA1642ECF0F408F29F1CDAAA66C2663EDCA32D7FF656ABD48E09
GitHub: https://github.com/Jason-Wang313/99_embodied_abstraction_failure_modes
Submission-hardening version: v5-expanded
Terminal decision: KILL_ARCHIVE
ICLR main ready: no
Desktop PDF copy: absent and prohibited

Evidence basis: fresh 2026-06-22 expanded v5 rerun of the local executable embodied-abstraction benchmark with 6 tasks, 8 abstraction-failure families, 8 splits, 14 methods, 10 seeds, 322,560 main rollout rows, 115,200 ablation rows, 259,200 stress rows, 138,240 fixed-risk rows, 96 hard paired tests, 24 negative cases, generated tables/figures, and a 29-page archive PDF with bright boxed clickable citations.

Terminal reason: `risk_bounded_abstraction_failure_audit_v5` is not submission-ready because `physics_aware_tamp` dominates it on hard success (0.67262 vs 0.28708), mechanical violation (0.16450 vs 0.45955), damage (0.13935 vs 0.37043), regret (0.06982 vs 0.63815), and robust utility (0.30626 vs -0.33399). The v5 audit also fails diagnostic, ablation, maximum-stress, fixed-risk, scope, and external-validation gates.
