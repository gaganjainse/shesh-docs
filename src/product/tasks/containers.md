# Containers and sandboxing

When the Shesh body runs untrusted code, it does so inside a throwaway box with no
network and no privileges. This chapter confirms the sandbox actually strips those
capabilities.

> **Note —** This chapter is section 8 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Rootless pods

- [ ] `podman` is installed and rootless mode works:
      `podman run --rm alpine echo ok`.
- [ ] `shesh-containers-mcp` → `run_sandboxed(["echo","hi"])` returns output.

## Hardening that must hold

- [ ] Sandboxed commands have **no network** by default (`--network=none`).
- [ ] `--cap-drop=ALL` is in effect (verify with a privileged syscall).
- [ ] Containers are removed after each run (`--rm`).

## The third-party bundle

- [ ] The third-party MCP bundle (filesystem, fetch, git) launches only when `npx`
      and `uvx` are present.
