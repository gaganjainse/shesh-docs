# Complete Audit and Master Roadmap

This chapter is the anchor document from a 2026-08-12 hardening pass: every
decision made, everything built, and every task remaining across the Shesh
ecosystem. Read it to understand how the fleet was reasoned into existence and
what was left to do.

> **Historical record —** Generated around 2026-08-12 and preserved as a
> planning snapshot. It is retained as a record, not as live reference. The
> authoritative factual baseline is the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md): the body is
> licensed **GPL-3.0-or-later** (not MIT), SheshAOS reports **877 passing tests
> with 1 ignored** at the baseline, and `gaganjainse/SheshOS` is an unpublished,
> conceptual project rather than a live upstream. The repo counts and test
> numbers below are historical; where they differ from the baseline, treat them
> as a record of that date.

## Summary

- Fifteen decisions (D1–D15) set the fleet's language policy, federation model, release channels, local-first stance, and governance.
- At the time of writing, sixteen repositories existed (fifteen active, one archived), with component and ecosystem tests all green.
- The remaining work was tagged P0 (blocks real use), P1 (soon), and P2 (later); the checkable form lived in TODO.md.
- Hardware validation, the kernel-to-SheshAOS merge, and real LLM/eval wiring were explicitly deferred as not faked.

## The 2026-08-12 evening delta

Several hardening passes landed that evening:

- **Dependency truth.** Hand-drawn graphs were replaced by `tools/depgraph.py`
  plus a CI freshness gate; `cargo-machete` trimmed about 24 declared-but-unused
  Rust dependencies (the source of the phantom edges in the hand graphs).
- **Silent failures (17:40 directive).** Zero error-class findings across every
  clone; three real bugs were surfaced and fixed (a smart-organizer fake
  savings, a `safety.sh` fake backup, and a voice console-crash silence), along
  with an earlier component batch.
- **Supply chain.** SheshAOS gained a real LICENSE, plus deny/machete/typos CI;
  actionlint 1.7.12 was pinned org-wide; link integrity was gated.
- **Workspace self-service (16:41 directive).** The orchestrator toolkit was
  adopted into `tools/` with `make verify-all`; the home directory was
  de-cluttered into `archive/adopted-or-oneoff-2026-08-12/`.
- Open threads (callable component-CI workflow, fork/archive triage, mirror
  naming drift, janitor TODO policy, and a PAT rotation that required owner
  action) were moved to TODO.md.

## Truthful answers

- **Can the assistant see the whole conversation?** This session's transcript,
  yes. Anything before the opening summary is known only through the files and
  docs created, not raw memory. The on-disk repositories are the source of
  truth.
- **Are the expected files present?** Yes. The components lived under
  `/home/user/sesha/components/shesh-*/`, each with a `pyproject.toml`, `src/`,
  `tests/`, a README, and CI. `shesh-audit` carried its modules plus eighteen
  tests.
- **What caused the workspace-over-budget notice?** The Rust toolchain
  (`~/.cargo` + `~/.rustup`, about 1 GB) was installed to test the kernel merge,
  plus large git clones. After removal, the workspace was 127 MB.

## Decisions made, and why

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Five languages only: Rust, Python, Lua, QML/JS, Bash | Minimize FFI; cross-language talk is MCP/JSON over processes |
| D2 | Exotic runtimes go in rootless Podman/Distrobox, not the host | Reproducible environments, no host pollution |
| D3 | Federated component repos plus manifest/locks, not a monorepo | Each component independently versioned and tested |
| D4 | Three release channels: stable/canary/devel | Daily work on devel, integration on canary, releases on stable |
| D5 | Local-first; cloud is opt-in behind policy | Privacy and offline operation; no keys in config |
| D6 | Governance: immutable base prompt plus evidence-backed `/refine` with rollback | Safe self-improvement |
| D7 | Agent roles: coordinator/planner/coder/researcher/vision/critic | Specialist models with a 6 GB-safe budget per role |
| D8 | `shesh-kernel` archived rather than force-merged | The two Rust trees diverged at the type level; forcing would ship a broken build |
| D9 | Newelle forked as `shesh-voice` with an overlay; core untouched | Keeps upstream rebase easy |
| D10 | ACP adopted alongside MCP | ACP is editor↔agent; MCP is agent↔tools; they stack |
| D11 | Catch-up scheduler, not fixed cron timers | Laptops sleep and shut down |
| D12 | Warmth via one optional offer at natural pauses, at most three per day | Proactive but never nagging |
| D13 | Hierarchical memory plus token-bounded context assembly | Solves retention and finite context together |
| D14 | Habit learning is frequentist with decay, not opaque weights | Inspectable and reversible |
| D15 | Every tool call passes through the `shesh-audit` Guard | allow/confirm/deny, logged, and emitted in SheshAOS event format |

## What existed (verified)

At the time, sixteen repositories were recorded (fifteen active, one archived):

