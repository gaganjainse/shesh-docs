# ADR-0013: Hierarchical Memory + Token-Bounded Context Assembly

Shesh stores memory in distinct tiers and assembles context within a hard token budget, so the
agent never overflows its window and never drops the mannerisms that make it sound like itself.
The design treats memory like a well-indexed filing cabinet: recent, frequent, and
personally important papers sit on top.

> **Summary —**
> - Memory splits into working, episodic, semantic, intentions, mannerisms, habits, and skills.
> - A ContextAssembler assembles context by priority and trims the lowest priority first.
> - Retrieval uses full-text search plus a pluggable embedder, offline or online.
> - A compaction step summarizes old episodes to keep growth bounded.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** memory, rag, context-window, token-budget

## Context

The agent needs several kinds of memory: episodic (what happened today and yesterday),
semantic (facts that persist), working (the current goal's steps), intentions (long-term
goals), mannerisms (tone), and habits (frequent actions).

The LLM context window is finite — phi4-mini holds roughly 8k tokens. A naive dump of all
history overflows; naive truncation loses the mannerisms that matter. Old episodes should
summarize rather than live forever.

## Decision

`shesh-memory` implements the hierarchy:

```text
working/         # current task trace (hot)
episodic/YYYY-MM-DD.md  # daily notes, appended
semantic.md      # persistent facts
intentions.md    # user's stated goals
mannerisms.md    # tone and communication style
habits.md        # frequentist learned habits
skills/*.md      # Markdown skills
```

The **ContextAssembler** assembles context within a token budget by priority: mannerisms,
intentions, facts, habits, skills, working, relevant (full-text or vector results), then
recent episodes. It trims the lowest priority first and never exceeds the model budget.

**Retrieval** uses full-text search over episodes plus a SQLite vector store (cosine) behind a
pluggable embedder: an offline deterministic hash embedder (no model, tests green) or, online,
Ollama's `nomic-embed-text`.

**Compaction** offers a `compact_memory()` MCP tool that summarizes old episodes in batches into
`semantic.md` via an injectable summarizer (an LLM in production, a deterministic stub offline),
with a retention window and deletion of very old entries.

MCP tools include `recall`, `remember`, `semantic_search`, `index_memory`, and
`compact_memory`.

## Consequences

### Benefits

- Context never overflows because the token budget is enforced.
- Important material — mannerisms and intentions — is always present.
- The past is searchable, and compaction prevents infinite growth.

### Costs

- Summarizer quality matters; the LLM summarizer needs evaluation.

## Links

- `docs/LEARNING.md`, `docs/components/shesh-memory.md`
- `shesh-memory` (26 tests)
- [ADR-0014: Habit Learning](0014-habit-learning.md), [ADR-0006: /refine Governance](0006-refine-governance.md)
