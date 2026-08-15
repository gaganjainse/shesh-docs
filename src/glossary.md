# Glossary

The Shesh fleet uses a small, consistent vocabulary. This chapter defines the terms so
the rest of the book can use them without repetition.

## The name

**Shesh** (शेष) derives from Shesh Naag, the many-headed serpent on which Vishnu rests —
an apt image for an agent whose "heads" are its specialist subagents. The desktop agent
and every component are spelled **shesh-** in repositories and package names, and written
**Shesh** in prose. The operating system is **SheshAOS**.

## Acronyms

| Term | Meaning |
|---|---|
| **AOS** | Agentic Operating System — the governance and runtime layer (SheshAOS) |
| **AB** | Agentic Body — the complete Brain + Mind + Soma system |
| **AM** | Agentic Mind — deliberation: models, planning, memory, learning |
| **AI** | Agentic Intelligence — the reasoning and model capability (distinct from the generic "AI") |
| **AS** | Agentic Soma — sensors and actuators (desktop, phone, tools) |
| **AP** | Agentic Physique — the hardware and device profile (for example, the MSI Sword) |
| **OS** | Operating System — the CachyOS/Linux layer beneath everything |

## The three layers of the body

The fleet organizes itself around a body metaphor, which the architecture chapters develop
in detail.

- **Brain** — the governance kernel (`shesh-audit`, `SheshAOS`): the event store, the
  policy engine, and the scheduler. Models may propose; the kernel disposes.
- **Mind** — deliberation (`shesh-mind`, `shesh-memory`, `shesh-harness`,
  `shesh-orchestrator`, `shesh-skills`): model routing, routing policy, memory, and
  self-improvement.
- **Soma** — the body (`shesh-voice`, `shesh-files`, `shesh-shell`, `shesh-system`,
  `shesh-acp`, `shesh-phone`): the sensors and actuators exposed over MCP.

## Protocols

Three protocols connect the pieces, and all three speak JSON-RPC over stdio or sockets.

- **MCP** (Model Context Protocol): agent ↔ tools.
- **ACP** (Agent Client Protocol): editor ↔ agent (for example, Zed or JetBrains).
- **A2A** (Agent2Agent): agent ↔ agent — a local bus today, remote-capable tomorrow.

## Components and products

Each `shesh-*` repository is a *component*. They integrate into the **shesh-ecosystem**
manifest and run on **shesh-desktop**, the CachyOS/Hyprland configuration that ties the
body to real hardware. A component is a part; the product is the assembled whole.
