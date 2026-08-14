# Summary

# Introduction

- [Introduction](./introduction.md)
- [How to Use These Docs](./how-to-use.md)
- [Glossary](./glossary.md)

# Part I: Product — shesh-ecosystem (clean)

- [Product Overview](./product/overview.md)
- [Getting Started](./product/getting-started.md)
- [Architecture](./product/architecture.md)
  - [Agentic Body](./product/architecture/agentic-body.md)
  - [Repo Topology — Federated Sinkhole](./product/architecture/repo-topology.md)
  - [Language Policy — 5 Languages](./product/architecture/language-policy.md)
  - [Multi-Agent](./product/architecture/multi-agent.md)
  - [ACP & A2A Protocols](./product/architecture/acp-a2a.md)
- [Concepts](./product/concepts.md)
  - [Learning & Memory](./product/concepts/learning.md)
  - [Containers & Venv](./product/concepts/containers-venv.md)
  - [Linux Layout & Disk Structure](./product/concepts/linux-layout.md)
- [Tasks — Manual Verification by Area](./product/tasks/overview.md)
  - [0. First Boot](./product/tasks/first-boot.md)
  - [1. Accounts, Keys, Secrets](./product/tasks/accounts-keys-secrets.md)
  - [2. MCP Mesh](./product/tasks/mcp-mesh.md)
  - [3. Voice — Newelle Fork](./product/tasks/voice.md)
  - [4. GPU, Power, MUX](./product/tasks/gpu-power-mux.md)
  - [5. Display & Desktop](./product/tasks/display-desktop.md)
  - [6. Backup — Restic](./product/tasks/backup.md)
  - [7. Phone — ADB Realme Narzo](./product/tasks/phone.md)
  - [8. Containers & Sandboxing](./product/tasks/containers.md)
  - [9. Agent Behavior](./product/tasks/agent-behavior.md)
  - [10. Security & Audit](./product/tasks/security-audit.md)
  - [11. Canary & Releases](./product/tasks/canary-releases.md)
- [Reference](./product/reference/overview.md)
  - [Manifest — components.toml](./product/reference/manifest.md)
  - [Channels — stable/canary/devel](./product/reference/channels.md)
  - [Components — All shesh-*](./product/reference/components/README.md)
  - [Models — Free Models Manifest](./product/reference/models.md)
  - [Upstreams — Sources & Steal-Map](./product/reference/upstreams.md)
- [Tutorials](./product/tutorials/overview.md)
  - [Organize Downloads — Smart Organizer v2](./product/tutorials/organize-downloads.md)
  - [Voice + Settings + Organizer Flow](./product/tutorials/voice-settings-organizer.md)
  - [Memory & Recall (RAG)](./product/tutorials/rag-vector.md)

# Part II: Factory — shesh-workspace (messy dev tooling)

- [Factory Overview — Product vs Factory Separation](./factory/overview.md)
- [Session Protocol — 60-sec Handoff](./factory/session-protocol.md)
- [Session Guard — Slowdown Detection](./factory/session-guard.md)
- [Secure PAT — Password Encryption](./factory/secure-pat.md)
- [GitHub Auth — Secure Loader](./factory/github-auth.md)
- [Setup Worker — Minimal Repos per Role](./factory/setup-worker.md)
- [Swarm — Multi-Agent via GitHub](./factory/swarm/README.md)
- [Efficiency — Selective Clone 36M→2M](./factory/efficiency.md)
- [Travel Mode — 1 Orchestrator Tab + Actions](./factory/travel-mode.md)
- [Foolproof Swarm Prompts — 5 Agents](./factory/foolproof-prompts.md)
- [Steal Infrastructure](./factory/steal-infrastructure.md)
- [Live Update System — Automatic](./factory/live-update.md)
- [Model Agnostic — Free Omniroute](./factory/model-agnostic.md)
- [LLM Adapter — 5-Layer Guard](./factory/llm-adapter.md)
- [Model Router — Capability-Based](./factory/model-router.md)
- [Eval Harness — Evidence-Backed /refine](./factory/eval-harness.md)

# Part III: Gateway — shesh-omniroute + OmniRoute Fork (optional cloud)

- [Gateway Overview — Optional to Local AI](./gateway/overview.md)
- [OmniRoute Study — 291 Providers 90+ Free](./gateway/omniroute-study.md)
- [Free Providers — Groq, OpenRouter, GitHub Models, HF](./gateway/free-providers.md)
- [Shesh-Omniroute Wrapper](./gateway/shesh-omniroute.md)

# Part IV: Desktop — shesh-desktop (illogical-impulse + CachyOS)

- [Desktop Overview — Style + Performance Non-Negotiable](./desktop/overview.md)
- [Master Index](./desktop/00-index.md)
- [Audit — Current Truth](./desktop/01-audit.md)
- [Roadmap — Phases 0-7](./desktop/02-roadmap.md)
- [Disk Structure — Work vs Personal vs Job](./desktop/03-disk-structure.md)
- [Device Profile — MSI Sword 16 HX](./desktop/04-device-profile.md)
- [Smart Organizer v2](./desktop/05-smart-organizer.md)
- [Shesh Agent — Newelle + Ollama + MCP](./desktop/06-shesh-agent.md)
- [Automations — Systemd Timers + Udev](./desktop/07-automations.md)
- [Ecosystem Tools — Phone Harness etc](./desktop/08-ecosystem-tools.md)
- [AI Prompts — Copy-Paste per Phase](./desktop/09-ai-prompts.md)
- [Licenses & Sources](./desktop/10-licenses-sources.md)
- [Ambient Design — Catch-Up + Warm Proactivity](./desktop/ambient-design.md)
- [Shesh Readme](./desktop/shesh-readme.md)
- [Checklist](./desktop/checklist.md)

