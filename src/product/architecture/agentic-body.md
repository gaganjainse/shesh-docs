# The Agentic Body: Brain, Mind, and Soma

Shesh treats an agent as a body, not a chatbot. This chapter sets out the unifying
metaphor — Mind, Brain, and Soma — that every other architecture document in the fleet
references, and it shows how those layers map to real repositories and protocols.

Think of the body the way you would think of a person. The **Mind** reasons and plans; the
**Brain** coordinates and governs; the **Soma** is the flesh that senses and acts in the
world. Shesh builds each layer as a replaceable component, then composes them into one
agent.

- **Summary**
  - The agent splits into Mind (deliberation), Brain (governance), and Soma (sensors/actuators).
  - The Brain is deterministic and local; the Mind may be nondeterministic and swappable.
  - Two protocols connect the layers: the Shesh Kernel Protocol and MCP.
  - Nothing the Mind proposes runs until the Brain validates it and writes an audit event.
  - The small models run locally; larger specialist models remain a target for bigger hardware.

---

## The three layers

The diagram shows the stack top to bottom: a slow, model-driven Mind, a fast deterministic
Brain beneath it, and the Soma where cognition meets the machine.

```text
┌─────────────────────────────────────────────────────────────┐
│  MIND — deliberative cognition                              │
│  Planner · reasoner · critic · long-term memory · theory    │
│  of self · model routing · goals. Slow, model-driven.       │
│  (SheshOS specialist models: planner / coder / vision)      │
├─────────────────────────────────────────────────────────────┤
│  BRAIN — coordination kernel (SheshAOS)                     │
│  Event store · policy/permission engine · task scheduler ·  │
│  router · audit/replay · resource budgets · tool broker.    │
│  Fast, deterministic, local. Models propose; brain disposes.│
├─────────────────────────────────────────────────────────────┤
│  SOMA — the living body (shesh-desktop + MCP + devices)      │
│  Sensors: screen, mic, files, input, phone, telemetry.      │
│  Actuators: hyprctl, shell, apps, GPU, voice, ADB phone.    │
│  The "nervous system": MCP servers, watchers, automations.  │
└─────────────────────────────────────────────────────────────┘
```

### Why split it this way

The **Mind** is allowed to be nondeterministic, slow, model-bound, and swappable — today
Gemma, Qwen, or phi4, tomorrow something else. The **Brain** must be deterministic,
auditable, crash-proof, and local. This is exactly SheshAOS: "models propose actions; the
kernel validates and records." It is the immune system — it stops the Mind from doing
damage. The **Soma** is where cognition meets the machine, and it is the largest surface.
Most of the best open-source projects (Newelle, MCP servers, computer-use agents) already
live here, so Shesh integrates them behind the Brain's policy gate rather than rebuilding
them.

---

## Mapping to the existing repositories

| Layer | Repository | Role in the body | Status |
|---|---|---|---|
| **Brain** | `SheshAOS` (12-crate Rust workspace, 981 tests) | Governance kernel: event store, policy, scheduler, router, tool broker, RPC/terminal | production-ready core, Ubuntu-targeted |
| **Mind** | `SheshOS` (SheshAOS v2) | Specialist-model routing: planner (Gemma 4 12B), coder (Qwen3-Coder 30B), vision (Qwen3.5 9B) | conceptual — see note below |
| **Brain (low-level)** | `shesha-kernel` | Alpha microkernel track; same crate family plus a protocols crate; deeper kernel design | archived |
| **Soma (desktop)** | `shesh-desktop` | CachyOS/Hyprland body: dotfiles, MCP servers, smart-organizer, GPU, automations | this ecosystem's main integration target |
| **Soma (memory)** | `rag-service` | Sensory memory: hybrid RAG (dense + BM25 + RRF) over ChromaDB | production API |
| **Mind (quality)** | `llm-eval-harness` | Reflection/self-check loop for the Mind (LLM-as-judge) | CI-ready |
| **Soma (language)** | `Vyākṛti` | A separate creative project — a Sanskrit programming language and IDE; it dogfoods the agent but is not part of the body | 123 tests |

