# The Factory Plane — Keeping the Workshop Out of the Product

![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue)

Until 2026-08-11 the fleet's shippable product and the tooling used to build it lived in one
repository, and every fresh agent session read both at once. This chapter explains the split
that separated them, what belongs on each side of the line, and which repository you open for
a given task.

## Summary

- One repository held two incompatible things: a clean installable product and a messy
  development harness. Agents mixed them, applying session protocol to component READMEs and
  cloning the whole fleet for platform work.
- The fleet now separates concerns across three owned repositories — product, factory, and
  gateway — plus a pinned upstream fork.
- `shesh-ecosystem` is the **Product** plane: manifest, channel locks, architecture docs, and
  gates. `shesh-workspace` is the **Factory** plane: session protocol, swarm, credentials,
  efficiency tooling.
- Development work and the shipped runtime use different model tiers on purpose: big free
  hosted models to build the system, small local models to run it.
- Unattended build work runs on GitHub Actions using free tiers only, with no paid API key.

## Why the planes had to split

A factory and a showroom serve opposite purposes. A showroom stays clean, labelled, and
predictable; a factory floor accumulates jigs, fixtures, and half-finished experiments because
that is how work gets done. Putting both in one room does not save space — it simply makes the
showroom unusable.

That is precisely what happened inside `shesh-ecosystem`. The repository carried the product
side — the `components.toml` manifest, the `channels/*.lock` files, the architecture documents,
and the `resolve_manifest.py` and `check_licenses.py` gates. It also carried the factory side:
`tools/session_guard.py`, `secure_pat.py`, `github_auth.py`, `setup_worker.py`,
`llm_adapter.py`, `model_router.py`, the `swarm/` and `autopilot/` trees, the session and swarm
documents, the `swarm-*.yml` workflows, and the `Containerfile`.

The consequence showed up in every new agent session. The model read both halves and could not
tell which rules applied, so it did things like enforce the session hopping protocol on a
component README, or clone 22 repositories to edit a single platform document.

## The three-repository split

Each repository now has one job, and its expected level of tidiness is stated up front.

| Repository | Plane | Purpose | Tidiness |
|---|---|---|---|
| `shesh-ecosystem` | Product | What the owner installs on the MSI Sword 16 HX | Clean; 63 tests, gate OK; no session protocol |
| `shesh-workspace` | Factory | Session protocol, swarm, secure PAT, efficiency, model-agnostic work, travel mode | Deliberately messy dev tooling |
| `shesh-omniroute` | Gateway | Wrapper over the OmniRoute fork; optional to the local model stack | Clean wrapper |
| `gaganjainse/OmniRoute` | Upstream fork | 291 providers, 90-plus free, 500-plus models, 1.53B tokens per month | Pinned fork of `diegosouzapw/OmniRoute`, upstream's own permissive license |

> **Note —** The Shesh fleet itself is licensed GPL-3.0-or-later; upstream forks keep their own
> licenses, and `scripts/check_licenses.py` refuses combinations that are incompatible.

## What belongs in each repository

The product repository keeps everything a user's installation depends on: the
`manifests/components.toml` and `models.toml` files (the latter now including the
`shesh-omniroute` component), the three channel locks for stable, canary, and devel, the
architecture set (agentic body, repo topology, language policy, multi-agent), the
getting-started, manual-verification, audit-and-roadmap, session-handoff, glossary, and
tooling-catalog documents, 19 architecture decision records, synced component READMEs, the
`scripts/` gates, the skills policy, and the build files. The model-agnostic strategy and the
OmniRoute study belong here too, because both describe product behavior.

The factory repository takes the development harness: the `tools/` scripts named above plus
`llm_worker.py`, the `swarm/` and `autopilot/` trees, `install.sh`, the session and swarm
documents, the three `swarm-*.yml` workflows, the `Containerfile` and `distrobox.ini`, the
signing and tracing scripts, `eval_model_agnostic.py`, the swarm queue, claims, heartbeats,
artifacts, and ledger, and a development copy of `models.toml`.

> **Note —** As recorded on 2026-08-11, `shesh-workspace` exists and carries the development
> tooling at commit `fbb77e3` on `main`, while `shesh-ecosystem` still contained its copies
> pending a cleanup commit. Treat this chapter as the intended boundary.

## Which repository a session opens

The routing rule is short enough to memorize, which is the point.

For component or ecosystem work — implementing `shesh-memory`, for example — open a session,
read only `shesh-ecosystem/docs/SESSION_HANDOFF.md`, do the work, run `make check`, and push to
`shesh-ecosystem`. For development tooling — session protocol, swarm, credentials, efficiency,
model-agnostic work — read `shesh-workspace/README.md` and its session protocol document, then
push to `shesh-workspace`. No session does both.

## Development models versus product models

The two planes deliberately draw on different model tiers, and conflating them caused real
confusion. Building the system does not require the small local models; those exist to run the
finished product.

| Purpose | Models | Why |
|---|---|---|
| Building the fleet | Free hosted models via the gateway: Groq free, OpenRouter `:free`, GitHub Models free, HuggingFace free | Industry-scale models at no cost, used only in development |
| Running the fleet | Local Ollama: `phi4-mini`, `qwen2.5-coder:3b`, `moondream2`, `nomic-embed-text` | 6 GB VRAM, offline, no API key, primary by default |

Including the small local models in the design does not degrade quality, because every caller
goes through the same guarded adapter. The five-layer guard in
[llm_adapter.py](llm-adapter.md) — strict JSON schema, uniform prompt, a validate-and-repair
loop with three retries, a free-first fallback chain ending in a deterministic stub, and a
judge score of at least 0.7 — holds the output shape constant regardless of which model
answers. Measured variance stays under 0.1 with 100 percent JSON validity.

Implementation follows the same idea. `manifests/models.toml` describes both tiers with
priorities: development picks big free models first, production picks local first, and the
adapter handles either. The `shesh-omniroute` component wraps the fork and exposes an
`omniroute_generate` tool through the same adapter, optional to the local stack and enabled in
the settings interface.

## Unattended build work without a paid key

Long unattended runs do not need a paid API key. The free implementation uses
`.github/workflows/swarm-llm-worker.yml`, triggered by cron every two hours and by manual
dispatch, and calls GitHub Models through the `GITHUB_TOKEN` the runner already provides —
`gpt-4o-mini`, `Phi-3-medium`, and similar, free for public repositories. Optional free keys
for Groq, OpenRouter, and HuggingFace extend the chain.

The flow is mechanical: pick an issue labelled `swarm:pending`, call `tools/llm_adapter.py` and
`tools/llm_worker.py` with a free model, produce a patch as `{"patch": ..., "summary": ...}`,
write `swarm/artifacts/llm-issue-N.md`, push branch `swarm/issue-N/llm-worker-<model>`, open a
pull request that says `Closes #N`, and let `swarm-auto-merge.yml` merge it once `make check`
is green. Paid providers remain possible by setting `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` and
changing the model input, but the free path already works.

## Where this fits

Read [Session Protocol](session-protocol.md) for the handoff discipline that keeps factory
sessions productive, [Efficiency](efficiency.md) for the selective-clone strategy that shortens
setup, and [Swarm](swarm/README.md) for the multi-session coordination bus. The cloud side is
documented under [Gateway](../gateway/overview.md), and the product side begins at
[Product Overview](../product/overview.md).
