# Exhaustive Audit — All Repositories (54 Unique)

This chapter records a 2026-08-11 sweep of every repository in the owner's
GitHub namespace: what existed, what each component did, and where the gaps
were. Reading it tells you how the fleet looked at the start of the build-out
and why later consolidation became necessary.

> **Historical record —** This audit was written on 2026-08-11 and preserved as
> a factual snapshot of that date. It is retained as a record, not as live
> reference. The authoritative factual baseline is the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md): the body is
> licensed **GPL-3.0-or-later** (not MIT), SheshAOS reports **877 passing tests
> with 1 ignored** at the baseline, and `gaganjainse/SheshOS` is an
> unpublished, conceptual project rather than a live upstream. Where the counts
> or claims below differ from that baseline, treat them as historical.

## Summary

- The sweep covered 54 unique repositories: 41 user repos, 22 in the Shesh family, 13 forked upstreams, and 11 other personal projects.
- Component state was uneven: most `shesh-*` repos had a `pyproject.toml`, tests, and CI; personal projects were mixed.
- The Brain layer was incomplete — the Rust kernel (`shesh-kernel`, later SheshAOS) had not yet merged, and a `shesh-brain` wrapper was still a plan.
- Mind and Soma layers were largely built: orchestrator, memory, harness, voice, shell, system, backup, phone, and containers all existed.
- Several "P0" gaps from this era (ACP server, orchestrator, harness, audit) were later closed; the 2026-08-15 audit tracks the residue.

## The 2026-08-12 evening addendum

The historical 54-repo audit above is preserved as written. The current live
state of the workspace at that time was recorded in
[`AUDIT_ECOSYSTEM_2026-08-12.json`](AUDIT_ECOSYSTEM_2026-08-12.json) (generated
by `tools/ecosystem_audit.py`; 28 local clones). The headline delta since the
original audit:

- All 28 `shesh-*` worktrees were byte-identical to their origin default
  branches after the day's snapshot-restore repairs.
- Latest CI run was green on every component repo (26 of 26 with workflows).
- SheshAOS: excised `tui`/`gui`/`terminal`/`zig` per ADR-0018; the historical
  note here said 872 tests and an MIT LICENSE. **Correction:** the current
  LICENSE is **GPL-3.0-or-later**, and the 2026-08-15 baseline reports **877
  passing tests with 1 ignored** — the 872 figure is historical.
- Silent-failure audit (SF1–SF6) covered every clone on ecosystem CI: 0 errors
  ecosystem-wide after the desktop and voice batches; SF5/SF6 remained warn-class
  by design.
- Naming-sweep remnants in this JSON (`shesha`, `seshaos`, `nexusaos` hits) are
  historical references in archival docs and CHANGELOGs, not live identifiers
  (ADR-0016/0017); the live names grep clean in source trees.

The original sweep generated its list from `src/all-repos` (41) +
`src/forks` (13) + `src/` (22) — shallow `--depth 1` clones totaling 1.5 GB in
`src/`, 508 MB in `all-repos`, and 879 MB in `forks`.

## What the sweep found

| Category | Count | Notes |
|----------|------:|-------|
| User repos total | 41 | `gaganjainse/*` from the API |
| Shesh family | 22 | `shesh-*` plus SheshAOS/SeshaOS/shesha-kernel/OmniRoute/shesh-omniroute/shesh-workspace |
| Other personal | 11 | AIM, ClinicLedger, FWRS, GameVault, Vyakrti, ePustakalay, grievance-portal, llm-eval-harness, rag-service, portfolio, ollama (fork) |
| Forked upstreams | 13 | prime-agent, Memento-Skills, phone-harness, servers (modelcontextprotocol), Hermes, Hyprland-Dots, hyprdots, leon, pipecat, openWakeWord, browser-use, khoj, OmniRoute |
| Total unique audited | 54 | Deduplicated by name |

All repositories had a README; most `shesh-*` repos had a `pyproject.toml`,
tests, and CI. Personal projects were mixed. A condensed per-repo table
(captured from the audit script) listed readme, pyproject, tests, CI, license,
size, and last commit for each. The full machine-readable record lives in
`docs/AUDIT_EXHAUSTIVE.json` (54 entries).

## Gaps by layer

The honest state of each layer at the time of the sweep:

### Brain (governance)

- **SheshAOS** — 7.5 MB Rust tree; the historical note reported 981 tests and a
  merge pending with `shesha-kernel`. The merge was blocked at the type level
  (57 compile errors; `russh::Error::msg` removed; `zig` required). Test counts
  here and below are historical; see the baseline note above.
