# 9. Agent behavior

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 9 of 16.

- [ ] Start a goal via `shesh-orchestrator-mcp` → `execute("...")`; it plans,
      delegates by role, and the critic approves
- [ ] **Background sessions** work: `start_session`, disconnect, `get_session`
      later shows progress/result
- [ ] `cancel_session` actually stops a long-running goal
- [ ] `/refine` only promotes a skill/memory change if the held-out evaluator
      scores ≥ 0.7 (check `recent_refinements`)
- [ ] The LLM is used when Ollama responds; offline, the deterministic stubs
      keep the system working
- [ ] **Memory compaction** runs without data loss:
      `shesh-memory-mcp` → `compact_memory()`; old episodes move to
      `semantic.md`, very old ones are deleted
- [ ] Semantic search (`semantic_search`) returns relevant memories
- [ ] Habits/intentions/mannerisms reflect your actual preferences over time

---
