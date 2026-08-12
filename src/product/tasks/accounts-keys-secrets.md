# 1. Accounts, keys, and secrets

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 1 of 16.

- [ ] **Ollama installed and running**: `systemctl --user status ollama`
- [ ] Models pulled for the 6 GB stack:
  - [ ] `phi4-mini` (primary/planner/researcher/critic)
  - [ ] `qwen2.5-coder:3b` (coder)
  - [ ] `moondream2` (vision)
  - [ ] `nomic-embed-text` (embeddings/RAG)
  - [ ] Pull only what you need: `ollama pull <model>`
- [ ] **`restic` installed** and a repo initialized: `restic -r <repo> snapshots`
- [ ] `restic` repository password stored in **gopass/KeePassXC**, referenced as
  `env:RESTIC_PASSWORD` or `gopass:shesh/backup` — **never** in plain config
- [ ] MCP servers resolve secrets via `shesh-secrets`:
  `shesh-secrets-mcp` → `get_secret("env:MY_TOKEN")`
- [ ] No API keys/tokens committed to any repo (run a secret scan)
- [ ] Git identity configured: `git config --global user.email/name`

---
