---
title: Agent context files
type: reference
summary: "The file conventions that configure AI agents, which the fleet adopts, and which it deliberately does not."
audience: contributor
status: current
verified: 2026-08-15
---

# Agent context files

Several competing conventions exist for telling an AI agent how to work in a
repository. This page records which the fleet uses, where each file lives, and
which conventions were evaluated and rejected.

## The conventions

| File | Purpose | Governance | Fleet use |
|---|---|---|---|
| `AGENTS.md` | Repository conventions for any coding agent | Agentic AI Foundation, Linux Foundation | **Adopted** |
| `SKILL.md` | A reusable capability, loaded on demand | Anthropic, Agent Skills spec | **Adopted** |
| `CLAUDE.md` | Claude Code specific additions | Anthropic | **Adopted**, as a thin import |
| `SOUL.md` | Agent persona, voice, and judgment | Community convention | **Not adopted** |
| `llms.txt` | Index for external AI crawlers | Independent proposal | **Not adopted** |
| `.cursorrules` | Cursor-specific rules | Cursor | **Not adopted**, superseded |

## AGENTS.md

A plain Markdown file at a repository root giving agents the operational context
that does not belong in a README: build commands, code style, architectural
constraints, and boundaries. It is read by more than thirty agents including
Codex, Cursor, Copilot, Gemini CLI, Aider, Zed, and Windsurf.

The specification has no required fields and no frontmatter. Structure is free.

**In this fleet:** the canonical file is
[`shesh-ecosystem/AGENTS.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/AGENTS.md).
Every other repository carries a short `AGENTS.md` that points at it and records
only local differences. This follows the single-sourcing rule: fleet-wide
judgment boundaries are stated once.

Keep it under roughly 300 lines. Recall degrades past that, and long steering
files are a known anti-pattern.

## SKILL.md

A directory containing `SKILL.md` with YAML frontmatter and a Markdown body,
packaging a capability the agent loads when relevant. Covered in detail under
[Skills](skills/index.md).

The distinction from `AGENTS.md` matters: `AGENTS.md` is always-on repository
context, while a skill is loaded only when its description matches the task.
Procedures belong in skills; conventions belong in `AGENTS.md`.

## CLAUDE.md

Claude Code reads `CLAUDE.md` rather than `AGENTS.md`. The fleet keeps a
`CLAUDE.md` that imports `AGENTS.md` with `@AGENTS.md` and adds only
Claude-specific notes, so there is no duplicated content to drift.

## What the fleet does not use

**`SOUL.md`** defines an agent's persona: identity, tone, and how it pushes
back. It is a genuine convention with real adoption, but it is not adopted here.
Shesh agents are operational rather than conversational, and the behaviour that
would go in a soul file — how to handle uncertainty, when to refuse, when to
stop — is already specified in the `safety-governance` and `autopilot` skills,
where it is enforced by the policy engine rather than being advisory prose.
Adding a persona layer would duplicate that with weaker enforcement.

**`llms.txt`** indexes a public website for external AI crawlers. It solves an
outward-facing problem the fleet does not have: the documentation is published
as a book, and none of the repositories serve marketing content. It is also an
independent proposal with no standards body and no committed consumer.

**`.cursorrules`** is Cursor-specific and superseded by `AGENTS.md`, which
Cursor also reads.

**`SPEC.md`** is not an established convention. Where a specification is needed,
the fleet uses an architecture decision record, which carries a date, a status,
and a superseding link.

## Precedence

When several sources give conflicting guidance:

1. An explicit instruction in the conversation.
2. The nearest `AGENTS.md` to the file being edited.
3. A parent `AGENTS.md`.
4. A loaded skill.

A user instruction always overrides a file.

## Related

- [Skills](skills/index.md) — the skill format and library.
- [Documentation policy](../governance/documentation-policy.md) — rules for what
  may be written where.
- [ADR-0018](../governance/adr/0018-adopt-vs-build.md) — the adopt-versus-build
  decision these choices follow.
