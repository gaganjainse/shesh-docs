# Skills Policy — Tool Risk Classes

Every tool call from every agent passes the audit guard before it runs. This chapter defines
the three verdicts the guard can return and the properties that make the policy fail closed.

- Status: living · last verified 2026-08-13
- Implementation: `shesh-audit/src/shesh_audit/policy.py` + `mcp_guard.py`
- Decision record: [ADR-0015](../adr/0015-guard-policy.md)

## The policy in one sentence

Every tool call passes the audit guard before execution. The policy is an ordered rule list;
first match wins; and the default for an unknown action is **confirm** — Shesh never silently
does something it was not explicitly allowed to do.

## The three verdicts

| Verdict | Meaning | Built-in examples |
|---|---|---|
| `allow` | proceed silently | read-only tools: `get_*`, `list_*`, `search*`, `recall`, `assemble_context` |
| `confirm` | ask the human first | `run_backup`, `set_power_profile`, and **everything unmatched** |
| `deny` | refuse, always | any path under `.ssh/`, `.gnupg/`, `Vaults/`, or job folders |

## Properties that matter

- **Fail-closed default.** An unrecognized tool name matches no rule, so it lands on
  `confirm` — an unknown capability can never self-authorize. This is deliberate and matches
  the MCP authorization guidance.
- **Protected paths deny even reads.** Secrets and job data are off-limits to every tool,
  regardless of the tool's name.
- **Description integrity.** Since 2026-08-13 the guard also pins MCP tool descriptions
  (learned on first boot, refused on drift) so a poisoned or rug-pulled server cannot change
  what a tool claims to do — see [Threat Model](./threat-model.md) §MCP and `tool_pins.py` in
  `shesh-audit`.
- **Receipts.** Allowed and denied calls are hash-chained into
  `~/.local/share/shesh/audit/events.jsonl` (verification:
  [Manual Verification](../verification/manual-verification.md) §10).

> **Note —** The 2026-08-15 audit (finding F-02) flagged that the `confirm` verdict currently
> proceeds to execute the tool rather than strictly gating it before execution. The intended
> posture — ask the human first, then run — is the design target; F-02 is tracked for
> remediation and is not yet closed. Do not describe `confirm` as fully isolated from side
> effects until that finding is resolved.

> **Tip —** Treat `confirm` as "ask before you commit," not "ask and the action never
> happened." Pair it with the protected-path denials for real safety.
