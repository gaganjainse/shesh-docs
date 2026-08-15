# Accounts, keys, and secrets

A federated agent is only as trustworthy as the secrets it can reach. This chapter
covers the local accounts, model downloads, and secret stores that must be in place
before the Shesh body can act on your behalf.

> **Note —** This chapter is section 1 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## The local model stack

Ollama must be installed and running as a user service before anything else works. The
6 GB stack pulls four models, each with a defined role in the agent's thinking.

- [ ] Ollama is installed and running: `systemctl --user status ollama`.
- [ ] Models for the 6 GB stack are pulled:
  - [ ] `phi4-mini` — primary planner, researcher, and critic.
  - [ ] `qwen2.5-coder:3b` — the coder.
  - [ ] `moondream2` — vision.
  - [ ] `nomic-embed-text` — embeddings and retrieval (RAG).
- [ ] Pull only what you need: `ollama pull <model>`.

## Secrets and backup vault

The backup vault and the secret store are the two places credentials must never live in
plain text.

- [ ] `restic` is installed and a repository is initialized:
      `restic -r <repo> snapshots`.
- [ ] The `restic` repository password lives in **gopass or KeePassXC** and is
      referenced as `env:RESTIC_PASSWORD` or `gopass:shesh/backup` — never in plain
      config.
- [ ] MCP servers resolve secrets through `shesh-secrets`:
      `shesh-secrets-mcp` → `get_secret("env:MY_TOKEN")`.

## Repository hygiene

- [ ] No API keys or tokens are committed to any repository (run a secret scan).
- [ ] Git identity is configured: `git config --global user.email` and `user.name`.
