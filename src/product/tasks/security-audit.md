# 10. Security & audit

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 10 of 16.

- [ ] Every tool call is logged: `~/.local/share/shesh/audit/events.jsonl`
- [ ] The hash chain verifies: no "tampered" results
- [ ] Nexus-format events appear in `nexus-events.jsonl` for the Rust brain
- [ ] Writing to `.ssh`, `.gnupg`, `Vaults/`, or job folders is **denied**
      (try via any MCP tool)
- [ ] Destructive terminal commands in ACP ask for confirmation
- [ ] No MCP server runs as root
- [ ] The audit Guard wraps every MCP server (check each server's logs for a
      "policy" line)

---
