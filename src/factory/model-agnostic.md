# The Model-Agnostic Workflow — Consistent Output From Inconsistent Models

Swap the model behind an agent and the agent's behavior changes: one returns clean JSON, the next
returns a friendly paragraph, and the orchestrator that consumed the first one breaks on the
second. This chapter explains the five layers the fleet uses to make every free model — local or
hosted — produce the same validated output shape.

## Summary

- Models differ in JSON support, tool calling, prompt sensitivity, context length, and training,
  and any of those differences can break a caller.
- The fix is not to find one good model; it is to declare a schema per task and refuse anything
  that does not match it.
- Five layers apply: strict schema, a uniform prompt, a validate-and-repair loop with three
  retries, a free-first fallback chain, and score-based grading.
- The chain always terminates in a deterministic stub, so callers never receive fabricated
  structure.
- The target is measured: variance under 0.1 in score and 100 percent JSON validity.

## Why models disagree

The variance is not random; it comes from five identifiable sources, and knowing which one you
are facing tells you which layer catches it.

| Source of variance | Example |
|---|---|
| JSON mode support | `phi4-mini` via Ollama supports JSON; `moondream2` does not, so one emits `{"steps": ...}` and the other emits prose |
| Tool calling | `gpt-4o-mini` supports tools; `gemma-2-9b-it:free` does not, so a coder role fails |
| Prompt sensitivity | Some models need a fenced `json` block, others need an explicit "output only JSON" instruction |
| Context length | `moondream2` holds 2048 tokens against `Phi-3-medium` at 128k, so long histories overflow the small model |
| Training focus | `qwen2.5-coder:3b` is strong at code, `moondream2` at vision, `phi4-mini` at reasoning — planner quality differs accordingly |

The concrete failure is easy to picture. Model A returns
`{"steps": [{"id": "1", "role": "coder", "goal": "organize"}]}`, which parses. Model B returns
"Sure! Here are steps: 1. Organize…", which does not. Without guardrails, the orchestrator breaks
on model B.

## Layer one: a schema per task, not per model

Every task declares its required output shape as a JSON schema. The shape belongs to the task, so
it does not change when the model does.

```json
{
  "type": "object",
  "required": ["steps"],
  "properties": {
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "role", "goal"],
        "properties": {
          "id": {"type": "string"},
          "role": {"type": "string", "enum": ["coder","researcher","vision","critic"]},
          "goal": {"type": "string"}
        }
      }
    },
    "approved": {"type": "boolean"}
  }
}
```

Conformance is validated rather than assumed. The schema lives on
`tools/llm_adapter.py:TaskSpec.schema`.

## Layer two: one prompt template for every model

The same template goes to every model, including those with no native JSON mode, because a clear
instruction plus an example works even where a mode flag does not.

```text
You are a {role} agent in Shesh ecosystem. You must output VALID JSON ONLY, no extra text.
Goal: {goal}
User request: {user_prompt}
Required JSON schema: {schema}
Rules:
- Output ONLY valid JSON, no markdown outside, no explanation
- Use a fenced json code block if you must, but the JSON inside must be valid
- Must contain: [...]
- Must NOT contain: [...]
Example valid output: {"steps": [{"id":"1", "role":"coder", "goal":"organize Downloads by type"}]}
```

A retry adds a repair instruction: *your previous output was invalid, the error was `{error}`,
fix it and output only valid JSON*. This works across Ollama, Groq, OpenRouter free, GitHub
Models, and HuggingFace. The builder is `tools/llm_adapter.py:build_prompt()`.

## Layer three: validate, repair, and retry three times

The loop is small enough to read in full, and its order is the point: parse, then validate, then
grade, then return.

```python
for model in chain:
    for attempt in range(3):
        raw = _call_model(model, prompt)
        data, err = extract_json(raw)          # fenced block, raw JSON, or brace scan
        if data is None:
            last_error = err; continue
        ok, verr = validate_against_schema(data, schema)
        if not ok:
            last_error = verr; continue
        score = grade_output(data, task)       # must_contain / must_not_contain
        if score < min_score:                  # 0.7
            last_error = f"score {score} < 0.7"; continue
        return data, model, score
```

`extract_json()` is deliberately forgiving about packaging and strict about content: it tries a
fenced block, then raw JSON, then a balanced-brace scan, which handles a model that wraps valid
JSON in commentary. `validate_against_schema()` checks required keys rather than merely confirming
the text parses. `grade_output()` applies the same `must_contain` and `must_not_contain` scoring
the held-out evaluator uses. After three failed attempts, the next model in the chain is tried.

## Layer four: a free-first fallback chain

`manifests/models.toml` describes every free model with its capabilities, context length, JSON
support, and priority. The chain runs from the most private and cheapest outward.

| Priority | Provider | Models | Notes |
|---|---|---|---|
| 1 | Ollama local | `phi4-mini`, `qwen2.5-coder:3b`, `moondream2`, `nomic-embed-text` | Offline, 6 GB VRAM, no API key |
| 2 | Groq free | `llama-3.1-8b-instant`, `llama-3.3-70b-versatile` | Free tier, 14.4k requests per day, needs `GROQ_API_KEY` |
| 3 | OpenRouter free | `google/gemma-2-9b-it:free`, `meta-llama/llama-3.1-8b-instruct:free`, `qwen/qwen-2-7b-instruct:free` | `:free` suffix, needs `OPENROUTER_API_KEY` |
| 3 | GitHub Models free | `gpt-4o-mini`, `Phi-3-medium-128k` | Uses `GITHUB_TOKEN`, free for public repositories |
| 4 | HuggingFace free | `Phi-3-mini-4k-instruct` | Needs `HF_TOKEN` |
| 99 | Stub | `stub-planner`, `stub-coder`, and peers | Deterministic, always valid, zero variance, final fallback |

