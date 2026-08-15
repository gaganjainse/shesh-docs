# Style and Performance: The Non-Negotiable Constraint

Two decisions in this project are fixed, and every other decision bends around them: the desktop
keeps the illogical-impulse look, and the machine keeps CachyOS performance. This chapter states
that constraint precisely and defines the only kind of work allowed inside it.

## Summary

- The visual layer is `end-4/dots-hyprland` (illogical-impulse) with Quickshell `ii`; the
  performance layer is CachyOS 260628. Neither is up for renegotiation.
- Shesh contributes backend systems that plug into the existing look. It never replaces the
  compositor config, the bar, or the theme engine.
- Seven components already integrate correctly through thin `custom/` overrides, Quickshell
  widgets, and systemd user services.
- Remaining work is backend only: desktop control, browser automation, media, containers,
  telemetry, and an optional cloud gateway.
- Patterns may be borrowed from rival dotfile projects; their visuals may not.
- Dependencies must be open source and usable without a metered API key.

> **Requirement —** "My need is style + performance. I am using illogical impulse because i love
> its look, and using CachyOS because i love its performance. We can't compromise on this, and last
> point don't break these systems or anything else per se. I am already using end-4's shesh-desktop
> so i don't need looks, i need a good backend and other systems that integrate into that look, do
> you understand. I am not using native Hyprland and need to customize it, i am already using the
> best customized dotfiles riced look."

## The two layers that cannot change

Think of the machine as a finished building. The facade and interior design are complete and
admired; what is missing is plumbing, wiring, and a building-management system. Shesh is the
building services contractor, not the architect. It runs pipes inside existing walls.

The **look** is `illogical-impulse` — end-4's dotfiles, carried in this fork as `shesh-desktop`.
It supplies Material You theming, Quickshell `ii` widgets, anti-flashbang, screen translate,
clipboard IPC, the keybind set, a Lua-configured Hyprland at 0.55 or newer, and the Quickshell
framework itself.

The **performance** base is CachyOS 260628: Arch-derived, Linux 6.18 live and 7.1 installed, the
BORE scheduler, and packages built with LTO, PGO, BOLT, and x86-64-v3/v4 targets. This is why the
distribution was chosen, so nothing may erode it.

Native Hyprland is not in use. The customized configuration is the product. Work that "starts
fresh" from upstream Hyprland defaults is work that destroys the deliverable.

## Four things this project must never do

| Prohibition | Why it matters |
|---|---|
| Do not replace the shell look with DankMaterialShell, `ekremx25/quickshell`, HyprPanel, or ashell | Each is a different visual identity; adopting one discards illogical-impulse |
| Do not switch shells to CachyOS Noctalia, even though 260628 ships it as a Hyprland option | The existing shell is already chosen and tuned |
| Do not erode CachyOS performance | No heavy dependency trees, no Flatpak for the voice agent, host kept clean via rootless Podman and Distrobox, `custom/` overrides kept thin, upstream rebased often |
| Do not break working systems | Hyprland, Quickshell, and CachyOS must all keep functioning through every change |

## Backend components that already fit inside the look

Each of these lands as a thin override, a Quickshell widget, or a systemd user service. None of
them repaints the desktop.

**shesh-files** pairs a Rust watcher with a Python classifier over Downloads, Desktop, Documents,
and Pictures. It debounces for 30 seconds, emits JSON, and applies deterministic extension and
name rules first, so the common case needs no model at all and stays private. Ambiguous files can
optionally reach Ollama `phi4-mini`, and screenshots can reach `moondream2` for vision. State
lives in a SQLite history and undo log under `~/.local/share/smart-organizer/`; deletions go
through `gio trash` rather than `rm`; a dry-run mode is always available. Low-confidence
decisions surface as `notify-send` action buttons. The tool is wired into MCP, so Shesh can act
on "organize downloads" or "undo last move" by voice, and its Quickshell indicator shows recent
moves with pause, resume, and undo — a widget inside the bar, not a replacement for it.

**shesh-shell** is the Hyprland and Quickshell MCP surface: a `hyprctl` wrapper plus Quickshell
IPC. It never rewrites the Hyprland configuration; it drives the compositor through the IPC that
already exists, behind the policy Guard.

