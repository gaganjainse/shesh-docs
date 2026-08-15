# OmniRoute study — free big models for Shesh

The Shesh fleet can reach large hosted models without spending money. This
chapter surveys the OmniRoute gateway, the free capacity it aggregates, and how
Shesh uses it as an optional cloud fallback behind an always-local primary.

## Summary

- OmniRoute is a self-hosted, OpenAI-compatible gateway that aggregates 291
  providers, more than 90 of them with a free tier.
- The documented free pool is on the order of 1.5B tokens per month, with token
  compression stretching it further.
- Shesh runs local models as the primary; OmniRoute is an opt-in, free cloud
  fallback behind the `shesh-mind` router.
- The fork `gaganjainse/OmniRoute` is wrapped as the planned `shesh-omniroute`
  component, kept separate from the clean product.

## What OmniRoute actually is

OmniRoute is a free, MIT-licensed AI gateway — not merely an OpenRouter client.
It presents one OpenAI-compatible endpoint, `http://localhost:20128/v1`, that
aggregates 291 providers. The project was forked to
[gaganjainse/OmniRoute](https://github.com/gaganjainse/OmniRoute) from
`diegosouzapw/OmniRoute` (38.9k stars, 5.1k forks, 6k commits, 500+ contributors).

Its catalog (`open-sse/config/freeModelCatalog.ts`) lists 516 models and more
than 90 free providers, 40+ of which are free forever with no card. It offers 19
routing strategies and a 12-engine token-compression stack — Session-Dedup, CCR,
Lite, RTK, Responses Tool Output, Headroom, Relevance, Caveman, Aggressive,
LLMLingua-2, Ultra, and OmniGlyph — that cuts 15% to 95% of tokens (about 89%
on average for tool-heavy sessions).

A quota-aware auto-fallback walks four tiers: Tier 1 subscription (Claude Code,
Codex, Copilot) to Tier 2 API (DeepSeek, Groq, xAI) to Tier 3 cheap (GLM at $0.5,
MiniMax at $0.2) to Tier 4 free (Kiro, Qoder, Pollinations, and others). The
gateway ships a built-in MCP server (105 tools), the A2A v0.3 protocol,
persistent memory, guardrails, cloud agents, TLS-fingerprint stealth, and a
Desktop/PWA client across 43 locales.

The dashboard at `http://localhost:20128` shows the live free-tier budget,
used versus remaining, a per-model grid, and 43 provider pools.

## Free tiers — the honest numbers

| Metric | Tokens/mo | Meaning |
|--------|-----------|---------|
| **Documented recurring steady** | **~1.51B** | Free-tier pools, each shared pool counted once. Source `freeModelCatalog.ts`, API `/api/free-tier/summary`, dashboard Free-Tier Budget. **Use this.** |
| + first month signup credits | ~2.13B | Steady plus one-time (Together $25, Z.AI 20M, DeepSeek 5M), first month only |
| + permanently free, no cap | un-quantifiable | `siliconflow`, `glm-cn` GLM-4-Flash, `tencent`, `baidu`, `kilo-gateway`, `opencode-zen` — real recurring, rate-limited, no token cap, never summed |
| + deposit-unlock boost | +~24M | OpenRouter $10 top-up raises free 50 to 1000 requests/day |
| Theoretical ceiling (all limits 24/7) | ~10B | Fantasy, not a guarantee |

**Biggest contributors:** `mistral` 1.00B, `llm7` 150M, `groq` 117M, `gemini` 60M,
`cerebras` 30M, `cloudflare-ai` 30M, `sambanova` 30M.

**Per-provider free (sample 2026-06-17):**

| Provider | Type | Steady/mo | Models | Notes |
|----------|------|-----------|--------|-------|
| `mistral` | recurring | ~1.00B | 5 | Consumer terms of service, personal needs |
| `llm7` | recurring | ~150M | 4 | Experimentation |
| `gemini` | recurring | ~60M | 6 | Flash family only, pooled |
| `cerebras` | recurring | ~30M | 2 | |
| `cloudflare-ai` | recurring | ~30M | 6 | 10k Neurons/day |
| `groq` | recurring | ~15M | 5 | 14.4k requests/day free tier |
| `openrouter` | recurring | ~1M | 1 | 50 requests/day free |
| `cohere` | recurring | ~800K | 6 | |
| `huggingface` | recurring | ~200K | 6 | |
| `glm-cn` | uncapped | uncapped* | 4 | GLM-4-Flash permanently free plus 20M signup |
| `kilo-gateway` | uncapped | uncapped* | 7 | Auto free rotating set: Nemotron 3, StepFun, Poolside |
| `opencode-zen` | uncapped | uncapped* | 6 | Six rotating free coding models |
| `siliconflow` | uncapped | uncapped* | 10 | DeepSeek V3.0/R1 free tier |

**Free forever, no card, no token cap (rate-limited):** Qoder AI (Qwen3-Max,
Kimi-K2 unlimited), Pollinations (GPT, Llama, Claude no key), Cloudflare AI (50+
models, 10k neurons/day), NVIDIA NIM (GLM, MiniMax ~40 RPM free), Cerebras
(GLM), Kilo Code, OpenCode Zen, Z.AI GLM, Requesty (GPT-OSS 120B, Nemotron free),
SiliconFlow (DeepSeek V3.2/R1).

**Why the number dropped from 1.94B to 1.51B:** an honesty correction. Gemini was
pooled correctly (each Flash variant had been counted separately, 462M falling
to 60M), Cloudflare was corrected from 122M to 30M, Doubao was reclassified as a
one-time credit, and shutdown tiers (Chutes, Phind, Kluster) were removed. New
free providers — Kilo, OpenCode Zen, and Z.AI — were added.

## Big industry models available free

OmniRoute's catalog includes industry-scale models for free, not only small
local ones:

- **Claude** via Kiro AI free (Claude Sonnet 4.5, Haiku 4.5, Opus 4.6) — about 50 credits/month per account
- **GPT** via Pollinations, OpenCode, Requesty, Puter — GPT-4o mini, 150M tokens/mo documented; GPT-OSS 120B free forever
- **Gemini** via the Gemini free tier — 60M tokens/mo, Flash family
- **DeepSeek** via DeepSeek V3.2/R1, V4 Flash/Pro — 5M signup plus recurring via SiliconFlow and NVIDIA NIM
- **Llama** via Groq, Cloudflare, Together, SambaNova — Llama 3.1 8B/70B and 3.3 70B
- **Mistral** Large 3 — 1B tokens/mo, the biggest single contributor
- **Qwen** Qwen3-Max and Qwen3-Next-80B-A3B via Qoder and Alibaba
- **Kimi** K2 and K3 (1M context) — free via the Kimi provider
- **GLM** GLM-4-Flash, 4.5-Flash, 4.7-Flash, permanently free via Z.AI and GLM-CN
- **MiniMax** M2.1 and M2 — about $0.2 plus free via NVIDIA NIM

These are not small local models. They are frontier 70B to 120B to 550B
parameter models that expose free tiers.

## How OmniRoute works for Shesh

The final product runs local models as the primary brain: `phi4-mini`,
`qwen2.5-coder:3b`, `moondream2`, and `nomic-embed-text` — about 6 GB VRAM,
offline, no API key — on the MSI Sword 16 HX system. OmniRoute is an optional
cloud fallback.

- Shesh local primary → if offline or needing larger reasoning → OmniRoute
  gateway `http://localhost:20128/v1` auto-fallback to free big models.
- Where you enable it is your choice. Through the `shesh-mind` router, if
  `cloud.enabled=true` (opt-in) and policy allows (not a protected path), the
  request routes to OmniRoute; otherwise it stays local.
- OmniRoute's RTK plus Caveman compression cuts 15% to 95% of tokens, stretching
  the free tiers so the on-order-of-1.5B monthly pool lasts longer.

### Separation of concerns

- **shesh-ecosystem = product** — clean, with `components.toml`, locks,
  architecture docs, and gates. No session protocol, no swarm dev tooling.
- **shesh-workspace = factory** — the development harness: session protocol,
  swarm orchestration (atomic file plus Issues locking and auto-merge), secure
  PAT flow, selective clone, model-agnostic adapter, travel mode.
- **OmniRoute forked as `gaganjainse/OmniRoute`** — embedded as the optional
  `shesh-omniroute` component (planned): local primary, OmniRoute optional cloud
  free fallback.

> **Note —** Per the 2026-08-15 fleet audit, `shesh-workspace` is archived. It
> holds the development tooling described above; the clean product remains
> `shesh-ecosystem`.

## Using OmniRoute to build the ecosystem

For building the ecosystem (development work in the Arena), OmniRoute's free big
models can produce higher-quality output than small local ones, even though the
final product runs locally.

1. **Install OmniRoute locally (free, no keys needed for basic use):**

    ```bash
    npm install -g omniroute
    omniroute
    # Dashboard http://localhost:20128, API http://localhost:20128/v1
    ```

2. **Point any OpenAI-compatible tool at it:**

    ```bash
    # Claude Code
    ANTHROPIC_BASE_URL=http://localhost:20128 claude
    # Codex CLI
    OPENAI_BASE_URL=http://localhost:20128/v1 codex
    # Cursor, Cline, Continue, etc.
    Base URL: http://localhost:20128/v1
    Model: auto  # smart routing, or specific like kimi-k2, claude-sonnet-4.5
    ```

3. **Connect free providers (no signup for some):** dashboard → Providers →
   Kiro AI (free Claude, ~50 credits/month) or OpenCode Free (no auth). Or add a
   Groq free key, an OpenRouter free key, and so on.

4. **Use it to build the ecosystem:** in the Arena, set
   `OPENAI_BASE_URL=http://localhost:20128/v1` and `OPENAI_API_KEY=any` (the
   OmniRoute key from the dashboard). Model `auto`, `kimi-k2`, or
   `claude-sonnet-4.5` — OmniRoute picks the cheapest free option that works and
   auto-falls back across the four tiers. The model-agnostic adapter
   (`tools/llm_adapter.py`) enforces one JSON schema, validation, and grading, so
   quality stays consistent even when different free models answer.

5. **Where you enable it in the finished product is your choice:** the final Shesh
   on the MSI runs the local Ollama primary (free, offline). If you opt in with
   `cloud.enabled=true` in the settings GUI, it routes through the OmniRoute
   gateway to free big models. The `shesh-mind` router is capability-based and
   free-first, stub last. The `SKILLS_POLICY.md` policy never sends protected
   paths (`.ssh`, `Vaults/`, `Job`) to the cloud regardless of setting.

> **Tip —** Free, no money: more than 90 providers, on the order of 1.5B tokens
> per month aggregated, 40+ free forever, plus 15% to 95% compression. The basic
> free models (Pollinations, Cloudflare) work the moment you install, no keys, no
> config.

## Integration into the Shesh ecosystem

- **As component:** `shesh-omniroute` (planned) — wraps the OmniRoute gateway as
  an MCP tool `omniroute_generate` with the same model-agnostic adapter, optional
  to local AI, enabled via the settings GUI `SheshConfig.qml`.
- **As dev tool:** `tools/omniroute/` (future) — uses OmniRoute free big models
  to build the ecosystem (code generation) with rigorous quality (schema,
  validation, fallback chain, grading).
- **Separation:** dev tooling (using OmniRoute to build) lives in
  `shesh-workspace`, not in the clean `shesh-ecosystem` product. Where you enable
  it in the finished product is your choice.

## References

- Fork: https://github.com/gaganjainse/OmniRoute (from diegosouzapw/OmniRoute)
- Workspace: https://github.com/gaganjainse/shesh-workspace (development harness)
- Ecosystem: https://github.com/gaganjainse/shesh-ecosystem (clean product)
- OmniRoute docs: https://github.com/diegosouzapw/OmniRoute/tree/main/docs
- Free tiers methodology: `open-sse/config/freeModelCatalog.ts` + `docs/reference/FREE_TIERS.md`
- Dashboard: http://localhost:20128 and `/dashboard/free-tiers` live budget
