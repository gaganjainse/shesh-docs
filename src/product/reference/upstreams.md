# Sources and Steal-Map

> **History —** This chapter is a research and planning log from 2026-08-09 (first-wave deep
> research) and 2026-08-11 (second-wave intake). It records what the fleet chose to absorb,
> from where, under what license, and which part of the Agentic Body it feeds. Treat it as
> provenance for past decisions, not as live operating instructions.

The fleet grows by adopting, adapting, and wrapping open-source work with attribution — never by
violating a license. Every upstream is forked, wrapped as a `shesh-*` component, pinned in the
manifest, and then upgraded and specialized for the CachyOS/Hyprland machine and its 6 GB VRAM
budget. Because many different systems integrate at once, the design avoids conflict by
namespacing through MCP stdio process boundaries, a Guard policy of allow/confirm/deny, separate
systemd services, and no in-process foreign-function calls.

Only open-source software qualifies: MIT, Apache-2.0, or GPL-3.0; truly free; no API key; no
subscription; self-hostable and offline-first. Online-led, per-query search services such as
Tavily are excluded. Self-hosted alternatives such as SearXNG and agent-search stand in for them.

Legend: **MIND** / **BRAIN** / **SOMA** mark the body layer; "first-wave" means adopt now,
"later" means track or reference.

---

## A. The user-facing agent and mind

### Newelle (qwersyk) — GPL-3.0 — first-wave — → `shesh-voice`
Frontend, voice, wake word, and MCP client. Already the primary mind shell.
- **Adopt:** wake word (1.3.0+), STT via faster-whisper, TTS (Kokoro/Piper/Edge), MCP client
  (stdio + http; 1.4.5 supports STDIO on native), subagents (1.3.5), skills, scheduled tasks,
  file permissions, chat folders and branching, OpenAI-compatible local API (1.4.0), Telegram
  interface.
- **Watch for:** better MCP tool lazy-loading and per-profile models.
- **Our fork (`shesh/` branch):** strip GNOME-only assumptions, add the Hyprland Quickshell
  overlay, prewire our MCP servers, set 6 GB-safe model defaults, and rename in the about-screen
  to "Shesh (Newelle core)".
- **Do not take:** the Flatpak manifest (use native AUR) and cloud provider defaults.

### Goose (block/goose) — Apache-2.0 — later — reference for `shesh-mind`
Model-agnostic agent with 70+ MCP extensions, CLI and desktop. Mine it for MCP extension
registry patterns, the desktop-plus-CLI shape, and provider abstraction. It does not replace
Newelle.

### Hermes Agent (NousResearch) — MIT — later — reference for skills/cron/gateway
Self-improving agent with skill creation, cron automations, and a multi-platform gateway. Adopt
the skill format, scheduled automations, and gateway pattern. Its companion `computer-use-linux`
(Apache-2.0) is the blueprint for deeper Soma control.

### Open Interpreter — AGPL-3.0 — later — patterns only
AGPL is incompatible with linking into the GPL-3 desktop unless kept as a separate process or
service. Use its approval-prompt and code-execution sandboxing patterns; do not vendor code.

### pi (earendil-works) — MIT — later — reference
The agent-loop harness under Prime Agent. Adopt its supply-chain hardening (lockfile as ground
truth, lifecycle allowlist) and clean agent-loop and state design. Read-only inspiration.

### Prime Agent / RLM Harness (PrimeIntellect) — MIT — later — reference
"Continual Harness": a supplemental prompt and skill store refined with evidence without
mutating the base system prompt. This is exactly how Shesh should learn safely. Implement it in
`shesh-mind`.

---

## B. Brain and governance (our own lineage)

### SheshAOS (our own) — MIT — first-wave — → `shesh-brain`
The kernel: event store, policy engine, scheduler, router, tool broker, and RPC. Already 981
tests.
- **Adopt from ourselves:** `shesh-kernel`, `shesh-rpc`, `shesh-ai` provider abstraction,
  `shesh-terminal`, resource budgets, append-only audit, and manifest lifecycle.
- **Adapt:** target CachyOS/Hyprland instead of Ubuntu/GNOME; make policy gate MCP tool calls;
  expose the event log as `shesh-audit`.