| Repo | Layer | Tests | Purpose |
|------|-------|------:|---------|
| SheshAOS | Brain | 981 (Rust, historical) | Governance kernel; Rust workspace of 12 crates |
| shesh-audit | Brain | 18 | Hash-chained event log, policy Guard, kernel bridge |
| shesh-mind | Mind | 13 | Role→model router (6 GB VRAM budget) |
| shesh-memory | Mind | 15 | Episodic/semantic/intention/habit memory plus context assembler |
| shesh-harness | Mind | 7 | Continual Harness: immutable base, `/refine`, rollback |
| shesh-orchestrator | Mind | 9 | Multi-agent RLM runtime, A2A bus, budgets |
| shesh-skills | Mind | 10 | Everyday MCP tools plus five Markdown skills |
| shesh-voice | Soma | — (fork) | Newelle fork plus overlay (wake/STT/TTS/MCP wiring) |
| shesh-files | Soma | 5 | Rust watcher plus Python classifier |
| shesh-shell | Soma | 3 | Hyprland/Quickshell MCP |
| shesh-system | Soma | 7 | Power/GPU/MUX/status MCP |
| shesh-acp | Soma | 9 | Agent Client Protocol server |
| shesh-backup | Soma | 8 | restic wrapper, AC/daily gating, verify |
| shesh-phone | Soma | 7 | ADB control for Realme Narzo, safe-bounds |
| shesh-desktop | Soma | 20 (ambient) | CachyOS/Hyprland dotfiles, settings GUI |
| shesh-ecosystem | — | 13 | Manifest, resolver, gates, docs, canary CI |
| ~~shesh-kernel~~ | ~~Brain~~ | — | **ARCHIVED**: superseded by SheshAOS, merge pending |

> **Note —** The test counts above are the historical figures from 2026-08-12.
> The [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md) is the
> authoritative baseline and reports different, verified numbers (for example,
> SheshAOS at 877 passing tests with 1 ignored).

Each component carried a standardized README (layer, license, ecosystem link,
tools, dev commands), and central documentation lived in
`shesh-ecosystem/docs/`.

## Penny-picked task list

Tasks were tagged P0 (blocks real use), P1 (soon), and P2 (future). The
checkable version lived in TODO.md.

- **Brain / governance.** Finish the `shesh-kernel`→SheshAOS merge (port leaf
  crates first, reconcile `KernelError`/TUI, bring in `shesh-protocols`, fix
  upstream build breaks, gate on `cargo test --workspace`). Wire the Guard in
  front of every MCP tool call. Consume `kernel-events.jsonl` from Rust. Add
  secret-manager integration. Pursue eBPF/Aya telemetry honestly. Add
  supply-chain provenance.
- **Mind / agents.** LLM-backed planner/critic in the orchestrator. A2A over a
  Unix socket, then optional remote. Persistent/background sessions. A real
  `/refine` loop with held-out grading. Automatic skill capture and deprecation.
  Episodic compaction. Honor currently-loaded models in the router.
- **Soma / body.** Package mature third-party MCP servers behind the Guard.
  Build `shesh-maintenance`, `update-check`, and `health`. Add phone
  vision→tap. Add container-control MCP. Add local-first email/calendar and
  messaging bridges. Add media tools. Complete ACP full sessions.
- **Desktop / physique.** Hardware validation on the physical MSI. Installer
  channel support with btrfs snapshot and rollback. Wire ambient offers to the
  Quickshell overlay. Make proactivity data-aware.
- **Platform / infrastructure.** Canary end-to-end test in a container. A
  Distrobox/Containerfile for onboarding. OpenTelemetry traces (local only).
  Install `shesh-ambient` as a user service.
- **Docs / process.** ADRs for D1–D15. A user getting-started guide.
  A doc-sync job copying each component README into `docs/components/`.

Several P2 items were already done: RAG (in `shesh-memory`), the skill
marketplace primitives (in `shesh-harness`), accessibility (a spec plus
checker), and a self-hosted update mirror (in `shesh-desktop`).

## What was explicitly not done

- The kernel merge was **not** force-merged (D8) — it would have shipped broken
  code.
- No repositories were deleted; the duplicate was archived. Personal and college
  projects (portfolio, AIM, ClinicLedger, Vyakrti, and others) were left
  untouched.
- Hardware/GPU/audio tests were **not** run — impossible in the sandbox.
- Real LLM/LLM-eval was **not** yet wired to `/refine` or the orchestrator;
  stubs were in place.

## Operating rules going forward

The autopilot rules that governed the build:

1. Anchor to TODO.md; pick the highest-priority unblocked item.
2. Branch per item; tests gate every push; never push red.
3. After every user message, append to the query log, update TODO.md, and
   refresh relevant docs.
4. Archive, never delete; no force-push to main.
5. Mark hardware-dependent items 🟡 rather than fake success.
6. Build proper working versions, not minimal stubs that become dead code.
7. First instinct when blocked = *steal*, not build — check `SOURCES.md`,
   `TOOLING_CATALOG.md`, and `manifests/upstreams.toml` for open-source tools to
   adopt, upgrade, and specialize.
8. Discard what Shesh made if something better exists to steal.
9. Upgrade the wrapper, not just fork and wrap.
10. Integrate systems without conflict — namespace via MCP stdio, the Guard,
    separate services and config dirs, one job per component.
11. Take the time to build properly; there is no deadline forcing stubs.
12. Treat style and performance as non-negotiable — the Hyprland look and
    CachyOS performance are the point.

## Manual verification

Items that could not be tested in the sandbox are tracked separately in
**[MANUAL_VERIFICATION.md](../verification/manual-verification.md)** and worked
through on the physical MSI after install. It covers accounts and keys, the MCP
mesh, voice/GPU/display, backup, phone, containers, agent behavior, security,
and the deliberate non-autopilot items (kernel merge, hardware validation).

> **Where this fits —** The [exhaustive audit](./exhaustive-audit.md) and
> [gap analysis](./gap-analysis.md) give the surrounding context, and the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md) is the live
> baseline.
