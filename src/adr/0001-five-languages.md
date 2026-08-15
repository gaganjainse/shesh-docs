# ADR-0001: Five Languages Only

Shesh builds its body in just five languages, and it keeps them apart at process
boundaries rather than in a shared memory space. That rule trades away a few exotic
runtimes for a build that is reproducible, auditable, and approachable for newcomers.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Decision makers:** Gagan Jain, Shesh Autopilot
- **Tags:** language, ffi, complexity

## Context

The ecosystem spans a governance kernel, AI glue, desktop compositor configuration, UI
shell, and installer scripts. Early prototypes mixed Rust, Python, Go, Zig, C, Lua, QML,
and TypeScript. The blend produced foreign-function-interface (FFI) nightmares, cross-toolchain
build failures — a `russh::Error::msg` API break and a terminal crate that demanded Zig — and
unsafe boundaries that were hard to audit.

Five languages cover every job the fleet has:

- Systems work, performance, and safety call for **Rust**.
- AI orchestration, MCP, retrieval-augmented generation (RAG), and embeddings call for **Python**.
- Hyprland configuration requires **Lua** (Hyprland 0.55 and later).
- The Quickshell UI is **QML/JS** (Qt6 declarative).
- Installer and glue scripts are **Bash 5+**.

## Decision

The tree permits only those five core languages:

- **Rust** for the brain, kernel, and watchers.
- **Python 3.11+** for the mind and MCP servers.
- **Lua** for Hyprland configuration only.
- **QML/JS** for Quickshell.
- **Bash** for the installer.

No Zig, C, Mojo, or Go belongs in the main build. Cross-language communication happens over
**MCP/JSON at process boundaries**, never through in-process FFI. Exotic runtimes — Node for
some MCP servers, Go tools — run inside **rootless Podman or Distrobox**, not on the host
(see [ADR-0002](0002-containers-and-venv.md)).

## Consequences

### Benefits

- The host build matrix shrinks to two toolchains, Rust and Python, and stays reproducible.
- The only auditable unsafe boundary is the MCP stdio/JSONL link.
- A new contributor needs to learn two languages to become productive.

### Costs

- Some upstream MCP servers need Node (`npx`); Shesh proxies them behind the Guard through
  `shesh-mcp-bundle` rather than linking them.
- Zig and C experiments must live in containers and can never be first-class citizens.

## Links

- `docs/architecture/LANGUAGE_POLICY.md`
- `docs/CONTAINERS_AND_VENV.md`
- [ADR-0002: Rootless Containers for Exotic Runtimes](0002-containers-and-venv.md)
