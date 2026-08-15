# ADR-0003: Federated Repos + Manifest, Not Monorepo

Shesh organizes its roughly twenty components as independent repositories tied together by a
single manifest, not as one monorepo. That choice lets each organ version and ship on its own
while a shared lockfile keeps the integrated whole auditable and testable before promotion.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** repo-topology, versioning, gates

## Context

The fleet spans about twenty components — audit, mind, memory, voice, desktop, and more. A
monorepo would couple the Rust and Python releases, make independent versioning awkward, and
inflate continuous integration (a 144 Hz display test cannot run in a sandbox).

Three needs shaped the decision: independent semantic versioning and CI per component, one
auditable integration point, and offline quality gates applied before promotion.

## Decision

- **Federated:** each `shesh-*` lives in its own repository under `gaganjainse/`, with a
  `pyproject.toml`, `src/`, `tests/`, and `ci.yml`.
- The **ecosystem repository** (`shesh-ecosystem`) holds `manifests/components.toml`, where
  every organ is declared with its layer, repo, version, license, channel, what it provides,
  and its upstream.
- `scripts/resolve_manifest.py` validates the schema and licenses, resolves versions
  deterministically, and writes `channels/{stable,canary,devel}.lock` with SHA256 hashes.
- `scripts/check_licenses.py` refuses GPL-incompatible licenses (AGPL or SSPL only as a
  separate service). The fleet body is **GPL-3.0-or-later**.
- `scripts/generate_mcp_config.py` emits the canonical `servers.json` plus Zed and Newelle
  configurations from the manifest.

## Consequences

### Benefits

- `shesh-audit` can release v0.1.0 without bumping `shesh-desktop`.
- `canary.lock` is the tested combination; `stable.lock` is the daily driver.
- Thirty ecosystem tests run offline, and component tests stay isolated (`--confcutdir`).

### Costs

- READMEs must sync into `docs/components/`; a doc-sync job automates that.
- Renames require GitHub redirects, handled by the existing `shesh` → `shesh` mapping.

## Links

- `docs/architecture/REPO_TOPOLOGY.md`
- `manifests/components.toml`, `scripts/resolve_manifest.py`
- [ADR-0019: shesh-core Monorepo](0019-shesh-core-monorepo.md) for the later consolidation
  of the smallest organs