# Part V: Architecture Decision Records (ADRs)

- [ADR Index — 18 Decisions](./adr/README.md)
- [ADR-0001 Five Languages Only](./adr/0001-five-languages.md)
- [ADR-0002 Rootless Containers](./adr/0002-containers-and-venv.md)
- [ADR-0003 Federated Repos + Manifest](./adr/0003-federated-repos.md)
- [ADR-0004 Three Release Channels](./adr/0004-three-channels.md)
- [ADR-0005 Local-First, Cloud Opt-In](./adr/0005-local-first.md)
- [ADR-0006 Immutable Base + Evidence-Backed /refine](./adr/0006-refine-governance.md)
- [ADR-0007 Six Agent Roles, 6GB VRAM Budget](./adr/0007-agent-roles.md)
- [ADR-0008 Archive shesh-kernel, Don't Force Merge](./adr/0008-kernel-archive.md)
- [ADR-0009 Newelle Fork as shesh-voice with Overlay](./adr/0009-shesh-voice-overlay.md)
- [ADR-0010 ACP + MCP Stack](./adr/0010-acp-plus-mcp.md)
- [ADR-0011 Catch-Up Scheduler, Not Fixed Cron](./adr/0011-catchup-scheduler.md)
- [ADR-0012 Warm Proactivity at Natural Pauses](./adr/0012-warm-proactivity.md)
- [ADR-0013 Hierarchical Memory + Token-Bounded Context](./adr/0013-hierarchical-memory.md)
- [ADR-0014 Habit Learning Frequentist with Decay](./adr/0014-habit-learning.md)
- [ADR-0015 Every Tool Call Through Guard](./adr/0015-guard-policy.md)
- [ADR-0016 Kernel Consolidation](./adr/0016-kernel-consolidation.md)
- [ADR-0017 Naming Purge Completed](./adr/0017-naming-purge-completed.md)
- [ADR-0018 Adopt vs Build](./adr/0018-adopt-vs-build.md)

# Part VI: Audits & Roadmaps

- [Complete Audit & Master Roadmap](./audits/audit-and-roadmap.md)
- [Exhaustive Audit — 54 Repos](./audits/exhaustive-audit.md)
- [Gap Analysis — Demo to Full Ecosystem](./audits/gap-analysis.md)
- [Tooling Catalog — Open-Source Only](./audits/tooling-catalog.md)
- [Incident — Five-Tab Swarm Collision (2026-08-11)](./audits/incident-2026-08-11-multi-tab-swarm.md)

# Part VII: Verification & Handoff

- [Manual Verification Checklist — 16 Sections](./verification/manual-verification.md)
- [Session Handoff — Anchor Document](./verification/session-handoff.md)

# Part VIII: Skills & Policies

- [Skills — Overview](./skills/overview.md)
- [Coding Skill](./skills/coding.md)
- [Web-Research Skill](./skills/web-research.md)
- [Docs-Writer Skill](./skills/docs-writer.md)
- [Safety & Governance Skill](./skills/safety-governance.md)
- [Daily-Briefing Skill](./skills/daily-briefing.md)
- [Autopilot Skill](./skills/autopilot.md)
- [Skills Policy — Tool Risk Classes](./policies/skills-policy.md)
- [Security Policy — Canonical Posture](./policies/security-policy.md)
- [Threat Model](./policies/threat-model.md)
- [Recovery Runbook](./policies/recovery.md)
- [Dependency Policy — Rolling Releases](./policies/dependency-policy.md)
- [Documentation Policy](./policies/documentation-policy.md)
- [Fork Gardening](./policies/fork-gardening.md)
- [Janitor TODO Policy](./policies/janitor-todo-policy.md)

# Part IX: Queries — Full Decision Trail

- [Query Log — All Prompts + Answers](./queries/querylog.md)
- [Query Log — All Agents Aggregated](./queries/querylog-all-agents.md)
- [Next Session Prompt — Auto-Generated](./queries/next-session-prompt.md)

# Part X: Portfolio — Completely Automatic (No Forks, Proper Priority)

- [Portfolio Overview — Smart, No Forks, Proper Priority](./portfolio/overview.md)
- [Auto-Update — GitHub API + generate:all + CI gates + Vercel deploy](./portfolio/auto-update.md)

# Part XI: SheshAOS — The Flagship Rust AI OS

- [SheshAOS Overview — Governance-First, Event-Sourced OS](./sheshaos/README.md)
- [Handover — Developer Transition Guide](./sheshaos/handover.md)
- [Architecture — Layers, Control Flow, Event Model](./sheshaos/architecture.md)

# Part XII: Standalone Projects — Portfolio Beyond the Ecosystem

- [Projects Index — Languages, Apps, AI Tooling](./projects/index.md)