- **Branches to study:** `bolt-optimize-raf-loop` (UI performance),
  `palette-ux-theme-switcher-a11y` (accessibility and theming), `recovery/phase-1` (resilience).

### shesh-kernel (our own) — MIT — later — research track
An alpha microkernel. Adopt its architecture ADRs (vte over Zig FFI, JSON-RPC id fix, resource
budgets, policy-decision events, wgpu terminal) as desktop-app lessons for a Quickshell or
terminal Shesh UI. Keep it as research, not the daily driver.

### SheshOS (our own) — MIT — later — `shesh-mind` spec
> **Note —** `gaganjainse/SheshOS` is **conceptual and unpublished**, not a live, reachable
> upstream. Treat it as a design specification for specialist model routing, not as cloneable
> code.
Its router logic maps three large models to small, 6 GB-safe equivalents — `phi4-mini`,
`qwen2.5-coder:3b`, and `moondream2` — while keeping the same interface so bigger models drop in
later.

### llm-eval-harness (our own) — MIT — later — `shesh-mind` reflection
An LLM-as-judge golden-set eval. Use it to grade specialists and gate mind changes.

---

## C. Soma — desktop shell and looks

### end-4/dots-hyprland — GPL-3.0 — first-wave — base of `shesh-desktop`
Our shell base. Adopt the Lua config (Hyprland 0.55+), Quickshell `ii` widgets, Material
You/matugen, the AI sidebar (Ollama/Gemini), anti-flashbang, screen translate, clipboard IPC,
and keybinds.
- **Upstream strategy:** keep `custom/` overrides thin and rebase often; add our MCP and
  automations without diverging `dots/`.
- **Watch:** their Quickshell and Lua migrations; their AI sidebar can host our overlay.

### ML4W 2.14.1 — GPL-3.0 — later — `statusbar.json` pattern
A single-file Quickshell bar config. Adopt the declarative bar pattern and, optionally, the
welcome-app concept. Do not take the GUI configurator.

### JaKooLit/Hyprland-Dots — (GPL-ish; verify) — later — robustness patterns
Distro guards, per-monitor refresh scripts, SDDM sugar-candy, and a reliable Bluetooth menu.
Borrow logic only; keep end-4 visuals.

### prasanthrangan/hyprdots (HyDE) — GPL-ish — later — theming
Wallbash (one wallpaper themes all apps), themepatcher, and `hyde-cli` modularity. We already use
matugen; consider Wallbash for apps matugen does not cover.

### CachyOS Noctalia shell — (CachyOS) — later — animation and performance ideas
Now a Hyprland option on the 260628 ISO. Compare animation curves and NVIDIA compositing hints;
do not switch shells.

### Caelestia-shell — Qt6/Quickshell — later — animation curves
Copy easing and blur parameters (QML, no dependency change) for 144 Hz smoothness.

---

## D. Soma — file and automation organs

### Our own smart-organizer (in shesh-desktop) — first-wave — → `shesh-files`
A Rust `notify` watcher plus a Python classifier and MCP. Promote it to its own repository and
add:
- **Adopt from `waku-agent`** (MIT): a single-afternoon agent harness shape (loop, memory,
  eval) as the structural model for `shesh-files`'s agent mode, not as a dependency.
- **Adopt from OpenAdapt** (MIT): record-and-replay demonstration for automations.
- Trash via `gio trash`; an undo log; and a SQLite history (already specced).

### system-aidai/openclaw family (MIT if used) — later — gateway ideas
Personal agent servers (moltis/clawdbot): a single Rust binary, sandboxed, multi-LLM, voice, and
Telegram. Reference for packaging Shesh as one binary later.

### Leon (leon-ai/leon) — MIT — later — skills architecture
A 17.4k-star open personal assistant in Python and Node with skills and memory layers. Older but
clean; mine its skill packaging and i18n.

### pipecat-ai/pipecat — BSD-2 — later — real-time voice pipeline
A 13.9k-star framework for voice and multimodal conversational pipelines. Use it if we outgrow
Newelle's voice pipeline (interruption, barge-in, low latency).

