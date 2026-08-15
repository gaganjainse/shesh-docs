# How to Use These Docs

This book is built to be read in order or consulted by task. The guidance below points you
to the right starting chapter depending on what you are trying to do.

## Start here, by intent

- **I am new to Shesh.** Begin with the [Introduction](./introduction.md), then
  [Product Overview](./product/overview.md) and
  [Getting Started](./product/getting-started.md). Read the
  [Agentic Body](./product/architecture/agentic-body.md) to understand the metaphor that
  frames the whole system.
- **I want to understand the architecture.** Move to the architecture chapters: the
  [Repo Topology](./product/architecture/repo-topology.md), the
  [Language Policy](./product/architecture/language-policy.md),
  [Multi-Agent](./product/architecture/multi-agent.md), and the
  [ACP & A2A Protocols](./product/architecture/acp-a2a.md).
- **I have a concrete task.** The Tasks section breaks verification into focused,
  step-by-step chapters — [First Boot](./product/tasks/first-boot.md),
  [Accounts and Secrets](./product/tasks/accounts-keys-secrets.md),
  [MCP Mesh](./product/tasks/mcp-mesh.md), and so on. Each reads like a checklist you can
  follow top to bottom.
- **I learn by doing.** The Tutorials section offers guided flows:
  [Organize Downloads](./product/tutorials/organize-downloads.md),
  [Voice and Settings](./product/tutorials/voice-settings-organizer.md), and
  [Memory and Recall](./product/tutorials/rag-vector.md).
- **I need exact details.** The Reference section holds the
  [Manifest](./product/reference/manifest.md), [Channels](./product/reference/channels.md),
  [Components](./product/reference/components/README.md),
  [Models](./product/reference/models.md), and [Upstreams](./product/reference/upstreams.md).
- **I build the system, not just run it.** The Factory and Desktop parts cover the
  development harness and the styling layer respectively.

## Search

The book ships with built-in full-text search. Press `S` to focus the search field, `?`
for help, and the arrow keys to move between results. Search is scoped to this compilation
only; for component-specific detail, follow the cross-links to the source repository.

## Three planes, one rule

The fleet separates **product**, **factory**, and **gateway** so that builder tooling never
complicates the system a person runs. When reading, keep that separation in mind: a chapter
in the Factory part describes how the system is built, not how it behaves on your machine.
The Desktop part describes how it looks and feels.

This is a reading compilation. The source of truth remains in each component's repository;
this book is the organized projection of all of them.
