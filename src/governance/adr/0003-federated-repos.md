---
title: "ADR-0003: Federate repositories behind one manifest"
type: explanation
summary: "Federate repositories behind one manifest."
audience: maintainer
status: current
verified: 2026-08-15
---

# ADR-0003: Federate repositories behind one manifest

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-08-09 |
| **Deciders** | Fleet maintainer |
| **Tags** | repo-topology, versioning, gates |

## Context

The fleet has ~20 components (audit, mind, memory, voice, desktop, etc.). A monorepo would couple Rust and Python releases, make independent versioning hard, and blow up CI (144 Hz display tests cannot run in sandbox).

The fleet needs:
- Independent semver + CI per component.
- One auditable integration point.
- Offline quality gates before promotion.

## Decision

- **Federated**: each `shesh-*` is its own repo under `gaganjainse/`, with `pyproject.toml`, `src/`, `tests/`, `ci.yml`.
- **Ecosystem repo** (`shesh-ecosystem`) holds `manifests/components.toml` — every organ declared with layer, repo, version, license, channel, provides, upstream.
- `scripts/resolve_manifest.py` validates schema + licenses, resolves versions deterministically, writes `channels/{stable,canary,devel}.lock` with SHA256.
- `scripts/check_licenses.py` refuses GPL-incompatible licenses (AGPL/SSPL only as separate service).
- `scripts/generate_mcp_config.py` emits canonical `servers.json` + Zed/Newelle configs from manifest.

## Consequences

### Benefits

- `shesh-audit` can release v0.1.0 without bumping `shesh-desktop`.
- `canary.lock` = tested combination; `stable.lock` = daily driver.
- 30 ecosystem tests offline; component tests isolated (`--confcutdir`).
- Need to sync READMEs to `docs/components/` — the project automate via doc-sync job.
- Renames require GitHub redirects (handled — shesh→shesh).

## References

- `docs/architecture/REPO_TOPOLOGY.md`
- `manifests/components.toml`, `scripts/resolve_manifest.py`
- D4 (channels)
