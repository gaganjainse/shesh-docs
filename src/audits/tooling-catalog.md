# Tooling and Skills Catalog

Shesh turns a demo into an ecosystem by doing two things well: building the
Shesh-specific organs itself, and packaging the best mature open-source MCP
servers behind its policy layer. This chapter lists both, and the discipline
that keeps them from clashing.

> **Historical record —** This catalog was written during the build-out and is
> preserved as a planning record. It is retained as a record, not as live
> reference. The authoritative factual baseline is the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md): the body is
> licensed **GPL-3.0-or-later**, and `gaganjainse/SheshOS` is an unpublished,
> conceptual project rather than a live upstream. Third-party server licenses
> noted below (MIT/Apache/AGPL) describe those upstreams, not the Shesh body.

## The discipline

The principle is *upgrade the wrapper, not just fork and wrap*. Shesh builds the
organs it owns — `shesh-system`, `shesh-shell`, `shesh-files`, `shesh-skills` —
and packages mature open-source MCP servers for the rest, pinning versions and
wrapping them in the policy and audit layer. The Newelle fork is the model
example: it stripped GNOME-only assumptions, added a Hyprland Quickshell
overlay, prewired the Shesh MCP servers, set 6 GB-safe model defaults, and
renamed the about screen to "Shesh (Newelle core)."

Integration is cautious but enterprising. Hyprland, Quickshell, MCP, voice,
eBPF, containers, and phone ADB all run together, but never in conflict: each
talks over MCP stdio process boundaries (never in-process FFI), passes through
the Guard's allow/confirm/deny policy, and runs as a separate systemd user
service with its own config directory (`~/.config/shesh/mcp/`) and btrfs
subvolume. One job per component, one process per MCP server, one policy gate.

Only open-source, truly free, keyless, self-hostable, offline-first tools are
wanted — MIT, Apache-2.0, or GPL-3.0. Hosted subscriptions such as Tavily
(paid per query, needs an API key) were discarded. Self-hosted alternatives
such as SearXNG, agent-search, and the DuckDuckGo MCP replace them.

## Organs Shesh builds

| Component | Repo | Provides |
|-----------|------|----------|
| shesh-system | gaganjainse/shesh-system | Power/GPU/MUX/backup and system status |
| shesh-shell | gaganjainse/shesh-shell | Hyprland/Quickshell control |
| shesh-files | gaganjainse/shesh-files | Real-time organizer (Rust + Python) |
| shesh-skills | gaganjainse/shesh-skills | Notes, web, git, docs, reminders, and a skill library |
| shesh-voice | Fork of Newelle | STT/TTS/wake word and chat UI |

Governance, routing, RAG, and ADB organs were planned at the time of writing
and later landed as `shesh-audit`, `shesh-mind`, `shesh-memory`, `shesh-phone`,
and others.

## Mature MCP servers Shesh packages

Each server is pinned in a component repo and runs as a stdio MCP server behind
the Shesh policy, scoped to the least privilege its task needs.

| Need | Recommended server | License | Why |
|------|--------------------|---------|-----|
| Local filesystem | @modelcontextprotocol/server-filesystem (Anthropic) | MIT | Scoped read/write; pointed only at allowed directories |
| Git operations | server-git (Anthropic) | MIT | Status/diff/log without shelling out |
| Web fetch | mcp-server-fetch (Anthropic) | MIT | Safe URL→markdown fetch |
| Sequential reasoning | server-sequential-thinking | MIT | Complex multi-step problem solving |
| Memory | server-memory (knowledge graph) | MIT | Persistent entity/relation memory |
| Browser automation | Playwright MCP (Microsoft) | Apache-2.0 | Real browser for JS sites; runs sandboxed |
| GitHub | github-mcp-server | MIT | Issues/PRs/CI using a PAT, read-only by default |
| SQLite | server-sqlite | MIT | Local analytics/history databases |
| Time/calendar | server-time | MIT | Timezone-aware scheduling |
| Docs (PDF/Office) | markitdown-mcp (Microsoft) | MIT | Convert PDF/DOCX/XLSX→markdown |
| Browser devtools | chrome-devtools-mcp | Apache-2.0 | Web dev and debugging |
| Search (self-hosted) | SearXNG (AGPL-3.0) + agent-search (MIT) + DuckDuckGo MCP | AGPL-3.0 / MIT | No API key, no subscription, self-hosted, offline-first |

All are stdio and lockfile-pinned via `uvx`/`npx`. No MCP server ever receives
broader filesystem or shell access than its task requires.

## Skills library

Shipped skills were `coding`, `web-research`, `docs-writer`,
`safety-governance`, and `daily-briefing`. Planned skills covered
email-messaging, calendar, terminal-ops, container-ops, kernel-tuning, media,
job-mode, writing, finance, and language (Vyakrti integration).

## What Shesh deliberately avoids

- **Hosted SaaS MCPs** (Notion, Slack, Linear, Stripe) until the cloud tier is
  explicitly opted in and audited; local-first is the default.
- **Arbitrary shell-execution MCPs** ("run any command") — scoped servers and
  policy are used instead.
- **AGPL servers linked into the body** — if needed, they run as isolated
  separate services.
- **Multiple agent runtimes** — Newelle is the host; Goose/Hermes/pi are
  references, not daemons.

## Promotion

Each third-party server is wrapped in a component repo that:

1. Pins the version (`uv.lock`/`package-lock.json`).
2. Sets its allowed directories and environment in a config under
   `~/.config/shesh/mcp/`.
3. Is registered in `manifests/components.toml`.
4. Passes the same lint, test, and license gate.
5. Runs through `shesh-audit` so every tool call is logged.

> **Where this fits —** The [gap analysis](./gap-analysis.md) explains why each
> package was needed, and the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md) tracks protocol
> and packaging findings (F-06, F-08, F-11).
