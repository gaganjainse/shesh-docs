# Multi-Agent and Orchestration Architecture

Shesh runs several agents at once without becoming an unobservable swarm. This chapter
explains how it borrows useful ideas from the Prime Agent RLM model, CrewAI-style role
crews, and Google's A2A for inter-agent messaging — while keeping governance in the Brain
(SheshAOS) and execution local-first.

- **Summary**
  - Three protocols point in three directions: ACP (editor↔agent), MCP (agent↔tools), A2A (agent↔agent).
  - Roles are configurations of one binary, not separate programs.
  - The Continual Harness edits supplemental state only; the base prompt stays immutable.
  - Autonomy is bounded by token, time, and turn budgets, never an unbounded loop.
  - Refine cannot touch policies, safety-governance skills, or the audit config.

---

## Three protocols, three directions

```text
        ACP (editor <-> agent)                 MCP (agent <-> tools)
 Zed/JetBrains ----> shesh-acp --┐
                                  ├──> shesh-orchestrator ---> MCP servers
 Newelle (voice/chat) ------------┘           |
                                            ---> child agents (RLM)
 A2A (agent <-> agent) <----------------------┘
```

- **ACP:** the editor launches an agent; the agent streams edits and permissions back. (P0)
- **MCP:** every agent calls tools through the same servers. (done)
- **A2A:** agents message other agents across a local bus, optionally remote. (P1)

See [ACP & A2A Integration](acp-a2a.md) for the protocol details.

---

## Agent roles: the Shesh crew

| Role | Model (6 GB safe) | Responsibility |
|---|---|---|
| **coordinator** | phi4-mini | Routes tasks, spawns subagents, enforces policy/audit |
| **planner** | phi4-mini | Decomposes goals into steps |
| **coder** | qwen2.5-coder:3b | Edits code, runs tests, produces diffs (ACP) |
| **researcher** | phi4-mini | web search/fetch, summarizes with citations |
| **vision** | moondream2 | screenshots/OCR/GUI understanding |
| **critic** | phi4-mini | Reviews outputs, gates promotion (eval harness) |

Roles are *configurations*, not separate programs: one binary with a role, a model, and a
tool allow-list.

---

## The RLM pattern (from Prime Agent)

The coordinator treats context as variables and subagents as function calls:

```python
# pseudocode — the Recursive Language Model style
plan = rlm("break this goal into steps", role="planner")
for step in plan:
    result = rlm(step, role=role_for(step), tools=tools_for(step))
    audit.log(step, result)
    if needs_review(step):
        critic.review(result)   # human or automated gate
```

Properties we adopt:

- **Persistent control environment** (a Python REPL/daemon) so state survives a turn.
- **Subagents are real child processes** with their own context; results return as messages.
- **Background/detached sessions** for long tasks; reattach later.
- **Bounded autonomy:** token/time/turn budgets plus quality gates; never an unbounded `while True`.

---

## The Continual Harness (self-evolution)

The harness stores mutable **supplemental state**, not the immutable base prompt:

```text
~/.local/share/shesh/harness/
├── supplemental.md       # extra system-prompt notes (refined, never base)
├── skills/               # auto-created skills (markdown + optional code)
├── memories/             # durable facts/lessons
├── subagents/            # reusable subagent specifications
└── refinements.jsonl     # append-only history: {id, trigger, edit, outcome, reverted}
```

`/refine` (a port of Prime Agent):

1. **Plan** (background LLM call): read the recent trajectory plus failures, propose the
   *smallest* CRUD edit to harness state that would improve outcomes.
2. **Apply** at a turn boundary: write the file, rebuild the prompt, record the outcome.
3. **Grade** with `llm-eval-harness` on a held-out check. Promote to canary only if it passes.
4. **Rollback** by refinement ID if it regresses.

The base system prompt is **immutable**. Safety and governance skills are **read-only** to
refine.

---

## Automatic skill lifecycle

Inspired by Memento-Skills (Read→Execute→Reflect→Write) and EvoSkill (frontier scoring):

1. **Capture** recurring successful patterns into a draft skill.
2. **Execute** the skill in similar contexts.
3. **Reflect** on success or failure; update.
4. **Score** against held-out tasks; maintain a top-N frontier; deprecate or archive unused or
   low-success skills ("discard the dross").
5. Skills are plain Markdown (plus optional code in `skills/<name>/`), reviewed in the settings UI.

---

## Safety boundaries (non-negotiable)

- Every subagent inherits the Brain's policy; destructive calls still require confirmation.
- Refine **cannot** edit `policies/`, `skills/safety-governance.md`, or the audit config.
- Autonomous mode is bounded (turns/tokens/time) and writes to a disposable working tree.
- The Prime "Factorio cheating" lesson applies: an agent optimizing a metric may game it,
  so gates verify real outcomes, and refinements are human-reviewable before reaching `stable`.

---

## Build order

1. `shesh-orchestrator`: process supervisor plus role configs plus RLM spawning over MCP (no A2A yet).
2. `shesh-harness`: CRUD state plus `/refine` plus rollback; skills are Markdown.
3. `shesh-acp`: expose the coordinator/coder to editors.
4. A2A local bus for subagent messaging; then optional remote.
5. Auto-skill scoring with `llm-eval-harness`, promoted through the canary gate.
