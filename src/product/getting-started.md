# Getting Started with Shesh on CachyOS/Hyprland

This chapter gets Shesh running on your machine: first a hardware-free developer check,
then the full desktop and AI body install, then the everyday tasks that prove the body
works. The instructions target the MSI Sword 16 HX B14VEKG (i7-14700HX, RTX 4050 6 GB,
1920×1200@144, 16 GB DDR5), but they work on any recent Arch-based system.

You need CachyOS 260628, Hyprland ≥0.55, Quickshell, and the Shesh overlay. The desktop
layer (dotfiles) and the AI layer (Brain/Mind/Soma) are independent, so you can mix and
match versions freely.

- **Summary**
  - A single `make check` proves the offline gate (ruff + 63 tests + license gate) without hardware.
  - Two install paths exist; both end in the same running state.
  - The local model set fits a 6 GB GPU budget through one-model-at-a-time VRAM scheduling.
  - Components install as isolated `pipx` binaries, never global `pip`.
  - A one-command health check verifies the whole body after reboot.

---

## Developer quick start (no hardware)

If you only want to prove the repository is sound, clone it and run the gate. This needs
no GPU, no display, and no network beyond the initial clone.

```bash
git clone https://github.com/gaganjainse/shesh-ecosystem.git
cd shesh-ecosystem
make check        # ruff + 63 tests + license gate + regenerate locks — must be green
python -m pytest tests/ -q
```

---

## Full install on CachyOS

There are two supported paths; pick one. The end state is identical either way:
Hyprland plus Quickshell, Ollama serving the 6 GB model set, and the `shesh-*-mcp`
servers installed and enabled as user services with `~/.config/shesh/mcp/servers.json`
wired for your clients.

### Path A — one repository: end-4 base with the Shesh overlay (recommended)

`shesh-desktop` is a fork of end-4/dots-hyprland (the "illogical-impulse" Quickshell
shell) with the Shesh overlay, device profile, and systemd units already baked in. One
command installs both the desktop and the AI stack.

```bash
bash <(curl -s https://raw.githubusercontent.com/gaganjainse/shesh-desktop/main/tools/bootstrap.sh)
# flags: --dry-run (print only) · --skip-ai · --skip-nvidia · --skip-power · --device msi-sword-cachyos|generic
```

After reboot, open **Settings → Shesh** to change everything without touching code: the
release **channel** (stable/canary/devel), which **MCP servers** run, the **Guard policy**
(default verdict: ask-before-acting, allow, or deny, plus a protect-secrets toggle), the
LLM and vision models, and the automations (organizer, power profile, backups). Toggles
persist to `~/.config/illogical-impulse/config.json`, and the Shesh service applies them
(MCP config to `~/.config/shesh/mcp/*.json`, policy to `~/.config/shesh/policy.json`).

### Path B — your own end-4/dots-hyprland plus the Shesh AI stack

If you already run end-4/dots-hyprland, install its dots first, then layer the Shesh AI
stack on top. This path is desktop-agnostic — it works with end-4 or with shesh-desktop.

```bash
# 1. end-4 dots (their canonical installer — clones to its own dir and sets up Hyprland + Quickshell)
cd /path/to/your/dots-hyprland && ./setup install
# (or: bash <(curl -s https://ii.clsty.link/get))

# 2. Shesh Brain/Mind/Soma + Ollama + MCP units (from the ecosystem repo)
git clone https://github.com/gaganjainse/shesh-ecosystem.git ~/src/shesh-ecosystem
bash ~/src/shesh-ecosystem/tools/install-shesh-stack.sh          # or: --skip-ai --dry-run first
```

### First-boot checks

Both paths end in the same state. After reboot, log into Hyprland and confirm the
plumbing responds:

```bash
hyprctl version
hyprctl monitors          # should show 1920x1200@144
wpctl status              # audio sinks/sources
```

The full first-boot checklist lives in `docs/MANUAL_VERIFICATION.md` §0.

### The 6 GB Ollama model set

Shesh runs a small, 6 GB-safe model set on the local GPU. One model is resident at a
time; `shesh-mind` budgets VRAM with a 5.5 GB ceiling.

```bash
sudo pacman -S ollama
systemctl --user enable --now ollama

ollama pull phi4-mini              # primary / planner / researcher / critic
ollama pull qwen2.5-coder:3b       # coder
ollama pull moondream2             # vision
ollama pull nomic-embed-text       # embeddings / RAG

# Optional: list what is loaded
ollama ps
```

