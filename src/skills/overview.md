# Skills — The Behavior Library

Skills are the reusable habits of the fleet: short Markdown documents that steer an agent
through a recurring task. This chapter maps the library and the rules that keep it safe.

- Status: living · last verified 2026-08-13
- Runtime component: [shesh-skills](https://github.com/gaganjainse/shesh-skills)
- Policy: [Skills Policy](../policies/skills-policy.md)

## What a skill is

Skills are Markdown documents with YAML frontmatter (`name`, `description`) that steer agent
behavior for a recurring task class. This directory is the canonical text; `shesh-skills`
serves them to agents over MCP. A skill shapes judgment, but it cannot by itself execute
code.

## The set

| Skill | Job |
|---|---|
| [coding](coding.md) | read-before-edit discipline, tests always, never push unreviewed |
| [web-research](web-research.md) | source-cited research protocol |
| [docs-writer](docs-writer.md) | documentation in the house [style](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/STYLE_GUIDE.md) |
| [safety-governance](safety-governance.md) | the immutable safety layer (never refined away) |
| [daily-briefing](daily-briefing.md) | morning and evening digest format |
| [autopilot](autopilot.md) | safe unattended progress rules |

## The rules

- Safety skills are **immutable** — the continual harness (`shesh-harness`) can refine
  supplemental state but never the base safety layer.
- New skills arrive as Markdown with frontmatter; because no code ships with them, a bad skill
  can degrade style but can never execute anything by itself.

> **Tip —** Treat the safety-governance skill as the highest-priority layer. It overrides the
> others, so a specialized skill can refine a task without weakening the guardrails.
