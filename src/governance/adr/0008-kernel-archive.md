---
title: "ADR-0008: Archive the kernel rather than force a merge"
type: explanation
summary: "Archive the kernel rather than force a merge."
audience: maintainer
status: current
verified: 2026-08-15
---

# ADR-0008: Archive the kernel rather than force a merge

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-08-10 |
| **Deciders** | Fleet maintainer |

## Context

_Not recorded._

## Decision

- **Do NOT force-merge** the two Rust trees — would ship broken build.
- Archive `shesh-kernel` as `shesha-kernel` (GitHub redirect) — superseded by SheshAOS.
- Document staged rebase plan in `SheshAOS/KERNEL_MERGE_PLAN.md`:
  1. Leaf crates first: protocols, waveobj, wps, blockctl, wconfig.
  2. Then ai/remote/rpc/gui/kernel/vault/tui/terminal.
  3. Reconcile `NexusError`, TUI API divergence.
  4. Bring in `shesh-protocols` (ACP+MCP wire impls) + CLI/worker bins.
  5. Fix upstream breaks: `russh`, `zig`.
  6. Gate: `cargo test --workspace` green on stable.
- Shesh ecosystem continues with SheshAOS Rust + Python `shesh-audit` bridge (`KernelBridge` emits EventKind JSONL).

## Consequences

### Benefits

- No broken main — honest audit over fake green.
- Clear path for future merge without blocking Python body.
- `SheshAOS` remains source of truth (Rust workspace).
- `shesh-brain` (packaged kernel for desktop) remains  todo until merge done.
- Two Rust histories to maintain until merge.

## References

- `SheshAOS/KERNEL_MERGE_PLAN.md` (in SheshAOS repo)
- `docs/history/AUDIT_AND_ROADMAP.md` §3.1
- TODO.md §1
