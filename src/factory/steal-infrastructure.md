# Upstream Harvesting — Infrastructure for Borrowing Instead of Rebuilding

Every time the fleet needed a capability, someone wrote it from scratch, and the result was
usually a thinner version of something that already existed in a mature project. This chapter
documents the infrastructure that inverts that reflex: one registry of tracked upstreams, one tool
to extract useful work from them, and one tool to adapt it to this machine.

## Summary

- `manifests/upstreams.toml` is the single registry of tracked upstreams, each annotated with what
  to take, how to improve it, and its conflict risk.
- Three tools under `tools/steal/` list the registry, extract features and issues, and apply an
  adapted patch.
- The rule is to look for existing work first and build only when nothing suitable exists —
  and to discard in-house code when something better appears.
- Integration is bounded by hard process, policy, and filesystem boundaries, so borrowing broadly
  does not create conflicts.
- The desktop look is fixed. Backend capability is borrowed; appearance is not replaced.

> **Directive —** The job is not merely to fork and wrap. Upgrade the wrapper for this system's
> needs, customize and specialize it for CachyOS, Hyprland, and a 6 GB VRAM budget, and improve it.
> Build proper working versions rather than minimal ones that decay into stubs. There is no time
> pressure, so there is no excuse for a stub.

## Why an inventory beats improvisation

A machine shop does not fabricate a bolt when a bolt of the right thread is on the shelf. It keeps
a parts inventory precisely so that the question "do we already have this?" is cheap to answer.
Without the inventory, fabricating is easier than searching, and the shop slowly fills with
one-off parts that nobody can maintain.

The registry is that inventory. It makes searching cheaper than building, and it records the answer
so the search happens once rather than in every session.

## The registry: manifests/upstreams.toml

The registry tracks more than 20 upstreams, grouped by what they contribute.

| Group | Upstreams | Contribution |
|---|---|---|
| Base look | `end-4/dots-hyprland` (illogical-impulse) | The appearance, which is kept as-is; only the backend improves |
| Dotfiles to learn from | ML4W, `JaKooLit/Hyprland-Dots`, HyDE, CachyOS Noctalia, Caelestia-shell, DankMaterialShell, `ekremx25/quickshell`, qs-hyprview, HyprPanel, rishot | Features, fixes, and interaction patterns |
| MCP servers, open source and key-free | filesystem, git, fetch, sequential-thinking, memory, playwright, DuckDuckGo, Obsidian, Chrome DevTools, SearXNG (AGPL-3.0, self-hosted, 70-plus engines), agent-search | Tooling with no API key and no subscription |
| Rust systems libraries | `notify-rs/notify` (3.3k stars), `aya-rs/aya` (4.7k stars) | Filesystem notification and pure-Rust eBPF |

Tavily was evaluated and rejected: it is closed source, priced at $0.005 per query, requires an API
key, and depends on a hosted service. The requirement is open source and genuinely free, so
`agent-search` — permissively licensed and bundling SearXNG behind a single command — took its
place.

Each entry states its intent explicitly rather than leaving it to interpretation.

```toml
[upstream.ekremx25-quickshell]
repo = "ekremx25/quickshell"
provides = ["modular-bar", "dock", "material-you", "eq-10-band"]
steal = ["bar_config.json declarative pattern", "single hyprctl --batch monitor management", "Night Light 1000-6500K"]
improve = "Upgrade the wrapper: flicker-free monitor management at 1920x1200@144, better network and Bluetooth integration"
conflict_risk = "low-medium"
```

> **Note —** Upstreams keep their own licenses. `scripts/check_licenses.py` refuses combinations
> incompatible with the fleet's GPL-3.0-or-later licensing, and the gate runs in CI.

## The tools

Four commands cover the whole cycle, from noticing that an upstream moved to landing an adapted
change.

`scripts/upstream_tracker.py` reads the upstreams declared in `manifests/components.toml`, queries
each for its latest release or tag and its open issue count, writes
`channels/upstream-status.json`, and prints a human summary. It powers the weekly check: when an
upstream advances past the current pin, open a rebase pull request on the fork, run the fork's
tests, and promote only if they pass.

