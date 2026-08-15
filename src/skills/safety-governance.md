---
name: safety-governance
description: Every autonomous action must be safe, audited, and reversible. Destructive actions require confirmation.
---

# Safety and Governance Skill — Highest Priority

This skill overrides the others. Before any tool call that changes state, the fleet classifies
the risk, respects forbidden scopes, and writes a receipt — so an autonomous action is always
safe, audited, and reversible.

## Before any state-changing call

1. **Classify risk:**
   - *read-only* (search, fetch, git status, list) → run freely.
   - *reversible write* (append note, organize a file into an undo log, create a branch) → run
     it, and log it.
   - *destructive* (delete, overwrite, `pacman -R`, force-push, write outside allowed dirs) →
     **stop and ask** for explicit confirmation.
2. **Scope:** never touch `~/Documents/Job`, `~/Projects/job`, `~/Vaults`, `~/.ssh`, or
   `~/.gnupg`.
3. **Audit:** every action is written to the append-only Shesh audit log. Report what you did.
4. **Offline by default:** no cloud calls unless the user enabled the cloud tier and confirms.
5. **Undo:** prefer moves to trash (`gio trash`) over deletes; keep an undo record.
6. **On error:** stop, report the exact command and error, suggest one fix — do not thrash.

> **Warning —** This skill is the floor, not the ceiling. A specialized skill may add steps,
> but it may never relax the destructive-action or scope rules defined here.
