# Summary

[Introduction](start/introduction.md)

# Start here

- [What Shesh is](start/what-is-shesh.md)
- [Install Shesh](start/install.md)
- [How to read these documents](start/reading-guide.md)
- [Glossary](start/glossary.md)

# Explanation

- [Architecture](explanation/index.md)
  - [The Agentic Body](explanation/agentic-body.md)
  - [Repository topology](explanation/repository-topology.md)
  - [Language policy](explanation/language-policy.md)
  - [Agent protocols](explanation/protocols.md)
  - [Multi-agent orchestration](explanation/multi-agent.md)
  - [Memory and learning](explanation/memory-and-learning.md)
  - [Ambient behaviour](explanation/ambient-behaviour.md)
- [Environment](explanation/isolation-model.md)
  - [Filesystem layout](explanation/filesystem-layout.md)
  - [Disk layout](explanation/disk-layout.md)
  - [Target hardware](explanation/target-hardware.md)
  - [The desktop layer](explanation/desktop-layer.md)
- [Adjacent systems](explanation/sheshaos.md)
  - [SheshAOS architecture](explanation/sheshaos-architecture.md)
  - [The cloud gateway](explanation/cloud-gateway.md)

# How-to guides

- [Overview](how-to/index.md)
- [Configure automations](how-to/configure-automations.md)
- [Configure the desktop agent](how-to/configure-the-desktop-agent.md)
- [Configure the organizer](how-to/configure-the-organizer.md)
- [Enable cloud routing](how-to/enable-cloud-routing.md)
- [Recover from failure](how-to/recover-from-failure.md)
- [Organize downloads](how-to/organize-downloads.md)
- [A voice-driven workflow](how-to/voice-driven-workflow.md)
- [Use semantic recall](how-to/use-semantic-recall.md)
- [Work on SheshAOS](how-to/work-on-sheshaos.md)

# Reference

- [Overview](reference/index.md)
- [Component catalogue](reference/components.md)
- [Manifest schema](reference/manifest-schema.md)
- [Release channels](reference/release-channels.md)
- [Models](reference/models.md)
- [Upstreams](reference/upstreams.md)
- [Licences and sources](reference/licences.md)
- [Cloud model providers](reference/cloud-providers.md)
- [Verification checklist](reference/verification-checklist.md)
- [Desktop verification checklist](reference/desktop-checklist.md)
- [Related projects](reference/related-projects.md)
- [Skills](reference/skills/index.md)
- [Agent context files](reference/agent-files.md)

# Governance

- [Security policy](governance/security-policy.md)
- [Threat model](governance/threat-model.md)
- [Dependency policy](governance/dependency-policy.md)
- [Documentation policy](governance/documentation-policy.md)
- [Skills policy](governance/skills-policy.md)
- [Fork maintenance](governance/fork-maintenance.md)
- [TODO policy](governance/todo-policy.md)
- [Architecture decision records](governance/adr/index.md)
  - [ADR-0001: Restrict implementation languages to five](governance/adr/0001-five-languages.md)
  - [ADR-0002: Run components in rootless containers and virtual environments](governance/adr/0002-containers-and-venv.md)
  - [ADR-0003: Federate repositories behind one manifest](governance/adr/0003-federated-repos.md)
  - [ADR-0004: Promote releases through three channels](governance/adr/0004-three-channels.md)
  - [ADR-0005: Run local first, make cloud opt-in](governance/adr/0005-local-first.md)
  - [ADR-0006: Gate self-refinement on measured evidence](governance/adr/0006-refine-governance.md)
  - [ADR-0007: Define six agent roles within a fixed video-memory budget](governance/adr/0007-agent-roles.md)
  - [ADR-0008: Archive the kernel rather than force a merge](governance/adr/0008-kernel-archive.md)
  - [ADR-0009: Fork Newelle as shesh-voice with an overlay](governance/adr/0009-shesh-voice-overlay.md)
  - [ADR-0010: Adopt the Agent Client Protocol alongside the Model Context Protocol](governance/adr/0010-acp-plus-mcp.md)
  - [ADR-0011: Schedule catch-up work rather than fixed cron](governance/adr/0011-catchup-scheduler.md)
  - [ADR-0012: Offer proactive help only at natural pauses](governance/adr/0012-warm-proactivity.md)
  - [ADR-0013: Store memory hierarchically with a token-bounded context](governance/adr/0013-hierarchical-memory.md)
  - [ADR-0014: Learn habits frequentist with decay](governance/adr/0014-habit-learning.md)
  - [ADR-0015: Route every tool call through the guard](governance/adr/0015-guard-policy.md)
  - [ADR-0016: Consolidate the kernel lineage](governance/adr/0016-kernel-consolidation.md)
  - [ADR-0017: Fix one naming convention across the fleet](governance/adr/0017-naming-purge-completed.md)
  - [ADR-0018: Prefer a maintained upstream over building](governance/adr/0018-adopt-vs-build.md)
  - [ADR-0019: Fold single-module services into shesh-core](governance/adr/0019-shesh-core-monorepo.md)