`tools/steal/upstream_registry.py` lists everything in the registry with its conflict risk, what to
take, and how to improve it.

```bash
python tools/steal/upstream_registry.py --list
python tools/steal/upstream_registry.py --report
```

`tools/steal/feature_extractor.py` reads recent commits, open issues, and pull requests from a
tracked upstream and filters them against a keyword list — animation, blur, performance,
bluetooth, wifi, network, smooth, buttery, response, eq, monitor, hdr, vrr, night light, wallpaper,
screenshot, dock, bar, material you, matugen, hyprpaper, swww.

```bash
python tools/steal/feature_extractor.py --upstream ekremx25-quickshell --all --out /tmp/features.json
```

Against `ekremx25/quickshell`, for example, it surfaces flicker-free monitor management via a
single `hyprctl --batch` call, a blue-light Night Light filter, a 10-band equalizer, network and
Bluetooth connection managers, and a matugen-driven wallpaper picker — all backend work that drops
into the existing look rather than replacing it.

`tools/steal/patch_applier.py` performs the adaptation in seven steps: branch as
`feat/upstream-<name>-<sha>`; copy or adapt the relevant file; customize for this hardware
(1920x1200 at 144 Hz, RTX 4050 with 6 GB, 16 GB DDR5, CachyOS performance settings, and the
illogical-impulse look preserved); specialize with a Guard policy, its own systemd service, its own
configuration directory, a btrfs subvolume, and a Python virtual environment; improve it with the
ambient offer overlay, power profile, GPU MUX and backup status, and VRAM-budget awareness; test
with `make check` and the component suite; and commit with attribution.

```bash
python tools/steal/patch_applier.py --feature /tmp/features.json \
  --upstream ekremx25-quickshell --index 0 --dry-run
python scripts/upstream_tracker.py --out channels/upstream-status.json
```

## Being enterprising without creating conflicts

Borrowing from a dozen projects only stays safe if the boundaries between them are structural
rather than conventional. Nine boundaries do that work.

| Boundary | Rule |
|---|---|
| One job per component | `shesh-files` watches Downloads, Desktop, Documents, and Pictures, and never touches `Projects/`, `Vaults/`, `Documents/Job`, or `.ssh`; enforced by `safety.sh` |
| One process per MCP server | Each `shesh-*-mcp` speaks stdio in its own systemd user service, never shared |
| One policy gate | Every tool call passes Guard `check(actor, tool, args)` and is allowed, confirmed, or denied — then logged as a kernel event |
| Separate configuration | `~/.config/shesh/mcp/` per server, `~/.config/shesh/messaging/` for flags, `~/.local/share/shesh/` for state, `~/.cache/shesh/` for cache |
| Separate btrfs subvolumes | `AI/Models` nocow, `Downloads` transient, `Documents/Personal` snapshotted hourly, `Documents/Job` not snapshotted per employer policy |
| Namespaced tools | Prefixes `fs_*`, `fetch_*`, `git_*` via the `shesh-mcp-bundle` proxy, so names cannot collide |
| Version pins and license gate | `manifests/components.toml` plus `scripts/check_licenses.py` |
| Test before push | `make check` runs ruff, pytest, the license gate, and lock resolution; autopilot refuses a red commit |
| Thin overrides | Keep `custom/` overrides in `shesh-desktop` thin against the end-4 base, rebase often, and add capability without diverging `dots/` |

The Quickshell-plus-Go pattern taken from DankMaterialShell and `ekremx25/quickshell` follows the
same discipline: a shell framework alongside a Go daemon for system monitoring, sharing QML widgets
through `dank-qml-common`, as separate processes communicating over IPC rather than shared memory.

## Proper implementations, not placeholders

Three components were built as minimal wrappers and then stalled there, which is the failure mode
the rule now forbids.

| Component | The stub | What proper means |
|---|---|---|
| `shesh-brain` | A wrapper routing through Guard, a stub scheduler, two tests | A real task router that routes on policy, a scheduler that budgets through the SheshAOS RPC or `systemd-run`, and a tool broker using the Guard and kernel bridge — with tests that verify routing rather than asserting a substring |
| `shesh-media` | Stub file creation around grim and slurp, a stub `wpctl` call | Actual `grim -g $(slurp)` region capture, `wf-recorder` with `pactl` audio, `swaybg` or `hyprpaper` with matugen palette extraction, real sink parsing — with tests that check the file exists and is non-empty |
| `shesh-messaging` | An opt-in flag file and a stub send function | Real Telegram Bot API calls with a token from `shesh-secrets`, `signal-cli` via subprocess, isolation in a systemd user service, an opt-in flag, and tests that mock the API |

