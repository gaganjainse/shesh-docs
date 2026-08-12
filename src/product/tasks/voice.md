# 3. Voice (shesh-voice / Newelle fork)

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 3 of 16.

- [ ] Fork `gaganjainse/shesh-voice` is tracking upstream `qwersyk/Newelle`
      (rebase occasionally)
- [ ] The overlay config copied:
  - [ ] `cp shesh-overlay/shesh-mcp-servers.json ~/.config/Newelle/mcp-servers.json`
  - [ ] Default model set to local Ollama `phi4-mini`
- [ ] **Wake word "hey shesh"** triggers listening (openwakeword)
- [ ] Speech-to-text transcribes your voice accurately (try faster-whisper)
- [ ] Text-to-speech reads responses aloud
- [ ] Mic permission / PipeWire access not blocked

---
