# ADR-0019: Fold sub-service shesh-* modules into shesh-core monorepo

Shesh folded its sixteen smallest `shesh-*` Python modules into one repository, `shesh-core`,
so a patch to a tiny organ no longer means editing sixteen repositories. The fleet keeps
federation where it earns its keep — genuinely independent services — and consolidates where a
"module" was really just a file wearing a repository's clothes.

> **Summary —**
> - Twenty-two `shesh-*` Python repos became six component repos plus domain repos.
> - The sixteen smallest sub-service modules fold into one `shesh-core` repo, command names
>   unchanged so existing MCP client configs keep working.
> - The folded repos are archived and made read-only; they are deprecated and archive-only.
> - The kept services now depend on a single `shesh-core>=0.1` instead of many packages.
> - The manifest still declares the organs; only their `repo` field now points at `shesh-core`.

## Status

- **Date:** 2026-08-13
- **Status:** Accepted
- **Tags:** architecture, federation, packaging, drift

## Context

The fleet had 22 `shesh-*` Python repositories. Fifteen carried under about 460 lines of
source each, yet each re-carried its own `pyproject.toml`, CI workflow, `SECURITY.md`, and
`dependabot.yml` — with subtle drift between them:

- ruff configurations differed (some `extend-select=["BLE","TRY"]`, some not; some added
  `select` or `ignore` on top).
- `shesh-files` had no console script, yet the MCP config generator emitted a nonexistent
  `shesh-files-mcp` command.
- Cross-repo dependencies (`shesh-audit>=0.1`, `shesh-mind>=0.1`) cannot resolve from PyPI, so
  the manifest and lock system must build them from git — fragile for anyone but the owner.

Federation ([ADR-0003](0003-federated-repos.md)) is the right call for **independently versioned
services**. A 150-line module is not a service; it is a file.

## Decision

Consolidate the sixteen sub-service modules plus the Wave configuration into one repository,
**`shesh-core`**:

- One `pyproject.toml` ships all sixteen packages (`shesh_audit`, `shesh_secrets`, `shesh_brain`,
  `shesh_mind`, `shesh_shell`, `shesh_system`, `shesh_files`, `shesh_media`, `shesh_messaging`,
  `shesh_calendar`, `shesh_backup`, `shesh_containers`, `shesh_ebpf`, `shesh_skills`,
  `shesh_mcp_bundle`, `shesh_acp`) plus the fifteen MCP console scripts — **command names
  unchanged**, so every existing MCP client configuration keeps working.
- One ruff configuration, one CI, one license (**GPL-3.0-or-later**), one `SECURITY.md`.
- The folded repositories are archived with a "superseded by shesh-core" banner. They are
  deprecated and **archive-only**: read their history, but do not build or ship from them.

Keep as separate repositories (genuinely independent services):
`shesh-memory`, `shesh-orchestrator`, `shesh-harness`, `shesh-phone`, `shesh-omniroute`,
plus the domain repositories `shesh-desktop`, `shesh-voice`, `shesh-docs`, and
`shesh-ecosystem`.

> **Warning —** The original record listed `shesh-omniroute` as MIT-licensed. That conflicts
> with the GPL-3.0-or-later baseline established by the 2026-08-15 fleet audit, which states
> the Shesh body is GPL-3.0-or-later and that no MIT claim should stand. The omniroute license
> requires verification; treat it as uncertain until confirmed, and do not rely on it as a
> fleet-wide license statement.

The kept services now depend on `shesh-core>=0.1` (one dependency instead of both `shesh-audit`
and `shesh-mind`). Import paths are unchanged because core ships the same top-level packages.

## Consequences

- Twenty-two repositories become six component repos (plus domain repos). One repository to
  patch for the small organs instead of sixteen.
- Cross-repo Python dependencies reduce to a single `shesh-core` (still git-resolved through the
  manifest and lock, but now one edge instead of many).
- The manifest keeps the 23 component *organs* — brain, mind, and soma declarations, `provides`,
  and channels — only their `repo` field now points at `gaganjainse/shesh-core`.
  `fetch-components.sh` clones each repository once and symlinks shared components; `install.sh`
  installs only unique repositories.
- The folded repositories' history is preserved — archived, not deleted.

## Links

- [ADR-0003: Federated Repos + Manifest](0003-federated-repos.md)
- [ADR-0018: Adopt-vs-Build](0018-adopt-vs-build.md)
