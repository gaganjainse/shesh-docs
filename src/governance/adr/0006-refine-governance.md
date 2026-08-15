---
title: "ADR-0006: Gate self-refinement on measured evidence"
type: explanation
summary: "Gate self-refinement on measured evidence."
audience: maintainer
status: current
verified: 2026-08-15
---

# ADR-0006: Gate self-refinement on measured evidence

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-08-09 |
| **Deciders** | Fleet maintainer |
| **Tags** | self-improvement, safety, continual-harness |

## Context

Self-modifying agents can "cheat" — mutate base prompt to bypass safety, or accumulate low-quality skills ("dross"). Prime Agent post-mortem showed need for **immutable base + mutable harness** with evidence gates.

The fleet needs:
- Safe self-evolution that survives reboots.
- Rollback if refinement hurts.
- No mutation of core policy without review.

## Decision

Adopt **Prime Agent's Continual Harness** pattern in `shesh-harness`:

- **Base prompt is immutable** — checked into repo.
- **Supplemental state** is CRUD: `harness.md` / `skills/*.md` / `memory/semantic.md` stored locally, mutable only via `/refine`.
- `/refine` flow:
  1. Read trajectory + held-out evaluation set.
  2. Propose smallest edit that improves score on held-out (must_contain/must_not_contain, structural checks, weight).
  3. Apply at turn boundary as system context (not base).
  4. Replay held-out with proposed edit; score must ≥ min_score (0.7).
  5. Record trigger/outcome in `recent_refinements`; allow rollback.

Implementation:
- `shesh-harness`: `propose_and_apply()`, `refine_with_llm()` MCP tool, `make_ollama_responder()` for local scoring.
- LLM responder uses `shesh-mind` routing; fallback to deterministic stubs.

## Consequences

### Benefits

- Safe evolution — base never cheats.
- Rollback via `rollback(refinement_id)` — supplemental store.
- Evaluator prevents low-quality promotion (`refine` only if ≥0.7).
- Held-out set must be curated, seeded from the query log + skills.
- Extra latency for LLM grader — offline stub fallback.

## References

- `docs/architecture/AGENTIC_BODY.md`, `docs/LEARNING.md`
- `shesh-harness`, `shesh-memory`
- D13, D14
