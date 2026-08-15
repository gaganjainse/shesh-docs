# Master Index: The Verified Desktop Baseline

Before a single installer command runs, a project needs an agreed set of facts. This chapter sets that agreement for the Shesh desktop: it states the exact hardware, the exact operating system, the model budget the GPU can sustain, and a map of the ten documents that build on them.

## Summary of the verified baseline

- Every figure in this chapter was independently verified against the manufacturer product page and the CachyOS release notes on 2026-08-09, and supersedes two earlier AI-written audits.
- The two prior audits stated the wrong display resolution and the wrong GPU; the corrected values are 1920x1200 at 144 Hz and an RTX 4050 with 6 GB.
- The 6 GB VRAM ceiling, not ambition, sets the local model roster. One GPU model runs at a time.
- Ten numbered documents run in dependency order, so each is read, applied, and checked before the next begins.
- Seven design principles govern every future decision; a proposal that breaks one needs an explicit, written exception.

> **Owner:** Gagan Jain (`gaganjainse`), Jaipur, India (Asia/Kolkata)
> **Device:** MSI Sword 16 HX B14VEKG-210IN
> **Operating system:** CachyOS 260628 (Arch-based, Linux 6.18 live and 7.1 installed, BORE scheduler)
> **Desktop:** Hyprland 0.55 or newer (the Lua configuration era) with Quickshell `ii`, on top of `end-4/dots-hyprland`
> **Last reconciled:** 2026-08-09

This folder is the reference of record for the Shesh desktop: the production-grade, AI-first, hands-off environment built on the `shesh-desktop` fork. Every document here was verified against the live repository on 2026-08-09. Together they supersede two prior AI-produced audits — an uploaded `shesh-desktop-audit.md` and a 63-page master-plan PDF — both of which contained factual errors now catalogued in [the audit chapter](./01-audit.md).

> **Warning —** The later fleet-wide audit of 2026-08-15 confirmed that earlier AI-written audits across this project contained factual errors. Trust the verified tables below and the audit chapter; treat any figure from an undated source as unverified.

## How to read these documents

The build is driven with AI assistants, so the documents are ordered to be applied one at a time: open one, act on it, verify the result, then move to the next.

| # | Document | What it gives you | When to open it |
|---|----------|-------------------|-----------------|
| 00 | This chapter | The map, the verified facts, the status vocabulary | Always start here |
| 01 | [Audit — Current Truth](./01-audit.md) | An independent audit of the live repository, with exact fixes | Before touching code |
| 02 | [Roadmap — Phases 0 through 7](./02-roadmap.md) | A dependency-ordered plan with effort and risk | When planning a session |
| 03 | [Disk Structure](./03-disk-structure.md) | The on-disk layout separating work, personal, and job data, plus a bootstrap script | When you install CachyOS |
| 04 | [Device Profile](./04-device-profile.md) | MSI Sword and CachyOS tuning: GPU, MUX, 144 Hz, power, kernel | During hardware setup |
| 05 | [Smart Organizer v2](./05-smart-organizer.md) | The real-time, AI-assisted file organizer specification | When clutter becomes the problem |
| 06 | [Shesh Agent](./06-shesh-agent.md) | The agent itself: Newelle, Ollama, and MCP, local-first | When building the assistant |
| 07 | [Automations](./07-automations.md) | Every autonomous job, systemd unit, and udev rule | When making the system hands-off |
| 08 | [Ecosystem Tools](./08-ecosystem-tools.md) | The broader tool set, including the Android phone harness | When expanding the system |
| 09 | [AI Prompts](./09-ai-prompts.md) | Copy-paste prompts per phase and per situation | Every work session |
| 10 | [Licenses and Sources](./10-licenses-sources.md) | The license manifest and every version-pinned link | For legal review and upgrades |

A parallel set of machine-actionable files lives alongside them: the [implementation checklist](./checklist.md), one line per task, plus the real code the documents reference in `tools/lib/common.sh`, `profiles/msi-sword-cachyos/`, and their neighbours.

## The verified hardware and software baseline

These values were checked against the manufacturer product page and the CachyOS release notes on 2026-08-09. Use them everywhere, and source them from the profile rather than retyping them.

| Component | Verified value | Notes |
|-----------|----------------|-------|
| CPU | Intel Core i7-14700HX (20 cores, 28 threads, Raptor Lake-HX) | The `-march=native` target |
| Integrated GPU | Intel Arc / UHD, integrated in the 14700HX | Primary Wayland renderer, to save power |
| Discrete GPU | NVIDIA RTX 4050 Laptop, 6 GB GDDR6, 96-bit bus | Not a 4070, and not 8 GB |
| Display | 16-inch FHD+, 1920x1200 (16:10), 144 Hz, IPS | Not 2560x1600; connector `eDP-1` |
| RAM | 16 GB DDR5-5600 (one 16 GB module, one SODIMM slot free, 96 GB maximum) | An upgrade to 32 or 64 GB is strongly advised for local models |
| Storage | 1 TB NVMe Gen4, with one Gen4 and one Gen5 M.2 slot | The second slot is free |
| Network | Wi-Fi 6E (likely AX211) and 2.5 G Ethernet | |
| Ports | One Thunderbolt/USB-C with DisplayPort and power delivery, three USB-A, HDMI 2.1 (8K60 or 4K120), RJ45, audio | |
| Operating system | CachyOS 260628, Linux 6.18 live and 7.1 installed, GCC 14.1, Python 3.13 | BORE scheduler; `chwd` handles drivers |
| AUR helper | Shelly is the default; paru was removed but can be reinstalled, as can yay | The installer must auto-detect |
| Hyprland | 0.55 or newer, Lua configuration; 0.56 is in git and rolling will pull it | The dotfiles already use Lua |
| Display manager | SDDM is recommended for Hyprland on CachyOS | greetd remains optional |

