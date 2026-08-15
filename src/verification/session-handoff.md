# Session Handoff — Shesh Ecosystem

Load this file at the start of a new session to continue exactly where the last
one stopped, without re-deriving context. It is the live anchor: the federation
state, the repository map, the autopilot contract, and the deliberate work that
must not be auto-forced.

> **Note —** This handoff was last refreshed around 2026-08-13 and is preserved
> as a working record. It is retained as a record, not as live reference. The
> authoritative factual baseline is the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md): the body is
> **GPL-3.0-or-later** (not MIT), SheshAOS reports **877 passing tests with 1
> ignored** at the baseline, and `gaganjainse/SheshOS` is an unpublished,
> conceptual project rather than a live upstream. Repo counts and test numbers
> below are historical snapshots; where they differ from the baseline, treat
> them as records of that date.

## Summary

- The fleet consolidated into a `shesh-core` monorepo (sixteen folded organs) plus six kept services and SheshAOS; the 2026-08-15 baseline records 31 repositories (10 active, 21 archived).
- Shesh is a local-first, federated agent OS for CachyOS/Hyprland on an MSI Sword 16 HX, governed by a policy/audit layer with a Newelle voice frontend and a Rust kernel (SheshAOS).
- The autopilot enforces a hard contract: no red commits, no force-push, Guard on every tool call, secrets only via `shesh-secrets`.
- Three items are deliberately non-autopilot: the kernel→SheshAOS merge, hardware validation on the physical MSI, and editor ACP testing.
- Read this file first, then the audit/roadmap, TODO, manual verification, session protocol, swarm, and the query log.

## Federation consolidation (2026-08-13, ADR-0019)

Sixteen sub-service `shesh-*` modules folded into the new `shesh-core` monorepo
(sixteen packages plus fifteen unchanged console-script names, 175 tests). Kept
as services: `shesh-memory`, `shesh-orchestrator`, `shesh-harness`,
`shesh-phone`, `shesh-omniroute` (now depend on `shesh-core>=0.1`). Seventeen
folded repos were archived. Manifest organs were unchanged (23); their repo
field points at `shesh-core`; locks regenerated (stable 1 / canary 19 / devel
23). `fetch-components.sh` clones once and symlinks.

## One-link install hardened (2026-08-13)

`bash <(curl -s .../shesh-desktop/main/tools/bootstrap.sh)` installs the whole
stack (desktop + device profile + shesh-core MCP + policy + configs). Fixes
included the setup exec bit, bootstrap flag passthrough, an empty
`mcp_servers` directory, and a canary-default shared venv with correct units.
The Guard policy is config-driven via `~/.config/shesh/policy.json`.

## Current position (2026-08-13, rolling dependency update)

A fleet-wide rolling dependency update moved SheshAOS and several personal
projects to latest majors with green CI. The Nexus→Shesh rename completed across
SheshAOS and the living docs (`kernel_ingest`, `kernel_bridge`,
`kernel-events.jsonl`, `KernelBridge`, `KernelError`); immutable history was
left untouched.

Recent closures included the canary P0 end-to-end test going green on
arch/fedora/ubuntu after wiring fixes; component README auto-sync with link
checking; a failure-memory offline loop with two real learner-bug fixes;
Dependabot fleet merges; and a pipecat transformers RCE advisory fix (dropped
the `[smart]` extra, bumped the lock to 5.15.0). shesh-voice's Flatpak build
was verified green. Known-good commit tips were recorded per repo.

## What Shesh is

Shesh is a local-first AI agent OS for Linux (target: CachyOS on an MSI Sword 16
HX). It is a federation of small MCP components governed by a policy/audit
layer, with a Newelle-based voice frontend and a Rust governance kernel
(SheshAOS, in progress).

**Naming (canon):** the product/OS is **SHESH**; the kernel project is
**SheshAOS**. All repos/packages/imports are `shesh-*` / `shesh_*`; environment
variables are `SHESH_*`. Legacy spellings survive only in immutable-history
classes (ADR/QUERYLOG/audits/attic) and real frozen artifacts.

## Repositories

