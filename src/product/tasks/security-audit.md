# 10. Security & audit

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 10 of 16.

- [ ] Every tool call is logged: `~/.local/share/shesh/audit/events.jsonl`
- [ ] The hash chain verifies: no "tampered" results
- [x] kernel-format events appear in `kernel-events.jsonl` and are ingested by the Rust kernel (`kernel_ingest`) — wiring done 2026-08-13; on-machine run remains a hardware check
- [ ] Writing to `.ssh`, `.gnupg`, `Vaults/`, or job folders is **denied**
      (try via any MCP tool)
- [ ] Destructive terminal commands in ACP ask for confirmation
- [ ] No MCP server runs as root
- [ ] The audit Guard wraps every MCP server (check each server's logs for a
      "policy" line)

---
