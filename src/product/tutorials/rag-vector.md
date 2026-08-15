# Tutorial — memory and recall (RAG today, vector search planned)

Status: living · last verified 2026-08-13

Component: [shesh-memory](https://github.com/gaganjainse/shesh-memory).

An honest scope note up front: `shesh-memory` today stores episodes under
`~/.local/share/shesh/memory/` as **human-readable, portable files with no vector database**.
Embedding-based retrieval is an explicitly optional future provider, not shipped code. This
tutorial covers what exists now, not the roadmap.

## What you get today

- **Memory layers** — a short-term and long-term split per ADR-0013, with token-bounded context
  assembly.
- **Habit learning** — frequentist with decay (ADR-0014): routines surface without an LLM call.
- **MCP tools (stdio)** — including `recall(query)` to search past episodes, and context assembly
  for prompt building.

## Walkthrough

1. Let the agent run for a day; episodes accumulate in the store.
2. Ask "what did we decide about X last week?" and the agent calls `recall`.
3. Inspect the store directly — it is plain files, so `grep` works, and
   [shesh-backup](https://github.com/gaganjainse/shesh-backup) covers it with the rest of
   `~/.local/share/shesh/`.

## When vector search lands

The provider seam is designed for it, and the migration path is additive: embeddings sit alongside
the plain store while the files stay canonical. It will be announced in QUERYLOG, and this
tutorial will be updated in the same commit — documentation changes with code, per
[documentation policy](../../policies/documentation-policy.md) rule 7.
