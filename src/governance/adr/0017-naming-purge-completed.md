---
title: "ADR-0017: Fix one naming convention across the fleet"
type: explanation
summary: "Fix one naming convention across the fleet."
audience: maintainer
status: current
verified: 2026-08-15
---

# ADR-0017: Fix one naming convention across the fleet

| | |
|---|---|
| **Status** | Accepted (completes ADR-0001's naming policy) |
| **Date** | 2026-08-12 |
| **Deciders** | Fleet maintainer |

## Context

ADR-0001/§Naming made **Shesh** / `shesh-*` / `shesh_*` the only spelling and
banned reintroducing "Shesh". In practice, 8 component packages plus desktop-layer
scripts kept the banned spelling in distribution names, import packages, runtime
data dirs, env vars, QML config namespaces and prose. The owner ruled on
2026-08-12: **no grandfathering — purge everywhere, breakage accepted.**

## Decision

_Not recorded._

## Consequences

### Benefits

- One spelling everywhere a user/agent looks: `shesh`.
- Future greps, tooling, and agent prompts have zero ambiguity.
- Local checkouts/installs from before 2026-08-12 must re-clone or run the
- rename tooling; entry-point names changed (`shesh-audit-mcp`→`shesh-audit-mcp`).
