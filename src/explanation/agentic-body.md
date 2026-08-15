---
title: The Agentic Body
type: explanation
summary: "Why Shesh separates governance, reasoning, and action into three layers, and what belongs in each."
audience: operator
status: current
verified: 2026-08-15
---

# The Agentic Body

Shesh is structured around one organising idea: an agent is not a chat interface
with tools attached, but a system with distinct faculties that have incompatible
requirements. Reasoning must be free to be slow and uncertain. Action must be
constrained and recorded. Conflating the two produces a system that is neither
capable nor safe.

The system therefore separates into three layers — Brain, Mind, and Soma. Every
other architecture document refers back to this division.

## The three layers

| Layer | Responsibility | Required properties | Implementation |
|---|---|---|---|
| **Mind** | Planning, reasoning, critique, memory, model routing | May be slow, non-deterministic, and replaceable | `shesh-memory`, `shesh-orchestrator`, `shesh-harness` |
| **Brain** | Policy, audit, scheduling, resource budgets, tool brokering | Must be fast, deterministic, local, and crash-safe | `shesh-core` (audit, secrets, brain), SheshAOS |
| **Soma** | Sensing and acting on the machine and connected devices | Must be explicit about capability and revocable | `shesh-core` tool servers, `shesh-desktop`, `shesh-voice`, `shesh-phone` |

The governing rule between them is that **the Mind proposes and the Brain
disposes**. A model never invokes a tool directly. It emits a proposed action;
the Brain evaluates that action against policy, executes it if permitted, and
appends the outcome to an append-only log.

## Why the layers are separated

**The Mind is allowed to be unreliable.** Model output is probabilistic, models
are swapped as better ones appear, and a plan may be wrong. Treating the
reasoning layer as untrusted is what makes it safe to use small local models: a
bad proposal is rejected rather than executed.

**The Brain must be trustworthy.** It is deterministic code with no model in the
path. It answers one question — may this action proceed — and records the answer.
Because it is deterministic, its behaviour can be tested, replayed from the event
log, and audited after the fact. Placing a model inside this layer would forfeit
every one of those properties.

**The Soma is the largest surface and the least novel.** File access, shell
execution, screen capture, and device control are solved problems with mature
implementations. Shesh integrates existing tools behind the policy gate rather
than reimplementing them. Each capability is a separate process exposing a Model
Context Protocol server, so a compromised or faulty tool is contained by process
boundaries and by the policy applied to its calls.

## How the layers communicate

Two protocols carry all traffic between layers; everything else is an adapter.

**Model Context Protocol** connects the Brain to the Soma. Every sensor and
actuator is an MCP server speaking JSON-RPC over standard input and output. Using
a published protocol rather than an internal interface means third-party servers
work without modification, and Shesh servers work in other MCP clients.

**The kernel protocol** connects Brain-internal components and the Brain to the
Mind. It carries typed, policy-checked, append-only event semantics.

Network transports are not used for local communication. Process boundaries with
standard input and output avoid opening a listening socket for a single-user
system. [Agent protocols](protocols.md) covers the full protocol layering,
including the Agent Client Protocol used by editors.

## A request end to end

Consider the spoken instruction "organise the downloads and switch to performance
mode".

1. **Soma** captures audio and transcribes it to text.
2. **Mind** parses the intent and proposes two actions: organise the downloads
   directory, and set the power profile to performance.
3. **Brain** evaluates each proposed action against policy, assigns task
   identifiers, and appends a pending event for each.
4. **Soma** executes the permitted calls through the relevant MCP servers.
5. **Brain** records each outcome in the audit log.
6. **Mind** composes a confirmation, which the Soma speaks.

Every arrow is an event in the log. Nothing the Mind proposes runs before the
Brain validates it, and every executed action leaves a record whose hash chain
can be verified afterwards. This is the system's central safety guarantee; see
[ADR-0015](../governance/adr/0015-guard-policy.md).

## Model sizing is a Mind concern

The Brain is indifferent to which model answers. That indifference is what lets
the same system run on a laptop with limited video memory and on a larger machine
with several resident models. On constrained hardware the Mind routes to small
specialised models and keeps one resident at a time; on a larger host it routes
to larger models over the same interfaces. No other layer changes.

The current model assignments are listed in [Models](../reference/models.md).

## Build order

The layers were built from the bottom up, but the safety properties were designed
from the top down:

1. **Soma** — make the body reliable first. A trustworthy set of tools is useful
   on its own.
2. **Brain** — route every tool call through the policy engine and the event log
   rather than letting clients execute directly.
3. **Mind** — add planning, routing, and memory on top of the governed tool
   surface.
4. **Refinement** — use the audit log and the evaluation harness to improve
   behaviour, with changes gated on measured outcomes.

Work on a later stage never blocks an earlier one, because each stage is useful
before the next exists.

## Naming

The agent is called Shesh at every layer. Repositories and packages are
lowercase and hyphenated, such as `shesh-memory`. Every tool server command ends
in `-mcp`, such as `shesh-system-mcp`, and every service unit is named
`shesh-<organ>.service`. Integrated upstream projects keep their own names where
they are vendored, and the licence and attribution are recorded in
[Licences and sources](../reference/licences.md). Naming rules are fixed by
[ADR-0017](../governance/adr/0017-naming-purge-completed.md).

## Related

- [Repository topology](repository-topology.md) — how these layers map onto
  repositories and how changes are promoted.
- [Agent protocols](protocols.md) — the protocols named above, in detail.
- [Multi-agent orchestration](multi-agent.md) — how the Mind divides work between
  specialised agents.
- [Memory and learning](memory-and-learning.md) — how the Mind retains and
  retrieves context.
- [SheshAOS](sheshaos.md) — the Rust implementation of the Brain.
