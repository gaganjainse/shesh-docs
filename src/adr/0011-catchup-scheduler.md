# ADR-0011: Catch-Up Scheduler, Not Fixed Cron

Shesh schedules maintenance with a catch-up timer that respects a laptop's life — sleep,
battery, and the user's attention — instead of firing fixed wall-clock jobs that boot the
machine mid-work. The design treats the laptop as a device that is often off, not a server
that is always on.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** scheduling, laptop, ambient

## Context

A laptop sleeps, shuts down, and runs on battery. Fixed wall-clock timers — "02:00 daily" —
misfire: a job runs at boot in the middle of work, or it misses the backup window entirely. The
user put it plainly: "You assume 24/7 live; it isn't. Don't boot mid-work."

Scheduling had to respect the laptop lifecycle, power state, and user attention.

## Decision

Shesh adopts a **catch-up scheduler** — a systemd timer with `OnStartupSec`, `OnCalendar`, and
jitter:

- `shesh-ambient`, inside `shesh-desktop`, defines:
  - `OnStartupSec=5m` plus `RandomizedDelaySec=2h` — jobs run soon after boot, not during the
    boot storm.
  - Heavy jobs (backup, maintenance) require `ConditionACPower=true` and an idle gate (no
    fullscreen, call, or high CPU).
  - Budget bounds: a maximum runtime, a CPU quota, and `IOSchedulingClass=idle`.
  - A courtesy policy that defers on fullscreen, game, call, or low battery.
- A daily backup timer uses `daily` plus `Persistent=true` — if missed, it runs at the next
  boot.
- Proactive offers from the ambient service are not timer-driven; they arrive at natural pauses
  (45 seconds to 15 minutes idle), throttled to three per day.

This is neither cron nor a lone systemd `OnCalendar`.

## Consequences

### Benefits

- The laptop stays friendly — no mid-work boot storm.
- Missed jobs eventually run through catch-up.
- AC and idle gating prevent battery drain.

### Costs

- The scheme is more complex than cron; it needs systemd user timers plus ambient scheduler
  logic.
- Jitter makes exact timing non-deterministic, as documented.

## Links

- `docs/history/attic/desktop-mirror-2026-08-13/AMBIENT_DESIGN.md`,
  `docs/history/attic/desktop-mirror-2026-08-13/07_AUTOMATIONS.md`
  (canonical now: `shesh-desktop` repository `docs/SHESH/`)
- `shesh-desktop/tools/shesh-ambient/`
- [ADR-0012: Warm Proactivity at Natural Pauses](0012-warm-proactivity.md)
