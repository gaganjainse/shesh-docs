# Gap Analysis — From Demo to Full Ecosystem

This chapter maps what the fleet had on 2026-08-09 against what a real,
world-integrated, self-improving AI environment needs. It is the backlog that
turned Shesh from a promising demo into a living system, and it explains why
each missing piece mattered.

> **Historical record —** This analysis was written on 2026-08-09 and is
> preserved as a planning snapshot. It is retained as a record, not as live
> reference. The authoritative factual baseline is the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md): the body is
> licensed **GPL-3.0-or-later** (not MIT), and `gaganjainse/SheshOS` is an
> unpublished, conceptual project rather than a live upstream. Where statuses
> below differ from that baseline, treat them as historical.

## Summary

- The fleet was strong on local-first tooling (MCP, power, files, voice) but thin on agent coordination and self-evolution.
- Three needs were rated P0 blockers: an ACP server for editors, specialist subagents in an orchestrator, and a Continual Harness with a `/refine` loop.
- World integration (browser, GitHub, email/calendar, messaging, phone) was mostly missing and slated for P1 work.
- Most P0 items named here were later built; the 2026-08-15 audit tracks what remained unfinished.

Legend: ✅ exists · 🟡 partial · ❌ missing.

## Protocols — the nervous system

| Need | Status | Gap / action |
|------|--------|--------------|
| MCP (agent→tools) | ✅ | Three servers live plus `shesh-skills`. |
| ACP (editor→agent) | ❌ **P0** | A `shesh-acp` server so Shesh runs inside Zed/JetBrains/Neovim with file, terminal, diff, and permission UX. MCP and ACP stack, not compete. |
| A2A (agent→agent) | ❌ P1 | Multi-agent coordination across trust boundaries; adopt Google A2A rather than inventing one. |
| JSON-RPC (brain internal) | ✅ in SheshAOS | `shesh-rpc` already used; wire Brain↔Soma over it. |
| Event stream / audit | 🟡 | A log existed conceptually; the `shesh-audit` component (append-only, hash-chained, queryable) was still to be built. |
| Streaming (voice/UI) | 🟡 | Newelle streamed TTS/STT; the MCP servers were request/response; SSE/streaming for long tasks was pending. |

## Agent topology — the mind

| Need | Status | Gap / action |
|------|--------|--------------|
| Single primary agent | ✅ Newelle | |
| Specialist subagents | ❌ **P0** | Coder/planner/reviewer/vision roles (the SheshOS thesis). Build `shesh-orchestrator` with RLM-style `rlm("subtask")` child-agent spawning. |
| Role-based crews | ❌ P1 | Researcher→writer→reviewer pipelines for docs and research. |
| Persistent/background agents | ❌ P1 | Daemon-backed sessions that survive disconnect, with long goals and heartbeats. |
| Agent-to-agent messaging | ❌ P1 | A direct message bus between running agents. |
| Human-in-the-loop | 🟡 | Policy asked for destructive actions; the ACP permission UX and approvals queue were pending. |
| Multiple model routing | 🟡 | `shesh-mind` was declared; the router (planner/coder/vision by task) was to be implemented. |

## Self-evolution — learn and discard the dross

| Need | Status | Gap / action |
|------|--------|--------------|
| Immutable base prompt | ✅ principle | |
| Continual Harness (CRUD state) | ❌ **P0** | Mutable supplemental prompts, skills, memories, and subagent specs as durable state the agent can refine. |
| `/refine` evidence loop | ❌ **P0** | Read trajectory → propose the smallest evidence-backed edit → apply at a turn boundary → record trigger and outcome. Never mutate the base. |
| Rollback of refinements | ❌ P1 | Refinement history with IDs; revert bad harness updates. |
| Automatic skill creation | ❌ P1 | "Read→Execute→Reflect→Write" (Memento-Skills); turn repeated wins into reusable skills. |
| Frontier-based skill evolution | ❌ P2 | EvoSkill/GEPA: mutate skill or prompt, score on held-out tasks, keep the top-N. |
| Discard/deprecation | ❌ P1 | Track skill usage and success; auto-archive low-value skills. |
| Reflection on failure | ❌ P1 | Failure traces → proposed fixes. |
| Eval harness for changes | ❌ P1 | Wire `llm-eval-harness` so refinements are graded before promotion (canary gate). |
| Memory (episodic/semantic) | 🟡 | `shesh-memory` was declared; RAG, entity memory, and a vector store were to be built. |

