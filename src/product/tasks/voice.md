# Voice with the Newelle fork

Voice turns the Shesh body from a thing you type at into a thing you talk to. This
chapter confirms the wake word, transcription, and speech synthesis all work through
the shesh-voice fork of Newelle.

> **Note —** This chapter is section 3 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Keep the fork aligned

`shesh-voice` is an active fork that tracks the upstream `qwersyk/Newelle` project.

- [ ] The fork `gaganjainse/shesh-voice` tracks upstream `qwersyk/Newelle`
      (rebase occasionally).

## Wire the local model

- [ ] Copy the overlay configuration:
  - [ ] `cp shesh-overlay/shesh-mcp-servers.json ~/.config/Newelle/mcp-servers.json`
  - [ ] Set the default model to the local Ollama `phi4-mini`.
- [ ] The wake word **"hey shesh"** triggers listening (openwakeword).
- [ ] Speech-to-text transcribes your voice accurately (try faster-whisper).
- [ ] Text-to-speech reads responses aloud.
- [ ] Microphone permission and PipeWire access are not blocked.
