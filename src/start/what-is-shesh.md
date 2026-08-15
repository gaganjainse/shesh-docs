---
title: What Shesh is
type: explanation
summary: "The scope, design commitments, and non-goals of the Shesh agent system."
audience: operator
status: current
verified: 2026-08-15
---

# What Shesh is

Shesh is a local-first agent system for Arch-based Linux desktops. It integrates
a governance kernel, a set of model-driven reasoning services, and a collection
of tool servers into one auditable whole, distributed the way a small Linux
distribution is: through a component manifest, pinned versions, and promotion
between release channels.

## Design commitments

These four properties constrain every component in the fleet.

**Local by default.** Inference runs against a local model server. Network model
providers exist, but no route leaves the machine unless you enable it explicitly.
See [The cloud gateway](../explanation/cloud-gateway.md) and
[ADR-0005](../governance/adr/0005-local-first.md).

**Governed action.** Every tool call passes through a policy engine before it
executes and is recorded in an append-only, hash-chained audit log. Models
propose; the kernel disposes. See [ADR-0015](../governance/adr/0015-guard-policy.md).

**Composable components.** Each capability is a separate package exposing a
Model Context Protocol server. A component can be replaced or removed without
rebuilding the system. See [Repository topology](../explanation/repository-topology.md).

**Staged promotion.** Changes reach a daily-driver machine only after passing
the gates for each [release channel](../reference/release-channels.md). Breakage
is intended to surface in `canary`, not on the machine you depend on.

## Scope

Shesh targets a single-user Linux workstation. The reference hardware and
software baseline is documented in [Target hardware](../explanation/target-hardware.md);
the system runs on other Arch-based configurations, but only the reference
configuration is verified.

Shesh is **not** a hosted service, a multi-tenant platform, or a general-purpose
agent framework for embedding in other products. It has no authentication model
beyond the operating system's, because it assumes exactly one trusted user on
one machine. Deploying it as a shared service would be unsafe.

## Component layers

| Layer | Responsibility | Determinism | Principal components |
|---|---|---|---|
| Brain | Policy, audit, scheduling | Deterministic | `shesh-core` (audit, secrets, brain), SheshAOS |
| Mind | Planning, routing, memory | Model-driven | `shesh-memory`, `shesh-orchestrator`, `shesh-harness` |
| Soma | Sensing and acting | Deterministic | `shesh-core` tool servers, `shesh-desktop`, `shesh-voice`, `shesh-phone` |

The full list, with the repository that owns each component, is in the
[component catalogue](../reference/components.md).

## Licensing

The integrated system is distributed under GPL-3.0-or-later. Individual
components retain licences compatible with that combination; the manifest records
each component's SPDX identifier, and the dependency gate rejects incompatible
additions. Third-party upstreams and their licences are listed in
[Licences and sources](../reference/licences.md).

## Related

- [Install Shesh](install.md) — bring up the system on a supported machine.
- [The Agentic Body](../explanation/agentic-body.md) — why the Brain, Mind, and
  Soma split exists and what belongs in each layer.
- [Component catalogue](../reference/components.md) — every component, its layer,
  and its channel.
- [Security policy](../governance/security-policy.md) — the guarantees the system
  makes and the ones it does not.
