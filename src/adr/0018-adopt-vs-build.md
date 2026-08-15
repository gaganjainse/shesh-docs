# ADR-0018: Adopt-vs-Build Decisions & the 2026-08-12 Excision

Shesh resolved a batch of "build our own or adopt the best" calls and then physically removed
the dead weight those decisions exposed, leaving the workspace smaller, honest, and green under
stricter gates. The record is part strategy and part cleanup: adopt where upstream is sound,
build only where the fleet is unique, and delete what no longer earns its place.

> **Summary —**
> - MCP: adopt standalone `fastmcp` 3, drop the official `mcp` shim and its warning bug.
> - Guard: import `shesh-audit` directly; a missing guard now crashes startup, never silently
>   falls back.
> - Terminal: adopt stock Wave; excise `shesh-terminal`, `shesh-gui`, `shesh-tui`, and orphaned
>   Zig.
> - LLM supply: local Ollama, retire GitHub Models routing; OmniRoute is the OpenAI-compatible
>   front.
> - Lint gates: tool-native clippy, not grep, which already caught two real unwraps.

## Status

- **Date:** 2026-08-12
- **Status:** Accepted
- **Tags:** strategy, dependencies, architecture, cleanup

## Context

The renovation surfaced a recurring question — build our own or adopt the web-best? — plus a
barrel of pre-commit archaeology: crates, directories, and fallback paths that the already-adopted
architecture had made dead weight, yet nobody had physically removed. This record captures each
adopt-versus-build call and the excision that followed.

## Decisions

### 1. MCP servers: adopt standalone `fastmcp` 3, drop the official `mcp` shim

`mcp` 1.29.0 bundles a FastMCP re-implementation whose settings model carries an unresolved
forward reference — every `FastMCP(...)` construction raises a `pydantic-settings`
`IncompleteFieldDefinitionWarning`. `mcp` 2.0.0 deletes `mcp.server.fastmcp` entirely, making
the unbounded `mcp>=1.0` a resolver landmine. The options were: suppress the warning, pin
`mcp<2` forever, or migrate to the upstream-maintained `fastmcp>=3.4.7,<4`. **Chosen: (c).** The
warning is a real bug in the shim, not noise, and the standalone package is where FastMCP
development actually happens. Twenty component repositories migrated; every suite now passes
under `pytest -W error` (warnings-as-errors), which is policy, not an option.

### 2. Guard enforcement: fail-fast, never silent fallback

Components carried `try: from shesh_audit … except ImportError: _MCP = FastMCP`. Worse, several
imported `shesh_audit.guard` — a module that **never existed** — so the fallback fired on every
run and tools ran unguarded while [ADR-0015](0015-guard-policy.md) claimed total coverage.
**Chosen: direct imports plus declared dependencies.** A missing guard now crashes the server at
startup. Internal dependencies install in CI via
`git+https://github.com/gaganjainse/<repo>.git@main` until packages are published to PyPI
(publication tracked as a user action).

### 3. Terminal & mission control: adopt Wave, excise the pretenders

[ADR-0016](0016-kernel-consolidation.md) adopted stock Wave Terminal. Leftovers from the
abandoned port were still workspace members and were breaking CI: `shesh-terminal`'s build
script requires a Zig toolchain (ADR-0001 forbids Zig and FFI in the main build), its "native
Zig VT100 parser" is a 71-line counter whose only caller was a demo `shesh pty` printout, and
`PtyManager` had zero callers (blockctl uses `portable-pty` directly). `shesh-gui` had zero
consumers; `shesh-tui` only fed the CLI default. Top-level `zig/` was an orphaned pre-Rust
kernel attempt. The dead `tests/` crate advertised six Criterion benchmarks that had never
executed. **Chosen: excise all of it.** SheshAOS is 9 crates plus a headless `shesh` CLI; three
real Criterion benchmarks cover the event store, WaveObj store, and broker hot paths; the
workspace is pure Rust again.

### 4. LLM supply: local Ollama models, retire GitHub Models routing

The swarm LLM worker's dependence on the GitHub Models free tier was replaced by the local stack
(Ollama phi4-mini and qwen2.5-coder per GETTING_STARTED), with OmniRoute as the
OpenAI-compatible front. The rationale: rate limits made CI non-deterministic, while local is
deterministic and zero-cost.

### 5. Lint gates: tool-native, not grep

The "no unwrap/expect in production code" gate was a grep that could not see `#[cfg(test)]`
scope, so it flagged only false positives. **Chosen:** every crate carries
`[lints] workspace = true`; `clippy -D warnings` with `clippy.toml`'s `allow-*-in-tests` is the
enforcement. That immediately found two real production unwraps the grep never could, now fixed.

## Consequences

### Benefits

- The workspace is smaller, honest, and green under stricter gates than before.
- The Zig toolchain requirement is gone from the main build (bootstrap and CI).
- The dependency graph is generated from `cargo metadata` and pyprojects
  (`tools/depgraph.py` plus `docs/architecture/DEPENDENCY_GRAPH.md`); a CI freshness gate makes
  doc drift a build failure.

### Costs

- `shesh pty` and `shesh tui` go away — breakage accepted, no grandfathering.
- PyPI publication of `shesh-*` packages remains an open user action; until then CI tracks
  `main` of internal dependencies.

## Links

- [ADR-0001: Language Policy](0001-five-languages.md),
  [ADR-0015: Guard](0015-guard-policy.md),
  [ADR-0016: Wave](0016-kernel-consolidation.md)
- `docs/architecture/DEPENDENCY_GRAPH.md`, `tools/depgraph.py`
