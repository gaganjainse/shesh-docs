# Manual verification tasks by area

Before the Shesh body is trusted on the MSI Sword 16 HX, a person must tick its health
by hand. This part breaks the fleet's verification checklist into twelve focused
chapters, one per subsystem, so each area can be read and checked on its own.

> **Note —** The full
> [Manual Verification Checklist](../../verification/manual-verification.md) (16
> sections, Part VII) is the canonical document for the hardware, accounts, and posture
> checks that must be ticked by hand on the real machine.

The twelve chapters below mirror sections 0 through 11 of that checklist. Sections 12
through 16 — rolling-dependency hygiene, security posture, the recovery drill,
deliberate-work items, and wiki setup — live only in the canonical checklist, so read
them there.

| Chapter | Area |
|---|---|
| [0](first-boot.md) | First boot on the MSI Sword 16 HX |
| [1](accounts-keys-secrets.md) | Accounts, keys, and secrets |
| [2](mcp-mesh.md) | The MCP server mesh |
| [3](voice.md) | Voice (shesh-voice / Newelle fork) |
| [4](gpu-power-mux.md) | GPU, power, and the MUX switch |
| [5](display-desktop.md) | Display and desktop |
| [6](backup.md) | Backup (restic) |
| [7](phone.md) | Phone (ADB, Realme Narzo) |
| [8](containers.md) | Containers and sandboxing |
| [9](agent-behavior.md) | Agent behavior |
| [10](security-audit.md) | Security and audit |
| [11](canary-releases.md) | Canary and releases |
