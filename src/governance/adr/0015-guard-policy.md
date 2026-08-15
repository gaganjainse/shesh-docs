---
title: "ADR-0015: Route every tool call through the guard"
type: explanation
summary: "Route every tool call through the guard."
audience: maintainer
status: current
verified: 2026-08-15
---

# ADR-0015: Route every tool call through the guard

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-08-09 |
| **Deciders** | Fleet maintainer |
| **Tags** | governance, security, audit, policy |

## Context

Agent can propose destructive actions: `rm`, write to `.ssh`, MUX switch, package `-Syu`, ADB tap outside safe area. The fleet needs governance that cannot be bypassed by a component forgetting to check.

SheshAOS is the Rust governance kernel (append-only event store, policy engine). But Python MCP servers are where tools execute.

The fleet needs a single choke point: every tool call checked, logged, emitted in SheshAOS format.

## Decision

- **`shesh-audit`** provides:
  - `AuditLog`: hash-chained append-only log (`events.jsonl`) + `verify_integrity()` that detects tampering.
  - `Policy`: allow/confirm/deny rules — read-only tools allow, protected paths deny, everything else confirm. Runtime-extensible (first match wins).
  - `Guard`: `check(actor, tool, args) -> Decision` + logs decision.
  - `GuardedMCP(FastMCP)`: middleware that policy-checks every MCP tool call before execution, denies protected paths, logs decision + result, emits kernel-format event via `KernelBridge`.
  - `KernelBridge`: writes `kernel-events.jsonl` in SheshAOS EventKind format — Rust kernel can later consume.
- All Python components import `GuardedMCP`:
  ```python
  try:
      from shesh_audit.guard import GuardedMCP
  except ImportError:
      from mcp.server.fastmcp import FastMCP as GuardedMCP  # graceful fallback
  ```
- Protected paths: `~/.ssh`, `~/.gnupg`, `Vaults/`, `~/Documents/Job`, job folders, etc. — denied regardless of confirmation.

MCP entry point `shesh-*-mcp` auto-wraps.

## Consequences

### Benefits

- No tool bypasses governance — middleware enforced at server boundary.
- Audit trail: every decision + result + hash chain.
- Kernel bridge: Python to Rust event flow (`kernel-events.jsonl`).
- Fallback to plain FastMCP if audit not installed (dev).

### Costs and risks accepted

- Policy must be kept fast — checked on every call (currently in-memory, <1ms).
- Confirm UX needs GUI/voice wiring — currently returns confirm status.

## References

- `docs/components/shesh-audit.md`, `policies/SKILLS_POLICY.md`
- `shesh-audit` (its test suite), `shesh-audit/src/guard.py`
- D6, D5, D1 (Rust kernel)
