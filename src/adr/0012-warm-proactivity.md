# ADR-0012: Warm Proactivity at Natural Pauses

Shesh offers help only at a natural pause, at most three times a day, and always grounded in
real signals — helpful and warm without sliding into nagging. The design answers the user's
request to "be active, helpful, warm, not passive" while respecting that interruption is
worse than silence.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** ambient, ux, proactivity

## Context

The previous assistant was binary: passive (never helps) or interrupting (breaks flow during
work). The user asked for activity and warmth, but nagging is worse than silence — it breeds
notification fatigue.

Helpfulness had to arrive without annoyance: one optional, context-aware offer when the user
naturally pauses, backed by real data.

## Decision

The proactivity engine lives in `shesh-ambient`:

- **Trigger:** a natural pause is 45 seconds to 15 minutes idle — not while typing, in
  fullscreen, gaming, on a call, under high CPU, or at low battery.
- **Frequency:** at most three offers per day, a 30-minute cooldown, and snooze support.
- **Content:** one optional offer, grounded in real signals — pending system updates, dirty git
  repositories, backup age over 24 hours, an inbox count, or "you have 3 unsynced notes." These
  are live signals, not static strings.
- **Presentation:** a Quickshell overlay, dismissible with Esc and offering a "don't ask today"
  option.
- **Warmth:** mannerisms from `shesh-memory` (the user's preferred tone) are injected through
  the ContextAssembler.

The data-aware signals are wired in `signals.py` and `offer_for_moment()`.

## Consequences

### Benefits

- The system is helpful without nagging, capped at three offers per day.
- Offers are actionable — a real inbox, a real git status.
- Snooze and cooldown respect the user.

### Costs

- Real data probes are needed; `signals.py` must stay cheap by using a cache.
- GUI hookup remains a task: the ambient service to the Quickshell overlay.

## Links

- `docs/history/attic/desktop-mirror-2026-08-13/AMBIENT_DESIGN.md`
  (canonical now: `shesh-desktop` repository `docs/SHESH/`)
- `shesh-desktop/tools/shesh-ambient/signals.py`
- [ADR-0011: Catch-Up Scheduler](0011-catchup-scheduler.md)
