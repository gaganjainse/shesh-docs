---
title: Repository topology
type: explanation
summary: "Why Shesh is distributed across many repositories, and how changes move from upstream to a working machine."
audience: operator
status: current
verified: 2026-08-15
---

# Repository topology

Shesh is distributed the way a Linux distribution is. Upstream projects are
tracked in forks, capabilities are packaged as components, components are pinned
together by a manifest, and the resulting combination is promoted through release
channels before it reaches a machine anyone depends on.

The purpose of this structure is to stay current with upstream work while keeping
a filter at every layer, so that a change upstream cannot break a working desktop
without first failing a gate.

## The five layers

```
① UPSTREAM FORKS          (mirrors of external projects, track main/default)
        │  cherry-pick / rebase our patches
        ▼
② COMPONENT REPOS        (one per Shesh organ; our code + vendored fork pins)
        │  tagged releases, semver, individually tested
        ▼
③ ECOSYSTEM INTEGRATION  (shesh-ecosystem: manifests pin component versions)
        │  built together, full integration tests → "canary"
        ▼
④ CANARY REPO            (shesh-ecosystem:canary branch — daily build, bleeding edge)
        │  soak on a spare machine/VM for N days; gates pass
        ▼
⑤ STABLE / DOTFILES      (shesh-desktop:main — your actual machine, production)
```

### Upstream forks

Each external dependency is forked, with project patches kept on a separate
branch. Automation opens a pull request when upstream advances, rebases the patch
branch, and runs the upstream test suite. Divergence is kept minimal and each
patch carries a reason; patches that are generally useful are offered upstream.
Nothing at this layer runs on a user's machine directly.

### Component repositories

A component is a capability with its own tests and its own release cadence.

[ADR-0019](../governance/adr/0019-shesh-core-monorepo.md) narrowed this layer
considerably. Sixteen modules that had one repository each were folded into
`shesh-core`, because a module of a few hundred lines is not a service: it was
carrying a build configuration, a continuous integration workflow, a security
policy, and a dependency-update configuration that all drifted apart from their
siblings. Federation remains correct for genuinely independent services and is
now applied only to those.

The current component repositories are listed in the
[component catalogue](../reference/components.md), which is generated from the
manifest. In summary:

| Repository | Contents |
|---|---|
| `shesh-core` | The consolidated tool servers and the governance primitives |
| `shesh-memory` | Hierarchical memory and habit learning |
| `shesh-orchestrator` | Multi-agent runtime and role definitions |
| `shesh-harness` | Skill lifecycle and refinement |
| `shesh-phone` | Android device control |
| `shesh-omniroute` | Network model gateway wrapper |
| `shesh-voice` | Speech input and output |
| `shesh-desktop` | Desktop shell and device profile |

Repositories that were folded into `shesh-core` are archived rather than deleted,
so their history remains reachable. They should not be installed; the console
script names they provided are now provided by `shesh-core`.

### Ecosystem integration

`shesh-ecosystem` holds the manifest that pins every component to a version, and
the scripts that resolve it. Resolution validates the manifest, checks that every
component's licence is compatible with the combined distribution, verifies the
pinned revisions, and writes a lockfile. This is where the combination is decided.

Integration tests at this layer verify that components work together, rather than
that each works alone.

### Canary and stable

The canary channel is built from the component versions that pass their own tests
and the integration suite. It is intended for a virtual machine, a spare device,
or a secondary account.

A canary build reaches stable only after soaking without regressions and passing
a manual sign-off. Installing a stable release takes a filesystem snapshot first,
so a promotion can be reversed. See
[Release channels](../reference/release-channels.md) and
[Promote a release](../reference/verification-checklist.md).

## Gates

Each layer has a gate that blocks promotion. Every gate is a script that runs
locally and in continuous integration; nothing is promoted by hand past a failing
gate.

| Layer | Gate |
|---|---|
| Fork | Upstream tests pass, patch branch rebases cleanly, licence check |
| Component | Unit tests, lint, no known vulnerabilities in dependencies |
| Ecosystem | Integration tests in a container, manifest resolves, tool-server smoke tests |
| Canary | Soak period, hardware checks for display, GPU, and audio, no failed service units |
| Stable | Manual sign-off and a rollback snapshot before applying |

## The manifest as the single source of truth

`manifests/components.toml` declares every component with its repository,
version, licence, upstream, and the capabilities it provides:

```toml
[component.shesh-voice]
repo    = "gaganjainse/shesh-voice"
version = "1.4.5-sesha1"
license = "GPL-3.0"
upstream = { name = "Newelle", repo = "qwersyk/Newelle", ref = "1.4.5" }
provides = ["mcp:voice", "wakeword", "stt", "tts"]
```

Documentation pages that list components are generated from this file rather than
maintained by hand, so the catalogue cannot drift from the manifest. The field
definitions are in [Manifest schema](../reference/manifest-schema.md).

## Why the structure stays manageable

The obvious objection to many repositories is that maintenance grows without
bound. Four properties keep it bounded:

- **Upstream does most of the work.** Shesh tracks projects rather than
  reimplementing them, so the maintained surface is the patch set, not the
  dependency.
- **Components are independent.** A component can be paused or removed without
  stopping the rest of the system.
- **Gates are automated.** Routine rebasing and testing run without intervention;
  only failures need attention.
- **Consolidation is applied when federation stops paying.** ADR-0019 is the
  precedent: when per-repository overhead exceeded the benefit of independent
  versioning, the repositories were merged.

## Related

- [The Agentic Body](agentic-body.md) — the layers these repositories implement.
- [Release channels](../reference/release-channels.md) — the promotion filters.
- [Component catalogue](../reference/components.md) — the current component list.
- [Fork maintenance](../governance/fork-maintenance.md) — how forks are kept current.
- [ADR-0003](../governance/adr/0003-federated-repos.md) and
  [ADR-0019](../governance/adr/0019-shesh-core-monorepo.md) — the federation
  decision and its later narrowing.
