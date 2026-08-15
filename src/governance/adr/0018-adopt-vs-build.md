---
title: "ADR-0018: Prefer a maintained upstream over building"
type: explanation
summary: "Prefer a maintained upstream over building."
audience: maintainer
status: current
verified: 2026-08-15
---

# ADR-0018: Prefer a maintained upstream over building

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-08-12 |
| **Deciders** | Fleet maintainer |
| **Tags** | strategy, dependencies, architecture, cleanup |

## Context

The renovation surfaced a recurring question — build its own or adopt the
web-best? — plus a barrel of pre-commit archaeology: crates, directories and
fallback paths that the already-adopted architecture had made dead weight but
that nobody had physically removed. This ADR records each adopt-vs-build call
and the resulting excision.

## Decision

_Not recorded._

## Consequences

### Benefits

- Workspace is smaller, honest, and green under stricter gates than before.
- Zig toolchain requirement eliminated from the main build (bootstrap + CI).
- Dependency graph is generated from `cargo metadata`/pyprojects
- (`tools/depgraph.py` + `docs/architecture/DEPENDENCY_GRAPH.md`); a CI
- freshness gate makes doc drift a build failure.
- `shesh pty`/`shesh tui` go away — breakage accepted, no grandfathering.
- PyPI publication of `shesh-*` packages remains an open user action;
- until then CI tracks `main` of internal deps.

## References

- ADR-0001 (language policy), ADR-0015 (guard, updated), ADR-0016 (Wave)
- `docs/architecture/DEPENDENCY_GRAPH.md`, `tools/depgraph.py`
