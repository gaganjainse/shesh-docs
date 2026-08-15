# ADR-0005: Local-First, Cloud Opt-In

Shesh runs fully offline by default and treats the cloud as an opt-in upgrade behind explicit
policy, so a laptop that sleeps, disconnects, and handles confidential job documents never
leaks data by accident. The design treats privacy as the default posture, not a setting to
discover later.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** privacy, security, offline

## Context

An AI operating system that phones home with file names, voice transcripts, or calendar events
violates user trust and reasonable GDPR expectations. The target user works on a laptop that
sleeps, goes offline, and processes job documents that must never leave disk.

Yet the fleet still needs embeddings and retrieval-augmented generation, model routing, and
occasional access to frontier models.

## Decision

The default is **offline only**:

- The local Ollama stack runs `phi4-mini`, `qwen2.5-coder:3b`, `moondream2`, and
  `nomic-embed-text` within a 6 GB VRAM budget.
- A local hash embedder stands in when Ollama is unavailable, so deterministic stubs keep the
  system working.
- No keys live in configuration. Secrets come from `shesh-secrets` (environment, gopass,
  KeepassXC, or file with a 0600 permission check that refuses world-readable files).

The cloud is **opt-in behind policy**:

- `[cloud] enabled = true` in configuration plus a per-session voice confirmation turns it on.
- The Guard denies cloud access for protected paths (`.ssh`, `Vaults/`, `~/Documents/Job`, and
  similar) regardless of setting.
- The audit log records every tool decision and route.

## Consequences

### Benefits

- The system works on an airplane — calendar, notes, and local-hash RAG all function.
- `shesh-secrets` resolves `get_secret("gopass:shesh/backup")` without ever logging the value.
- Sandboxed containers disable the network by default, so exfiltration cannot happen by
  accident.

### Costs

- Local models are weaker than frontier models, so `shesh-mind` must budget VRAM carefully.
- The first Ollama pull is roughly 10 GB, documented in GETTING_STARTED.

## Links

- `policies/SKILLS_POLICY.md`, `docs/architecture/AGENTIC_BODY.md`
- `shesh-secrets`, `shesh-mind`, `shesh-memory`
- [ADR-0015: Every Tool Call Through shesh-audit Guard](0015-guard-policy.md)
