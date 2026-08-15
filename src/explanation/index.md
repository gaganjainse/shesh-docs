---
title: Architecture
type: explanation
summary: "An index of the chapters that explain how Shesh is designed and why."
audience: operator
status: current
verified: 2026-08-15
---

# Architecture

These chapters explain the reasoning behind the system's structure. They describe
why components are separated the way they are, which guarantees each layer
provides, and which trade-offs were accepted. For instructions, use the
[how-to guides](../how-to/index.md); for exact values, use
[Reference](../reference/index.md).

## Core model

- [The Agentic Body](agentic-body.md) — the Brain, Mind, and Soma layers, what
  belongs in each, and why governance is kept separate from reasoning.
- [Repository topology](repository-topology.md) — why the code is distributed
  across many repositories, how upstream forks are tracked, and how components
  are promoted.
- [Language policy](language-policy.md) — the permitted implementation languages
  and the process-boundary rule that keeps them from interfering.

## Runtime behaviour

- [Agent protocols](protocols.md) — how the Model Context Protocol, Agent Client
  Protocol, and Agent2Agent protocol layer together.
- [Multi-agent orchestration](multi-agent.md) — agent roles, budgets, delegation,
  and the limits placed on autonomy.
- [Memory and learning](memory-and-learning.md) — the memory hierarchy, habit
  formation, and how context is assembled within a token budget.
- [Ambient behaviour](ambient-behaviour.md) — when the system offers to act on
  its own and the constraints on interruption.

## Environment

- [Isolation model](isolation-model.md) — rootless containers and Python
  environment separation.
- [Filesystem layout](filesystem-layout.md) — where configuration, state, and
  logs are written.
- [Disk layout](disk-layout.md) — subvolume and partition arrangement.
- [Target hardware](target-hardware.md) — the reference machine and the
  constraints it imposes.
- [The desktop layer](desktop-layer.md) — the shell, its upstream, and the Shesh
  overlay.

## Adjacent systems

- [SheshAOS](sheshaos.md) — the Rust governance kernel.
- [SheshAOS architecture](sheshaos-architecture.md) — its layers and event model.
- [The cloud gateway](cloud-gateway.md) — how optional network model providers
  are reached, and why they are off by default.

## Related

- [Architecture decision records](../governance/adr/index.md) — the dated record
  of each load-bearing decision, including the ones since superseded.
- [Component catalogue](../reference/components.md) — every component, its layer,
  and its owning repository.
