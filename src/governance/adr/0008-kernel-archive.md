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
- Archive `shesh-kernel` as `shesh-kernel` (GitHub redirect) — superseded by SheshAOS.
- Staged rebase plan, revised below with measured figures:
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

## Measured divergence (2026-08-15)

The plan above was written without numbers. Comparing the two trees crate by
crate, counting Rust lines:

| Crate | shesh-aos | shesh-kernel | Status |
|---|---:|---:|---|
| `protocols` | — | 2,045 | kernel only |
| `gui` | — | 1,717 | kernel only |
| `tui` | — | 1,257 | kernel only |
| `terminal` | — | 651 | kernel only |
| `worker` | — | 189 | kernel only |
| `kernel` | 11,786 | 15,614 | diverged, +3,828 |
| `cli` | 133 | 440 | diverged, +307 |
| `waveobj` | 4,015 | 4,169 | diverged, +154 |
| `remote` | 407 | 304 | diverged, −103 |
| `blockctl` | 935 | 1,016 | diverged, +81 |
| `rpc` | 519 | 583 | diverged, +64 |
| `wconfig` | 705 | 756 | diverged, +51 |
| `ai` | 525 | 542 | diverged, +17 |
| `vault` | 731 | 745 | diverged, +14 |
| `wps` | 1,297 | 1,310 | diverged, +13 |

This splits the work into two very different halves.

**5,859 lines carry no merge conflict at all.** The five kernel-only crates
have no counterpart in shesh-aos, so porting them is a move plus a rename, not
a reconciliation. `protocols` is the one with external value: it holds the ACP
and MCP wire implementations.

**The rest is a genuine reconciliation, and `kernel` is 96 per cent of it.**
The eight small crates differ by 13 to 154 lines each, mostly the divergence
already sampled in `vault`, where shesh-aos replaced an
`unwrap_or_else(|_| unsafe { unreachable_unchecked() })` with a total function
returning an empty vector. That direction matters: shesh-aos has zero `unsafe`
blocks, shesh-kernel has three, so shesh-aos is not the older tree and a
merge cannot be a one-way copy.

`kernel` at +3,828 lines is not a rebase. It is a rewrite decision that needs
its own ADR once somebody has read both.

### Suggested order, revised

1. `protocols`, `worker` — no counterpart, no conflict, immediate value.
2. `terminal`, `gui`, `tui` — no counterpart; `tui` needs the API
   reconciliation the original plan named.
3. The eight small diverged crates, smallest first, each as its own PR with
   `cargo test --workspace` green. Take the safety direction from shesh-aos.
4. `kernel` last, under a new ADR.

Until step 4, both trees stay. The archive is bounded and documented rather
than open-ended: `shesh-kernel/README.md` names exactly what is only there.

## References


- The staged plan lives in this ADR. An earlier revision cited
  `shesh-aos/KERNEL_MERGE_PLAN.md`, which does not exist in that repository;
  the reference was dangling and is replaced by the section above.
- `docs/history/AUDIT_AND_ROADMAP.md` §3.1
- TODO.md §1
