# Threat Model — The Shesh Ecosystem

Security is not a feature you bolt on; it is the shape of the system under attack. This
chapter lists what the fleet protects, who might harm it, and the controls that stand between
them — written for anyone about to touch the Guard policy, an MCP server, a CI workflow, or
the desktop.

- Five assets are protected: the PAT, the audit ledger, local secrets, the desktop machine,
  and CI integrity.
- Six actor classes span supply chain, prompt injection, and rogue contributors.
- A hard "lethal trifecta" rule forbids combining private-data access, untrusted content, and
  external comms in one component.
- Residual risks — prompt injection, TOFU pins, the standing PAT — are accepted and documented.

## Who should read this

Anyone changing security-relevant behavior should read this first: the Guard policy, MCP
servers, CI workflows, secrets handling, or the desktop. Read it before touching those
surfaces.

## Assets — what we protect

1. **GitHub PAT and org** — a fine-grained PAT at `~/.config/shesh/github.pat`; compromise
   means org-wide code control.
2. **The hash-chained audit ledger** (`~/.local/state/shesh/audit/*.jsonl`) — the forensic
   record; tamper-evident, not tamper-proof.
3. **Local secrets** in external stores (gopass, keepassxc) resolved by `shesh-secrets`;
   tokens (Telegram bot, Signal account) at runtime.
4. **The desktop machine itself** — files, camera and microphone paths (media, voice),
   displays, and the GPU.
5. **CI integrity** — 26 repositories auto-merging outputs that users run locally.

## Actors — who might harm it

- A malicious or compromised **third-party dependency or Action** (supply chain).
- **Prompt injection** through content an agent ingests (docs, web pages, tool outputs, MCP
  tool descriptions).
- **Rug-pull or poisoned MCP tool** (description mutated post-approval — the Invariant Labs
  2025-04 class).
- A compromised **upstream fork** the fleet tracks (dots, terminal, models list).
- A rogue **swarm worker or pull-request author** (the auto-merge path).
- Physical or OS-level compromise — **out of scope**: the fleet assumes the OS keeps its
  guarantees and does not defend against a root-level attacker.

## Surfaces and controls

Each row pairs a surface with its control and the evidence that the control exists.

| Surface | Threat | Control | Evidence |
|---|---|---|---|
| PAT file | leak via git or transcripts | push protection plus secret scanning (53/53 repos); gitleaks gate; askpass refuses world-readable PAT; rotation reminder open | `SECURITY.md`; `component-ci.yml` gitleaks step |
| Audit ledger | silent tampering | sha256 hash chain, `verify()`; verify-runbook in [Recovery](./recovery.md) | `shesh-audit` `log.py` |
| MCP tool defs | rug pull, poisoning | tool-pin verify at both seams; poisoning-marker scan | `shesh-audit` `tool_pins.py` plus tests |
| MCP tool calls | destructive action | Guard allow/confirm/deny; two-phase confirmations in `shesh-brain` | `gate.py`, brain `81777f5` |
| **Lethal trifecta** | private data + untrusted content + external comms at once | architectural rule below | below |
| GH Actions | tag rewrite (`tj-actions`) | all actions SHA-pinned; Dependabot moves pins weekly | 2026-08-13 sweep, 26 repos |
| GH Actions | fork pull-request RCE (`pull_request_target`) | trigger removed fleet-wide; same-repo guard; read-all default tokens; zizmor gate | `swarm-auto-merge.yml` |
| GH Actions | injection via pull-request metadata | fields pass through env, never inline (actionlint-gated) | pull-request body handling |
| Dependencies | known CVEs | Dependabot alerts plus auto-security-fixes plus weekly bump PRs (pip and actions); `cargo-deny` | org API state |
| Backups | silent loss | `shesh-backup` plus recovery drill | [Recovery](./recovery.md) |
| Vendor forks | upstream rug-pull (dots, and so on) | thin overrides; rebase reviewed; archived forks excluded from audits | manifest policy |

## The lethal-trifecta rule

A component must not combine all three of: **(a) reads private data**, **(b) ingests
untrusted content**, **(c) can exfiltrate** (network send). Compliant splits that live today
show the pattern: `shesh-messaging` sends but reads no private stores; `shesh-secrets` reads
stores but has no network surface; `shesh-knowledge` ingests content but cannot send. New
components are checked against this rule in review (it sits in the component README template).

## Residual risks — accepted and documented

1. **Prompt injection has no complete mitigation** (Willison's curse) — the fleet reduces
   blast radius through the trifecta split and confirmations, but does not claim prevention.
2. **TOFU pins:** a poisoned *first* version would be learned as good. Accepted for the
   fleet's own-authored servers; third-party MCP servers are not auto-mounted — a deliberate
   decision, revisited before adopting any.
3. **The PAT itself is a standing credential on disk.** Mitigations are push protection, least
   scope, and the pending rotation reminder. OIDC or app-token replacement is the follow-up
   when multi-agent workers run in Actions only.
4. **Voice and audio paths** (`shesh-voice`) implicitly trust local audio daemons.

> **Note —** The 2026-08-15 audit added two findings that sit in this residual-risk space and
> are not yet closed. Finding F-03: the ACP terminal bridge invokes shells with `shell=True`,
> widening the injection surface. Finding F-12: the `fetch_url` helper is exposed to
> server-side request forgery. Both are tracked for remediation; the intended controls are
> parameterized execution and URL allowlisting respectively. Do not describe them as fixed.

## Verification discipline

Security claims in this repository follow the house tell-triple: what is STATED here, what is
VERIFIED by which gate or test, and what EVIDENCE to check. A claim without a gate rots
silently — every row above names its enforcement point.

> **Warning —** The threat model is a live weapon, not a certificate. Re-read it before any
> change to a security surface, and update the relevant row when a control changes.
