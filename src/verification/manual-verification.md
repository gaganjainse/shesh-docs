# Manual Verification Checklist

Shesh automates many things and unit-tests all of them, but some checks cannot
run in the build sandbox. This checklist is the on-machine confirmation pass:
work through it on the real MSI laptop after install, with real hardware,
accounts, and GUI apps, and tick each item as you confirm it.

> **Note —** This is a live checklist. The authoritative factual baseline is the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md): the body is
> **GPL-3.0-or-later**, SheshAOS reports **877 passing tests with 1 ignored** at
> the baseline, and `gaganjainse/SheshOS` is an unpublished, conceptual project
> rather than a live upstream. A few counts quoted here reflect earlier
> snapshots; rely on the baseline for license and test facts.

Last updated: 2026-08-13 (16 sections). The companion
`docs/history/queries/QUERYLOG.md` records what changed and why.

## Summary

- Confirm first boot into CachyOS/Hyprland at 1920×1200 @ 144 Hz with audio and microphone working.
- Verify accounts and secrets: Ollama models, a restic repo, secret resolution, and no committed keys.
- Run the end-to-end canary and confirm the MCP mesh, voice, GPU/MUX, desktop, backup, phone, and containers.
- Walk through agent behavior, security/audit, canary releases, dependency hygiene, security posture, and a recovery drill.
- Mark the kernel merge, hardware validation, and editor ACP testing as deliberate, non-autopilot work.

## 0. First boot

- [ ] Boots into CachyOS / Hyprland without errors
- [ ] `hyprctl version` works; keybinds from the desktop fork are active
- [ ] Resolution is **1920×1200 @ 144 Hz** (check `hyprctl monitors`)
- [ ] The Quickshell status bar / settings render with no pink placeholders
- [ ] Audio works (speakers + headphone jack): `wpctl status`, play a sound
- [ ] Microphone works (for wake word / STT)
- [ ] Network (Wi-Fi + Ethernet) connects
- [ ] `~/.local/share/shesh/` directory tree exists after first run

## 1. Accounts, keys, and secrets

- [ ] **Ollama installed and running**: `systemctl --user status ollama`
- [ ] Models pulled for the 6 GB stack: `phi4-mini` (primary/planner/researcher/critic), `qwen2.5-coder:3b` (coder), `moondream2` (vision), `nomic-embed-text` (embeddings/RAG)
- [ ] **`restic` installed** and a repo initialized: `restic -r <repo> snapshots`
- [ ] `restic` repository password stored in **gopass/KeePassXC**, referenced as `env:RESTIC_PASSWORD` or `gopass:shesh/backup` — **never** in plain config
- [ ] MCP servers resolve secrets via `shesh-secrets`: `get_secret("env:MY_TOKEN")`
- [ ] No API keys/tokens committed to any repo (run a secret scan)
- [ ] Git identity configured: `git config --global user.email/name`

## 2. MCP mesh (the core integration)

After installing all `shesh-*` packages, run the canary:

```bash
bash scripts/e2e-canary.sh   # from shesh-ecosystem
```

- [ ] **E2E canary passes** (all components import, policy denies protected paths, memory/orchestrator/ACP/backup/calendar/vectors/traces all respond)
- [ ] Generate the MCP config: `python scripts/generate_mcp_config.py --channel canary`
- [ ] `~/.config/shesh/mcp/servers.json` lists the expected MCP servers
- [ ] **Newelle (shesh-voice)** starts and its MCP panel shows the servers connected
- [ ] Restart Newelle and ask it to **list its tools** — it should see `check_system_updates`, `semantic_search`, `start_session`, and others
- [ ] Zed (or another MCP client) can connect via the generated `zed.json`
- [ ] Each MCP server starts standalone without import errors

## 3. Voice (shesh-voice / Newelle fork)

- [ ] Fork `gaganjainse/shesh-voice` is tracking upstream `qwersyk/Newelle`
- [ ] The overlay config copied: `cp shesh-overlay/shesh-mcp-servers.json ~/.config/Newelle/mcp-servers.json`
- [ ] Default model set to local Ollama `phi4-mini`
- [ ] **Wake word "hey shesh"** triggers listening (openwakeword)
- [ ] Speech-to-text transcribes your voice accurately (faster-whisper)
- [ ] Text-to-speech reads responses aloud
- [ ] Mic permission / PipeWire access not blocked

