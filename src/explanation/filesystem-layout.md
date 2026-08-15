---
title: Filesystem layout
type: explanation
summary: "Never hand-edit these except via the package manager or the installer:."
audience: operator
status: current
verified: 2026-08-15
hardware_verified: no
---

# Filesystem layout

Shesh follows the Filesystem Hierarchy Standard and the XDG base directory
specification rather than writing everything into the home directory. Doing so
keeps backup policies precise and ensures the package manager, systemd, and
containers each find files where they expect them.

---

## System directories (owned by the distro / pacman)
Do not hand-edit these paths. Change them through the package manager or the installer:

| Path | Purpose | Shesh interaction |
|---|---|---|
| `/usr/bin`, `/usr/lib` | distro packages | installs via `pacman`/AUR only |
| `/usr/local/bin`, `/usr/local/lib` | sysadmin-local binaries | the `nvidia-run` and `msi-mux-switch` helperser` symlinks |
| `/etc` | system config | udev rules, `sysctl.d`, `zram-generator.conf`, mkinitcpio |
| `/boot` | kernels/bootloader | only via `mkinitcpio`/bootloader config tooling |
| `/var` | system state/logs | journal, pacman cache |
| `/run`, `/tmp` | runtime/ephemeral | never persist anything here |

Rule: anything added under `/etc` or `/usr/local` carries a comment `# managed-by=shesh-desktop`
so `2.undo-setups.sh` can revert it precisely.

---

## User directories (XDG base directory spec)
| Variable | Path | What lives there |
|---|---|---|
| `XDG_CONFIG_HOME` | `~/.config` | dotfiles (Hyprland, Quickshell, Newelle, Shesh config) |
| `XDG_DATA_HOME` | `~/.local/share` | app data: Shesh audit log, Chroma memory, icons, fonts |
| `XDG_STATE_HOME` | `~/.local/state` | venvs, logs, history, systemd user state |
| `XDG_CACHE_HOME` | `~/.cache` | regenerable caches (**never backed up**) |
| `XDG_BIN_HOME` | `~/.local/bin` | user binaries (sm-watcher, shesh-*-mcp) |

Every Shesh component obeys these via the shared `tools/lib/common.sh` and Python `platformdirs`/
`pathlib` conventions — no hardcoded `~/.shesh` sprawl (a legacy `~/.cache/sesha` dir from pre-canon builds may exist on old installs; delete it at migration).

---

## Where each Shesh component stores data
| Component | Config | State/data | Cache |
|---|---|---|---|
| Shesh MCP servers | `~/.config/shesh/` | `~/.local/state/shesh/.venv` | `~/.cache/shesh` |
| Audit log | — | `~/.local/share/shesh/audit/` | — |
| Smart-organizer | `~/.config/smart-organizer/` | `~/.local/share/smart-organizer/{history.db,undo}` | `~/.cache/smart-organizer` |
| Ollama models | `~/.config/ollama` | **`~/AI/Models/ollama`** (symlinked, large) | — |
| HuggingFace | — | **`~/AI/Weights-Cache`** | — |
| Newelle | `~/.config/newelle` | `~/.local/share/Newelle` | `~/.cache/Newelle` |
| Quickshell | `~/.config/quickshell` | `~/.local/share/quickshell` | — |
| Hyprland | `~/.config/hypr` | `~/.local/state/hyprland` | — |
| Restic backups | `~/.config/shesh/backup.conf` | `~/Backups` repo | — |

The large AI assets stay under `~/AI/` (excluded from snapshots/backups — regenerable) while config
and the audit log stay in their proper XDG homes.

---

## Systemd unit search paths (user vs system)
| Kind | Path | Used for |
|---|---|---|
| system units | `/etc/systemd/system/`, `/usr/lib/systemd/system/` | `nvidia-suspend`, zram, display manager |
| user units | `~/.config/systemd/user/` | Shesh MCP servers, organizer watcher, timers |
| system drop-ins | `/etc/systemd/system/<unit>.d/` | overrides the project adds |

The installer `install -Dm644` units into the user dir; it never writes to `/usr/lib`.

---

## Containers (Podman/Distrobox)
| Path | Purpose |
|---|---|
| `~/.local/share/containers` | rootless podman storage (images/volumes) |
| `~/.config/containers` | podman registries/policy |
| Distrobox homes | inside the container; host `$HOME` is shared |

This is why Shesh uses **rootless Podman** — all container state stays under the user's XDG data dir,
no daemon, no root-owned `/var/lib/docker`.

---

## Reorganization summary (what changed from a flat `$HOME`)
- `~/Pictures`, `~/Music`, `~/Videos` consolidated into **`~/Media/{Images,Music,Videos,...}`**.
- `~/Downloads` is transient (auto-sorted, 30-day cleanup).
- `~/Desktop` renamed **`~/Desk`** and kept empty.
- Code split into **`~/Projects/{job,personal,labs,forks,_archive}`**.
- AI assets isolated in **`~/AI/{Models,Datasets,Vectors,Weights-Cache,Sessions}`**.
- Secrets in **`~/Vaults`** (700 perms), notes in **`~/Notes`**.

The one-time layout creator is `tools/setup-dirs.sh` (idempotent, dry-run capable).