| Repo | Layer | Tests (historical) | Purpose |
|------|-------|------:|---------|
| SheshAOS | Brain | 872 (Rust, historical) | Governance kernel — merge pending |
| shesh-ecosystem | — | 61 (Python) | Manifest, gates, docs, autopilot, this wiki source |
| shesh-audit | Brain | 29 | Hash-chained event log, GuardedMCP, tool pins, kernel bridge, secrets |
| shesh-secrets | Brain | 8 | env/gopass/keepassxc/file secret resolution |
| shesh-orchestrator | Mind | 28 | Multi-agent RLM runtime, sessions, A2A, traces |
| shesh-memory | Mind | 26 | Episodes, FTS, vector embeddings, habits, intentions, compaction |
| shesh-mind | Mind | 13 | Role-to-model router (6 GB VRAM budget) |
| shesh-harness | Mind | 14 | Self-improvement with held-out `/refine` evaluator |
| shesh-skills | Mind | 10 | Everyday tools plus Markdown skills |
| shesh-calendar | Mind | 6 | iCalendar vdir reader |
| shesh-voice | Soma | — | Newelle fork plus MCP overlay (wake word/STT/TTS) |
| shesh-desktop | Soma | 26 | CachyOS/Hyprland dotfiles, ambient offers |
| shesh-files | Soma | 5 | Rust watcher plus classifier |
| shesh-shell | Soma | 3 | Hyprland/Quickshell MCP |
| shesh-system | Soma | 13 | Power/GPU/MUX, updates, health, maintenance |
| shesh-backup | Soma | 8 | Restic wrapper, AC-gated |
| shesh-phone | Soma | 7 | ADB control for Realme Narzo |
| shesh-containers | Soma | 5 | Podman/distrobox sandboxed exec |
| shesh-mcp-bundle | Soma | 4 | filesystem/fetch/git proxied through Guard |
| shesh-acp | Soma | 12 | Agent Client Protocol (editor integration) |

> **Note —** Test counts above are the 2026-08-13 figures. The
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md) is the
> authoritative baseline and reports verified numbers (for example, SheshAOS at
> 877 passing tests with 1 ignored).

## Where the code lives on disk

- Components: `/home/user/src/shesh-*/` (canonical; `sesha` directory names on
  older machines are a known legacy typo).
- Ecosystem: `/home/user/shesh-ecosystem/` (canonical) — use the
  `shesh-ecosystem` repo at the workspace root.
- Each component: `pyproject.toml`, `src/shesh_<name>/`, `tests/`,
  `.github/workflows/ci.yml`, `.gitignore`.
- MCP entry points are `shesh-<name>-mcp` console scripts.

## The autopilot

`tools/autopilot/` in shesh-ecosystem is the foolproof self-running system:

- **safety.py** — hard invariants: no red commits, no force-push, protected
  paths, rollback on failure, canonical remote check.
- **ledger.py** — a durable JSONL task journal at
  `~/.local/share/shesh/autopilot/ledger.jsonl`; resumes after interruption.
- **gate.py** — runs `ruff` + `pytest` in isolation before commit.
- **runner.py** — `process_task`: implement → gate → safe_commit → safe_push,
  with one retry and soft rollback; never pushes red.
- **cli.py** — `python -m tools.autopilot.cli {list,seed,run}`.

Before building any feature, run the autopilot tests:
`cd shesh-ecosystem && python3 -m pytest tests/autopilot -q`.

## How to build safely (the contract)

1. Pick the next pending item from TODO.md (or seed it).
2. **First instinct = steal, not build.** Check SOURCES.md, TOOLING_CATALOG.md,
   and `manifests/upstreams.toml` for open-source tools to adopt, upgrade, and
   specialize.
3. Work in one component; keep changes small and focused, but build proper
   working versions — no minimal stubs that become dead code.
4. **Always** run that component's tests: `cd components/shesh-<x> && python3 -m pytest tests/ -q`.
5. Use `GuardedMCP` from shesh-audit for any new MCP server.
6. Never store secrets in config — use `shesh-secrets` references
   (`env:`, `gopass:`, `file:0600`).
