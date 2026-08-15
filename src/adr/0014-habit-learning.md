# ADR-0014: Habit Learning is Frequentist with Decay, Not Opaque Weights

Shesh learns habits by counting observed behavior and letting it decay, not by training opaque
neural weights. The design keeps what the agent "learns" inspectable and reversible — a ledger
a person can read and undo, not a black box.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** learning, habits, interpretability

## Context

The fleet should learn habits, intentions, and mannerisms from observed behavior. Two paths
existed: opaque neural weights (not inspectable, not reversible, needing training data) or
frequentist counting with decay (inspectable, reversible, simple).

The user is technical and wants something inspectable and reversible, not a black box.

## Decision

- **Habits** are learned through frequency, corroboration, and decay in `shesh-memory`:
  - Event: "the user runs `check_system_updates` after boot, five days in a row at 9am."
  - A counter increments; after corroboration (three or more times) the habit is promoted to a
    candidate in `habits.md`.
  - Decay: if unseen for 30 days, the weight decays and is eventually archived.
  - The user reviews candidate habits through `/refine` or a settings GUI — they are never
    auto-applied as "always allow."
- **Intentions** are explicit: "you told me to remind about backup daily" lands in
  `intentions.md`, never inferred.
- **Mannerisms** are style snippets collected from the user's edits and approvals, ranked by
  frequency.
- Everything is stored as Markdown — human-readable, git-tracked, and rollback-capable.

No embedding-only learning and no opaque vector is used.

## Consequences

### Benefits

- Inspectable: `cat ~/.local/share/shesh/memory/habits.md` shows the truth.
- Reversible: delete a line or roll back through the harness.
- Decay prevents stale habits from lingering.

### Costs

- Less expressive than a neural approach, though sufficient for desktop habits.
- The corroboration threshold (currently three occurrences) needs tuning.

## Links

- `docs/LEARNING.md`, `shesh-memory/src/habits.py`
- [ADR-0013: Hierarchical Memory](0013-hierarchical-memory.md)
