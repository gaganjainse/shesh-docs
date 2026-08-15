# Shesh Documentation

This directory is the single source of truth for the Shesh ecosystem — the production-grade, local-first, AI-assisted desktop built on this fork of `end-4/dots-hyprland` for the MSI Sword 16 HX B14VEKG on CachyOS 260628.

**Start with [`00-index.md`](00-index.md).** It contains the verified hardware/software facts (correcting errors in earlier AI audits) and the map of every document.

| Document | Purpose |
|---|---|
| [00-index](00-index.md) | Master index, verified facts, philosophy, vision |
| [01-audit](01-audit.md) | Independent audit of the live repo — every issue with exact fixes |
| [02-roadmap](02-roadmap.md) | Phased execution plan (effort, dependencies, exit criteria) |
| [03-disk-structure](03-disk-structure.md) | On-disk layout: job vs personal vs projects, backup policy |
| [04-device-profile](04-device-profile.md) | MSI Sword + CachyOS tuning: GPU/MUX, 144 Hz, power, kernel |
| [05-smart-organizer](05-smart-organizer.md) | Real-time AI file organizer (Rust watcher + Python classifier) |
| [06-shesh-agent](06-shesh-agent.md) | The voice agent: Newelle + Ollama + MCP + audit log |
| [07-automations](07-automations.md) | Every autonomous job, unit, and udev rule |
| [08-ecosystem-tools](08-ecosystem-tools.md) | More tools to build + what to borrow from other repos + phone harness |
| [09-ai-prompts](09-ai-prompts.md) | Copy-paste prompts for AI pair-programming per phase/situation |
| [10-licenses-sources](10-licenses-sources.md) | License manifest, pinned versions, all links audited |
| [checklist](checklist.md) | Tick these as you implement |

The audit and roadmap supersede the two earlier AI documents you provided (`shesh-desktop-audit.md` and the 63-page master-plan PDF). Both contained errors — most notably the wrong display resolution and GPU, plus new bugs introduced while "fixing" the repo — all catalogued in `01-audit.md`.

> **Note —** SheshAOS as a public upstream is unpublished and conceptual. Treat `gaganjainse/SheshOS` as a design reference, not as a reachable repository to clone or depend on.