7. Commit with the task id; push through the autopilot safety guards.
8. After each user message, append to the query log and update TODO.md.
9. Archive, don't delete; no force-push to main; no root.
10. Mark hardware-only items 🟡 rather than faking success.
11. Upgrade the wrapper, not just fork and wrap.
12. Integrate systems without conflict — MCP stdio, the Guard, separate
    services and config dirs, one job per component, one process per MCP server.
13. Treat style and performance as non-negotiable.

## What is done

- All repos renamed Shesh→Shesh (GitHub redirects old names).
- Governance: audit log, GuardedMCP, policy, kernel event bridge, secrets.
- Agents: orchestrator with roles, persistent sessions + cancel, A2A UDS, local
  JSONL traces, LLM planner/critic with Ollama plus stubs.
- Memory: episodic + FTS + vector embeddings, habits/intentions/mannerisms,
  compaction/retention, semantic search MCP.
- Self-improvement: held-out evaluator, `refine_with_llm`.
- Skills: notes/web/code/docs/reminders plus five skills.
- Calendar (iCal vdir), containers (podman sandbox), MCP bundle via Guard.
- System: power/GPU/MUX, restic backup, read-only update check, health,
  maintenance/cache clean.
- Phone (ADB safe-area), ACP (session/prompt/terminal/diff/cancel/perm).
- Desktop: ambient scheduler with data-aware signals, settings GUI.
- Platform: manifest resolver, license gate, three channels, MCP config
  generator, canary end-to-end covering all components.
- Autopilot safety core; the documentation set (audit/roadmap, glossary,
  manual verification, tooling catalog, this handoff, query log).

## What remains (priority order)

### 🔴 Blocked (deliberate / hardware — do not auto-force)

- **shesh-kernel → SheshAOS merge.** Follow `KERNEL_MERGE_PLAN.md`: port leaf
  crates first, reconcile `KernelError`/TUI APIs, bring in `shesh-protocols`
  (ACP+MCP wire impls) and CLI/worker, fix upstream `russh`/`zig` breaks, gate
  on `cargo test --workspace` green.
- **Hardware validation on the physical MSI Sword 16 HX** — run through
  `docs/MANUAL_VERIFICATION.md`.
- **Docs** — the reading compilation lives in `shesh-docs` (mdBook); GitHub
  wikis are disabled fleet-wide.
- **Editor ACP testing** against real Zed/JetBrains (protocol implemented).

### 🟡 P1 (unblocked, build next)

- LLM-backed auto skill capture (Read→Execute→Reflect→Write) with deprecation.
- Distrobox/Containerfile for one-command onboarding.
- Installer channels with btrfs snapshot + rollback.
- Local email (IMAP via vdirsyncer/neomutt); messaging bridges
  (Telegram/Signal, isolated).
- Media tools (screenshots, recording, wallpaper, audio routing).
- OTLP export of local traces.
- Decide the fate of `shesh-maint` (finish or fold into shesh-system).
- Wire ambient signals into the live offer loop and the desktop GUI.

## Known gotchas

- **Editable installs:** after any package rename, run `pip install -e .` in
  each component or imports resolve to stale names.
- **Pytest isolation:** from the ecosystem repo, use
  `-p no:cacheprovider -o addopts= --confcutdir <repo>` (the gate does this).
- **Ollama models** for the 6 GB stack: `phi4-mini`, `qwen2.5-coder:3b`,
  `moondream2`, `nomic-embed-text`.
- **Workspace budget:** do not install the Rust toolchain or large clones in
  the sandbox; keep `/home/user`` under ~150 MB.
- The local workspace folder may be named `sesha` (typo); ignore it — all
  remotes/packages are canonical `shesh-*`.

## First commands for a fresh session

```bash
cd /home/user/shesh-ecosystem
export PATH="$HOME/.local/bin:$PATH"

# 1. Verify everything is green
for d in ../components/shesh-*/; do
  (cd "$d" && python3 -m pytest tests/ -q -p no:cacheprovider)
done
python3 -m pytest tests/ -q -p no:cacheprovider

# 2. Read the anchors
$ PAGER TODO.md docs/history/AUDIT_AND_ROADMAP.md docs/MANUAL_VERIFICATION.md

