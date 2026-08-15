# Learning Architecture

Shesh learns your intentions, habits, and mannerisms without destabilizing itself or
overflowing the model's context window. This chapter describes the memory layers, how
context is assembled, how habits form, and how the Continual Harness keeps self-improvement
reviewable.

- **Summary**
  - Memory is layered, from a small working context up to durable habits and learned skills.
  - Context assembly trims lowest-priority sections first so the prompt always fits.
  - Habit learning is frequentist and inspectable, not hidden model state.
  - The Continual Harness edits supplemental state only; the base prompt and safety skills are immutable.
  - Ambient signals feed episodes and habits without keystroke-level surveillance.

---

## Memory layers

1. **Working** — the current task or session, always in context and small.
2. **Episodic** — append-only JSONL events (`remember`) with SQLite full-text search.
3. **Semantic** — durable facts about the user (`note_fact`), editable Markdown.
4. **Intentions** — active goals with priority and a lifecycle.
5. **Mannerisms** — communication-style preferences, editable Markdown.
6. **Habits** — corroborated recurring patterns with confidence and decay.
7. **Procedural/Harness** — learned skills and supplemental prompt refinements.

---

## Context assembly

`shesh-memory assemble_context(query, working, max_tokens)` builds a bounded prompt in
priority order: mannerisms, intentions, semantic facts, active habits, skills, the working
task, relevant episodes, and a recent tail. The lowest-priority sections are trimmed first,
so the prompt always fits.

---

## Habit learning

`shesh-memory learn_habit(signature, description, success)` counts observations with
reliability-weighted confidence. After enough corroboration it becomes a candidate habit;
confidence decays over time and stale habits archive. This is frequentist, not hidden model
state, so the user can inspect, edit, or disable it.

---

## The Continual Harness

`shesh-harness refine(trigger, trajectory)` proposes the smallest supported change to
supplemental state, evaluates it, applies it only if the score passes, records the
before/after, and supports revert. The immutable base prompt and the safety skills cannot
be changed. This prevents overfitting and cheating loops, and makes self-improvement
reviewable. See [Multi-Agent Architecture](../architecture/multi-agent.md) for the full
harness lifecycle.

---

## The ambient feedback loop

`shesh-ambient` observes coarse signals (workspace switches, idle, completed commands) and
records episodes and habits without keystroke-level surveillance. Proactive offers are
informed by active intentions and habits, but they are always optional.

---

## Retention policy

- Episodes are retained indefinitely but summarized and archived by a future compaction job.
- Habits decay with a two-week half-life and archive below a threshold.
- Harness refinements are append-only; bad ones are reverted, not deleted.
