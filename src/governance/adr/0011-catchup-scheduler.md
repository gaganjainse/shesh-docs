---
title: "ADR-0011: Schedule catch-up work rather than fixed cron"
type: explanation
summary: "Schedule catch-up work rather than fixed cron."
audience: maintainer
status: current
verified: 2026-08-15
---

# ADR-0011: Schedule catch-up work rather than fixed cron

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-08-09 |
| **Deciders** | Fleet maintainer |
| **Tags** | scheduling, laptop, ambient |

## Context

Laptop sleeps, shuts down, runs on battery. Fixed wall-clock timers (`02:00 daily`) misfire: job runs at boot mid-work, or misses backup window entirely. User complaint: "You assume 24/7 live; it isn't. Do not boot mid-work."

The fleet needs scheduling that respects laptop lifecycle, power, and user attention.

## Decision

Adopt **catch-up scheduler** (systemd timer with `OnStartupSec` + `OnCalendar` + jitter):

- `shesh-ambient` in `shesh-desktop` defines:
  - `OnStartupSec=5m` + `RandomizedDelaySec=2h` — jobs run soon after boot, not during boot storm.
  - Heavy jobs (backup, maintenance) need `ConditionACPower=true` + `idle` gate (no fullscreen/call/high-CPU).
  - Budget bounds: max runtime, CPU quota `IOSchedulingClass=idle`.
  - Courtesy policy: defer if fullscreen/game/call/low battery.
- Daily backup timer: `daily` + `Persistent=true` — if missed, runs at next boot.
- Proactive offers (ambient) not timer-driven: at natural pauses (45s–15m idle), throttled ≤3/day.

Not cron, not systemd `OnCalendar` alone.

## Consequences

### Benefits

- Laptop-friendly — no mid-work boot storm.
- Missed jobs eventually run (catch-up).
- AC + idle gating prevents battery drain.
- More complex than cron — need systemd user timers + ambient scheduler logic.
- Jitter makes exact timing non-deterministic — documented.

## References

- `docs/history/attic/desktop-mirror-2026-08-13/AMBIENT_DESIGN.md`, `docs/history/attic/desktop-mirror-2026-08-13/07_AUTOMATIONS.md` (canonical now: shesh-desktop repo docs/SHESH/)
- `shesh-desktop/tools/shesh-ambient/`