# 3. Continue with the next P1 from the remains section
```

## Design principles (do not violate)

- **Local-first / offline** — every tool degrades to deterministic stubs.
- **Governed** — every tool call passes the Guard; policy decides.
- **Federated** — one job per component; the manifest integrates them.
- **Tested before push** — the autopilot refuses red commits.
- **Small, reversible, audited** — commits, events, rollback.
- **No secrets in repos** — `shesh-secrets` only.
- **Steal first, make second** — first instinct when blocked is to adopt
  open-source; discard what Shesh made if something better exists.
- **Proper working versions, not minimal stubs.**
- **Upgrade the wrapper, not just fork and wrap.**
- **Cautious but enterprising, no conflicts** — namespace via MCP stdio, the
  Guard, separate services, config dirs, btrfs subvolumes, and uv venvs.
- **Style + performance non-negotiable** — the Hyprland look and CachyOS
  performance are the point; improve style, do not change it.

## Session protocol — hot hopping

Arena snapshots at ~128 MB / 10k files slow after 60 minutes or many tool
calls. The solution is a 60-second handoff with zero loss:
`tools/session_guard.py` monitors workspace size, file count, age, latency, and
uncommitted files, then creates `docs/SESSION_HOP_ALERT.md` past thresholds.
`scripts/supervise.sh` and the runner call the guard before each task; on a hop
they finish the current task, commit, push, and exit. `tools/session_guard.py
--handoff` generates `docs/NEXT_SESSION_PROMPT.md` plus `dist/handoff.json`.
`tools/github_auth.py` loads the PAT securely and never logs its value.

**When to hop:** the guard says HOP, you feel lag, ~60 minutes elapsed, or
`make check` starts slow.

## Swarm — parallel sessions via GitHub as bus

Arena chats have no connection to each other, but you can open several Agent
Mode tabs and want parallel work without overwrite. GitHub is the bus:
`swarm/` queue/claims/heartbeats/artifacts/ledger.jsonl.

- Orchestrator: `python tools/swarm/orchestrator.py --seed TODO.md --monitor`.
- Workers: `python tools/swarm/worker.py --component shesh-memory` (atomic
  claim via `git pull --rebase` + add claim + commit + push; first push wins).
- Branch per task `swarm/<agent-id>/<task-id>`; `make check` gates merge to
  main.
- Safety: component filter avoids same-file edits; heartbeat every poll;
  orchestrator re-queues stale claims; the Guard is still enforced; no secrets
  in swarm files.

It is actionable for two to four workers with component partitioning, with
caveats (no real-time 45s poll, PAT needed, manual tab opening, more workers
means more git conflicts). Best is one orchestrator plus two workers.

## New session accomplishments (2026-08-11)

That session fixed manifest/lock drift, cloned and verified component tests,
synced component READMEs, created fifteen ADRs plus a getting-started guide,
built the Containerfile/distrobox.ini/install.sh, added supply-chain signing
and OTLP export, implemented the session protocol and swarm tooling, and
updated TODO/QUERYLOG/AUDIT_AND_ROADMAP links.

## Message to give the next AI

Copy from `docs/NEXT_SESSION_PROMPT.md`:

```
You are continuing Shesh — federated local-first AI OS for CachyOS/Hyprland on
MSI Sword 16 HX. GitHub owner: gaganjainse. Main repo: shesh-ecosystem. Read
docs/SESSION_HANDOFF.md FIRST, then AUDIT_AND_ROADMAP, TODO, MANUAL_VERIFICATION,
SESSION_PROTOCOL, SWARM, GETTING_STARTED, queries/QUERYLOG.md. PAT: set
GITHUB_PAT env or ~/.config/shesh/github.pat (0600) or gh auth login. Run:
cd /home/user && git pull origin main && make check && python
tools/session_guard.py --status. Then pick the next pending item from TODO.md
and continue the autopilot.
```

> **Where this fits —** The [next session prompt](../queries/next-session-prompt.md)
> carries the copy-paste block with live numbers, and the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md) is the factual
> baseline to reconcile against.