Watch the budget with `watch nvidia-smi`. See `docs/CONTAINERS_AND_VENV.md` for the
surrounding toolchain.

### Rust, uv, and rootless Podman

Rust is only needed if you touch the SheshAOS kernel; CI already has it. The core daily
toolchain is `uv` for Python and rootless Podman for isolation.

```bash
# uv for Python
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# Rootless Podman
sudo pacman -S podman buildah
podman info  # should show rootless
podman run --rm alpine echo ok

# Distrobox for exotic runtimes
sudo pacman -S distrobox
```

### Installing the Shesh components (pipx, not pip)

Components install as isolated `pipx` binaries so their dependencies never collide.

```bash
# From shesh-ecosystem
python scripts/generate_mcp_config.py --channel canary
cat ~/.config/shesh/mcp/servers.json   # 9 servers

# Install each component (example)
for repo in shesh-audit shesh-mind shesh-memory shesh-orchestrator shesh-skills \
            shesh-system shesh-shell shesh-files shesh-backup shesh-phone \
            shesh-containers shesh-mcp-bundle shesh-calendar shesh-acp shesh-secrets; do
  echo "=== $repo ==="
  pipx install git+https://github.com/gaganjainse/$repo.git --force
done

# Verify
for s in shesh-{audit,system,shell,files,skills,memory,mind,harness,orchestrator,backup,phone,containers,secrets,calendar,acp}-mcp; do
  command -v "$s" && echo "ok  $s" || echo "MISSING $s"
done
```

If you prefer `uv`, the equivalent is `uv tool install git+https://github.com/gaganjainse/shesh-audit.git`.

### Voice (shesh-voice, a Newelle fork)

The voice stack is a native build of the Newelle fork with the Shesh MCP overlay.

```bash
git clone https://github.com/gaganjainse/shesh-voice.git
cd shesh-voice
# Native build (not Flatpak)
meson setup build
meson compile -C build
sudo meson install -C build

# Overlay MCP config
mkdir -p ~/.config/Newelle
cp shesh-overlay/shesh-mcp-servers.json ~/.config/Newelle/mcp-servers.json

# Launch
newelle
# In Newelle settings:
# - Provider: Ollama -> phi4-mini (localhost:11434)
# - Wake word: openwakeword, phrase "hey shesh"
# - STT: faster-whisper
# - TTS: Piper
```

Muse's MCP panel should show the nine servers in green.

### Secrets (no keys in config)

`shesh-secrets` resolves secrets from several backends so credentials never live in plain
config files.

```bash
pipx install git+https://github.com/gaganjainse/shesh-secrets.git
shesh-secrets-mcp  # then in any MCP client:

# Env backend (simplest)
export MY_TOKEN=xxx
shesh-secrets-mcp -> get_secret("env:MY_TOKEN")

# gopass
gopass insert shesh/valt/backup  # restic password
get_secret("gopass:shesh/backup")

# KeepassXC
# File (0600 only, refuses world-readable)
echo "secret" > ~/.config/shesh/my.key
chmod 600 ~/.config/shesh/my.key
get_secret("file:~/.config/shesh/my.key")
```

Never commit a key. Run `git secrets --scan` or `truffleHog` before pushing.

### Backup (restic, real)

```bash
sudo pacman -S restic
restic -r /srv/shesh-backup init   # or gdrive/s3 via rclone

# Store the password via shesh-secrets
# Configured in shesh-backup as env:RESTIC_PASSWORD or gopass:shesh/backup

shesh-backup-mcp -> run_backup
restic -r /srv/shesh-backup snapshots

# Test restore to a temp dir before trusting it
mkdir /tmp/restore-test
restic -r /srv/shesh-backup restore latest --target /tmp/restore-test
```

Set a daily systemd timer:

```bash
systemctl --user enable --now shesh-backup.timer
```

### Phone (Realme Narzo 90x, ADB)

```bash
sudo pacman -S android-tools
# On phone: Developer Options -> USB debugging ON

adb devices  # should list the device
pipx install git+https://github.com/gaganjainse/shesh-phone.git
shesh-phone-mcp
# Try a safe tap:
# tap at 500,500 — allowed (inside the safe area)
# tap at 10,10 — denied (status bar protected)
```

### Container sandbox

The container organ runs commands with no network and dropped capabilities.

