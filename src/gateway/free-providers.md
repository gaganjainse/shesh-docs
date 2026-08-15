# Free providers — Groq, OpenRouter, GitHub Models, and more

> **Note —** Extracted from the full [OmniRoute study](omniroute-study.md).
> Figures were re-verified on 2026-06-17 and are refreshed under CI gates.

Shesh's optional cloud gateway can draw on a large pool of free model capacity.
This chapter distills that capacity into the figures a builder can plan around,
and explains why the honest number is smaller than early estimates.

## Summary

- Plan around the ~1.51B recurring steady free pool; everything else is one-time
  credit or unmeasurable.
- `mistral`, `llm7`, and `groq` supply the largest steady free capacity.
- Several providers are uncapped but rate-limited, stretching the pool without a
  hard token ceiling.
- Frontier models — Claude, GPT, Gemini, DeepSeek, Llama, Qwen, Kimi, GLM,
  MiniMax — all expose free tiers.

## Free tiers — the honest numbers

The single figure to plan around is the **documented recurring steady** pool. It
counts each shared free tier once and is the value the catalog, the API summary,
and the dashboard all agree on. Everything else is either one-time credit or
uncapped and unmeasurable.

| Metric | Tokens/mo | Meaning |
|--------|-----------|---------|
| **Documented recurring steady** | **~1.51B** | Free-tier pools, each shared pool counted once. Source `freeModelCatalog.ts`, API `/api/free-tier/summary`, dashboard Free-Tier Budget. **Use this.** |
| + first month signup credits | ~2.13B | Steady plus one-time (Together $25, Z.AI 20M, DeepSeek 5M), first month only |
| + permanently free, no cap | un-quantifiable | `siliconflow`, `glm-cn` GLM-4-Flash, `tencent`, `baidu`, `kilo-gateway`, `opencode-zen` — real recurring, rate-limited, no token cap, never summed |
| + deposit-unlock boost | +~24M | OpenRouter $10 top-up raises free 50 to 1000 requests/day |
| Theoretical ceiling (all limits 24/7) | ~10B | Fantasy, not a guarantee |

> **Warning —** Counting rate limits around the clock would inflate the pool to a
> ~10B fantasy. Treat the ~1.51B recurring steady figure as the planning baseline.

**Biggest contributors:** `mistral` 1.00B, `llm7` 150M, `groq` 117M, `gemini` 60M,
`cerebras` 30M, `cloudflare-ai` 30M, `sambanova` 30M.

## Per-provider free capacity

The sample below reflects the 2026-06-17 refresh. "Uncapped" means rate-limited
but without a hard token ceiling.

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
| `siliconflow` | uncapped | uncapped* | 10 | DeepSeek V3.2/R1 free tier |

**Free forever, no card, no token cap (rate-limited):** Qoder AI (Qwen3-Max,
Kimi-K2 unlimited), Pollinations (GPT, Llama, Claude no key), Cloudflare AI
(50+ models, 10k neurons/day), NVIDIA NIM (GLM, MiniMax ~40 RPM free), Cerebras
(GLM), Kilo Code, OpenCode Zen, Z.AI GLM, Requesty (GPT-OSS 120B, Nemotron
free), SiliconFlow (DeepSeek V3.2/R1).

## Why the number dropped from 1.94B to 1.51B

The revision was an honesty correction, not a loss of capacity. Gemini was pooled
correctly (each Flash variant had been counted separately, 462M falling to 60M),
Cloudflare was corrected from 122M to 30M, Doubao was reclassified as a one-time
credit, and shutdown tiers (Chutes, Phind, Kluster) were removed. New free
providers — Kilo, OpenCode Zen, and Z.AI — were added.

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
parameter models that happen to expose free tiers.