**shesh-system** covers power, GPU and MUX switching, backup, and status. It calls
`powerprofilesctl`, which CachyOS already ships, switches the MUX through `msi-mux-switcher`,
runs restic backups, checks updates read-only, reports health, and cleans caches. It integrates
as systemd user services rather than as a bar.

**shesh-audit** is a hash-chained, append-only event log with a policy Guard and a Nexus bridge.
It sits behind every MCP server and records every tool call. It has no user interface at all, so
it cannot conflict with the look.

**shesh-voice** is the Newelle fork overlay: wake word "hey shesh", `faster-whisper` for speech
to text, Piper for speech synthesis, an MCP client over stdio, model defaults chosen for a 6 GB
GPU, and an about screen reading "Shesh (Newelle core)". It hosts its overlay inside the existing
illogical-impulse AI sidebar rather than replacing it.

**shesh-ambient**, which lives in the desktop repository, is the polite catch-up scheduler
described in [Ambient Design](./ambient-design.md). It triggers on `OnStartupSec` plus jitter
instead of a fixed wall-clock hour, requires AC power and idleness for heavy jobs, bounds itself
with a catch-up budget, and defers during fullscreen windows, calls, high CPU, or low battery.
Proactivity is limited to one optional offer at a natural pause between 45 seconds and 15 minutes
of idleness, throttled to at most three per day and always snoozeable.

## Backend components still to build

These come from the second wave of research recorded in `GAP_ANALYSIS.md` and `SOURCES.md`,
filtered down to backend work only.

- **shesh-control MCP** gives the agent eyes and hands beyond `hyprctl`: the AT-SPI accessibility
  tree, Wayland input injection, screenshots, and compositor window targeting. Borrow from
  `computer-use-linux` (Apache-2.0) and wrap it as an MCP server behind brain policy, with
  destructive actions requiring approval. It drives existing Hyprland windows and paints nothing.
- **shesh-browser MCP** drives a real browser in a sandboxed profile for web tasks, borrowing from
  `browser-use`. It has no interface of its own.
- **shesh-files improvements** replace the custom polling loop with `notify-rs/notify`
  `RecommendedWatcher`, the cross-platform filesystem notification crate already used by
  Alacritty, `cargo watch`, mdBook, and Zed. Polling wastes I/O; the crate reacts in under
  100 ms.
- **shesh-system improvements** take backend logic only from neighbouring projects: single-batch
  monitor management via `hyprctl --batch` to avoid flicker when changing resolution, refresh
  rate, HDR, or VRR; a night-light backend built on `hyprsunset` or `gammastep` with a
  1000–6500 K slider and a fixed-time schedule; and the `dgop` system-monitoring library plus
  shared QML widgets from `dank-qml-common`. The bars those projects ship stay behind.
- **shesh-media** covers screenshots through a `grim`/`slurp` pipeline, screen recording,
  wallpaper, and audio routing. Check `configs/quickshell/rishot` first, since illogical-impulse
  may already provide a pure Wayland Quickshell screenshot app bound to Print.
- **shesh-messaging** runs isolated, opt-in Telegram and Signal services as separate systemd
  units with no interface.
- **shesh-containers** wraps Podman and Distrobox for sandboxed execution, for example
  `run_sandboxed(["echo","hi"])` with `--cap-drop=ALL --network=none`.
- **shesh-ebpf** provides read-only eBPF telemetry through Aya in Rust, behind the Guard.
- **shesh-omniroute** is the free-model gateway — 291 providers, more than 90 of them free —
  strictly optional and always secondary to the local Ollama primary. Its enable switch belongs
  in the settings GUI (`SeshaConfig.qml`), styled exactly like the existing General, Bar, and
  Services pages.

> **Note —** The settings page and its service still carry the legacy `Sesha` file names. Treat
> that spelling as a naming artifact from an earlier iteration, not as a second product.

## What to borrow, and what to leave alone

| Source | Borrow | Leave behind |
|---|---|---|
| ML4W 2.14.1 | The declarative single-file `statusbar.json` pattern, if a backend ever needs it | The GUI configurator |
| JaKooLit/Hyprland-Dots | Per-monitor refresh scripts, SDDM handling, Bluetooth menu logic | The visuals |
| prasanthrangan/hyprdots (HyDE) | Wallbash's one-wallpaper-themes-everything idea for apps `matugen` does not cover; `themepatcher` and `hyde-cli` modularity | The theme set and the look |
| CachyOS Noctalia | Animation curves and NVIDIA compositing hints | The shell itself |
| Caelestia-shell | Easing and blur parameters in QML for 144 Hz smoothness, with no dependency change | Anything visual |

