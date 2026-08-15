---
title: How-to guides
type: how-to
summary: "An index of task-oriented guides for an installed system."
audience: operator
status: current
verified: 2026-08-15
---

# How-to guides

Each guide solves one problem on an installed system. Guides assume Shesh is
already installed; if it is not, start with [Install Shesh](../start/install.md).

Guides state what to do. The reasoning lives in
[Explanation](../explanation/index.md), and exact values live in
[Reference](../reference/index.md).

> **Note.** For confirming that an installed system behaves correctly, use the
> [verification checklist](../reference/verification-checklist.md). It covers
> first boot, secrets, tool servers, voice, GPU and power, display, backups,
> phone, containers, agent behaviour, security, and releases in one place, so
> you can work down it without changing pages.

## Configuration

- [Configure automations](configure-automations.md) — timers and device rules.
- [Configure the desktop agent](configure-the-desktop-agent.md) — the agent
  surface in the desktop shell.
- [Configure the organizer](configure-the-organizer.md) — automatic file sorting.
- [Enable cloud routing](enable-cloud-routing.md) — opt in to a network model
  provider.

## Operating

- [Recover from failure](recover-from-failure.md) — roll back a bad promotion or
  restore from backup.

## Walkthroughs

Longer flows that combine several capabilities:

- [Organize downloads](organize-downloads.md)
- [A voice-driven workflow](voice-driven-workflow.md)
- [Use semantic recall](use-semantic-recall.md)

## Contributing

- [Work on SheshAOS](work-on-sheshaos.md) — build and test the Rust kernel.

Documentation for the contributor tooling lives in
[shesh-workspace](https://github.com/gaganjainse/shesh-workspace/tree/main/docs),
alongside the tools it describes.

## Related

- [Verification checklist](../reference/verification-checklist.md) — every manual
  check, by area.
- [Component catalogue](../reference/components.md) — what each component does.