## World integration — integrate, don't isolate

| Need | Status | Gap / action |
|------|--------|--------------|
| Web search | ✅ `shesh-skills` (keyless DDG) | |
| Web fetch | ✅ | |
| Browser automation | ❌ P1 | Package Playwright MCP (sandboxed) for JS sites and testing. |
| GitHub | 🟡 | Read-only `github_view`; add GitHub MCP (issues/PRs/CI) with a scoped PAT. |
| Email/calendar/contacts | ❌ P1 | Local-first CalDAV/IMAP (`vdirsyncer`/`khal`/`neomutt`), not cloud-locked. |
| Messaging (Telegram/WhatsApp/Signal) | ❌ P2 | Optional bridges as separate, isolated services. |
| Phone (Realme Narzo) | 🟡 declared | The `shesh-phone` ADB harness needed implementation. |
| Editor/IDE | ❌ **P0** | An ACP server (see above). |
| Docs conversion (PDF/Office) | ✅ pandoc | |
| Obsidian/notes | ✅ notes vault | |
| Containers/sandboxing | ❌ P1 | `shesh-containers`: podman/distrobox control for untrusted code. |
| Cloud fallback | 🟡 policy existed | OmniRoute/LiteLLM proxy behind explicit opt-in. |

## Soma and desktop completeness

| Need | Status | Gap / action |
|------|--------|--------------|
| Power/GPU/MUX | ✅ `shesh-system` | |
| Hyprland control | ✅ `shesh-shell` | |
| File organizer | ✅ `shesh-files` | |
| Voice/wake word | ✅ `shesh-voice` (Newelle) | |
| Display/GPU runtime validation | ❌ P1 | A hardware smoke-test suite (could not run in the build sandbox). |
| Backup (real restic) | 🟡 script referenced | Implement and verify. |
| Scheduling/reminders | ✅ basic | |
| Media/screenshots/recording | ❌ P2 | |
| Accessibility (a11y) | ❌ P2 | |

## Platform and infrastructure

| Need | Status | Gap / action |
|------|--------|--------------|
| Component repos | ✅ four live at the time | |
| Ecosystem manifest + locks + gates | ✅ | |
| Cross-distro CI | 🟡 canary workflow defined | Add ACP/multi-agent tests. |
| Canary integration tests | ❌ P1 | Spin up MCP+ACP+orchestrator in a container; assert end-to-end. |
| Reproducible dev environments | 🟡 documented | Provide a `distrobox assemble`/Containerfile for onboarding. |
| Secret management | ❌ P1 | KeePassXC/gopass integration; never put keys in config or MCP. |
| Telemetry/observability | ❌ P1 | OpenTelemetry traces and a journal; local only. |
| Supply-chain security | 🟡 lockfiles | Add sigstore/provenance. |
| Installer/updater | 🟡 setup existed | Need channel-based update (stable/canary/devel) with rollback snapshots. |
| Documentation | ✅ extensive | Keep an ADR for each protocol decision. |

## The immediate P0 backlog

Four builds anchored the next phase:

1. **`shesh-acp`** — a minimal ACP server: session init, prompt-turn streaming,
   permission requests, and a file/terminal bridge so Shesh works in
   Zed/JetBrains.
2. **`shesh-orchestrator`** — a multi-agent runtime: RLM subagent spawning,
   role routing, agent-to-agent messaging, persistent sessions, and heartbeats.
3. **`shesh-harness`** — the Continual Harness: durable CRUD state, `/refine`,
   rollback, and automatic skill creation, gated by `llm-eval-harness`.
4. **`shesh-audit`** — an append-only, hash-chained event log and policy engine
   bridging to SheshAOS.
5. **Canary end-to-end test** — a container that boots every server and runs a
   real task.

P1 work followed: memory, browser/GitHub MCP packaging, email/calendar, phone,
containers, observability, a secret manager, and hardware tests. The rest of
the document set carried the architecture and specs for the first four items.

> **Where this fits —** The [exhaustive audit](./exhaustive-audit.md) records
> what existed when this plan was drawn, and the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md) reports which
> gaps survived to the baseline.