> **Rule —** Recorded in `TODO.md` and `SESSION_HANDOFF.md`: do not create minimal stubs that
> become dead code. Build working implementations with tests, integration, and documentation. When
> facing a problem, first check `SOURCES.md`, `TOOLING_CATALOG.md`, `upstreams.toml`, and the
> Hyprland and MCP ecosystems for something to adapt. Build only when nothing suitable exists, and
> discard in-house code when something better appears.

## Style and performance are not negotiable

The owner's requirement is specific: the look comes from illogical-impulse — end-4's dotfiles, with
Material You theming, Quickshell widgets, anti-flashbang handling, screen translation, clipboard
IPC, keybindings, and Lua configuration — and the performance comes from CachyOS 260628, with the
BORE scheduler, LTO, PGO, BOLT, x86-64-v3 and v4 targets, and Zen 4 tuning.

Neither may be compromised. DankMaterialShell, `ekremx25/quickshell`, HyprPanel, and ashell are
sources of backend logic, not replacements for the shell, because adopting their appearance would
break the look the owner already chose.

What does get adopted is capability: the springy pill-bar morphing from `Gakuseei/Ricelin`
(`Singletons/Motion.qml`, `morphCurve [0.16,1,0.3,1,1,1]`), the pure-Wayland screenshot tool rishot
(`qs -c rishot`), `swww` live wallpaper switching with GIF support alongside `hyprpaper`,
flicker-free monitor management through a single `hyprctl --batch` call from `ekremx25`, per-monitor
refresh scripts from JaKooLit, a reliable Bluetooth menu, a Night Light slider from 1000 to 6500 K
with a fixed-time schedule, and a 10-band PipeWire filter-chain equalizer.

The backend that integrates into that look is the fleet itself: `shesh-files`, `shesh-shell`,
`shesh-system`, `shesh-audit`, the `shesh-voice` overlay, the `shesh-ambient` catch-up scheduler,
`shesh-control` for AT-SPI and Wayland input injection, `shesh-browser` with a sandboxed profile,
`shesh-containers`, `shesh-ebpf` on Aya, `shesh-media`, `shesh-messaging`, and the optional
`shesh-omniroute` gateway. See the [desktop overview](../desktop/overview.md).

## Distance to a first release

The roadmap in the desktop repository runs through phases zero to seven; the estimate below is as
recorded there.

| Milestone | Estimate |
|---|---|
| Before installing CachyOS | Phase 0 pre-install fixes — 16 tasks over one or two sessions, covering the N-01 through N-10 regressions plus the MSI DMI content check and the zram configuration item; without them `./setup install` crashes |
| Shippable, fast and presentable | Phases 0 through 3, roughly the first week |
| Organizer v2 and automations | Phases 4 and 5, roughly the second week |
| Voice agent | Phase 6, weeks three and four |
| First release overall | About three to four weeks with the owner and an assistant, provided backend patterns are adapted rather than rebuilt and the look is left intact |

The honest status split is worth keeping. Mind and Brain are on track — more than 100 tests, 19
decision records, model-agnostic free-first routing, a swarm with atomic locks, auto-merge and an
hourly janitor, and a password-protected credential flow. Soma and Desktop went off track by
rebuilding what should have been adapted, which introduced 10 new bugs and made progress look
further along than it was because stub files existed. The correction is the subject of this
chapter: keep the look, adapt the backend, and lint every script in CI.

## Where this fits

[Fork gardening](../policies/fork-gardening.md) describes how pinned forks are kept current, the
[tooling catalog](../audits/tooling-catalog.md) records what is already adopted, and the
[desktop roadmap](../desktop/02-roadmap.md) holds the phase detail summarized above. Repository
boundaries are defined in [repo topology](../product/architecture/repo-topology.md).
