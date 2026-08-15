# The MCP server mesh

The Model Context Protocol mesh is the nervous system that lets the Shesh agent touch
its tools. This chapter confirms every server imports, starts, and answers before the
body is considered wired.

> **Note —** This chapter is section 2 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Run the canary

After installing every `shesh-*` package with `pipx`, run the end-to-end canary from
the `shesh-ecosystem` repository. It is the single fastest signal that the mesh is
intact.

```bash
bash scripts/e2e-canary.sh   # from shesh-ecosystem
```

- [ ] The E2E canary passes: all 16 components import, the policy engine denies
      protected paths, and the memory, orchestrator, ACP, backup, calendar, vectors,
      and traces servers all respond.
- [ ] Each MCP server starts standalone without import errors — for example,
      `shesh-system-mcp` (press Ctrl-C to exit).

## Generate and verify the configuration

- [ ] Generate the MCP configuration:
      `python scripts/generate_mcp_config.py --channel canary`.
- [ ] `~/.config/shesh/mcp/servers.json` lists **9 MCP servers**
      (audit, backup, files, harness, memory, mind, orchestrator, shell, skills; plus
      containers, secrets, and calendar when those are installed).
- [ ] **Newelle** (shesh-voice) starts and its MCP panel shows the connected servers
      in green.
- [ ] Restart Newelle and ask it to list its tools — it should see
      `check_system_updates`, `semantic_search`, `start_session`, and the rest.
- [ ] Zed or another MCP client connects through the generated `zed.json` if you use
      one.
