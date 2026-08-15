---
title: Cloud model providers
type: reference
summary: "OmniRoute catalog includes industry-used big models free, not only small local:."
audience: operator
status: current
verified: 2026-08-15
---

# Cloud model providers

> Extracted from the full [OmniRoute study](https://github.com/gaganjainse/shesh-docs-archive/blob/main/src/omniroute-study.md); numbers re-verified 2026-06-17, refresh CI-gated.

## Free tiers — honest numbers (2026-06-17 refresh, CI-gated)
| Metric | Tokens/mo | Meaning |
|--------|-----------|---------|
| **Documented recurring steady** | **~1.51B** | Free-tier pools, each shared pool counted once. Source `freeModelCatalog.ts`, API `/api/free-tier/summary`, dashboard Free-Tier Budget. **Use this.** |
| + first month signup credits | ~2.13B | Steady + one-time (Together $25, Z.AI 20M, DeepSeek 5M) first month only |
| + permanently free no cap | un-quantifiable | `siliconflow`, `glm-cn` GLM-4-Flash, `tencent`, `baidu`, `kilo-gateway`, `opencode-zen` — real recurring, rate-limited, no token cap, never summed (counting RPM×24/7 would inflate to ~10B fantasy) |
| + deposit-unlock boost | +~24M | OpenRouter $10 top-up raises free 50→1000 req/day |
| Theoretical ceiling (all rate limits 24/7) | ~10B | Fantasy, not guarantee |

**Biggest contributors:** `mistral` 1.00B, `llm7` 150M, `groq` 117M, `gemini` 60M, `cerebras` 30M, `cloudflare-ai` 30M, `sambanova` 30M

**Per-provider free (sample 2026-06-17):**

| Provider | Type | Steady/mo | Models | Notes |
|----------|------|-----------|--------|-------|
| `mistral` | recurring | ~1.00B | 5 | Consumer ToS personal needs |
| `llm7` | recurring | ~150M | 4 | Experimentation |
| `gemini` | recurring | ~60M | 6 | Flash family only, pooled |
| `cerebras` | recurring | ~30M | 2 | |
| `cloudflare-ai` | recurring | ~30M | 6 | 10k Neurons/day |
| `groq` | recurring | ~15M | 5 | 14.4k req/day free tier |
| `openrouter` | recurring | ~1M | 1 | 50 req/day free |
| `cohere` | recurring | ~800K | 6 | |
| `huggingface` | recurring | ~200K | 6 | |
| `glm-cn` | uncapped | uncapped* | 4 | GLM-4-Flash permanently free +20M signup |
| `kilo-gateway` | uncapped | uncapped* | 7 | Auto free rotating set: Nemotron 3, StepFun, Poolside |
| `opencode-zen` | uncapped | uncapped* | 6 | 6 rotating free coding models |
| `siliconflow` | uncapped | uncapped* | 10 | DeepSeek V3.2/R1 free tier |

**Free forever, no card, no token cap (rate-limited):** Qoder AI (Qwen3-Max, Kimi-K2 unlimited), Pollinations (GPT, Llama, Claude no key), Cloudflare AI (50+ models 10k neurons/day), NVIDIA NIM (GLM, MiniMax ~40 RPM free), Cerebras (GLM), Kilo Code, OpenCode Zen, Z.AI GLM, Requesty (GPT-OSS 120B, Nemotron free), SiliconFlow (DeepSeek V3.2/R1)

**Why numbers dropped from 1.94B→1.51B:** Honesty correction — gemini pooled (was inflated counting each Flash variant 462M→60M), cloudflare corrected 122M→30M, doubao reclassified as one-time credit, removed shutdown tiers (chutes, phind, kluster). New free providers added Kilo, OpenCode Zen, Z.AI.

---

## Big industry-used free models (not small local)
OmniRoute catalog includes **industry-used big models** free, not only small local:

- **Claude** via Kiro AI free (Claude Sonnet 4.5, Haiku 4.5, Opus 4.6) ~50 credits/month per account free
- **GPT** via Pollinations, OpenCode, Requesty, Puter — GPT-4o mini 150M tokens/mo documented, GPT-OSS 120B free forever
- **Gemini** via Gemini free tier — 60M tokens/mo, Flash family
- **DeepSeek** via DeepSeek V3.2/R1, V4 Flash/Pro — free tier 5M signup + recurring via SiliconFlow, NVIDIA NIM
- **Llama** via Groq, Cloudflare, Together, SambaNova — Llama 3.1 8B/70B/3.3 70B
- **Mistral** Large 3 — 1B tokens/mo biggest contributor
- **Qwen** Qwen3-Max, Qwen3-Next-80B-A3B via Qoder, Alibaba
- **Kimi** K2, K3 1M context — Moonshot AI founding friend, free via Kimi provider
- **GLM** GLM-4-Flash/4.5-Flash/4.7-Flash permanently free via Z.AI, GLM-CN
- **MiniMax** M2.1, M2 — cheap $0.2 + free via NVIDIA NIM

These are **not small local** — they are frontier 70B-120B-550B models with free tiers.
