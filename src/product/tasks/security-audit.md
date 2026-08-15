# Security and the audit trail

Every action the Shesh body takes leaves a tamper-evident record, and every tool call
passes through a guard. This chapter confirms that the audit trail is honest and the
policy engine actually denies protected paths.

> **Note —** This chapter is section 10 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## The event log

- [ ] Every tool call is logged to `~/.local/share/shesh/audit/events.jsonl`.
- [ ] The hash chain verifies with no "tampered" results.
- [x] Kernel-format events appear in `kernel-events.jsonl` and are ingested by the
      Rust kernel (`kernel_ingest`) — wiring done 2026-08-13; the on-machine run
      remains a hardware check.

## Guardrails that must hold

- [ ] Writing to `.ssh`, `.gnupg`, `Vaults/`, or job folders is **denied** (try via
      any MCP tool).
- [ ] Destructive terminal commands in ACP ask for confirmation.
- [ ] No MCP server runs as root.
- [ ] The audit Guard wraps every MCP server — check each server's logs for a
      "policy" line.