### The model budget imposed by 6 GB of VRAM

A Q4_K_M model needs roughly its file size plus 1 to 1.5 GB of KV-cache headroom at a 4k context. That arithmetic, not preference, decides the roster below. Run one GPU model at a time, and push vision offload to the integrated GPU or CPU where it is supported.

| Role | Model | VRAM | Why it earns the slot |
|------|-------|------|-----------------------|
| Primary reasoning and chat | phi4-mini (3.8B Q4) | ~3.2 GB | The best quality-to-size ratio that fits 6 GB |
| Code | qwen2.5-coder:3b Q4 | ~2.8 GB | Fast, and strong on code |
| Embeddings and retrieval | nomic-embed-text | <0.5 GB | Small enough to co-reside with the primary model |
| Vision, for screenshots | moondream2 Q4 | ~2.5 GB | The smallest usable vision model |
| Occasional heavy work | qwen2.5:7b Q4 | ~4.6 GB | Needs partial CPU offload, and is slower |
| Avoid entirely | qwen3:14b, llava:13b, mistral:7b at 8k | 6–9 GB | Overflows 6 GB, causing thrashing or an out-of-memory failure |

> **Note —** With 16 GB of system RAM you can offload 7B layers to the CPU, but expect only 5 to 15 tokens per second. A 32 GB memory upgrade is the single largest quality improvement available for local AI on this machine, because it makes 7B to 9B models comfortable.

## The status vocabulary

Every issue in this document set carries one of five states. The authoritative issue list with current status lives in [the audit](./01-audit.md).

| Status | Meaning |
|---|---|
| **Broken** | Fails on a clean CachyOS 260628 install today |
| **Bug or risk** | Works sometimes, but is wrong or fragile |
| **Incomplete** | Scaffolded by a prior AI pass, but never finished |
| **Done** | Verified present and correct in the live repository |
| **New** | Proposed, not yet started |

## Seven principles that govern every decision

These principles are drawn from the project's own history: the SheshAOS design work (governance-first, event-sourced, with an append-only audit trail), SeshaOS (archived, now SHESH) and its local-first specialist models, Vyakrti as a Sanskrit programming language, a RAG service, and an LLM evaluation harness.

> **Note —** SheshAOS as a public upstream is unpublished and conceptual. Treat `gaganjainse/SheshOS` as a design reference, not as a reachable repository to clone or depend on.

1. **Local-first and private.** Voice, files, memory, and models run on the device. Cloud access is an opt-in fallback in the OmniRoute style, never the default.
2. **Governance and auditability.** Borrowing the SheshAOS append-only event log, every autonomous action Shesh takes is recorded, replayable, and reversible, and policy gates destructive actions.
3. **Performance without compromise.** Appearance (end-4's Material You with Quickshell polish) and speed (144 Hz, the CachyOS BORE scheduler, NVMe kyber) are both first-class, and bloat inherited from other distributions or devices is pruned.
4. **Hands-off.** If something can be automated safely, it is automated. You speak; the system acts.
5. **Composable rather than monolithic.** Small tools — the organizer, the MUX switcher, the backup job — are exposed over MCP and IPC, and one agent orchestrates them. There is no giant binary.
6. **The right language for each layer.** Rust for systems, watchers, and kernel-adjacent work; Python for AI glue; Lua and QML for the shell; Bash for the installer. This matches the existing Rust, Python, and TypeScript skill set.
7. **Indian-rooted identity.** The names — Shesh, Vyakrti, Nexus — and the Sanskrit and Indic framing are deliberate, and stay consistent across the system.

Every future decision aligns to these seven. A proposal that violates one needs an explicit exception recorded in this chapter.

## The vision in one paragraph

Shesh is the local AI layer between you and a CachyOS/Hyprland machine. It watches folders and organizes them, switches GPU and power profiles according to what you are doing, backs up and maintains the system in the background, and answers by voice through a Quickshell overlay — while writing every action to a SheshAOS-style audit log, so nothing it does is invisible or irreversible. Over time it becomes the desktop expression of the SheshAOS and SHESH thesis: an AI-first operating environment built on a fast, attractive, trustworthy open base.

## Where this fits

Read [the audit](./01-audit.md) next for the current defect list, then [the roadmap](./02-roadmap.md) for the order in which to fix it. The vocabulary used across the whole book is defined in the [glossary](../glossary.md).
