# shesh-harness — Self-Improvement With Guardrails

An agent allowed to rewrite its own prompt will eventually rewrite it to score well rather than
to work well. The continual harness is the component that prevents that: it keeps the base
prompt immutable, requires evidence and evaluation before any change applies, and can revert any
refinement by identifier.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python) ![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue) ![Tests](https://img.shields.io/badge/Tests-23-success) ![CI](https://github.com/gaganjainse/shesh-harness/actions/workflows/ci.yml/badge.svg)

- **License:** GPL-3.0-or-later
- **Owner:** Gagan Jain ([@gaganjainse](https://github.com/gaganjainse))
- **Layer:** Mind (self-improvement)
- **Part of:** [shesh-ecosystem](https://github.com/gaganjainse/shesh-ecosystem)

## Why the component exists

The harness implements the Prime Agent `/refine` pattern, and it treats every proposed change to
the agent's own instructions as a candidate rather than a decision. A candidate must cite
evidence, pass evaluation, and clear tests before it is promoted.

The result is a system that can learn a user's intentions without destabilizing itself. Learning
is permitted; drifting is not.

## Working with the repository

```bash
uv sync --extra dev
uv run pytest -q        # 23 tests
uv run ruff check .
```

> **Note —** `uv.lock` pins the full dependency tree. Use `uv sync --frozen` — or
> `uv pip install -r <(uv export --frozen)` — for a reproducible, locked build.

## Tools exposed over MCP

The harness speaks the Model Context Protocol over stdio and exposes a small surface.

| Tool | Purpose |
|---|---|
| `get_prompt_block()` | Supplemental prompt and memories for the current turn |
| `add_memory(text)` | Record a durable memory |
| `upsert_skill(name, body)` / `list_skills()` | Manage the skill set |
| `refine(trigger, trajectory)` | Propose, evaluate, and apply one small change |

Every refinement is recorded append-only with its trigger, the before and after state, its
score, and its outcome — which is what makes reverting by identifier possible rather than
aspirational.

## Status

Component CI is green on the reusable ecosystem pipeline. Security posture and vulnerability
reporting are covered in
[SECURITY.md](https://github.com/gaganjainse/shesh-harness/blob/main/SECURITY.md).

## Where this fits

The same grading contract — `must_contain`, `must_not_contain`, structural checks, and a minimum
score of 0.7 — is reused by the [model-agnostic workflow](model-agnostic.md), so a refinement is
judged by the same standard as a model response. Compiled reading for the whole fleet lives in
[shesh-docs](https://github.com/gaganjainse/shesh-docs).

## License

GPL-3.0-or-later — see
[LICENSE](https://github.com/gaganjainse/shesh-harness/blob/main/LICENSE).
