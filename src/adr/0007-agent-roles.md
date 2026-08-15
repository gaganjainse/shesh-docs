# ADR-0007: Six Agent Roles, 6 GB VRAM Budget

Shesh splits work across six specialist roles served by small local models, all fitting inside
a 6 GB VRAM budget through careful routing. The design mimics a crew without adopting the
weight of a full multi-agent framework.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** multi-agent, routing, vram

## Context

A single generalist model asked to plan, code, see, and critique burns VRAM and conflates
skills. On a 6 GB RTX 4050 Mobile with 16 GB of RAM, specialist small models need a router to
share the limited memory. The target display is 1920x1200 at 144 Hz.

The fleet needed crew-like specialization without CrewAI's complexity.

## Decision

Six roles, inspired by Prime Agent and CrewAI, map to 6 GB-safe models:

| Role | Model (6 GB-safe) | Job |
|------|-------------------|-----|
| coordinator | phi4-mini | Triages the user goal, delegates |
| planner | phi4-mini | Produces JSON steps |
| coder | qwen2.5-coder:3b | Writes patches and tools |
| researcher | phi4-mini | Web, notes, and full-text search |
| vision | moondream2 | Screenshot, OCR, vision-to-tap |
| critic | phi4-mini | Approves or rejects the plan |
| embedding | nomic-embed-text | RAG embeddings |

The `shesh-mind` router exposes `select_model(role)` and `plan_session()`, which budget the
distinct loaded models. It prefers already-loaded models to avoid eviction-and-reload thrash,
honors a 5.5 GB budget, and falls back along a chain. `shesh-orchestrator` runs the RLM
runtime — planner, then role agents, then critic, then a trace. One GPU model stays resident at
a time; the router evicts before loading another, with the policy living in `shesh-system`.

## Consequences

### Benefits

- A 6 GB laptop runs every role through routing instead of running out of memory.
- `shesh-mind-mcp` exposes `list_roles` and `plan_session` for auditing.
- The critic gates `/refine`.

### Costs

- Small models are weaker than a 70B model, so prompting and JSON extraction (a balanced-brace
  scan) need care.
- Embeddings are separate from chat models, which requires a provider abstraction.

## Links

- `docs/architecture/MULTI_AGENT.md`, `docs/components/shesh-mind.md`
- `shesh-mind`, `shesh-orchestrator`
- [ADR-0005: Local-First, Cloud Opt-In](0005-local-first.md)
