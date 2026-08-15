# ADR-0016: Kernel Consolidation — Merge Withdrawn, Wave Adopted

Shesh withdraws the plan to merge the archived `shesha-kernel` into SheshAOS and adopts stock
Wave Terminal as the mission-control surface instead. The decision unblocks the stale TODO
queue through judgment rather than through years of porting work that no consumer required.

> **Summary —**
> - The kernel-merge plan is withdrawn; `shesha-kernel` stays archived per ADR-0008.
> - SeshaOS is archived, folded into SheshAOS.
> - Stock Wave Terminal is adopted as mission control; no heavy Rust port.
> - SheshAOS remains the canonical Rust kernel; `shesh-protocols` is demoted to archive-candidate.
> - The fleet maintains zero third implementations of its protocol wires.

## Status

- **Date:** 2026-08-12
- **Status:** Accepted (supersedes the staged-merge plan portion of [ADR-0008](0008-kernel-archive.md))

## Context

TODO §1 carried a blocked plan to merge the archived `shesha-kernel` (Rust, 13 crates plus a
worker binary) into SheshAOS (Rust, 12 crates). Review on 2026-08-12 reopened two questions:
did the merge bring anything the fleet actually needed (especially `shesh-protocols`, a
2,045-line ACP and MCP wire implementation), and was the kernel's `waveobj` / `wps` / `blockctl`
/ `wconfig` crates — a one-to-one Rust port of Wave Terminal — worth finishing?

## Evidence (measured on fresh clones, 2026-08-12)

- **ACP already exists in Python:** `shesh-acp`, a JSON-RPC 2.0 stdio server for
  Zed/JetBrains/Neovim, with 12 of 12 tests green.
- **MCP already exists in Python:** 17 `shesh-*-mcp` servers plus the GuardedMCP policy wrapper
  in `shesh-audit`, with 191 component tests green across 19 of 20 components.
- **A Python-to-Rust bridge already exists:** `shesh_audit/nexus_bridge.py` emits Nexus-format
  JSONL events into the Rust event store path.
- `shesh-protocols` in Rust would be a **third implementation** of owned wires; no consumer
  requires Rust-native ACP or MCP today.
- Wave Terminal is roughly 60k lines of TypeScript (React 19, Monaco, xterm-webgl) plus about
  75k lines of Go, with 22k stars and active maintenance. A solo Rust port is multi-year and,
  by the author's own measure, "nowhere near Wave."
- Divergence between the kernel and SheshAOS is shallow in most crates but total in the ones
  that matter (`NexusError`, TUI API); the kernel carries two extra files (protocols, worker
  binary) worth noting, nothing blocking.
- SeshaOS (359 lines) was already folded into SheshAOS and was redundantly live.

## Decision

- **Withdraw the kernel-merge plan.** No crate porting. `shesha-kernel` remains archived
  ([ADR-0008](0008-kernel-archive.md)). Close GitHub issues #7–13.
- **Archive SeshaOS** (superseded by SheshAOS; folded in per TODO).
- **Adopt stock Wave Terminal** as the mission-control surface. No rewrite and no heavy fork:
  integration uses documented surfaces only — custom `widgets.json` widgets, `wsh` RPC,
  workspaces, and an OpenAI-compatible AI endpoint toward OmniRoute or local Ollama. Fork
  `gaganjainse/waveterm` as pin-plus-insurance, upstream-first patches. The wrapper and config
  live in `gaganjainse/shesh-wave`.
- **SheshAOS stays the canonical Rust kernel.** `shesh-protocols` is demoted to a P3
  archive-candidate — port only if a future Rust consumer needs native ACP or MCP. `shesh-brain`
  scope is unchanged.
- Rust crate prefix `sheshaaos-*` normalization is deferred to the next Rust-enabled session
  (needs cargo; see the ADR-0017 exception register).

## Consequences

### Benefits

- TODO §1 is unblocked by a decision instead of by labor; the queue is honest again.
- The terminal strategy has one owner (stock Wave), and the daily-driver terminal choice
  (foot, ghostty, tmux) is orthogonal and free.
- Zero third implementations of protocol wires to maintain.

### Costs

- Rust ambitions narrow to the governance kernel plus optional-salvage crates.
- `shesh-protocols` Rust ACP/MCP parity is postponed indefinitely.

## Links

- [ADR-0008: Kernel Archive](0008-kernel-archive.md),
  [ADR-0010: ACP + MCP](0010-acp-plus-mcp.md),
  [ADR-0017: Naming Purge](0017-naming-purge-completed.md)
- shesh-ecosystem issues #7–13 (closed by this decision)
- gaganjainse/shesh-wave (Wave integration wrapper)
