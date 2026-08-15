# ADR-0009: Newelle Fork as shesh-voice with Overlay, Core Untouched

Shesh forks the Newelle voice assistant as `shesh-voice`, keeps its core untouched, and layers
Shesh-specific behavior in a separate overlay directory. The approach buys a complete voice
stack in days instead of months while preserving the ability to rebase on upstream.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** voice, stt, tts, upstream-rebase

## Context

The fleet needs wake word, speech-to-text, text-to-speech, a chat UI, and an MCP client.
Newelle (qwersyk/Newelle) is GPL-3.0 and already provides all of them: openwakeword,
faster-whisper, Piper/Kokoro/Edge TTS, subagents, skills, STDIO MCP since 1.4.5, a Telegram
interface, and an OpenAI-compatible local API.

Building voice from scratch would take months, and forking with heavy edits would make rebasing
painful.

## Decision

- Fork Newelle as `shesh-voice` (GPL-3.0) and keep the **core untouched**.
- Add an overlay directory, `shesh-overlay/`, containing:
  - `shesh-mcp-servers.json`, which wires all `shesh-*` MCP servers.
  - A default model of local Ollama `phi4-mini`, not a cloud model.
  - A wake word model: "hey shesh" via openwakeword.
  - An about-screen rebrand reading "Shesh (Newelle core)" with a link to the ecosystem.
- Build natively with Meson, not Flatpak, for host audio (PipeWire) and MCP stdio.
- Track upstream `main` with a weekly rebase job in `upstream_tracker.py`.

## Consequences

### Benefits

- A 14k-star voice stack arrives in days, not months.
- Upstream features — subagents, skills 1.3.5, chat folders 1.4.0 — merge cleanly.
- Local-first operation holds: Piper and faster-whisper run offline.

### Costs

- GNOME assumptions remain, so a Quickshell overlay is needed for Hyprland.
- TTS and STT model downloads are roughly 2 GB, documented in MANUAL_VERIFICATION.

## Links

- `shesh-voice` repository, `shesh-voice/shesh-overlay/`
- `docs/components/shesh-voice.md`
- `docs/SOURCES.md` §A