### openWakeWord (dscripka) — Apache-2.0 — later
A fallback if Newelle's wake word is insufficient; train a custom "Hey Shesh" model.

---

## E. Soma — computer and device control

### computer-use-linux (avifenesh) — Apache-2.0 — later
An AT-SPI accessibility tree plus Wayland input injection, screenshots, and compositor window
targeting. This is the missing "eyes and hands" for Shesh on Hyprland beyond `hyprctl`. Evaluate
maturity; wrap it as a `shesh-control` MCP server behind brain policy, where destructive actions
require approval.

### OS-Copilot (Ubuntu) — Apache-2.0 — later
A Linux-oriented shell-and-screenshot agent; a good reference for Linux-first control.

### browser-use — MIT — later
Drives a real browser for web tasks. Wrap it as `shesh-browser` MCP and run it in a separate
sandboxed profile.

### phone-harness concept (ShawnPana) — MIT — first-wave — → `shesh-phone`
macOS-only upstream; we port the OCR-to-coordinate-to-act loop to **ADB on the Realme Narzo 90x**,
using `moondream2` vision instead of OCR and direct coordinates via `adb shell input`.

---

## F. Mind — memory and knowledge

### Khoj — AGPL-3.0 — later — patterns only (or a separate service)
A self-hosted second brain over docs, Obsidian, and Emacs. AGPL means run it as a **separate
service** the brain talks to, never link it. We prefer our own `rag-service` (MIT), which is
license-clean.

### AnythingLLM / Jan / GPT4All — MIT/Apache — later
Reference UIs and local model management; not direct dependencies.

---

## G. Build-your-own and learning track (build-your-own-x, MIT)

Use the test-driven, increment-by-increment tutorials for the `shesh-kernel` research track:
build-a-shell, build-a-database, build-an-interpreter, build-a-docker. Not production code — a
learning scaffold so the AI-first kernel vision stays grounded rather than fanciful.

---

## H. Dotfile and rice leaderboard signals (star-history / trendshift)

Fastest-moving in 2026: Newelle (voice/MCP), Hermes/pi/Prime (agents), and end-4/Noctalia/Caelestia
(Quickshell shells). The signal is clear — **Quickshell + MCP + local voice** is the winning
combination, and it is exactly our stack. We are surfing the wave, not fighting it.

---

## I. License compatibility for our GPL-3 body

| License | Vendored into GPL-3 code? | Notes |
|---|---|---|
| MIT / BSD-2 / Apache-2.0 | Yes, with attribution and NOTICE | bulk of the ecosystem |
| LGPL | Dynamic linking only | Quickshell |
| GPL-3 | Same license | Newelle, end-4, HyDE |
| AGPL-3.0 | Separate service only | Open Interpreter, Khoj — never link |
| Elastic / SSPL / source-available | No | Suna and similar — skip |

We maintain `NOTICES.md` and a per-component `LICENSE` in each `shesh-*` repository. The manifest
gate (`scripts/check-licenses.py`) refuses incompatible licenses.

---

## J. First-wave intake (done 2026-08-09)

1. **Fork and track:** Newelle and end-4/dots-hyprland — Done; now `shesh-voice` (41M) and
   `shesh-desktop` (22M).
2. **Promote from shesh-desktop:** `shesh-files`, `shesh-shell`, `shesh-system`, and the
   `shesh-voice` Newelle wrapper config — Done.
3. **Bridge:** `shesh-audit` to the SheshAOS event store — Done via KernelBridge.
4. **Reference-only (read, do not vendor yet):** Goose, Hermes, pi, Prime, computer-use-linux,
   pipecat, Leon — Done; cataloged in TOOLING_CATALOG.
5. **Weekly upstream-tracker bot** (`scripts/upstream-tracker.py`) — Done.

## K. Second-wave intake — 2026-08-11 deep research

> **History —** The user directed: Tavily is not completely free but subscription-based; do not
> use online-led tools, only open-source ones. Our job is not merely to fork and wrap, but to
> upgrade the wrapper for our needs, customize and specialize it for our system, and improve it.
> We integrate many different systems, but there must be no conflict — cautious but enterprising.

