# model_router.py — Choosing a Model by Capability, Free Tier First

Callers ask for a role — planner, researcher, critic, coder — and never for a model by name.
This chapter explains the capability mapping behind that indirection, the order in which
providers are tried, and why hardcoded model names kept breaking.

Status: living · last verified 2026-08-13
Source: `tools/model_router.py` · Strategy: [Model-Agnostic Workflow](model-agnostic.md)

## The selection chain

`Router.pick(role)` walks the chain from cheapest and most private to most remote: local Ollama
if it is reachable, then Groq free, then OpenRouter free, then GitHub Models free, and finally a
deterministic stub. The chain order and the free-tier claims behind it are research-backed in
the [OmniRoute study](../gateway/omniroute-study.md), which surveyed 291 providers and
re-verified free tiers on 2026-06-17 under a CI-gated refresh.

## Why capability beats a name

A router keyed to `role → phi4-mini` broke the first time a model was renamed or a pulled model
went missing. Capabilities such as `reasoning`, `code`, and `long-context` describe what the
caller actually requires, and they survive provider churn.

The reasoning mirrors the fleet's dependency policy applied to models: roll forward, degrade
honestly, and never fabricate. A router that cannot find a capable model returns the stub rather
than an answer it cannot support.

## What is verified

Chain fallback and stub termination are unit-tested in the ecosystem suite under `make check`,
and `shesh-mind` consumes the router for its role dispatch. The guarded output shape that sits
above the router is documented in [llm_adapter.py](llm-adapter.md).
