---
name: daily-briefing
description: Produce a concise morning briefing: calendar/tasks, weather, system health, updates, unread notes.
---

# Daily Briefing Skill (08:00)

A good morning briefing is five lines, not fifty. This skill gathers the day's essentials —
health, updates, agenda, and inbox — into a short spoken summary plus a dated note.

## What it gathers

1. **System health:** `get_system_status` (battery, RAM, GPU temperature), failed units, and
   the last backup.
2. **Updates:** the number of pending repository and AUR packages (notify, never auto-update).
3. **Agenda:** today's note `~/Notes/Daily/YYYY-MM-DD.md` and any reminders due.
4. **Weather:** optional, only if configured and online.
5. **Inbox:** files in `~/Documents/Inbox` and unprocessed notes.

## Output

A short spoken summary (five lines or fewer) plus a Markdown section appended to today's daily
note. Flag anything red — low disk, high temperature, backup failure — prominently.

> **Tip —** The briefing notifies about updates but never applies them. An unattended upgrade
> is exactly the kind of silent change the fleet's safety skill is built to prevent.
