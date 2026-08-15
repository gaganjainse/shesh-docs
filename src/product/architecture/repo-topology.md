# Repository Topology: the Federated "Sinkhole"

Shesh does not reinvent its dependencies; it forks them, keeps the forks rolling, steals
the best parts into component repositories, integrates those into one ecosystem manifest,
and promotes the result through canary to stable. This chapter explains the topology and
the gates that keep breakage off your daily driver.

The model is exactly how a Linux distribution works: upstream projects become distro
packages, packages move through testing into core. The fleet stays current with upstream
and stays in control, with a filter at every layer.

- **Summary**
  - Five layers carry a change from upstream fork to the stable machine.
  - Sixteen small organs consolidated into `shesh-core` (175 tests, one CI) under ADR-0016.
  - Every promotion is blocked by an automated gate in `scripts/gates/`.
  - A single manifest (`components.toml`) is the source of truth, resolved to `shesh.lock`.
  - Upstream does most of the work; the fleet tracks, customizes, and specializes.

> **Note —** Our job is not merely to fork and wrap, but to upgrade the wrapper for our
> needs and to customize it for the CachyOS/Hyprland/6 GB-VRAM system. The Newelle fork,
> for example, strips GNOME-only assumptions, adds the Hyprland Quickshell overlay,
> prewires the MCP servers, sets 6 GB-safe model defaults, and renames the about-screen to
> "Shesh (Newelle core)". That is upgrade and specialization, not just a wrapper.
>
> The fleet integrates many systems — Hyprland, Quickshell, MCP, voice, eBPF, containers,
> phone ADB, and OmniRoute — but they must not conflict. We stay cautious yet enterprising:
> namespace through MCP stdio process boundaries (never in-process FFI, per the
> [language policy](language-policy.md)), a Guard policy of allow/confirm/deny, separate
> systemd user services, separate config dirs under `~/.config/shesh/mcp/`, separate btrfs
> subvolumes, and separate Python venvs via `uv`. One job per component, one process per
> MCP server, one policy gate — that is how integrations avoid clashing.

---

## The layers, bottom to top

The diagram traces a change from a raw upstream fork to the dotfiles running on your
machine.

```text
1. UPSTREAM FORKS          (mirrors of external projects, track main/default)
        |  cherry-pick / rebase our patches
        v
2. COMPONENT REPOS         (one per Shesh organ; our code + vendored fork pins)
        |  tagged releases, semver, individually tested
        v
3. ECOSYSTEM INTEGRATION   (shesh-ecosystem: manifests pin component versions)
        |  built together, full integration tests -> "canary"
        v
4. CANARY REPO             (shesh-ecosystem canary branch — daily build, bleeding edge)
        |  soak on a spare machine/VM for N days; gates pass
        v
5. STABLE / DOTFILES       (shesh-desktop main — your actual machine, production)
```

### 1. Upstream forks (`gaganjainse/fork-<project>`)

A bare fork of each external project we use, carrying a tiny `shesh/` branch with our
patches (MCP additions, branding, config, bug fixes). A bot opens a pull request weekly
when upstream advances; CI rebases the branch and runs the upstream tests. We never diverge
more than necessary — every patch has a reason and an attempt to upstream it. These are raw
material intake; nothing here runs on your machine directly.

### 2. Component repositories (`shesh-<organ>`)

**Federation consolidation (2026-08-13, ADR-0016):** the 16 sub-~460-LOC modules that were
one repository per organ folded into **`shesh-core`** — one repository shipping all 16
packages with unchanged console-script names (175 tests, one `pyproject`, one `ruff`
config, one CI). Federation still fits *independently versioned services*, but a 150-line
module is a file, not a service.

Remaining component repositories (real services):

- `shesh-core` — audit (policy/event log), secrets, brain, mind, shell, system, files,
  media, messaging, calendar, backup, containers, eBPF, skills, mcp-bundle, acp, wave config.
- `shesh-memory` — hierarchical memory plus habit learner (rag-service wrapper).
- `shesh-orchestrator` — multi-agent RLM runtime (coordinator/planner/coder/…).
- `shesh-harness` — skill marketplace primitives.
- `shesh-phone` — ADB Android harness (vision → tap).
- `shesh-omniroute` — free-model AI gateway wrapper (MIT).
- `shesh-voice` — Newelle fork (STT/TTS/wake word).
- `shesh-desktop` — end-4 dots fork plus Quickshell overlay plus device profile.

Each has its own tests and is independently usable.

### 3. Ecosystem integration (this repository, `shesh-ecosystem`)

The **workspace manifest** pins every component to a specific tag and the upstream fork
SHA. Integration tests prove the organs work together (for example, voice → brain policy →
file move). It produces a lockfile (`shesh.lock`), like a distro repository snapshot. This
is where we decide the combination — "the best of everything."

### 4. Canary (`canary` branch)

Built daily from the latest component tags that pass their own tests. It runs the full
integration suite; if green, it publishes a canary release. It is intended for a VM, a
spare laptop, or a secondary user account — not your main work.

### 5. Stable, on your machine (`shesh-desktop:main`)

Only canary releases that soaked N days with no regressions merge here. This is what runs
on the MSI Sword daily. Boring is good.

---

## Filters and quality gates at each layer

| Layer | Gate that blocks promotion |
|---|---|
| 1. Fork | upstream tests pass; our `shesh/` branch rebases cleanly; license check |
| 2. Component | unit tests, lint (`shellcheck`/`ruff`/`cargo test`), no known CVEs in deps, signature/attestation |
| 3. Ecosystem | integration tests on an Arch/CachyOS container; manifest resolves; MCP smoke tests |
| 4. Canary | soak period, hardware smoke test (display/GPU/audio), no failed systemd units |
| 5. Stable | manual sign-off plus rollback snapshot (btrfs) before apply |

Every gate is a script in `scripts/gates/`, runnable locally and in CI. Nothing is promoted
by hand without a green gate.

---

## Manifests: the single source of truth

`manifests/components.toml` lists every organ with its repository, version, license, and
source:

```toml
[component.shesh-voice]
repo    = "gaganjainse/shesh-voice"
version = "1.4.5-sesha1"
license = "GPL-3.0"
upstream = { name = "Newelle", repo = "qwersyk/Newelle", ref = "1.4.5" }
provides = ["mcp:voice", "wakeword", "stt", "tts"]
```

`scripts/resolve-manifest.py` resolves the full set, checks that licenses are
GPL-3-compatible, verifies tag SHAs, and writes `shesh.lock`. This is the package-repo
metadata, in one auditable file.

---

## Why this is not a sinkhole of endless work

- **Upstream does most of the work.** We track; we do not rewrite. Forks plus thin patches.
- **Components are independent.** You can pause any organ without stopping the body.
- **Gates are automated.** The weekly bot does the rebasing and testing; you only review failures.
- **Stable is protected.** Canary absorbs the breakage; your machine gets only tested combinations.
- **We start narrow.** Phase 1 builds three components (files, shell, system) that already
  exist in shesh-desktop; the rest are added as the gates and time allow.

---

## Repository creation order

1. `shesh-ecosystem` (this repository — the orchestrator/manifests).
2. Forks of the first-wave upstreams (Newelle, end-4/dots-hyprland, plus the Rust/Python deps).
3. Component repositories split from the working shesh-desktop code:
   `shesh-files`, `shesh-shell`, `shesh-system`, `shesh-voice`.
4. `shesh-audit` (brain bridge) once MCP is stable.
5. Everything else (memory, phone, mind) after the integration harness proves itself.

The exact first-wave list and the steal-map is in `SOURCES.md`.
