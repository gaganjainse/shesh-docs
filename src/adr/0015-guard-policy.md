# ADR-0015: Every Tool Call Passes Through shesh-audit Guard

Shesh routes every tool call through a single guarded choke point in `shesh-audit`, so no
component can forget to check policy and no destructive action can slip past the log. The Guard
is the turnstile at the factory gate: every worker passes through it, and it records who went
where.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** governance, security, audit, policy

## Context

The agent can propose destructive actions — `rm`, a write to `.ssh`, a multiplexer switch, a
package `-Syu`, an ADB tap outside the safe area. Governance must be impossible to bypass
simply because a component forgot to check.

SheshAOS is the Rust governance kernel, with its append-only event store and policy engine. The
Python MCP servers, though, are where tools actually execute. The fleet needed one choke point
where every tool call is checked, logged, and emitted in SheshAOS format.

## Decision

`shesh-audit` provides the pieces:

- `AuditLog`: a hash-chained append-only log (`events.jsonl`) with `verify_integrity()` to
  detect tampering.
- `Policy`: allow / confirm / deny rules — read-only tools are allowed, protected paths are
  denied, everything else is confirmed. It is runtime-extensible, with the first match winning.
- `Guard`: `check(actor, tool, args) -> Decision`, also logging the decision.
- `GuardedMCP(FastMCP)`: middleware that policy-checks every MCP tool call before execution,
  denies protected paths, logs the decision and result, and emits a Nexus-format event through
  `NexusBridge`.
- `NexusBridge`: writes `nexus-events.jsonl` in SheshAOS `EventKind` format, which the Rust
  kernel can later consume.

Every Python component imports `GuardedMCP`:

```python
try:
    from shesh_audit.guard import GuardedMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP as GuardedMCP  # graceful fallback
```

Protected paths — `~/.ssh`, `~/.gnupg`, `Vaults/`, `~/Documents/Job`, job folders, and similar —
are denied regardless of confirmation. The MCP entry point `shesh-*-mcp` auto-wraps.

## Consequences

### Benefits

- No tool bypasses governance; the middleware is enforced at the server boundary.
- The audit trail captures every decision, result, and hash chain.
- The Nexus bridge flows Python events into the Rust store (`nexus-events.jsonl`).
- A fallback to plain FastMCP works when the audit package is absent during development.

### Costs

- Policy must stay fast; it is checked on every call (in-memory, under 1 ms today).
- The confirm UX still needs GUI and voice wiring; it currently returns a confirm status.

## Links

- `docs/components/shesh-audit.md`, `policies/SKILLS_POLICY.md`
- `shesh-audit` (20 tests), `shesh-audit/src/guard.py`
- [ADR-0005: Local-First](0005-local-first.md), [ADR-0018: Adopt-vs-Build](0018-adopt-vs-build.md)
