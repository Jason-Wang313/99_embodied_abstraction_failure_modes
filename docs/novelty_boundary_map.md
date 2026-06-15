# Novelty Boundary Map

## Crowded Territory

- VLA agents with motion planning.
- Neuro-symbolic predicates.
- Active relational state abstraction.
- LLM-TAMP failure reasoning.
- Corrective planning with language models.
- Runtime monitoring and replanning.
- Grounded geometric TAMP.

## Boundary Tested

The only potentially novel boundary was an explicit abstraction-failure audit that detects erased mechanics and decides whether to refine predicates, query mechanics, switch to TAMP, monitor/replan, or proceed.

## What The v4.1 Continuation Audit Found

The boundary is not strong enough. The proposed method improves failure classification and mechanics-retention recall, but grounded geometric TAMP outperforms it on task success and ablations remove predicate refinement or the cost model without hurting success/regret. The 2026-06-15 rerun reproduced this negative pattern.

## Boundary Decision

Novelty remains an idea seed, not a submission-ready contribution.
