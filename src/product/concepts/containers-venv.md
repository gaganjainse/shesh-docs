# Containers, Virtual Environments, and Reproducible Development

Shesh keeps the host clean. Every non-core runtime lives in a **rootless Podman** container
or a per-component **uv** virtual environment. This chapter explains the toolchain and why
it matches the [language policy](language-policy.md): the "do not break anything" rule is
enforced technically, not by discipline alone.

- **Summary**
  - Each Python component is a `uv` project with a committed `uv.lock`; CI runs `uv sync --frozen`.
  - Rust uses `rustup` and `cargo`; release binaries are LTO/stripped into `~/.local/bin`.
  - Podman is daemonless and rootless; Distrobox shares `$HOME` for interactive dev.
  - Untrusted or non-core-language agents run in rootless containers with limited mounts, never linked into the host.
  - Keep secrets out of containers; pass them via a secret service, never a committed compose file.

---

## Python — Astral `uv` (not pip/venv/poetry)

Each Python component (`shesh-*` MCP servers, classifier, rag-service) is a proper `uv`
project:

```bash
cd tools/shesh
uv init --bare --lib            # if creating fresh
uv add mcp[cli] fastmcp httpx
uv add --dev pytest ruff
uv sync                        # creates .venv, installs exactly per uv.lock
uv run python -m pytest         # run inside the venv
uv run ruff check .
```

Rules:

- Commit `pyproject.toml` **and** `uv.lock`. CI runs `uv sync --frozen` (no implicit resolution).
- One venv per component under `~/.local/state/<component>/.venv` at install time (the
  installer uses `uv venv` plus `uv pip install -r …` only for the dotfiles bootstrap;
  components use `uv sync`).
- Never `sudo pip`, never global `pip install`. Use `uvx <tool>` for one-off CLIs.
- Pin Python ≥ 3.11 (we use 3.13 in dev/CI; CachyOS ships 3.13).

---

## Rust — rustup and cargo

```bash
rustup default stable
cargo fmt --check && cargo clippy -D warnings && cargo test
```

Release binaries are LTO/stripped (already set in `watcher-rs/Cargo.toml`). Install to
`~/.local/bin`.

---

## Containers — rootless Podman and Distrobox

**Podman** is the engine (daemonless, rootless, user namespaces). **Distrobox** is the
wrapper for long-lived dev environments that need host `$HOME`, Wayland, and audio.

### A quick isolated test box (Arch, throwaway)

```bash
podman run --rm -it archlinux:latest bash
# inside: pacman -Syu git bash shellcheck python ...
```

### A persistent dev container with host integration

```bash
distrobox create --name shesh-dev --image archlinux:latest \
  --additional-packages "git base-devel shellcheck python uv rustup"
distrobox enter shesh-dev
```

This shares `$HOME`, the Wayland socket, and PipeWire — so you can run GUI and ML tooling
without polluting CachyOS. Export binaries or apps to the host with `distrobox-export`.

### Canary and other-distro testing

The canary gate runs components against multiple bases in CI:

```bash
for img in archlinux:latest fedora:40 ubuntu:24.04; do
  podman run --rm -v "$PWD":/src:ro -w /src "$img" ./scripts/gate-in-container.sh
done
```

Use this to validate the installer on Fedora or Ubuntu (guarded paths) without a VM.

### Isolating non-core or cloud tools

Any agent or service in a non-approved language (Go, Mojo, a Node-heavy tool) or any
cloud-tier agent runs in a rootless container with a read-only mount of only the paths it
needs, exposing MCP over a Unix socket. It never links into the host.

---

## Security notes

- Prefer rootless Podman over Docker (ArchWiki): rootful Docker containers have unrestricted
  host filesystem access by default.
- Distrobox is **not a security sandbox** — it shares your home. Use it for convenience, not
  for isolating untrusted code (use plain podman with limited mounts for that).
- Pin image digests in CI for reproducibility; use `:latest` only on dev boxes.
- Keep secrets out of containers; pass them via `systemd-ask-password` or a secret service,
  never in an environment variable inside a committed compose file.

---

## Why this stack over the alternatives

- **uv** replaces pip-tools/poetry/virtualenv: 10–100× faster, lockfile and project metadata
  in one file, `uvx` for ephemeral tools. Best practice in 2026.
- **Podman** over Docker: daemonless, rootless, systemd integration, OCI-compatible.
- **Distrobox** over raw podman for interactive dev: POSIX shell, any OCI image, app/binary export.
- No Conda/mamba (heavy, conflicts with system Python); no Nix on the host (we keep `dist-nix/`
  for upstream parity but do not run it daily).
