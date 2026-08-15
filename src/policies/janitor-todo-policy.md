# Janitor TODO Policy — Append and Attest Only

A cleanup agent that both discovers and clears work can quietly redefine what counts as
done. This chapter records Decision D4: the janitor and swarm agents may only grow the TODO
ledger or attest completions — they may never clear it.

## The decision

Decision D4-A (the MUST option) governs here. The janitor and swarm agents may only *grow*
the TODO ledger or *attest* that work is finished. They may never remove items or reset the
list.

## The rules

1. **Add freely.** Janitor runs may append new findings as ⬜ items, each tagged with the
   discovering commit or run reference.
2. **Flip ⬜ → ✅ only with evidence in the same commit.** The flip commit message must name
   the pull request or commit that proves the work (for example, `done by c85ea43`). A bare
   flip with no pointer is reverted in review.
3. **Never delete, never clear.** No janitor run may remove items, rewrite sections, or
   downscope wording. Ambiguity is an oracle question, not an edit permission.
4. **Stale items stay put.** An item remains in the ledger until an orchestrator session
   moves it under an `## Archive` heading with an explicit `archive:`-prefixed commit message
   explaining why each item is obsoleted.
5. **Auditable by construction.** Every TODO.md mutation by an automated agent carries its
   run URL in the commit trailer (`Swarm-Run: …`), enforced by review, so the ledger's
   history is reconstructable end to end.

## Why seed-and-clear is forbidden

A janitor that both seeds and clears controls the *denominator* of done. Completion numbers
become unfalsifiable, and silently dropped items are exactly the silent-failure class that
`tools/silent_failures.py` exists to gate (SF1–SF4). Attest-only keeps the ledger monotone
and every ✅ provable.

> **Tip —** Treat the TODO ledger as an append-only log, not a checklist to empty. The value
> is in what stays visible, not in reaching zero.

*Orchestrated 2026-08-13 (Decision D4, user-chosen MUST option).*
