# Fork Gardening Policy

A fork is a liability until the living documentation or a manifest proves it earns its
place. This chapter records Decision D2 (executed 2026-08-13): a fork stays only if living
docs or a manifest cite it as active plumbing or a load-bearing study source.

## The rule

A fork earns its place only if living documentation — excluding immutable history such as
QUERYLOG, ADRs, changelogs, and audit snapshots — or a manifest cites it as active plumbing
or a load-bearing study source. Uncited or strictly-superseded forks are **archived, never
deleted**. Archiving is reversible with one API call and preserves every byte.

Think of the fork list as a garden, not a graveyard: plants that no longer get cited are
lifted into cold storage where they can be replanted, not composted.

## Verdicts from the 2026-08-13 sweep

| Fork | Verdict | Reason |
|---|---|---|
| hyprdots | **archived** | Stale (upstream last push 2025-03); strictly superseded by Hyprland-Dots (2026-02) as the dots study base. Live docs cite the *upstream* project, never the fork. |
| Hyprland-Dots | keep | Cited in 6 living docs including manifests; the current dots study and reference base for the shesh-desktop lineage. |
| register | **archived** | Zero true citations — every "register" hit is the English word, not the repo. |
| Hermes-Function-Calling | **archived** | Zero citations anywhere in living docs. |
| leon | **archived** | Only parked as a 🔜-study entry (SOURCES.md, skills architecture). The fork is unconsumed; the upstream pointer stays in SOURCES.md for later mining. |
| khoj | **archived** | Only appears in an audit tally; nothing living cites it. |
| servers | keep | 39 living references — the MCP protocol reference; load-bearing. |
| ollama | keep | 14 living references, manifest-cited — local-model plumbing. |
| OmniRoute | keep | 13 living references, 2 manifest entries — the free-model gateway for the ecosystem. |
| openWakeWord | keep | 3 living references — wake-word path for shesh-voice. |
| phone-harness | keep | 6 living references, manifest-cited — the shesh-phone lineage. |
| Memento-Skills | keep | 3 living references, manifest-cited — skills architecture source. |
| prime-agent | keep | 4 living references, manifest-cited — orchestrator study source (D6 lineage). |
| pipecat | keep | 2 living references — voice-pipeline study source. |
| browser-use | keep | 3 living references — shesh-browser automation study. |
| waveterm | keep | Active local clone; the shell and terminal substrate direction for SheshAOS. |

## Re-audit trigger

Any fork whose living-doc citation count drops to zero at a quarterly review is archived at
the next orchestrator session.

> **Note —** Archiving preserves the repository intact. If a future decision reverses a
> verdict, the fork returns to active status with a single API call.