## Rules of integration

These rules come from `REPO_TOPOLOGY.md` and `LANGUAGE_POLICY.md`, extended by the second research
wave. Together they explain why adding a component does not destabilize the whole.

- **One job per component.** `shesh-files` watches Downloads, Desktop, Documents, and Pictures and
  never touches `Projects/`, `Vaults/`, `Documents/Job`, or `.ssh`. Enforcement lives in
  `safety.sh`.
- **One process per MCP server.** `shesh-audit-mcp`, `shesh-system-mcp`, and their siblings each
  speak stdio from their own systemd user service. Nothing is shared.
- **One policy gate.** Every tool call passes `Guard.check(actor, tool, args)`, which returns
  allow, confirm, or deny, then logs the decision and emits a Nexus event.
- **Separate configuration and state directories.** `~/.config/shesh/mcp/` per server,
  `~/.config/shesh/messaging/` for flags, `~/.local/share/shesh/` for state, `~/.cache/shesh/`
  for cache.
- **Separate btrfs subvolumes.** `AI/Models` is nocow, `Downloads` is transient,
  `Documents/Personal` snapshots hourly, and `Documents/Job` is never snapshotted, per employer
  policy.
- **Namespaced tools.** Names are prefixed `fs_*`, `fetch_*`, `git_*` through the
  `shesh-mcp-bundle` proxy, so two servers cannot collide.
- **Pinned versions and a license gate.** `manifests/components.toml` pins versions and
  `scripts/check_licenses.py` refuses incompatible licenses.
- **Tests before push.** `make check` runs ruff, pytest, the license check, and lockfile
  verification; autopilot refuses a red commit.
- **Thin overrides.** `custom/` stays small in `shesh-desktop`, upstream is rebased often, and MCP
  or automation work never diverges `dots/`.
- **Separate processes, IPC between them.** Following DankMaterialShell and `ekremx25`, a
  compiled daemon handles system monitoring while QML handles the interface, communicating over
  IPC rather than shared memory. Shesh adopts the same split: a daemon for system state, QML for
  the surface, MCP for tools.

## Open source only, with no metered gateway

> **Requirement —** "Tavily not completely free but subscription based, don't want things that are
> online-led, only want open-source things"

Two candidates are therefore discarded: Tavily, at roughly 0.005 USD per query with a required API
key and a closed-source, online-led model, and Brave Search, at 5 USD per 1,000 queries with a key.

What remains is genuinely free, key-free, and open source: the filesystem server
(`@modelcontextprotocol/server-filesystem`), Git (`server-git`), Fetch (`mcp-server-fetch`),
Sequential Thinking, the Memory knowledge graph, Microsoft's Playwright MCP, Context7 with an
optional key, DuckDuckGo for privacy-first search with no key, Obsidian, Chrome DevTools, SearXNG
(AGPL-3.0) as a self-hosted metasearch front end across more than 70 engines with no key and full
privacy, `agent-search` which bundles SearXNG into a one-command MCP deployment with zero keys,
and Tor as an option.

## Upgrade the wrapper, do not merely wrap it

Forking is the beginning of the work, not the end. Each fork is specialized for this system and
improved, which is what separates a product from a repackaging.

| Upstream | Becomes | The upgrade |
|---|---|---|
| Newelle | `shesh-voice` | Strips GNOME-only assumptions, adds a Hyprland Quickshell overlay, prewires the MCP servers, sets 6 GB-safe model defaults, wake word "hey shesh", `faster-whisper` and Piper, renamed in the about screen to "Shesh (Newelle core)" |
| end-4/dots-hyprland | `shesh-desktop` | Keeps `custom/` thin and adds a `shesh` configuration object to the Quickshell settings system, a settings page (`SeshaConfig.qml`) styled like General, Bar, and Services, and a service (`Sesha.qml`) that applies toggles to systemd units and `hyprctl` |
| `modelcontextprotocol/servers` filesystem | `shesh-mcp-bundle` | Proxies through the Guard with `fs_*` tool prefixing, a handshake, skip-if-missing behaviour, a policy check on every call, and a logged Nexus event |
| `phone-harness` concept | `shesh-phone` | Ports a macOS-only OCR-to-coordinate-to-act loop onto ADB for a Realme Narzo 90x, with safe-area bounds and `moondream2` vision in place of OCR |

