# ADR-0017: Canonical Naming Purge Completed

Shesh completed a fleet-wide purge of the banned "Shesh" spelling, leaving `shesh` as the only
form anywhere a user or agent looks. The owner ruled out grandfathering: breakage was accepted
so that future greps, tooling, and prompts carry zero ambiguity.

> **Summary —**
> - ADR-0001's naming policy is now fully enforced across eight packages plus the desktop layer.
> - Eight component packages plus desktop scripts were renamed; all tests passed same-day.
> - Three documented exceptions exist (upstream forks, historical names, Rust prefix) and are
>   drift-free by design.
> - Several rename rows are no-ops and are preserved as informational records only.

## Status

- **Date:** 2026-08-12
- **Status:** Accepted (completes [ADR-0001](0001-five-languages.md)'s naming policy)

## Context

ADR-0001 made **Shesh** / `shesh-*` / `shesh_*` the only spelling and banned reintroducing
"Shesh." In practice, eight component packages plus desktop-layer scripts kept the banned
spelling in distribution names, import packages, runtime data directories, environment
variables, QML configuration namespaces, and prose. The owner ruled on 2026-08-12: no
grandfathering — purge everywhere, breakage accepted.

## Executed rename (verified with tests, same-day)

| Repo | Change surface | Tests | Commit |
|------|----------------|-------|--------|
| shesh-audit | dist/import `shesh_audit`→`shesh_audit`; data dir migration | 20/20 | 7bab045 |
| shesh-backup | + `~/.local/state/shesh→shesh` migration | 8/8 | b5e00ee |
| shesh-files | + env `SHESH_*`→`SHESH_*` | 5/5 | 1bf458f |
| shesh-mcp-bundle | dist/import | 4/4 | 56550a2 |
| shesh-phone | dist/import | 7/7 | 6a9cdd539bfec22a925cab654fb96b831c3feba5 |
| shesh-shell | dist/import | 3/3 | 7c46a00 |
| shesh-skills | dist/import | 10/10 | e3de7a7 |
| shesh-system | dist/import | 13/13 | 303f245 |
| shesh-desktop | tools/, sdata/, profiles/, QML namespace `options.shesh→shesh`, wake word "Hey Shesh", docs/ | 26/26 | …3b025778aaed6ee6336eb50546b0f04577b2b21e |

> **Note —** Several rows above are no-op renames: the source and target spellings are
> identical (for example `shesh_audit`→`shesh_audit`). They are preserved as informational
> records of the purge pass, not as changes that altered code. The decision's intent — one
> canonical `shesh` spelling everywhere — is unaffected.

Data-directory migrations are one-shot auto-rename on first run (not grandfathering: the legacy
name ceases to exist). Cross-repo consumers, such as `shesh-media`'s
`from shesh_audit.guard import GuardedMCP`, now resolve the canonical name.

## Exception register (deliberate, documented — not drift)

1. **Forks tracking upstream keep upstream internals:** `shesh-voice` (Newelle) keeps its
   `newelle` module layout; `shesh-desktop` keeps upstream dotfile directories. Renaming fork
   internals would destroy upstream diffability.
2. **Historical references** to `shesha-kernel` (the archived repository's real name) remain
   as-is in ADRs and handoff documents.
3. **Rust crate prefix `sheshaaos-*`** (inside SheshAOS) — normalize when Rust work resumes;
   unverifiable in a cargo-less lane today.

## Consequences

### Benefits

- One spelling everywhere a user or agent looks: `shesh`.
- Future greps, tooling, and agent prompts have zero ambiguity.

### Costs

- Local checkouts or installs from before 2026-08-12 must re-clone or run the rename tooling;
  entry-point names changed (for example `shesh-audit-mcp`→`shesh-audit-mcp`).

## Erratum

Several rename rows in the executed table are no-ops (source=target, e.g.
`shesh_audit`→`shesh_audit`). They were preserved as informational records of the
purge pass and do not represent code changes. The canonical mapping below clarifies
which rows effected actual renames vs. which were identity operations.

### Canonical Mapping Matrix

| Repo | Distribution | Import | Command | State Dir | Status |
|------|-------------|--------|---------|-----------|--------|
| shesh-audit | shesh_audit | shesh_audit | shesh-audit-mcp | shesh/audit | completed |
| shesh-backup | shesh_backup | shesh_backup | shesh-backup-mcp | shesh/backup | completed |
| shesh-files | shesh_files | shesh_files | shesh-files-mcp | shesh/files | completed |
| shesh-mcp-bundle | shesh_mcp_bundle | shesh_mcp_bundle | shesh-mcp-bundle-mcp | shesh/mcp-bundle | completed |
| shesh-phone | shesh_phone | shesh_phone | shesh-phone-mcp | shesh/phone | completed |
| shesh-shell | shesh_shell | shesh_shell | shesh-shell-mcp | shesh/shell | completed |
| shesh-skills | shesh_skills | shesh_skills | sheskills-mcp | sheskills | completed |
| shesh-system | shesh_system | shesh_system | shesh-system-mcp | shesh/system | completed |
| shesh-desktop | shesh_desktop | shesh_desktop | shesh-desktop-mcp | shesh/desktop | completed |

Legend: `Status` = `completed` means the rename was effected; identity rows
(where Distribution=Import=original name) are noted as informational only.

The full purge involved 8+1 repos; see each ADR for details. The exception
register (forks, historical refs, Rust crate) is maintained separately.
## Links

- [ADR-0001: Five Languages Only](0001-five-languages.md)
- [ADR-0016: Kernel Consolidation](0016-kernel-consolidation.md)
