# llm_adapter.py — One Guarded Output Shape Over Every Model

The adapter is a pressure regulator between unpredictable models and code that expects
structure: whatever model answers, callers receive the same validated output shape or an honest
stub. This chapter describes the five layers that make that guarantee hold.

Status: living · last verified 2026-08-13
Source: `tools/llm_adapter.py` · Strategy: [Model-Agnostic Workflow](model-agnostic.md)

## The five-layer guard

Each layer catches a different failure, and the order matters: nothing reaches a caller until it
has survived all five.

1. **Schema** — the caller declares the expected JSON shape before generation begins.
2. **Generation** — the request goes through the model-agnostic router on a free-first chain.
3. **Parse and validate** — malformed output never reaches the caller.
4. **Grading** — responses are scored, and weak answers retry or fall further down the chain.
5. **Stub last** — the chain terminates in a deterministic stub rather than a fabricated answer.

## Why the guard exists

Swarm workers run unattended for hours, so nobody is watching when a provider regresses.
Without the guard, a bad response becomes a bad patch and the bad patch reaches a pull request.
With it, output quality stays consistent to a variance under 0.1 across providers; the
measurement method is described in the [model-agnostic workflow](model-agnostic.md).

## Related tooling

`tools/llm_worker.py` is the swarm worker built on the adapter, running on the GitHub Models
free tier with `GITHUB_TOKEN` alone and no paid key. `tools/model_router.py` is the
capability-based picker underneath it, documented in [model_router.py](model-router.md).
