# ADR-0008: Archive shesh-kernel, Don't Force Merge

Shesh archives the experimental `shesh-kernel` rather than force-merging it into SheshAOS,
accepting two Rust histories over a single broken build. The decision keeps the mainline honest
— a real audit beats a fake green checkmark.

## Status

- **Date:** 2026-08-10
- **Status:** Accepted

## Context

SheshAOS, with 981 Rust tests across 12 crates, is the governance kernel. The archived
`shesh-kernel` — an alpha microkernel — diverged at the type level: 57 compile errors, a
`NexusError` / `TUI` API mismatch, an upstream removal of `russh::Error::msg`, and a terminal
crate that required Zig.

## Decision

- **Do not force-merge** the two Rust trees; that would ship a broken build.
- Archive `shesh-kernel` as `shesha-kernel` (with a GitHub redirect), superseded by SheshAOS.
- Document a staged rebase plan in `SheshAOS/KERNEL_MERGE_PLAN.md`:
  1. Leaf crates first — protocols, waveobj, wps, blockctl, wconfig.
  2. Then ai, remote, rpc, gui, kernel, vault, tui, terminal.
  3. Reconcile the `NexusError` and TUI API divergence.
  4. Bring in `shesh-protocols` (the ACP and MCP wire implementations) and the CLI and worker
     binaries.
  5. Fix the upstream breaks in `russh` and `zig`.
  6. Gate on `cargo test --workspace` passing on stable.
- The ecosystem proceeds with SheshAOS Rust plus the Python `shesh-audit` bridge, where
  `NexusBridge` emits `EventKind` JSONL.

> **Note —** ADR-0016 later withdrew the staged-merge plan entirely. `shesha-kernel` remains
> archived; this record's "do not force-merge" stance still holds.

## Consequences

### Benefits

- The mainline never breaks — an honest audit beats a fake green.
- A clear path for a future merge exists without blocking the Python body.
- SheshAOS stays the source of truth as the Rust workspace.

### Costs

- `shesh-brain` (the packaged kernel for desktop) stays a pending task until any merge
  completes.
- Two Rust histories must be maintained until a merge happens.

## Links

- `SheshAOS/KERNEL_MERGE_PLAN.md` (in the SheshAOS repository)
- `docs/history/AUDIT_AND_ROADMAP.md` §3.1
- [ADR-0016: Kernel Consolidation](0016-kernel-consolidation.md)
