---
title: Introduction
type: explanation
summary: "What Shesh is, how this book is organised, and where to start reading."
audience: operator
status: current
verified: 2026-08-15
hardware_verified: no
---

# Introduction

Shesh is a local-first agent system for Arch-based Linux desktops. It runs a set
of cooperating processes that observe the machine, reason about what you are
doing, and act on your behalf through audited tool calls. Everything runs on your
own hardware by default; network model providers are opt-in.

This book is the single documentation source for the whole fleet. Each component
repository carries a README describing how to build and run that component; the
conceptual material, operating procedures, reference tables, and governance
records live here.

## What the system does

Shesh is organised as three layers, described in detail in
[The Agentic Body](../explanation/agentic-body.md):

- **Brain** — a deterministic governance kernel. It holds the policy engine, the
  append-only audit log, and the scheduler. Models propose actions; the Brain
  decides whether they run and records the outcome.
- **Mind** — the deliberative layer. Planning, model routing, memory, and
  self-improvement live here. It is allowed to be slow and non-deterministic.
- **Soma** — sensors and actuators. Files, shell, system state, the desktop
  shell, voice, and a connected phone, each exposed as a Model Context Protocol
  server.

Components communicate over three protocols: the Model Context Protocol between
agents and tools, the Agent Client Protocol between editors and agents, and the
Agent2Agent protocol between agents. [Agent protocols](../explanation/protocols.md)
explains the layering.

## How this book is organised

The book follows the [Diátaxis](https://diataxis.fr/) framework. Each part serves
one kind of need, and a page belongs to exactly one part.

| Part | Use it when you want to | Type |
|---|---|---|
| [Start here](reading-guide.md) | Install the system and run it once | Tutorial |
| [Explanation](../explanation/index.md) | Understand why the system is shaped this way | Explanation |
| [How-to guides](../how-to/index.md) | Accomplish a specific task | How-to |
| [Reference](../reference/index.md) | Look up an exact fact, flag, or field | Reference |
| [Governance](../governance/security-policy.md) | Understand the rules and past decisions | Reference |

Two companion repositories hold material that is deliberately not in this book:
[shesh-workspace](https://github.com/gaganjainse/shesh-workspace/tree/main/docs)
documents the contributor tooling, next to the tools themselves, and
[shesh-docs-archive](https://github.com/gaganjainse/shesh-docs-archive) preserves
superseded audits, incident reports, and decision logs. Archived pages are
records, not guidance; they are not maintained and may contradict the current
system.

## Reading paths

- **New to Shesh:** [What Shesh is](what-is-shesh.md) →
  [Install Shesh](install.md) → [The Agentic Body](../explanation/agentic-body.md).
- **Operating an installed system:** [How-to guides](../how-to/index.md) and the
  [verification checklist](../reference/verification-checklist.md).
- **Contributing code:** [Development environment](https://github.com/gaganjainse/shesh-workspace/blob/main/docs/index.md) and
  the [architecture decision records](../governance/adr/index.md).
- **Assessing the security posture:** [Security policy](../governance/security-policy.md)
  and [Threat model](../governance/threat-model.md).

## Conventions

Every page declares its type, audience, and a `verified` date in its front
matter. The `verified` date is when a maintainer last checked the page's claims
against the committed code. A page whose claims cannot be verified against code
is moved to History rather than left in place.

Documentation is written to the [style guide](https://github.com/gaganjainse/shesh-docs/blob/main/STYLEGUIDE.md),
which the continuous integration pipeline enforces.

## Related

- [What Shesh is](what-is-shesh.md) — the system in one page, with its scope and
  non-goals.
- [Glossary](glossary.md) — terms and acronyms used throughout the book.
- [Repository topology](../explanation/repository-topology.md) — why the code is
  split across many repositories and which ones matter.
