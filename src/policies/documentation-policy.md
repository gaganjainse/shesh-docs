# Documentation Policy — Single Source of Truth, Ownership, Gates

Documentation rot begins the moment two files claim to own the same topic. This chapter sets
the canonical home for every content class and the gates that keep the book consistent.

- One topic, one home; duplicates become pointer stubs so links never rot.
- Governed docs carry front matter: title, status, and last-verified date.
- Every behavior claim follows the tell-triple: STATED / VERIFIED / EVIDENCE.
- CI enforces links, naming, and the one-way mirror into the mdBook build.

## Research basis

The policy follows docs-as-code with a hybrid topology — decentralized authoring, centralized
governance — the pattern Grab and Pinterest validated. The single source of truth per topic is
enforced by automation rather than by memory.

## Canonical homes

| Content class | Canonical home | Notes |
|---|---|---|
| Cross-cutting decision or policy | `shesh-ecosystem/docs/` (+ `docs/policies/`) | shesh-docs renders these |
| Component behavior or usage | the component repo's README (+ its `docs/` when large) | ecosystem links, never copies prose |
| Security posture or reporting | `SECURITY.md` here; `THREAT_MODEL.md`; `RECOVERY.md` | components link, do not restate |
| Immutable history | `docs/history/adr/*`, `docs/history/queries/QUERYLOG.md`, `docs/history/audits/*` | records, never rewritten; links or names may be repaired |
| Session state | `TODO.md` + SESSION docs | fused 2026-08-13: one state doc family |
| Rendered, user-facing | shesh-docs (mdBook) | populated ONLY by `scripts/sync-docs.sh` — never hand-edit `src/` |

## The rules

1. **One topic, one home.** Duplicates are merged by fusion; the loser becomes a pointer stub
   so inbound links never rot.
2. **Front matter on governed docs** (`docs/policies`, `THREAT_MODEL`, `RECOVERY`, `SECURITY`):
   title, status (`living` | `frozen` | `archived`), and last-verified date. History classes
   (adr, queries, audits, attic) are exempt by definition.
3. **The tell-triple for claims:** STATED / VERIFIED / EVIDENCE — a behavior claim names its
   gate or test. An undated "works" claim is a bug.
4. **Links:** relative links resolve through the mirror (sync-docs copies subtrees);
   cross-repo references use absolute `github.com` URLs. CI gates: ecosystem linkcheck plus
   shesh-docs strict check; orphans are reported.
5. **Naming canon:** Shesh uppercase in prose, `shesh-*` kebab repos, `SHESH_SNAKE` for
   environment variables; no legacy names outside immutable history (`rename_sweep2.py` plus
   the docs gate).
6. **Archive-not-delete for docs too:** obsolete docs move to `docs/history/attic/` with a
   pointer, never vanish unlinked.
7. **Docs change with code:** a pull request that changes behavior updates its doc in the same
   commit (docs that claim behavior get gates where feasible).

## Maintenance machinery

The machinery exists today and runs in CI:

- `tools/linkcheck.py` — internal-link integrity (it found 21 rot spots on adoption).
- `tools/rename_sweep2.py` — canonical-name enforcement.
- `tools/docs_index.py` — regenerates `docs/INDEX.md` and reports orphans.
- `scripts/sync-docs.sh` — one-way mirror into mdBook; REQUIRED/OPTIONAL with loud skips;
  render target overridable via `DOCS_REPO`.
- Dependabot plus canary CI — keeps the machinery itself from rotting.

> **Tip —** If you are tempted to copy a policy paragraph into a component README, link instead.
> A copy is a future contradiction waiting to happen.
