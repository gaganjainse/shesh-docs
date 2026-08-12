# ADR-0015: Every Tool Call Passes Through shesh-audit Guard

**Date:** 2026-08-09
**Status:** Accepted (implementation notes updated 2026-08-12)
**Tags:** governance, security, audit, policy

## Context
Agent can propose destructive actions: `rm`, write to `.ssh`, MUX switch, package `-Syu`, ADB tap outside safe area. We need governance that cannot be bypassed by a component forgetting to check.

SheshAOS is the Rust governance kernel (append-only event store, policy engine). But Python MCP servers are where tools execute.

We need a single choke point: every tool call checked, logged, emitted in SheshAOS format.

## Decision
- **`shesh-audit`** provides:
  - `AuditLog`: hash-chained append-only log (`events.jsonl`) + `verify_integrity()` that detects tampering.
  - `Policy`: allow/confirm/deny rules — read-only tools allow, protected paths deny, everything else confirm. Runtime-extensible (first match wins).
  - `Guard`: `check(tool, args, actor=…) -> Decision` + logs decision; optionally mirrors to the kernel bridge.
  - `GuardedMCP(FastMCP)`: policy-checks every MCP tool call, with two enforcement seams and an exactly-once guarantee:
    1. `GuardedMCP.tool()` wraps directly registered functions (works in-process, e.g. unit tests).
    2. `GuardMiddleware` (FastMCP 3 protocol middleware) covers mounted/proxied tools that never pass through the decorator.
  - `KernelBridge`: appends `kernel-events.jsonl` in the SheshAOS kernel EventKind format (`SheshAOS/crates/shesh-kernel/src/events.rs`) — the Rust kernel consumes it directly.
- All Python components import the guard **directly** (no fallback):

  ```python
  from shesh_audit.mcp_guard import GuardedMCP as _MCP

  mcp = _MCP("shesh-system")
  ```

  `shesh-audit` is a declared runtime dependency of every guarded component. A
  missing guard must crash the server at startup — running third-party tools
  unguarded because an import silently fell back to plain FastMCP is exactly
  the failure mode this ADR exists to prevent (the original text documented a
  `try/except ImportError` fallback to a `shesh_audit.guard` module that never
  existed; nothing was ever guarded through that path).
- Protected paths: `~/.ssh`, `~/.gnupg`, `Vaults/`, `~/Documents/Job`, job folders, etc. — denied regardless of confirmation.

MCP entry point `shesh-*-mcp` auto-wraps.

## Consequences
- ✅ No tool bypasses governance — enforced at the function seam and the server protocol boundary.
- ✅ Audit trail: every decision + result + hash chain.
- ✅ Kernel bridge: Python→Rust event flow (`kernel-events.jsonl`).
- ✅ Import failure is loud: the server refuses to start unguarded; `shesh-audit` is pinned into CI via `git+…@main` until packages are published to PyPI.
- ❌ Policy must be kept fast — checked on every call (currently in-memory, <1ms).
- ❌ Confirm UX needs GUI/voice wiring — currently returns confirm status (the ACP layer surfaces it to a human in-editor).

## Links
- `docs/components/shesh-audit.md`, `policies/SKILLS_POLICY.md`
- `shesh-audit` (20 tests), `shesh-audit/src/shesh_audit/mcp_guard.py`
- D6, D5, D1 (Rust kernel)