## 4. GPU, power, and MUX (MSI-specific)

- [ ] **NVIDIA driver loaded**: `nvidia-smi` shows the GPU and temp/power
- [ ] `powerprofilesctl list`; switching performance↔balanced↔power-saver works
- [ ] `shesh-system-mcp` → `set_power_profile("gaming")` changes it
- [ ] **MUX switch**: `sudo msi-mux-switcher status`; switching requires a reboot as documented
- [ ] GPU VRAM stays under the 5.5 GB budget when two models load (`watch nvidia-smi`)
- [ ] Hybrid graphics routes apps correctly (`__NV_PRIME_RENDER_OFFLOAD=1`)

## 5. Display and desktop

- [ ] Refresh rate stays at 144 Hz (no drop to 60)
- [ ] Fractional/HiDPI scaling looks correct
- [ ] Screen recording / screenshots work (the `grim`+`slurp` pipeline)
- [ ] Notifications appear and are not duplicated
- [ ] Idle inhibitor works during video/media
- [ ] The **ambient offer overlay** appears at natural pauses (not while typing or gaming) and does not nag (max three per day, 30-minute cooldown)

## 6. Backup

- [ ] `shesh-backup-mcp` → `run_backup` completes (after a manual first `restic init`)
- [ ] First backup verified: `restic -r <repo> snapshots` lists it
- [ ] `check_system_updates` reports pending pacman/AUR packages (read-only)
- [ ] **System update is never automatic** — it only notifies; you run `pacman -Syu`
- [ ] `clean_system_caches("user")` frees space without error
- [ ] A scheduled backup timer is enabled if you want daily unattended runs
- [ ] **Test a restore** to a temp dir before trusting backups

## 7. Phone (shesh-phone, Realme Narzo)

- [ ] ADB debugging enabled on the phone; `adb devices` lists it
- [ ] `shesh-phone-mcp` connects (safe-area taps land on screen)
- [ ] Taps **outside the status/nav bars are refused** (try a coordinate at y=10)
- [ ] Screenshots pull successfully
- [ ] Vision model can describe a screenshot if wired
- [ ] The phone does **not** accept destructive commands without confirmation

## 8. Containers / sandboxing

- [ ] `podman` installed and rootless works: `podman run --rm alpine echo ok`
- [ ] `shesh-containers-mcp` → `run_sandboxed(["echo","hi"])` returns output
- [ ] Sandboxed commands have **no network** by default (`--network=none`)
- [ ] `--cap-drop=ALL` is in effect
- [ ] Containers are removed after each run (`--rm`)
- [ ] The third-party MCP bundle launches only if `npx`/`uvx` are present

## 9. Agent behavior

- [ ] Start a goal via `shesh-orchestrator-mcp` → `execute("...")`; it plans, delegates by role, and the critic approves
- [ ] **Background sessions** work: `start_session`, disconnect, `get_session` later shows progress/result
- [ ] `cancel_session` actually stops a long-running goal
- [ ] `/refine` promotes a skill/memory change only if the held-out evaluator scores ≥ 0.7
- [ ] The LLM is used when Ollama responds; offline, deterministic stubs keep the system working
- [ ] **Memory compaction** runs without data loss; old episodes move to `semantic.md`
- [ ] Semantic search returns relevant memories
- [ ] Habits/intentions/mannerisms reflect your actual preferences over time

## 10. Security and audit

