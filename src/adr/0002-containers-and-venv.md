# ADR-0002: Rootless Containers for Exotic Runtimes

Shesh runs any tool that needs a runtime outside its five core languages inside a rootless
container, so the host stays clean and the build stays reproducible. The rule trades a one-time
pull cost for isolation that survives across CachyOS, Fedora, and Ubuntu canary machines.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** containers, reproducibility, security

## Context

Several useful tools require runtimes the core build does not: Node.js for filesystem and fetch
MCP servers, Playwright, Go linters, and the like. Installing them on the host pollutes the
development environment, creates version conflicts — a system Node fighting a project's pinned
Node — and breaks reproducibility across the CachyOS/Fedora/Ubuntu canary matrix.

The fleet needs isolation without a Docker daemon and without root.

## Decision

- **Rootless Podman** is the default runtime. No Docker daemon is used.
- **Distrobox** supports interactive development of exotic stacks through `distrobox-assemble`.
- `uv` manages Python virtual environments with lockfiles.
- Containers are **ephemeral** (`--rm`), run with `--network=none` and `--cap-drop=ALL` by
  default for sandboxed tasks (`shesh-containers`).
- The third-party MCP bundle (`shesh-mcp-bundle`) launches `npx` or `uvx` only when present,
  and fails open by skipping the missing tool.

## Consequences

### Benefits

- The host carries only CachyOS 260628 and Hyprland.
- `shesh-containers-mcp` runs `run_sandboxed(["echo","hi"])` fully offline.
- Canary CI exercises the same container on Arch, Fedora, and Ubuntu.

### Costs

- The first run needs a Podman pull, documented in MANUAL_VERIFICATION.
- GUI applications that need the host Wayland socket require explicit passthrough, also
  documented.

## Links

- `docs/CONTAINERS_AND_VENV.md`
- `shesh-containers`, `shesh-mcp-bundle`
- [ADR-0001: Five Languages Only](0001-five-languages.md)
