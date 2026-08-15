# Tutorial — voice, settings, and organizer working together

Status: living · last verified 2026-08-13

Components: [shesh-voice](https://github.com/gaganjainse/shesh-voice) (the Newelle fork) and
Smart Organizer v2 (in `shesh-desktop`).

This is the daily-driver flow: you speak to the assistant, it files your downloads, and the
settings overlay stays out of the way. The three pieces are independent, but the order in which
you set them up decides whether the experience is smooth.

## Setup order matters

1. **Voice overlay first.** Install `shesh-voice` per
   [GETTING_STARTED §1.5](../getting-started.md), then confirm the mini-window and hotkeys work
   (the Newelle upstream supports STT, TTS, and a wake word).
2. **Local model stack.** Voice talks to the local Ollama 6 GB stack; if Ollama is down, the model
   router falls back free-first (see [model-router](../../factory/model-router.md)).
3. **Then the organizer.** Follow [organize-downloads](organize-downloads.md) — dry-run, rules,
   systemd.

## The combined flow

- Say "Organize my downloads" and the organizer pipeline runs; every move is logged by the apply
  layer.
- Every tool call passes the audit guard. Organizer moves match the policy in
  [skills/POLICY](../../policies/skills-policy.md), and anything novel asks first.

## Verify

- [ ] Ask by voice to organize Downloads, then confirm the audit log shows the tool calls at
  `~/.local/share/shesh/audit/events.jsonl`.
- [ ] Confirm a deny case: ask the assistant to touch something under `~/.ssh` — it must refuse
  (policy `deny`, no confirmation prompt).