- [ ] Every tool call is logged: `~/.local/share/shesh/audit/events.jsonl`
- [ ] The hash chain verifies: no "tampered" results
- [ ] Kernel-format events appear in `kernel-events.jsonl` and are ingested by the Rust kernel (wiring done 2026-08-13; on-machine run remains a hardware check)
- [ ] Writing to `.ssh`, `.gnupg`, `Vaults/`, or job folders is **denied**
- [ ] Destructive terminal commands in ACP ask for confirmation
- [ ] No MCP server runs as root
- [ ] The audit Guard wraps every MCP server (each server's logs show a "policy" line)

## 11. Canary / releases

- [ ] The daily canary GitHub Actions run is green
- [ ] If you switch to **stable**, a `btrfs snapshot` is taken before install
- [ ] Rollback works: boot the snapshot from grub/btrfs-grub
- [ ] Component versions in `manifests/components.toml` match what is installed

## 12. Rolling dependency hygiene (monthly, ~5 minutes)

CachyOS rolls; so does Shesh. Full protocol: `docs/policies/DEPENDENCY_POLICY.md`.

- [ ] **Dependabot PRs are landing green** and being merged, not piling up
- [ ] **SheshAOS supply-chain job is green** (cargo-deny + cargo-machete + typos)
- [ ] **Python tool floors are current** — spot-check `pytest`, `ruff`, `fastmcp` floors against PyPI
- [ ] **Rust tree refreshes monthly** — `cargo update` in SheshAOS, then `cargo test --workspace` + `cargo clippy` must stay green
- [ ] **No deprecated actions/content** left pinned-and-forgotten
- [ ] **Break-glass works** (only if a bump breaks CI): downgrade the offender by exactly one minor, repeat once; if still broken, drop and replace

## 13. Security posture (GitHub-side browser checks, quarterly)

Canonical posture: `SECURITY.md`; threat model: `docs/THREAT_MODEL.md`.

- [ ] **Push protection + secret scanning ON** in every repo
- [ ] **Private vulnerability reporting enabled** on shesh-ecosystem
- [ ] **Dependabot alerts are empty or triaged**
- [ ] **SHA pins intact** in recent CI runs
- [ ] **PAT hygiene**: `~/.config/shesh/github.pat` is mode 600, never pasted into chats
- [ ] **Outstanding owner action**: rotate the PAT (it appeared in tool transcripts on 2026-08-11/12)
- [ ] **Tool-pin defense live** (`shesh-audit` ≥ 53a60b6): first MCP server boot prints `learned pin`; a tampered tool description refuses with `ToolPinDrift`
- [ ] **swarm-auto-merge canary**: the workflow refuses non-`swarm/*` branches and `pull_request_target` is gone

## 14. Recovery drill (quarterly, ~15 minutes)

Runbook: `docs/RECOVERY.md`. Automated checker: `tools/dr_check.sh`.

- [ ] `bash tools/dr_check.sh` reports all-green locally
- [ ] **Backup restore actually restores**: `restic restore latest --target /tmp/restore-test --include ~/.config`
- [ ] **Workspace-restore drill known by heart** (re-seed PAT perms, re-add dropped remotes, fetch, reset, restore exec bits)
- [ ] **Stale-base repair drill**: know the graft pattern for when a snapshot rewinds HEAD
- [ ] **Incident comms path works**: you can open a `SECURITY: …` issue without proof-of-concept details

## 15. Deliberate (non-autopilot) work

These are 🔴 in TODO.md and intentionally **not** auto-forced:

- [ ] **shesh-kernel → SheshAOS merge**: follow `KERNEL_MERGE_PLAN.md`; port leaf crates first, reconcile `KernelError`/TUI, bring in `shesh-protocols`, fix upstream `russh`/`zig` build breaks, gate on `cargo test --workspace`
- [ ] **Hardware validation on the physical MSI** (this whole document)
- [ ] Rebase shesh-voice on upstream Newelle periodically
- [ ] Set up real CalDAV/IMAP sync with vdirsyncer if wanted
- [ ] Optionally connect Telegram/Signal bridges (isolated accounts)
- [ ] Test ACP against actual Zed/JetBrains

## 16. Wiki (one-time setup)

GitHub wikis are disabled fleet-wide; this compiled book (`shesh-docs`) is the documentation source.

## Quick health command

Run this anytime; it should report all-green:

```bash
echo "=== Shesh health ===" && \
systemctl --user is-active ollama && \
bash ~/src/shesh-ecosystem/scripts/e2e-canary.sh && \
for s in shesh-{audit,system,shell,files,skills,memory,mind,harness,orchestrator,backup,phone,containers,secrets,calendar,acp}-mcp; do
  command -v "$s" >/dev/null && echo "ok  $s" || echo "MISSING  $s"
done && \
echo "=== done ==="
```
