# Architecture Decision Records (ADRs)

> 19 decisions that define Shesh. Status: all Accepted. See `AUDIT_AND_ROADMAP.md` for decision map.

These records capture the architectural choices that shape the Shesh fleet: the languages
it speaks, the way it is packaged and released, and the boundaries that keep a local-first
agent safe to run on a daily driver. Each record follows the same anatomy — a Status, the
Context that forced a choice, the Decision itself, and its Consequences — so the reasoning
stays legible long after the code it describes was written.

A decision, once Accepted, is treated as immutable. When circumstances change, a new record
supersedes the old one rather than rewriting history. ADR-0016 and ADR-0017 are the clearest
examples: each explicitly narrows or completes an earlier record instead of editing it.

## The decision map

| # | Title | Date | Status |
|---|-------|------|--------|
| 0001 | [Five Languages Only](0001-five-languages.md) | 2026-08-09 | Accepted |
| 0002 | [Rootless Containers for Exotic Runtimes](0002-containers-and-venv.md) | 2026-08-09 | Accepted |
| 0003 | [Federated Repos + Manifest, Not Monorepo](0003-federated-repos.md) | 2026-08-09 | Accepted |
| 0004 | [Three Release Channels](0004-three-channels.md) | 2026-08-09 | Accepted |
| 0005 | [Local-First, Cloud Opt-In](0005-local-first.md) | 2026-08-09 | Accepted |
| 0006 | [Immutable Base + Evidence-Backed /refine](0006-refine-governance.md) | 2026-08-09 | Accepted |
| 0007 | [Six Agent Roles, 6 GB VRAM Budget](0007-agent-roles.md) | 2026-08-09 | Accepted |
| 0008 | [Archive shesh-kernel, Don't Force Merge](0008-kernel-archive.md) | 2026-08-10 | Accepted |
| 0009 | [Newelle Fork as shesh-voice with Overlay](0009-shesh-voice-overlay.md) | 2026-08-09 | Accepted |
| 0010 | [ACP Adopted Alongside MCP](0010-acp-plus-mcp.md) | 2026-08-09 | Accepted |
| 0011 | [Catch-Up Scheduler, Not Fixed Cron](0011-catchup-scheduler.md) | 2026-08-09 | Accepted |
| 0012 | [Warm Proactivity at Natural Pauses](0012-warm-proactivity.md) | 2026-08-09 | Accepted |
| 0013 | [Hierarchical Memory + Token-Bounded Context](0013-hierarchical-memory.md) | 2026-08-09 | Accepted |
| 0014 | [Habit Learning is Frequentist with Decay](0014-habit-learning.md) | 2026-08-09 | Accepted |
| 0015 | [Every Tool Call Through shesh-audit Guard](0015-guard-policy.md) | 2026-08-09 | Accepted |
| 0016 | [Kernel Consolidation — Merge Withdrawn, Wave Adopted](0016-kernel-consolidation.md) | 2026-08-12 | Accepted |
| 0017 | [Canonical Naming Purge Completed](0017-naming-purge-completed.md) | 2026-08-12 | Accepted |
| 0018 | [Adopt-vs-Build Decisions & the 2026-08-12 Excision](0018-adopt-vs-build.md) | 2026-08-12 | Accepted |
| 0019 | [Fold sub-service shesh-* modules into shesh-core monorepo](0019-shesh-core-monorepo.md) | 2026-08-13 | Accepted |

> **Note —** This table previously omitted ADR-0019. It is restored here so the count of
> nineteen decisions matches the index above. The records themselves are unchanged.

## How to add a new ADR

Copy an existing record as a template, then edit its title, date, context, decision, and
consequences. Link the new record from `AUDIT_AND_ROADMAP.md` and from `TODO.md` if it is a
P0 or P1 item.

```bash
cp docs/history/adr/0001-five-languages.md docs/history/adr/0020-my-decision.md
# Edit: update title, date, context, decision, consequences
# Link from AUDIT_AND_ROADMAP and TODO if P0/P1
```

Keep every ADR immutable after it is Accepted. Supersede with a new ADR when a decision must
change, rather than rewriting the original.
