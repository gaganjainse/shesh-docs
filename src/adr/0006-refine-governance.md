# ADR-0006: Immutable Base + Evidence-Backed /refine

Shesh evolves by editing a small, reviewable layer of supplemental state rather than its
immutable base prompt, and every refinement must prove it helps on a held-out test set. The
pattern stops a self-modifying agent from quietly rewriting its own safety rules.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** self-improvement, safety, continual-harness

## Context

Self-modifying agents can cheat: they mutate the base prompt to bypass safety, or they
accumulate low-quality skills — what the team calls "dross." A post-mortem of the Prime Agent
showed the need for an immutable base paired with a mutable harness, gated by evidence.

Three needs drove the decision: safe self-evolution that survives reboots, rollback when a
refinement hurts, and no mutation of core policy without review.

## Decision

Shesh adopts the Prime Agent's Continual Harness pattern inside `shesh-harness`:

- The **base prompt is immutable** — it is checked into the repository.
- **Supplemental state** is create-read-update-delete: `harness.md`, `skills/*.md`, and
  `memory/semantic.md` live locally and change only through `/refine`.

The `/refine` flow is disciplined:

1. Read the trajectory and a held-out evaluation set.
2. Propose the smallest edit that improves the held-out score (via `must_contain` /
   `must_not_contain` checks, structural checks, and weighting).
3. Apply it at a turn boundary as system context, never as base.
4. Replay the held-out set with the proposed edit; the score must reach at least 0.7.
5. Record the trigger and outcome in `recent_refinements`, allowing rollback.

In implementation, `shesh-harness` provides `propose_and_apply()`, a `refine_with_llm()` MCP
tool, and `make_ollama_responder()` for local scoring. The LLM responder uses `shesh-mind`
routing, with a deterministic stub fallback.

## Consequences

### Benefits

- Evolution stays safe because the base prompt can never cheat.
- `rollback(refinement_id)` reverts changes in the supplemental store.
- The evaluator blocks low-quality promotion — `/refine` runs only when the score is 0.7 or
  higher.

### Costs

- The held-out set must be curated; it is seeded from the query log and the skills.
- The LLM grader adds latency, though an offline stub provides a fallback.

## Links

- `docs/architecture/AGENTIC_BODY.md`, `docs/LEARNING.md`
- `shesh-harness`, `shesh-memory`
- [ADR-0013: Hierarchical Memory](0013-hierarchical-memory.md),
  [ADR-0014: Habit Learning](0014-habit-learning.md)
