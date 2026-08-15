# ADR-0010: ACP Adopted Alongside MCP

Shesh stacks two protocols — MCP for tools and ACP for editor integration — instead of
inventing a third, so editors like Zed and JetBrains can host the agent with proper streaming
and permission UX. A2A carries agent-to-agent traffic, keeping each link in its lane.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** protocols, editor, mcp, acp

## Context

MCP connects an agent to tools — shell, files, memory. Editors such as Zed and JetBrains need
an agent-to-editor protocol: sessions, file views, diffs, terminals, and permission prompts.
Inventing one would be needless duplication; the Agent Client Protocol (ACP) from Zed is
precisely that.

Three needs shaped the decision: tools via MCP, editor integration via ACP, and agent-to-agent
communication via A2A.

## Decision

- **Stack them:** MCP for tools, ACP for the editor, A2A for agent-to-agent. All speak
  JSON-RPC over stdio or Unix domain sockets.
- Implement `shesh-acp` with:
  - Session initialization, prompt streaming, and cancellation.
  - Permission responses (allow, deny, or destructive确认).
  - A terminal bridge (`terminal/exec`).
  - Filesystem and diff messages (`fs/read`, `diff/apply`).
- The ACP server is **not** an MCP server; `generate_mcp_config.py` excludes it from
  `servers.json`.
- ACP traces feed the same JSONL recorder as MCP traces (the `recent_traces` MCP tool).

## Consequences

### Benefits

- Zed and JetBrains can host Shesh with streaming and a permission UX.
- The MCP mesh stays clean — nine servers in `servers.json`, ACP separate.
- Canary end-to-end tests exercise an ACP session and prompt round-trip.

### Costs

- The ACP specification is still evolving; the upstream tracker watches the
  `agent-client-protocol` repository.
- Real editor testing needs manual verification on MMSI hardware.

## Links

- `docs/ACP_A2A.md`, `docs/architecture/MULTI_AGENT.md`
- `shesh-acp`, `scripts/generate_mcp_config.py`
- [ADR-0016: Kernel Consolidation](0016-kernel-consolidation.md) for the protocol-wires decision
