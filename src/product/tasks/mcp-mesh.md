# 2. MCP mesh (the core integration)

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 2 of 16.

After `pipx install`-ing all `shesh-*` packages, run the canary:

```bash
bash scripts/e2e-canary.sh   # from shesh-ecosystem
```

- [ ] **E2E canary passes** (all 16 components import, policy denies protected
      paths, memory/orchestrator/ACP/backup/calendar/vectors/traces all respond)
- [ ] **Generate the MCP config**: `python scripts/generate_mcp_config.py --channel canary`
- [ ] `~/.config/shesh/mcp/servers.json` lists **9 MCP servers**
      (audit, backup, files, harness, memory, mind, orchestrator, shell, skills;
      + containers/secrets/calendar if installed)
- [ ] **Newelle (shesh-voice)** starts and its MCP panel shows the servers
      connected (green)
- [ ] Restart Newelle and ask it to **list its tools** — it should see
      `check_system_updates`, `semantic_search`, `start_session`, etc.
- [ ] Zed / another MCP client (if you use one) can connect via the generated
      `zed.json`
- [ ] Each MCP server starts standalone without import errors, e.g.
      `shesh-system-mcp` (Ctrl-C to exit)

---