From web search on 2026-08-11 (awesome-hyprland, best MCP servers 2026, CachyOS June 2026, Rust
eBPF, file watcher).

### K.1 Desktop shells — Quickshell ecosystem
Steal, upgrade, and specialize for 1920x1200 at 144 Hz with an RTX 4050 and 6 GB VRAM.
- **DankMaterialShell** (AvengeMedia/DankMaterialShell) — MIT, Quickshell + Go, a complete
  Wayland desktop shell optimized for Hyprland/Niri/Sway/MangoWC; replaces waybar, swaylock,
  swayidle, mako, fuzzel, and polkit. Provides dankcalendar (local/Google/Microsoft/CalDAV), a
  dgop system-monitoring TUI, dank-qml-common shared QML, and dankgo common Go modules.
  **Adopt:** calendar integration, the system-monitoring TUI library, and shared QML widgets;
  upgrade the wrapper for our MSI with power-profile, GPU MUX, and backup-status widgets, and
  specialize for the 6 GB VRAM budget.
- **ekremx25/quickshell** — MIT, a modern feature-rich Wayland shell with a modular bar, dock,
  Material You theming, event-driven design, a 10-band EQ, multi-monitor, HDR/VRR/10-bit,
  night light via hyprsunset/gammastep, OSD volume/brightness, an app drawer with fuzzy search,
  a wallpaper picker with matugen, a lock screen, mouse/keyboard sensitivity, and
  network/bluetooth/VPN managers. **Adopt:** the `bar_config.json` declarative pattern, dock
  drag-and-drop pinning, single `hyprctl --batch` monitor management (no flicker), a night-light
  1000-6500K slider with a fixed-time schedule that wraps at midnight, and an EQ filter-chain
  rather than a rebuild.
- **qs-hyprview** (dom0/qs-hyprview) — MIT, a native, highly customizable Quickshell window
  switcher and Expose for Hyprland with nine mathematical layout algorithms and zero-latency
  smooth animations. **Adopt:** the nine layout algorithms for an overview, upgraded for 144 Hz
  smoothness and specialized for Hyprland workspace overview.
- **awesome-hyprland list:** `hyprpaper` (wallpaper daemon with IPC), `hyprpicker` (colorpicker),
  launchers (`rofi`/`tofi`/`bemenu`/`wofi`/`fuzzel`/`yofi`), `swww` (wallpaper daemon with live
  switching and GIF support), `ironbar` (Rust bar), `HyprPanel` (TypeScript bar/panel with
  context menus), `ashell` (Rust ready-to-go bar), `ignis` (Python GTK4 widget framework).
  **Adopt:** `swww` live switching with GIF for wallpaper (better than hyprpaper), the
  `HyprPanel` context-menu pattern, and `ashell` as a reference bar — upgrade the wrapper with a
  Shesh ambient-offer overlay, not just a bar.

### K.2 MCP servers — truly free, open-source, no API key, no subscription
From Best Free MCP Servers 2026 (designrevision.com, 2026-07-30): truly free, keyless,
accountless, open-source reference servers from `@modelcontextprotocol`.
- **Filesystem** — sandboxed local file read/write — truly free, no key — MIT — already packaged
  in `shesh-mcp-bundle`; upgrade the wrapper with scoped allowed dirs (`~/Projects/personal`,
  `~/Documents/Inbox`), and Guard-deny `~/Documents/Job` and `~/.ssh`.
- **Git** — repository operations on a local repo — truly free — MIT — already packaged; upgrade
  with a read-only `git_view` and `github_view` via `shesh-secrets` scoped PAT.
- **Fetch** — fetch a URL and return clean markdown — truly free — MIT — already packaged; upgrade
  with a `Shesh/1.0` user-agent, a timeout, and a content-size limit.
- **Sequential Thinking** — structured step-by-step reasoning — truly free — MIT — package next.
- **Memory** — a persistent knowledge graph — truly free — MIT — we have `shesh-memory`
  hierarchical memory, but can adopt the knowledge-graph pattern.
- **Playwright** — drives a real local browser — truly free — MIT — package next
  (`npx @playwright/mcp@latest`), sandboxed, no key.
