---
name: autopilot
description: Continue the Shesh build autonomously by following TODO.md, testing every change, and updating docs/querylog.
---

# Autopilot Skill

Autopilot lets the fleet make unsupervised progress without drifting off the map. When the
user says "continue" or asks for unattended work, this skill anchors every move to `TODO.md`
and stops at clear boundaries.

## The rules

1. **Anchor to TODO.md.** Read it top to bottom. Pick the highest-priority ⬜ item that is not
   🔴 blocked. Do not invent scope outside the list — if something new is discovered, add it
   to TODO first.
2. **One branch per item.** `feat/<short-name>`. Use small Conventional Commits. Never force-
   push `main`. Never delete repositories (archive instead).
3. **Tests gate everything.** Every component has tests; add one for the change. Run the
   component's `pytest -q`, `cargo test`, or `ruff check`. If a gate fails, fix it before
   moving on. If a dependency (GPU, display) is missing, mark the item 🟡 and note the
   hardware gate rather than faking success.
4. **Update docs as you go.**
   - Flip the TODO status (⬜ → 🟡 or ✅).
   - Append the user's prompt, your answer, and doc links to
     `docs/history/queries/QUERYLOG.md`.
   - If you created or changed a component, refresh `docs/components/`.
5. **Stay local-first and safe.** No cloud calls by default. Destructive actions require
   confirmation. Every action flows through the `shesh-audit` policy.
6. **Stop conditions:** all ⬜ done, a 🔴 is hit, tests cannot pass, or the user interrupts.
   Report what shipped, what is blocked, and what is next.
7. **Workflow helper:** `scripts/supervise.sh [--loop|--dry-run]` enforces the
   branch/test/commit/TODO-update cycle. Use it, but the implementation judgment is yours.

> **Warning —** The autopilot may run without a human watching, but it must never fabricate a
> pass. A 🟡 hardware gate is honest; a false ✅ is a violation of the audit discipline.