```bash
shesh-containers-mcp -> run_sandboxed(["echo","hi"])
# Should return "hi" with --network=none and --cap-drop=ALL
podman run --rm alpine echo ok  # manual check
```

---

## Everyday use

### Voice

Say "hey shesh", then speak a goal: "organize my Downloads by type, allow". Newelle shows
the plan (planner), delegates to the coder or researcher, the critic approves, and then
asks confirmation before moving files.

### Memories and habits

```bash
shesh-memory-mcp -> recall("my backup habit")
shesh-memory-mcp -> semantic_search("how do I greet users?")
# Habits learned: check ~/.local/share/shesh/memory/habits.md
```

### Background sessions

```bash
shesh-orchestrator-mcp -> start_session(goal="refactor all ...", use_llm=true)
# Disconnect, work on other things
shesh-orchestrator-mcp -> get_session(id)
shesh-orchestrator-mcp -> list_sessions
shesh-orchestrator-mcp -> cancel_session(id)  # actually stops the loop
```

### Traces

```bash
shesh-orchestrator-mcp -> recent_traces(limit=5)
cat ~/.local/share/shesh/traces/*.jsonl | jq .
```

---

## Canary and promotion flow

The daily canary boots all components in containers; if it is green on your MSI, you
promote to stable behind a btrfs snapshot.

```bash
# Daily canary (runs in CI): boots all 16 components in containers
bash scripts/e2e-canary.sh

# If green on your MSI, promote:
git checkout -b promote/canary-$(date +%Y%m%d)
make check
git add channels/ && git commit -m "chore: promote canary $(date -I)"
# Open PR -> merge -> stable after btrfs snapshot

# Switch channels (installer with snapshot + rollback):
curl -fsSL https://raw.githubusercontent.com/gaganjainse/shesh-ecosystem/main/tools/install.sh | bash -s -- --channel canary
# Installer does:
# btrfs subvolume snapshot / /@snapshots/pre-shesh-canary-$(date +%Y%m%d)
# pipx upgrade all shesh-* from canary.lock
# If boot fails -> select the snapshot in grub-btrfs
```

---

## Hardware checks (required on the MSI)

Work through `docs/MANUAL_VERIFICATION.md` top to bottom. The key signals are Hyprland at
144 Hz, the NVIDIA MUX via `nvidia-smi`, the wake word, PipeWire via `wpctl`, a pink
Quickshell render check, a backup restore, the phone safe-area, rootless Podman, and
green Newelle MCP.

One command covers the body's health:

```bash
echo "=== Shesh health ===" && \
systemctl --user is-active ollama && \
bash ~/src/shesh-ecosystem/scripts/e2e-canary.sh && \
for s in shesh-{audit,system,shell,files,skills,memory,mind,harness,orchestrator,backup,phone,containers,secrets,calendar,acp}-mcp; do
  command -v "$s" >/dev/null && echo "ok  $s" || echo "MISSING  $s"
done && \
echo "=== done ==="
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: mcp` | `pipx install mcp fastmcp` and `pip install -e ./src/shesh-*` |
| Hyprland keybinds missing | `cd ~/Workspace/shesh-desktop && git pull && ./dots/.config/hypr/install.sh` |
| Quickshell pink placeholders | `quickshell --reload`, check the QML log `journalctl --user -u quickshell` |
| Newelle MCP red | `cat ~/.config/shesh/mcp/servers.json`, verify the `shesh-*-mcp` entries are in PATH |
| Ollama OOM | `shesh-mind-mcp -> list_installed_models`, `ollama ps`, unload with `ollama stop` |
| Backup fails | `restic check`, password backend `shesh-secrets-mcp -> get_secret` |
| Podman rootless fails | `podman system migrate`, `loginctl enable-linger $USER` |
| Audit log tampered | `shesh-audit-mcp -> verify_integrity()` — shows the broken hash chain |
| Workspace over budget | `rm -rf ~/.cargo ~/.rustup ~/.cache __pycache__ */__pycache__ .pytest_cache` |

---

## Where to go next

- Read `docs/SESSION_HANDOFF.md` for the prioritized task list.
- Read the architecture decision records in `docs/history/adr/` (19 decisions).
- Pick a todo from `TODO.md` — the highest unblocked open item.
- Run `npm`-free autopilot with `python -m tools.autopilot.cli run`; it loops: implement →
  gate → safe commit → push.

Shesh is an agent that is a body, not a chatbot.