- **DuckDuckGo** — privacy-first web search — truly free, no key — from `shesh-skills` keyless
  DDG HTML, now a formal `duckduckgo-mcp` server; upgrade with rate limiting and result
  deduplication.
- **GitHub** — repos, issues, PRs — free with an account, needs a PAT token — we have
  `shesh-secrets` multi-backend, so it is acceptable.
- **Obsidian** — read/write Obsidian vaults — fully free, no key — MIT — package for the Notes
  vault `~/Notes/` (Obsidian/logseq).
- **Chrome DevTools MCP** — browser devtools — fully free — open-source.

**Discarded per user request (online-led, subscription, not open-source):**
- **Tavily MCP** — closed-source, about $0.005 per query, needs an API key, online-led,
  subscription — **discarded**; replaced with self-hosted open alternatives below.
- **Brave Search MCP** — needs an API key, about $5 per 1k queries, not fully free —
  **discarded** unless the user explicitly opts in with a key via `shesh-secrets`.
- **Perplexity MCP** — needs an API key, subscription — **discarded**.

**Open-source, self-hosted search alternatives to Tavily (free, no keys, self-hostable,
offline-first):**
- **SearXNG** — AGPL-3.0, a self-hosted metasearch over 70+ engines, no key, fully private, no
  monthly fees, no vendor lock-in — `docker compose up`; aggregates 70+ sources on
  `localhost:3939`.
- **agent-search** (brcrusoe72/agent-search) — MIT, a self-hosted search API and MCP server for
  AI agents that bundles SearXNG, zero API keys, one-command deploy, 17 endpoints, layered
  content extraction with optional browser rendering, cross-engine deduplication, prompt-injection
  scrubbing, adaptive failure analysis (evolver), and an optional Tor-anonymized stack — an
  open-source alternative to Tavily, Exa, and Serper.
- **fastCRW** — AGPL-3.0, Rust with bundled SearXNG, Tavily-style endpoints, an adapter shim, and
  an MCP server (`crw_search`, `crw_scrape`, `crw_crawl`, `crw_map`); a Rust runtime about 8 MB
  with low idle RAM.
- **OrioSearch** — MIT, Python FastAPI + SearXNG + Redis, an explicit Tavily drop-in.
- **TrailSearch / tavily-open** (jianjungki/tavily-open) — MIT, powered by SearXNG and Crawl4AI,
  a self-hosted web search, crawl, and content-extraction API with a low-cost search router that
  checks local SQLite FTS first, then SearXNG, and calls Brave only when explicitly enabled.

**Steal and upgrade:** package `agent-search` as a `shesh-search` component — MIT, zero keys,
one command, an MCP server for Claude Desktop/Cursor, with a Tor option. It beats Tavily because
it is free forever, private, and keyless. Upgrade the wrapper with a Guard policy (allow search,
deny exfiltration of protected paths), a cache at `~/.cache/shesh/search/`, and result ranking via
RRF.

### K.3 Rust eBPF and observability — Aya and friends
From search: **aya-rs/aya** (4.7k stars) is a pure-Rust eBPF library focused on developer
experience and operability, with no libbpf dependency, fast builds, BTF portability, and
tokio/async-std support.
- **Top Rust eBPF projects:** `aya` (4.7k), `oryx` (2.5k, TUI network sniffing), `rbpf` (1.1k,
  Rust VM JIT), `kunai` (1k, threat hunting), `pulsar` (1k, modular runtime security for IoT),
  `libbpf-rs` (998, minimal opinionated tooling), `tracexec` (436, an execve/at tracer),
  `aya-template` (cargo-generate template).
- **Observability:** `vector` (22.2k), `greptimedb` (6.5k, an Observability 2.0 database for
  metrics/logs/traces), `autometrics-rs` (834, easy metrics), `weaver` (450, OTel Weaver semantic
  conventions).

**Steal:** use `aya` and `aya-template` (`cargo generate --name demo -d program_type=xdp
https://github.com/aya-rs/aya-template`) for execve/openat/tcp-retransmit tracers. We stubbed
this in `shesh-ebpf` with a `/proc` fallback; upgrade to real Aya programs for execve, openat, and
tcp_retransmit_skb via `BPF_MAP_TYPE_PERF_EVENT_ARRAY`, read-only, behind the Guard
allow/confirm/deny. P2 is a minimal done state; real Rust comes later.

