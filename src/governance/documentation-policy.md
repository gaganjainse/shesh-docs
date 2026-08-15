---
title: Documentation Policy
type: reference
summary: "Research basis: docs-as-code with a hybrid topology (decentralized authoring,."
audience: maintainer
status: current
verified: 2026-08-15
---

# Documentation Policy

Research basis: docs-as-code with a hybrid topology (decentralized authoring,
centralized governance) — the pattern Grab/Pinterest validated; single source
of truth per topic, enforced by automation rather than memory.

## Canonical homes (the map every agent applies)
| Content class | Canonical home | Notes |
|---|---|---|
| Cross-cutting decision/policy | `shesh-ecosystem/docs/` (+ `docs/policies/`) | shesh-docs renders these |
| Component behavior/usage | the component repo's README (+ its docs/ when big) | ecosystem links, never copies prose |
| Security posture/reporting | `SECURITY.md` here; THREAT_MODEL.md; RECOVERY.md | components link, does not restate |
| Immutable history | `shesh-docs-archive` and `governance/adr/*` | records, never rewritten; links and names may be repaired |
| Session state | TODO.md + SESSION docs | fused 2026-08-13: one state doc family |
| Rendered/user-facing | shesh-docs (mdbook) | populated ONLY by scripts/sync-docs.sh — never hand-edit src/ |

## Rules
1. **One topic, one home.** Duplicates are merged by fusion; the loser
   becomes a pointer stub so inbound links never rot.
2. **Front matter on governed docs** (docs/policies, THREAT_MODEL, RECOVERY,
   SECURITY): title, status (living|frozen|archived), last-verified date.
   History classes (adr/queries/audits/attic) are exempt by definition.
3. **The tell-triple for claims:** STATED / VERIFIED / EVIDENCE — a behavior
   claim names its gate or test. Undated "works" claims are bugs.
4. **Links:** relative links resolve through the mirror (sync-docs copies
   subtrees); cross-repo references use absolute github.com URLs. CI gates:
   ecosystem linkcheck + shesh-docs strict check; orphans are reported.
5. **Naming canon:** SHESH uppercase in prose, `shesh-*` kebab repos,
   SHESH_SNAKE for env vars; no legacy names outside immutable history
   (rename_sweep2.py + docs gate).
6. **Archive, do not delete:** obsolete documents move to the [shesh-docs-archive](https://github.com/gaganjainse/shesh-docs-archive) repository
   with a pointer, never vanish unlinked.
7. **Docs change with code:** a PR that changes behavior updates its doc in
   the same commit (docs-that-claim get gates where feasible).

## Maintenance machinery (exists today, runs in CI)
- `tools/linkcheck.py` — internal-link integrity (found 21 rot spots on adoption).
- `tools/rename_sweep2.py` — canonical-name enforcement.
- `tools/docs_index.py` — regenerates docs/INDEX.md + reports orphans.
- `scripts/sync-docs.sh` — one-way mirror into mdbook; REQUIRED/OPTIONAL with
  loud skips; render target overridable via DOCS_REPO.
- Dependabot + canary CI — keeps the machinery itself from rotting.
