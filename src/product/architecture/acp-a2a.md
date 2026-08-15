# ACP and A2A Integration

Alongside MCP, Shesh adopts two more protocols so the agent can live inside editors and
coordinate other agents. This chapter covers ACP (Agent Client Protocol) for editor
integration and A2A (Agent2Agent) for agent-to-agent messaging, and shows how the three
fit together as the fleet's nervous system.

---

## ACP — Agent Client Protocol (Zed/JetBrains)

- **Direction:** editor (client) ↔ coding agent (server), over JSON-RPC 2.0 via stdio.
- **Why:** implement once and run in Zed, JetBrains, Neovim, and Emacs without per-editor plugins.
- **Versus MCP and the others:** ACP is the outer layer (a human in an editor driving the
  agent); MCP is the inner layer (the agent calling tools). Shesh runs both.
- **Component:** `shesh-acp` (P0).

Minimum ACP surface we implement:

- `initialize` and capability negotiation.
- `session/new`, `session/prompt` with **streaming** token updates.
- `fs/read_text_file`, `fs/write_text_file`, `fs/list`, terminal create/exec (permission-gated).
- `session/request_permission` before edits or commands (human-in-the-loop).
- Progress and diff updates so the editor shows the changes.

The ACP server spawns `shesh-orchestrator` (coder role) as its agent, handing it the MCP
endpoint list. All actions still flow through the Brain policy and audit. Reference:
<https://agentclientprotocol.com> (Zed Industries).

---

## A2A — Agent2Agent (Google/Linux Foundation)

- **Direction:** agent ↔ agent across processes and trust boundaries.
- **Why:** lets Shesh's specialist subagents talk directly (coordinator → researcher →
  critic), and later lets remote agents participate without us inventing a protocol.
- **Component:** `shesh-orchestrator` speaks A2A on a local Unix socket (P1).

We use A2A for **local agent messaging first**; remote or cross-organization A2A is off by
default and requires explicit opt-in plus the cloud tier.

---

## Protocol layering: the complete nervous system

The diagram shows the editor reaching the coordinator through ACP, the coordinator fanning
out to specialist roles over A2A, and every tool call dropping through the Brain to the
Soma organs over MCP.

```text
Editor (Zed/JetBrains)
   | ACP (stdio JSON-RPC, streaming, permissions)
   v
shesh-acp ---> shesh-orchestrator (coordinator)
                   |  A2A (local socket)   |-- planner --|
                   |---------------------->| coder       |  each over
                   |                       | researcher  |  MCP to tools
                   |                       | vision      |
                   |                       |-- critic ---|
                   v
              Brain (SheshAOS policy + audit event log)
                   | MCP (stdio JSON-RPC)
                   v
   shesh-files / shesh-shell / shesh-system / shesh-skills / ...
```

---

## Security

- ACP permission requests map one-to-one to Brain policy classes (auto/confirm/deny).
- A2A agents authenticate over the Unix socket (peer credentials) plus a per-session token.
- No agent ever gets broader filesystem or tool access than its role's allow-list.
