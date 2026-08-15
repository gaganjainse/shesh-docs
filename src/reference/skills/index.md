---
title: Skills
type: reference
summary: "The agent skill library, its file format, the permission model, and the rules that govern it."
audience: operator
status: current
verified: 2026-08-15
---

# Skills

A skill packages instructions for a recurring class of task. Skills are text
only: a skill can shape how an agent reasons or writes, but it cannot execute
anything by itself.

Shesh follows the [Agent Skills specification](https://agentskills.io), so these
skills load unmodified in Claude Code, Codex, Cursor, and other compliant
agents. `shesh-skills` is the canonical source; this page links to each skill
rather than copying it.

## Permission model

This is the most misunderstood part of the format, so it is stated first.

**`allowed-tools` is a pre-approval, not a sandbox.** It lets an agent use the
listed tools during the turn that invokes the skill without prompting for
permission. It grants; it removes nothing. Every tool remains callable whether
or not it appears in the list.

Three consequences follow:

- Adding `allowed-tools` to a skill **widens** the permission surface. Each
  entry is a decision that must be justified by the skill's own body.
- A grant is scoped, never blanket. Write `Bash(git status:*)`, not `Bash`.
- **A safety skill must not carry a grant at all.** `safety-governance` is
  always active, so any grant on it would widen every session in the fleet —
  precisely the opposite of its purpose.

Restriction is a separate mechanism: `disallowed-tools` in Claude Code, or the
`shesh-audit` policy engine for enforcement that works in any client. A skill
cannot enforce itself, so `safety-governance` declares its dependency on the
policy engine in its `compatibility` field. Without that engine, the skill is
advisory text.

## The library

| Skill | Purpose | Pre-approved tools |
|---|---|---|
| [`audio-control`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/audio-control/SKILL.md) | Control output volume, list audio devices, and switch the active sink | none |
| [`audit-review`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/audit-review/SKILL.md) | Inspect the audit log and verify its integrity | none |
| [`autopilot`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/autopilot/SKILL.md) | Make safe unattended progress on the backlog | yes |
| [`backup-run`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/backup-run/SKILL.md) | Run, inspect, and prune backups | none |
| [`bluetooth`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/bluetooth/SKILL.md) | Pair, connect, disconnect, and list Bluetooth devices | none |
| [`brightness`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/brightness/SKILL.md) | Read and set screen brightness | none |
| [`calendar-check`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/calendar-check/SKILL.md) | Read the calendar and report what is scheduled | none |
| [`clipboard`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/clipboard/SKILL.md) | Read and replace the clipboard | none |
| [`coding`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/coding/SKILL.md) | Write, test, and refactor code safely | yes |
| [`daily-briefing`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/daily-briefing/SKILL.md) | Produce the morning or evening digest | yes |
| [`disk-cleanup`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/disk-cleanup/SKILL.md) | Reclaim disk space by clearing caches and reporting what is consuming storage | none |
| [`docs-writer`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/docs-writer/SKILL.md) | Write or revise documentation in the house style | yes |
| [`file-organizer`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/file-organizer/SKILL.md) | Sort files into folders by type, date, or project | none |
| [`git-inspect`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/git-inspect/SKILL.md) | Report repository state, recent history, and what has changed | yes |
| [`gpu-mode`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/gpu-mode/SKILL.md) | Inspect and switch the hybrid graphics MUX between integrated and discrete mode | none |
| [`messaging-send`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/messaging-send/SKILL.md) | Send and read messages through connected bridges | none |
| [`model-routing`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/model-routing/SKILL.md) | Choose which model handles a task and inspect what is installed | none |
| [`notes-capture`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/notes-capture/SKILL.md) | Append to and search the Markdown notes vault | none |
| [`notifications`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/notifications/SKILL.md) | Send a desktop notification | none |
| [`policy-inspect`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/policy-inspect/SKILL.md) | Explain what the agent is currently permitted to do and why an action needs confirmation | none |
| [`power-profile`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/power-profile/SKILL.md) | Switch the system power profile between performance, balanced, and power-saver | none |
| [`process-inspect`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/process-inspect/SKILL.md) | Find what is consuming CPU, memory, disk, or network | none |
| [`safety-governance`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/safety-governance/SKILL.md) | The immutable safety layer governing destructive and irreversible actions | none |
| [`sandbox-run`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/sandbox-run/SKILL.md) | Run an untrusted command inside a rootless container with no network | none |
| [`screen-recording`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/screen-recording/SKILL.md) | Start and stop screen recording | none |
| [`screenshot-capture`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/screenshot-capture/SKILL.md) | Take a screenshot of the screen, a window, or a region | none |
| [`secrets-handling`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/secrets-handling/SKILL.md) | Store and retrieve credentials without exposing them | none |
| [`service-control`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/service-control/SKILL.md) | Inspect and restart systemd units | none |
| [`session-control`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/session-control/SKILL.md) | Lock, suspend, hibernate, log out, reboot, or power off | none |
| [`system-health`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/system-health/SKILL.md) | Report overall machine state: load, memory, disk, temperature, and failed services | none |
| [`system-updates`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/system-updates/SKILL.md) | Check for and report pending system package updates | none |
| [`thermal-check`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/thermal-check/SKILL.md) | Report CPU and GPU temperature, fan behaviour, and thermal throttling | none |
| [`wallpaper`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/wallpaper/SKILL.md) | Set the desktop wallpaper | none |
| [`web-research`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/web-research/SKILL.md) | Research a topic from primary sources and report with citations | none |
| [`wifi`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/wifi/SKILL.md) | Inspect and change network connections, including Wi-Fi and airplane mode | none |
| [`window-appearance`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/window-appearance/SKILL.md) | Adjust window opacity, floating state, and fullscreen | none |
| [`workspace-control`](https://github.com/gaganjainse/shesh-skills/blob/main/skills/workspace-control/SKILL.md) | Switch workspaces, move windows between them, and list what is open where | none |

## File format

Each skill is a directory containing `SKILL.md`:

```text
skills/
└── power-profile/
    └── SKILL.md
```

The file has YAML front matter followed by a Markdown body:

```yaml
---
name: power-profile
description: Switch the system power profile between performance, balanced, and
  power-saver. Use when the user asks to save battery or speed the machine up.
license: GPL-3.0-or-later
---
```

| Field | Required | Constraint |
|---|---|---|
| `name` | Yes | Kebab-case, at most 64 characters, matches the directory name |
| `description` | Yes | At most 1,024 characters; states what the skill does **and** when to use it |
| `license` | No | SPDX identifier |
| `compatibility` | No | Environment requirements, at most 500 characters |
| `allowed-tools` | No | Tools pre-approved while the skill is active |
| `metadata` | No | Free-form key-value map |

No other keys are permitted. A spec-compliant packager rejects unknown fields
with a hard error rather than ignoring them, so an extra key breaks portability.

## Loading

Skills use progressive disclosure: listing a skill costs only its name and
description, and the body is read when the skill is selected.

| Tool | Returns |
|---|---|
| `list_skills` | Name, description, licence, and grants for every skill |
| `get_skill(name)` | The same metadata plus the instruction body |

Resolution order, first match winning, so a user skill overrides a shipped one:

1. `$SHESH_SKILLS_DIR`
2. `$XDG_DATA_HOME/shesh/skills`
3. The directory shipped with the package

A malformed skill is skipped rather than raising, so one bad directory cannot
make the rest unavailable.

## Coverage

Every skill names the specific Model Context Protocol tool it calls. A skill is
not written for a capability the fleet does not expose, because its instructions
would fail at the first call and the agent would believe the job was possible.

Capabilities without a backing tool are recorded in
[GAPS.md](https://github.com/gaganjainse/shesh-skills/blob/main/GAPS.md), with
the interface each would need and a candidate upstream where one exists.

## Rules

- Safety skills are immutable. The continual harness may refine supplemental
  state, never the base safety layer.
- No code ships with a skill. A poor skill can degrade style but cannot act.
- The description is the routing signal. It is the only text an agent sees
  before deciding to load the skill.
- Every destructive step names its irreversibility and requires confirmation.
- Tool risk classes are defined in the
  [skills policy](../../governance/skills-policy.md).

## Validation

```bash
python3 -m pytest tests/test_skills_spec.py -q
```

The suite checks layout, frontmatter fields and limits, name and directory
agreement, description quality, body length, loader behaviour, that no skill
pre-approves a bare shell, and that `safety-governance` carries no grant.

## Related

- [Agent context files](../agent-files.md) — how skills relate to `AGENTS.md`.
- [Multi-agent orchestration](../../explanation/multi-agent.md) — role dispatch.
- [Skills policy](../../governance/skills-policy.md) — tool risk classes.