### K.4 File watcher — notify-rs
- **notify-rs/notify** (3.3k stars) is a cross-platform filesystem-notification library in Rust,
  used by Alacritty, cargo watch, mdBook, and Zed, across Linux inotify, macOS FSEvents,
  Windows ReadDirectoryChangesW, FreeBSD kqueue, and more. **Steal:** replace our custom
  watcher-rs with the `notify` RecommendedWatcher, which selects the best backend automatically.
  We already did this in `shesh-files`, but the audit found that smart-organizer `--watch` is a
  polling loop, not inotify, and wastes I/O — ensure we use the `notify` crate, not a custom
  polling loop.
- **Other Rust file managers:** `yazi` is a blazing-fast terminal file manager with async I/O, a
  client-server architecture, a Lua pub-sub, and a plugin/theme package manager. **Steal:** async
  task scheduling, real-time progress, and the package-manager pattern for `shesh-files`.

### K.5 CachyOS June and August 2026 — performance
From search: CachyOS June 2026 ships Python PGO, a GCC patch, and an OpenBLAS fix, plus the
CachyOS Hyprland Noctalia desktop option, a GNOME Resources app, and Welcome-app improvements.
August 2026 ships Linux 6.18 LTS and 7.1, KDE Plasma 6.7.4, an improved installer, and the
Noctalia greeter login screen instead of SDDM, with the BORE scheduler, LTO, PGO, BOLT, and
x86-64-v3/v4 and Zen4 gaming meta.
**Steal:** Noctalia animation curves and NVIDIA compositing hints, a BORE-versus-EEVDF scheduler
comparison, and `cachyos-rate-mirrors` plus `cachyos-gaming-meta` — already in CachyOS, so we do
not rebuild.

### K.6 Computer-use agents
- **Best open-source AI computer-use agents 2026:** `Fazm` (MIT, Claude/GPT-4o/Ollama + the
  Accessibility API + vision on macOS), `Browser Use` (MIT, 52k stars, any LangChain model with
  DOM + vision, cross-platform), `Open Interpreter` (AGPL-3.0), `UI-TARS` (Apache-2.0, a
  custom fine-tuned screenshot-native model), `OS-Copilot` (Apache-2.0, shell + screenshot on
  Linux/macOS), `OpenAdapt` (MIT, screenshot + recording), `Skyvern` (AGPL-3.0).
- **Our gap:** `computer-use-linux` (Apache-2.0) provides an AT-SPI tree, Wayland input
  injection, screenshots, and compositor window targeting — the missing eyes and hands for Shesh
  beyond `hyprctl` — so we need a `shesh-control` MCP behind policy.

## L. Avoiding conflict while staying enterprising

> **History —** The user directed: integrate many different systems, but there must be no conflict
> between them. We must be cautious but enterprising.

**Design we already have (LANGUAGE_POLICY.md):**
- Five languages only: Rust, Python, Lua, QML/JS, and Bash — no Zig, C, Mojo, or Go. This
  minimizes foreign-function calls; cross-language talk happens over MCP/JSON between processes,
  never through in-process links.
- Exotic runtimes go in rootless Podman or Distrobox, not on the host — reproducible environments
  with no host pollution.
- Federated component repositories plus manifest and locks, not a monorepo — each component is
  independently versioned and tested.
- MCP over stdio process boundaries — one job per component, one process per MCP server, one
  policy gate — so integrations do not clash.
- A Guard policy of allow/confirm/deny, plus a hash-chained audit and protected-path denials.

**New from second-wave research:**
- **Quickshell + Go** (DankMaterialShell, ekremx25) shows how to avoid conflict: a shell framework
  (outfoxxed/quickshell) plus a Go daemon for system monitoring, with shared QML widgets via
  `dank-qml-common` — separate processes where QML widgets communicate over IPC, not shared memory.
  Adopt the same split: a Go daemon for system, QML for UI, and MCP for tools, all separate.
