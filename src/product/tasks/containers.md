# 8. Containers / sandboxing

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 8 of 16.

- [ ] `podman` installed and rootless works: `podman run --rm alpine echo ok`
- [ ] `shesh-containers-mcp` → `run_sandboxed(["echo","hi"])` returns output
- [ ] Sandboxed commands have **no network** by default (`--network=none`)
- [ ] `--cap-drop=ALL` is in effect (verify with a privileged syscall)
- [ ] Containers are removed after each run (`--rm`)
- [ ] The third-party MCP bundle (filesystem/fetch/git) launches only if
      `npx`/`uvx` are present

---