`Router.pick(role, min_context, require_json, free_only=True)` filters by capability — a planner
role requires the `planner` capability — then by context length and JSON support, and sorts by
priority, a JSON bonus, and descending context. Because schema, validation, and grading are
identical at every step, the output shape does not depend on which model in the chain succeeded.
See [model_router.py](model-router.md).

For gateway routing, set `LITELLM_CONFIG` or run a LiteLLM proxy: the adapter tries
`litellm.completion()` when the library is installed and otherwise calls Ollama, Groq,
OpenRouter, or GitHub Models directly. A missing key skips that model and moves to the next
rather than raising.

## Layer five: grading, and measuring the variance

Grading reuses the harness contract: `must_contain`, `must_not_contain`, structural checks, a
score from 0 to 1, and a `min_score` gate of 0.7. `tools/llm_adapter.py:grade_output()` applies
it per response.

Measurement is the other half. `scripts/eval_model_agnostic.py` — planned, and listed in the
factory tooling inventory — runs the same tasks across every free model and reports the spread:
it runs a task such as "organize Downloads" against `phi4-mini`, a Groq Llama 8B, `gemma-2-9b:free`,
`gpt-4o-mini`, and the stub, then checks each output for valid JSON, required keys, required
substrings, and score. If every model scores at least 0.7 and produces the same shape, quality is
consistent.

That is the precise claim being made. Not that every model is equally capable, but that invalid or
low-quality output is caught and retried or replaced, and that valid output always has the same
shape, so the orchestrator does not break.

## Enabling the free providers

Every model in `models.toml` is free to use. What differs is whether a key is needed.

| Provider | How to enable | Cost |
|---|---|---|
| Ollama local | `ollama pull phi4-mini qwen2.5-coder:3b moondream2 nomic-embed-text` | Free, offline |
| Groq | Create a free key at `https://console.groq.com/keys`, export `GROQ_API_KEY` | Free, 14.4k requests per day |
| OpenRouter | Create a free key at `https://openrouter.ai/keys`, export `OPENROUTER_API_KEY`, use `:free` models | Free |
| GitHub Models | Export `GITHUB_TOKEN` from the existing token; free for public repositories | Free |
| HuggingFace | Create a free read token at `https://huggingface.co/settings/tokens`, export `HF_TOKEN` | Free |
| Stub | Always available, no key | Free, zero variance |

```bash
export GROQ_API_KEY=... OPENROUTER_API_KEY=... HF_TOKEN=...
export GITHUB_TOKEN=$(cat ~/.config/shesh/github.pat)
python tools/model_router.py --role planner --list
python tools/llm_adapter.py --role planner --goal "test" --prompt "organize"
```

Store keys in `~/.config/shesh/env` at mode 600 rather than in shell history where practical. A
LiteLLM proxy can consume the same set, and `manifests/models.toml` converts into a LiteLLM
configuration.

> **Note —** No paid provider is required anywhere in this workflow. Missing keys cause a model
> to be skipped, never a crash.

## Calling the workflow

```python
from tools.llm_adapter import ModelAgnosticAdapter, TaskSpec
from tools.model_router import Router

router = Router()                                    # loads free models from models.toml
model = router.pick(role="planner", require_json=True, free_only=True)

adapter = ModelAgnosticAdapter()
task = TaskSpec(
    role="planner",
    goal="organize Downloads by type",
    schema={"type": "object", "required": ["steps"]},
    must_contain=["organize"],
    must_not_contain=["rm -rf /"],
    min_score=0.7,
)
data, used_model, score = adapter.generate(task, user_prompt="...", max_retries=3)
```

If `phi4-mini` fails to produce valid JSON three times, the adapter tries the Groq Llama 8B, then
`gemma-2-9b:free`, then `gpt-4o-mini`, then the stub. It always returns valid JSON, and the
validation and grading gates are identical at every step.

```bash
python tools/llm_adapter.py --role planner --goal "organize Downloads" --list-models
python tools/llm_adapter.py --role planner --goal "organize Downloads" --prompt "organize Downloads"
python scripts/eval_model_agnostic.py --role planner --tasks 10   # planned harness
```

The goal is variance under 0.1 in score with 100 percent JSON validity. When a model misses that
bar, the response is to adjust the prompt template or schema, or to lower that model's priority in
`models.toml`.

## How components consume it

Four consumers changed when the workflow landed, and each change removed a hardcoded assumption.

| Component | Before | After |
|---|---|---|
| `shesh-mind` | Hardcoded role-to-model mapping | `Router.pick(role)` — capability-based, free-first, falling back through Groq, OpenRouter, GitHub Models, then stub |
| `shesh-orchestrator` | `LLMAgents` called Ollama directly | Uses `ModelAgnosticAdapter`, so planner and critic quality is consistent across models |
| `shesh-harness` | Held-out evaluator scoring 0 to 1 with a 0.7 minimum | Same grading now shared with the adapter, so self-improvement is safe regardless of model |
| Swarm workers | Provider chosen implicitly | `--model-policy free-only` restricts them to free models |

## Why the earlier failure does not repeat

Before, a hardcoded `phi4-mini` meant that an unavailable Ollama or a model weak at JSON took the
whole workflow down, and quality varied with the model of the day.

Now, capability-based routing, a strict schema, validation, a repair loop, a fallback chain, a
grading gate, and a deterministic final stub combine so that the output shape is identical
regardless of model, invalid output is retried or replaced, and the score gate holds quality at
0.7 or better. The adapter that implements all of this is documented in
[llm_adapter.py](llm-adapter.md); the provider survey behind the chain order is the
[OmniRoute study](../gateway/omniroute-study.md).