- **HyprPanel / ashell / qs-hyprview** are each a standalone drop-in replacement with no heavy
  Python background processes; logic lives entirely in QML/JS. Keep our shell as a standalone
  drop-in that does not modify Hyprland core, so it does not conflict with Noctalia (a CachyOS
  option); the user can switch shells via `hyprland.conf` `exec-once`.
- **Aya eBPF** is pure Rust with no C toolchain and BTF portability; eBPF programs run inside the
  kernel, not in userspace, so they do not conflict with userspace MCP servers — a separate
  domain.

**Cautious-but-enterprising checklist:**
- [ ] One job per component — `shesh-files` watches only Downloads/Desktop/Documents/Pictures,
  never Projects/, Vaults/, Documents/Job, or `.ssh`.
- [ ] One process per MCP server — `shesh-audit-mcp`, `shesh-system-mcp`, and so on, each stdio,
  not shared.
- [ ] One policy gate — every tool call passes `Guard.check(actor, tool, args)` returning
  allow/confirm/deny, then is logged and emitted as a kernel event.
- [ ] Separate config dirs — `~/.config/shesh/mcp/` per server, `~/.config/shesh/messaging/`
  flags, `~/.local/share/shesh/` state, `~/.cache/shesh/` cache.
- [ ] Separate btrfs subvolumes — `AI/Models` nocow, `Downloads` transient,
  `Documents/Personal` snapshotted hourly, `Documents/Job` not snapshotted per employer policy.
- [ ] Namespace via MCP — tool names prefixed `fs_*`, `fetch_*`, `git_*` through the
  `shesh-mcp-bundle` proxy, so nothing collides.
- [ ] Version pin plus license gate — `manifests/components.toml` and
  `scripts/check_licenses.py` refuse incompatible licenses (AGPL/SSPL only as separate services).
- [ ] Test before push — `make check` runs ruff, pytest, license, and lock checks; autopilot
  refuses red commits.

## M. Discard what we made if something better exists

> **History —** The user directed: we can discard what we made if something better exists to
> steal, and we should never engage in pointless brooding.

- **Discard custom power/GPU logic** — steal the night-light backend `hyprsunset`/`gammastep`,
  the EQ filter-chain, and monitor management via `hyprctl --batch` from `ekremx25/quickshell`
  instead of rebuilding.
- **Discard a custom bar/panel** — steal the `HyprPanel` context-menu pattern, the `ashell`
  ready-to-go bar, and the `qs-hyprview` nine layout algorithms for overview.
- **Discard a custom file-watcher polling loop** — the audit found that smart-organizer `--watch`
  is a polling loop, not inotify, and wastes I/O — replace it with `notify-rs/notify`
  RecommendedWatcher.
- **Discard a custom web-search/fetch DDG HTML scraper** — package `agent-search` (MIT,
  self-hosted SearXNG, zero keys), the truly free, keyless DuckDuckGo MCP, and self-hosted
  SearXNG metasearch over 70+ engines.
- **Keep only Shesh-specific organs** — `shesh-audit` (hash-chained), `shesh-brain` (packaged
  kernel), `shesh-mind` (6 GB VRAM router), `shesh-memory` (hierarchical plus habit learning),
  `shesh-harness` (continual harness plus `/refine`), `shesh-orchestrator` (RLM plus A2A UDS plus
  sessions), and `shesh-ambient` (catch-up scheduler plus warm proactivity).
- **Package, do not rebuild** — mature MCP servers: Filesystem, Git, Fetch, Sequential Thinking,
  Memory, Playwright, Context7, DuckDuckGo, Obsidian, and Chrome DevTools — all truly free, no
  key, MIT/Apache-2.0, open-source reference servers from the Model Context Protocol project.

## N. First-wave intake (done 2026-08-09) — kept for history

1. **Fork and track:** Newelle and end-4/dots-hyprland — Done.
2. **Promote from shesh-desktop:** `shesh-files`, `shesh-shell`, `shesh-system`, and `shesh-voice`
   — Done.
3. **Bridge:** `shesh-audit` to the SheshAOS event store — Done.
4. **Reference-only:** Goose, Hermes, pi, Prime, computer-use-linux, pipecat, Leon — Done (read).
5. **Upstream-tracker bot** — Done.