> **Note —** `SheshOS` is an unpublished, conceptual specification (the "SheshAOS v2" mind
> design). Do not treat `gaganjainse/SheshOS` as a live, reachable upstream; the working
> mind today is `shesh-mind` plus `shesh-memory` and `shesh-orchestrator`. The kernel
> research track lives in the archived `shesha-kernel` repository.

The `SheshOS` brief targets Ubuntu/GNOME with 16 GB RAM and three large models
(12B/30B/9B). The actual machine (RTX 4050 6 GB) cannot keep those resident at once. The
ecosystem resolves this by making the **Mind layer model-routed**: on the laptop it uses
small models (phi4-mini, qwen2.5-coder:3b, moondream2), and the same protocols target the
larger SheshOS models on a future bigger box or when offloaded. The Brain does not care
which model answers.

---

## The nervous system: how the layers talk

Two protocols carry everything; everything else is an adapter.

1. **Shesh Kernel Protocol** (from `shesh-rpc`, JSON-RPC over a Unix socket) — Brain-internal
   and Brain↔Mind. Strongly typed, append-only event semantics, policy-checked.
2. **Model Context Protocol (MCP 2026-07-28)** — Brain↔Soma. Every actuator and sensor is an
   MCP server (stdio locally; HTTP only when explicitly bridged). This lets Shesh reuse the
   entire MCP ecosystem (Newelle, Goose, Hermes, pi) as interchangeable Soma organs.

The flow for "Hey Shesh, organize my downloads and switch to performance mode" runs like
this:

```text
mic (Soma) → STT (Soma/Newelle) → text
  → MIND: parse intent, propose tool calls {organize_downloads, set_power(performance)}
  → BRAIN: policy check (both auto-allowed), append events, assign task IDs
  → SOMA: MCP calls smart-organizer.organize() + system_control.set_power()
  → Soma sensors observe result (file list, powerprofilesctl)
  → MIND: formulates confirmation → TTS (Soma) → audit event committed
```

Every arrow is an event in the append-only log. Nothing the Mind proposes executes until
the Brain validates it. That governance guarantee is inherited from SheshAOS.

---

## Build order

The body grows bottom-up but is safe top-down, following `shesh-kernel`'s phased plan
(event store → kernel runtime → resource budgets → model providers → tool broker →
IPC/MCP/ACP):

1. **Soma first (this ecosystem):** make the body reliable — dotfiles, MCP servers,
   organizer, automations, voice. A body you can trust.
2. **Brain wiring:** connect Shesh's audit log to SheshAOS's event store; route MCP tool
   calls through `shesh-kernel` policy instead of Newelle executing directly.
3. **Mind specialists:** plug SheshOS model routing into `shesh-ai`'s provider abstraction;
   use `llm-eval-harness` to grade each specialist.
4. **Reflection loop:** the Mind uses the audit log plus the eval harness to propose
   improvements to skills — the "Continual Harness" idea: small, evidence-backed updates,
   never mutating the base prompt.
5. **Kernel track (research):** eBPF sensing for Soma, then `shesh-kernel` experiments on the side.

Step 1 never blocks on step 4. The body ships and is useful immediately; the Brain plugs in
behind it without changing how Soma works.

---

## Naming conventions

- **No "Jarvis".** The agent is **Shesh** (शेष) across all layers.
- **Kernel family** is the brain/kernel family (SheshAOS, shesh-kernel, shesh-* crates) —
  formerly "Nexus", renamed per Shesh canon.
- **Shesh** is the whole body and the user-facing agent (SheshOS is the mind spec; shesh-*
  are the MCP organs).
- **Soma** is the bodily/device-layer codename (soma-* sensors/actuators).
- Components we integrate keep their **upstream names** in `sources/upstream/` (attribution),
  but our forks and wrappers are renamed: `shesh-voice` (wraps Newelle voice), `shesh-files`
  (organizer), `shesh-shell`, `shesh-memory`, `shesh-phone`, and so on.
- Every MCP server is `shesh-<organ>-mcp`. Every systemd unit is `shesh-<organ>.service`.
