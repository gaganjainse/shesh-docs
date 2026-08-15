# Security Policy

The Shesh security posture is one shared rulebook, not fifty-three private copies. This
chapter explains how to report a vulnerability, what the fleet defends today, and where it
honestly leaves gaps.

- One canonical policy lives at the ecosystem root; every `shesh-*` component links to it.
- Vulnerabilities go through GitHub private reporting; acknowledgement targets 7 days.
- A rolling `main` model means only the latest `main` is supported, and fixes roll forward.
- Secrets, supply chain, CI, and on-machine tool calls each have enforced controls.
- Image signing and third-party MCP sandboxing are deliberately out of scope today.

## Canonical home

This file is the single source of truth for the ecosystem. Every `shesh-*` component links
here instead of carrying its own copy, so one posture is maintained across the fleet.

## Reporting a vulnerability

A private email or direct channel is not yet wired up for a solo project, so use one of two
paths:

- Open a **private vulnerability report** on the affected GitHub repository.
- Or open an issue titled `SECURITY: …` **without** proof-of-concept details, and expect a
  private thread to be opened from there.

Response target: acknowledged within 7 days, triaged within 30.

## Supported versions

This is a rolling-release ecosystem on `main`. Only the latest `main` is supported. No
release branches are maintained today; the security model is "roll forward fast" (see
[Dependency Policy](./dependency-policy.md)).

## Posture summary

The following posture was verified on 2026-08-13.

### Secrets

Push protection and secret scanning are enabled on all 53 active repositories. A gitleaks
gate runs in every component's CI through the reusable pipeline. Secrets are never read into
repository files: `tools/git_askpass.py` reads the personal access token from
`~/.config/shesh/github.pat` (mode 600; a world-readable file is refused). `shesh-secrets`
resolves external stores (gopass, keepassxc, or file) at runtime.

### Supply chain

All GitHub Actions are pinned to immutable SHAs (latest releases), and Dependabot opens
weekly moves so pins cannot silently rot or be rewritten (the `tj-actions` class of attack).
`cargo-deny`, `cargo-machete`, and `typos` run in the SheshAOS supply-chain job; only two
documented RUSTSEC ignores exist (no patch available or unreachable path). `pip install` in
CI never runs leniently — no `|| true` anywhere, including inside workflow YAML since
2026-08-13.

### Workflow and CI/CD

No `pull_request_target` trigger exists anywhere. The one instance (swarm auto-merge) ran
checked-out pull-request code with a write token and was removed in favor of a same-repo
guard on 2026-08-13. `permissions: read-all` sits at every workflow top level, with writes
granted per job. `zizmor` static analysis gates every workflow change. Checkouts drop the
credential after clone (`persist-credentials: false`) except for the three workflows that
legitimately push.

### Attack resistance on the machine

Every MCP tool call passes the Guard policy engine in `shesh-audit`. The default for an
unknown action is **confirm** — never auto-allow. The two-phase confirmation flow completes
in `shesh-brain`, and every decision and resolution lands in the hash-chained audit ledger.
Tool-description integrity pins defend against rug-pull and tool-poisoning: any mutation
after first boot refuses registration until explicitly re-pinned with
`python -m shesh_audit.tool_pins --repin <server>`. Failure reporting is audited ecosystem-
wide, so no tool can fabricate success.

### Recovery

[Recovery](./recovery.md) is a tested runbook, executed four times against real sandbox
incident patterns in a single week. `tools/dr_check.sh` verifies the recovery prerequisites
are in place. The archive-not-delete policy sends anything dropped to `~/archive/` with a
manifest, never to `/dev/null`.

## Out of scope today

Some protections are intentionally parked or out of reach:

- Release signing and attestation for SheshAOS images (cosign/Rekor evaluation is a
  deliberate parked item; see the open TODO).
- A sandbox profile for running third-party MCP servers (the fleet only runs its own).
- GUI process isolation on the desktop — nothing here runs setuid, and the
  [Threat Model](./threat-model.md) documents what is intentionally not defended.

> **Note —** The audit of 2026-08-15 found residual risks in this area (for example, the
> ACP terminal bridge and the `fetch_url` helper). These are tracked findings, not closed
> fixes; see the threat model's residual-risk section for the honest status.

Related: [Threat Model](./threat-model.md) · [Recovery](./recovery.md) · [all policies](./)
