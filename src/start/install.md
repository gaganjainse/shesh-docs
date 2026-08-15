---
title: Install Shesh
type: tutorial
summary: "Install the Shesh desktop and agent stack on an Arch-based system and confirm it runs."
audience: operator
status: current
verified: 2026-08-15
---

# Install Shesh

By the end of this tutorial you have a running Shesh installation: the desktop
shell, a local model server, and the tool servers registered with a client. You
follow one path from start to finish; alternatives and tuning are covered in the
[how-to guides](../how-to/index.md).

## Prerequisites

- An Arch-based Linux system. The reference configuration is CachyOS with
  Hyprland 0.55 or later and Quickshell; see
  [Target hardware](../explanation/target-hardware.md).
- A user account with `sudo` access.
- At least 20 GB of free disk space for models and container images.
- A discrete GPU is optional. Without one, models run on the CPU and responses
  are slower.

> **Note.** Only the reference configuration is verified end to end. Other Arch
> derivatives generally work, but you may need to adapt package names.

## Step 1: Install the desktop and agent stack

The bootstrap script installs the desktop layer and the agent stack together.
Inspect it before running it, as you would with any script fetched over the
network.

```bash
curl -fsSL https://raw.githubusercontent.com/gaganjainse/shesh-desktop/main/tools/bootstrap.sh -o bootstrap.sh
less bootstrap.sh
bash bootstrap.sh --dry-run
```

`--dry-run` prints the actions without changing the system. When the plan looks
correct, run it:

```bash
bash bootstrap.sh
```

Useful flags:

| Flag | Effect |
|---|---|
| `--dry-run` | Print planned actions and exit |
| `--skip-ai` | Install the desktop layer only |
| `--skip-nvidia` | Skip proprietary driver configuration |
| `--skip-power` | Skip power-profile configuration |
| `--device <profile>` | Select a hardware profile |

Reboot and log in to Hyprland when the script finishes.

## Step 2: Install the local model server

```bash
sudo pacman -S ollama
systemctl --user enable --now ollama
```

Pull the model set. Each model has a distinct role, described in
[Models](../reference/models.md).

```bash
ollama pull phi4-mini
ollama pull qwen2.5-coder:3b
ollama pull moondream2
ollama pull nomic-embed-text
```

The routing layer keeps one model resident at a time and enforces a VRAM ceiling,
so a 6 GB card can serve all four roles.

## Step 3: Install the container runtime

Sandboxed tool execution requires rootless Podman.

```bash
sudo pacman -S podman
podman info --format '{{.Host.Security.Rootless}}'
```

The command prints `true` on a correctly configured system.

## Step 4: Install the agent components

The tool servers ship as a single distribution, `shesh-core`, which provides
every Model Context Protocol server command. Install it and the independent
services in isolated environments:

```bash
pipx install git+https://github.com/gaganjainse/shesh-core.git
pipx install git+https://github.com/gaganjainse/shesh-memory.git
pipx install git+https://github.com/gaganjainse/shesh-orchestrator.git
pipx install git+https://github.com/gaganjainse/shesh-harness.git
pipx install git+https://github.com/gaganjainse/shesh-phone.git
```

> **Note.** Earlier releases distributed each tool server as its own repository.
> Those repositories are archived and superseded by `shesh-core`, which keeps the
> same command names, so existing client configurations continue to work. See
> [ADR-0019](../governance/adr/0019-shesh-core-monorepo.md).

## Step 5: Generate the client configuration

```bash
git clone https://github.com/gaganjainse/shesh-ecosystem.git ~/src/shesh-ecosystem
cd ~/src/shesh-ecosystem
python scripts/generate_mcp_config.py --channel canary
```

This writes a server list to `~/.config/shesh/mcp/servers.json` containing the
servers enabled for the channel you selected. Channels are explained in
[Release channels](../reference/release-channels.md); `canary` is the right
choice while you are setting the system up.

## Verify

Confirm the desktop session:

```bash
hyprctl version
hyprctl monitors
wpctl status
```

Confirm the model server responds:

```bash
ollama list
```

Confirm a tool server starts. The command runs in the foreground and speaks
JSON-RPC on standard input; press <kbd>Ctrl</kbd>+<kbd>C</kbd> to exit.

```bash
shesh-system-mcp
```

Confirm the generated client configuration is present and non-empty:

```bash
python -c "import json;print(list(json.load(open('$HOME/.config/shesh/mcp/servers.json'))['mcpServers']))"
```

The command prints the list of registered server names.

## What to do next

Work through the [verification checklist](../reference/verification-checklist.md)
on the machine. It covers the hardware, audio, GPU, and policy checks that cannot
be automated.

## Related

- [Configure MCP servers](../reference/verification-checklist.md) — add, remove, or
  re-point tool servers after installation.
- [Configure secrets](../reference/verification-checklist.md) — set up credential storage
  before connecting anything that needs a token.
- [Set up voice](../reference/verification-checklist.md) — enable wake word, speech to text,
  and speech synthesis.
- [The Agentic Body](../explanation/agentic-body.md) — what you installed and
  why it is arranged this way.