## Distance to a CachyOS install and a first release

The phases below are drawn from [Roadmap — Phases 0 through 7](./02-roadmap.md), filtered to
backend work.

**Phase 0, pre-install fixes, one to two sessions.** Repair the 10 regressions catalogued in
[the audit](./01-audit.md) — the new bugs N-01 through N-10, the MSI DMI content check in BUG-05,
and the zram configuration in HIGH-05. This must happen *before* CachyOS is installed, or
`./setup install` crashes. It touches the installer only, never the look.

**Phase 1, CI gates, half a session.** Extend ShellCheck to every `.sh` file and add Arch
container CI, so this class of bug cannot reach `main` again.

**Phase 2, refactor, one to two sessions.** One source per systemd unit, a straight-line read
through the installer, and an uninstall path that genuinely reverses itself.

**Phase 3, device tuning, one session plus on-device verification.** Set the monitor to
`eDP-1,1920x1200@144`, decide VRR and tearing, configure the NVIDIA hybrid path with
`GBM_BACKEND=nvidia-drm`, keep the iGPU primary for compositing, use `prime-run` or `nvidia-run`
for offload, drive the MUX through `msi-mux-switcher`, set up 8 GB of zstd ZRAM, confirm the BORE
scheduler, configure PipeWire at quantum 256 and 48 kHz, and disable Wi-Fi power saving on the
AX211. Borrowed easing and blur parameters from Caelestia-shell keep 144 Hz smooth without a new
dependency.

That places the CachyOS install one to two sessions away, gated on the Phase 0 fixes.

**Phase 4, Smart-Organizer v2, two to three sessions.** The Rust `notify` watcher at roughly
3 MB, a classifier that tries deterministic rules before any model, optional `phi4-mini` and
`moondream2` passes, `rules.toml`, SQLite history with an undo log, `gio trash` instead of `rm`,
and `notify-send` action buttons. Its only visible surface is a Quickshell indicator.

**Phase 5, automations, one to two sessions.** Power profile and GPU hints on AC change via udev,
a nightly deep scan with backup verification and maintenance, a weekly notification-only
`pacman -Syu` reminder that never updates on its own, a disk alert at 80 percent, monthly SMART
and battery reports, and font cache regeneration through pacman hooks.

**Phase 6, the Shesh agent, three to five sessions.** Newelle 1.4.5 from the AUR rather than
Flatpak, Ollama 0.32 or newer with 6 GB-safe models, three MCP servers over stdio, a Quickshell
overlay showing listening, thinking, and speaking states driven by Newelle's OpenAI-compatible
endpoint, the audit log, a daily 08:00 briefing skill, and an optional ADB phone harness. The
overlay supplements the illogical-impulse bar; it does not replace it.

Taken together, Phases 0 through 3 in the first week, 4 and 5 in the second, and 6 across weeks
three and four put a first release roughly three to four weeks out — but only if backend patterns
are borrowed rather than reinvented, and only if the look is left alone.

## Where the fleet actually stands

The Mind and Brain planes are on track: memory, harness, orchestrator, skills, audit, and a
model-agnostic free-first router, with swarm coordination through GitHub Issues using atomic
locks, PR auto-merge, a scheduled janitor on true hours, and a secure PAT password flow. The
2026-08-09 reconciliation recorded more than 100 tests and 15 ADRs across those repositories.

> **Note —** Test and ADR counts are date-scoped. The 2026-08-15 fleet audit is the current
> baseline for fleet-wide totals; re-verify before quoting these figures elsewhere.

The Soma and Desktop planes were off track. Work that should have been borrowed as backend logic
was rebuilt instead, 10 new bugs were introduced, and stub files made the repository look further
along than it was. The correction is now recorded: keep the illogical-impulse look intact, borrow
backend logic only, and lint every script in CI so the N-01 through N-09 class of defect cannot
slip through again.

## Where this fits

Read [the master index](./00-index.md) for the verified hardware and software baseline, then
[the audit](./01-audit.md) for the issue list this chapter refers to.
