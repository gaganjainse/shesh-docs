# Display and desktop

The desktop is the face the Shesh body shows you, and a flickering or mis-scaled screen
breaks trust faster than any bug. This chapter confirms the display, notifications, and
the ambient-offer overlay behave on the real hardware.

> **Note —** This chapter is section 5 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Smoothness and capture

- [ ] The refresh rate holds at **144 Hz** and does not drop to 60.
- [ ] Fractional and HiDPI scaling look correct.
- [ ] Screen recording and screenshots work through the `grim` + `slurp` pipeline.
- [ ] Notifications appear and are not duplicated.
- [ ] The idle inhibitor works during video and media.

## The ambient offer overlay

The overlay is the body's way of suggesting a task at a natural pause. It is built to be
quiet, not naggy.

- [ ] The ambient offer appears at natural pauses — not while you type or game — and
      never nags: at most **three offers per day** with a **30-minute cooldown**.
