---
title: "ADR-0016: Consolidate the kernel lineage"
type: explanation
summary: "Consolidate the kernel lineage."
audience: maintainer
status: current
verified: 2026-08-15
---

# ADR-0016: Consolidate the kernel lineage

| | |
|---|---|
| **Status** | Accepted (supersedes the staged-merge plan portion of ADR-0008) |
| **Date** | 2026-08-12 |
| **Deciders** | Fleet maintainer |

## Context

open item §1 carried a -blocked plan to merge the archived `shesha-kernel` (Rust,
13 crates + worker bin) into `SheshAOS` (Rust, 12 crates). Two questions were
re-opened in review on 2026-08-12:

1. Do the project actually need what the merge would bring (esp. `shesh-protocols`
   — the 2,045-LOC ACP+MCP wire implementation)?
2. The kernel's `waveobj`/`wps`/`blockctl`/`wconfig` crates were the start of a
   **1:1 Rust port of Wave Terminal** (crate names mirror `wavetermdev/waveterm`
   `pkg/*` one-to-one). Is that rewrite worth finishing?

## Decision

- **Withdraw the kernel-merge plan.** No crate porting. `shesha-kernel` remains
  archived (ADR-0008). Close GitHub issues #7–13.
- **Archive SeshaOS** (superseded by SheshAOS; folded in per open item).
- **Adopt stock Wave Terminal** as the mission-control surface. No rewrite, no
  heavy fork: integration via documented surfaces only (custom `widgets.json`
  widgets, `wsh` RPC, workspaces, OpenAI-compatible AI endpoint → OmniRoute or
  local Ollama). Fork `gaganjainse/waveterm` = pin + insurance, upstream-first
  patches. Wrapper/config lives in `gaganjainse/shesh-wave`.
- **SheshAOS stays the canonical Rust kernel.** `shesh-protocols` is demoted
  to P3 archive-candidate — port only if a future Rust consumer needs native
  ACP/MCP. `shesh-brain` scope unchanged.
- Rust crate prefix `sheshaaos-*` normalization deferred to the next Rust-enabled
  session (needs cargo; see ADR-0017 exception register).

## Consequences

### Benefits

- open item §1 unblocked by decision instead of by labor; queue honest again.
- Terminal strategy has one owner (stock Wave), terminal-daily-driver choice
- (foot/ghostty/tmux) is orthogonal and free.
- Zero third implementation of protocol wires to maintain.
- Rust ambitions narrowed to governance kernel + salvage-optional crates.
- `shesh-protocols` Rust ACP/MCP parity postponed indefinitely.

## References

- ADR-0008 (kernel archive), ADR-0010 (ACP+MCP), ADR-0017 (naming purge)
- shesh-ecosystem issues #7–13 (closed by this decision)
- gaganjainse/shesh-wave (Wave integration wrapper)