- **shesh-audit** — hash-chained event log, GuardedMCP, Nexus bridge, and
  multi-backend secrets; needed CI release-gate integration.
- **shesh-secrets** — `env`/`gopass`/`keepassxc`/`file` backends; refuses
  world-readable files.
- **shesh-brain** — missing; the plan was to package the kernel for the desktop
  and route tool calls through policy.

### Mind (deliberation)

- **shesh-mind** — role-to-model router with a 6 GB VRAM budget; later became a
  model-agnostic, capability-based router.
- **shesh-memory** — episodic/semantic/intention/habit memory with FTS, vector
  embeddings, and Ollama `nomic-embed-text`; compaction included.
- **shesh-harness** — continual harness with an immutable base and a held-out
  `/refine` evaluator.
- **shesh-orchestrator** — multi-agent RLM runtime, A2A broker, persistent
  sessions, and JSONL traces.
- **shesh-skills** — everyday tools plus five Markdown skills.
- **shesh-calendar** — iCalendar vdir reader.
- **shesh-omniroute** — wrapper for the OmniRoute fork (291 providers, 90+
  free, local-Ollama-primary optional).

### Soma (body)

- **shesh-files** — Rust watcher plus Python classifier.
- **shesh-shell** — Hyprland/Quickshell MCP.
- **shesh-system** — power/GPU/MUX, read-only update check, health, and
  maintenance.
- **shesh-voice** — Newelle fork with a wake word, faster-whisper STT, Piper
  TTS, and an MCP overlay.
- **shesh-desktop** — CachyOS/Hyprland dotfiles with a catch-up ambient
  scheduler and throttled warmth.
- **shesh-backup** — restic wrapper with AC-gated, daily backup and verify.
- **shesh-phone** — ADB safe-area tapping.
- **shesh-containers** — podman/distrobox sandboxed execution.
- **shesh-mcp-bundle** — filesystem/fetch/git proxied through the Guard.
- **shesh-acp** — ACP server for editor integration.

### Platform and infrastructure

- **shesh-ecosystem** — manifest resolver, license gate, three channels
  (stable/canary/devel), MCP config generator, canary end-to-end covering all
  components, Containerfile, distrobox.ini, `install.sh` with btrfs
  snapshot-and-rollback, and supply-chain signing.
- **shesh-workspace** — the development factory: session protocol, swarm
  orchestration, secure credentials, and efficiency tooling.
- **OmniRoute fork** — 291 providers, 90+ free, 500+ models, ~1.53 B free
  tokens per month. (OmniRoute itself is MIT-licensed upstream; this note is
  about that upstream, not the Shesh body.)

### Other personal projects

AIM, ClinicLedger, VillageClinicLedger, FWRS, GameVault, Vyakrti, ePustakalay,
grievance-portal, llm-eval-harness, rag-service, and portfolio were left
untouched per the archive-don't-delete policy.

## Loose ends carried from earlier TODOs

Several items from 2026-08-09 remained open: the `shesh-brain` wrapper,
messaging bridges (Telegram/Signal), media tools, ACP testing against real
editors, and the hardware canary. The kernel-to-SheshAOS merge was explicitly
flagged as blocked — do not force it; a staged, crate-by-crate plan lived in
`KERNEL_MERGE_PLAN.md`.

## Upgrade plan for a clean multi-agent base

The goal was to leave no loose ends so multi-agent work could proceed on a
stable base: clear the P1 backlog, prove CI gates green, keep `shesh-workspace`
apart from the clean `shesh-ecosystem` product, adopt model-agnostic free
models, lean on GitHub Actions for true-hours unattended work, and improve
clone efficiency. The detailed step list (build `shesh-brain`, media tools,
manual ACP verification, demo script, supply-chain provenance, doc sync, and
ADRs) is preserved in the original record.

## Metrics

- Total cloned: 41 all-repos + 13 forks + 22 older `src/` = 54 unique audited.
- Size on disk: `src/` 1.5 GB, `all-repos` 508 MB, `forks` 879 MB (~2.9 GB
  total) — flagged as a workspace-over-budget risk to be cleaned after the
  audit JSON was saved.
- Ecosystem tests: 30 passed (GATE OK at the time).
- Component tests: 182+ passed where dependencies were present.
- Locks: stable 1, canary 16, devel 20 (including shesh-omniroute).
- ADRs: 15. Docs: 40+ in ecosystem, 10+ in workspace.

> **Where this fits —** For the live factual baseline and the P0–P3 findings
> that supersede these numbers, read the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md). The companion
> [gap analysis](./gap-analysis.md) and [incident post-mortem](./incident-2026-08-11-multi-tab-swarm.md)
> continue the story.
