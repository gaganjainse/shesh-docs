# Agent behavior

The agent is the part of the Shesh body that plans, delegates, and learns. This chapter
confirms a goal actually moves through planning, background execution, self-improvement,
and memory without losing data.

> **Note —** This chapter is section 9 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Planning and sessions

- [ ] Start a goal through `shesh-orchestrator-mcp` → `execute("...")`; it plans,
      delegates by role, and the critic approves.
- [ ] **Background sessions** work: `start_session`, disconnect, and a later
      `get_session` shows progress or result.
- [ ] `cancel_session` actually stops a long-running goal.

## Learning and memory

- [ ] `/refine` promotes a skill or memory change only when the held-out evaluator
      scores **≥ 0.7** (check `recent_refinements`).
- [ ] The LLM is used when Ollama responds; offline, the deterministic stubs keep the
      system working.
- [ ] **Memory compaction** runs without data loss: `shesh-memory-mcp` →
      `compact_memory()`; old episodes move to `semantic.md` and very old ones are
      deleted.
- [ ] Semantic search (`semantic_search`) returns relevant memories.
- [ ] Habits, intentions, and mannerisms reflect your actual preferences over time.
