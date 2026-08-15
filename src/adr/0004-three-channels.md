# ADR-0004: Three Release Channels

Shesh promotes code through three release channels — devel, canary, and stable — the way a
Linux distribution stages raw work into a soak test and then into the daily driver. The gate
keeps a broken Hyprland keybinding from ever landing on the machine a person depends on.

## Status

- **Date:** 2026-08-09
- **Status:** Accepted
- **Tags:** releases, promotion, safety

## Context

The developer machine is a CachyOS daily driver on an MSI Sword 16 HX. Breaking the desktop
shell blocks all work. The fleet needs staging like a distribution: raw work flows into an
integration soak, then into a stable release.

A naive single-branch release once pushed a workspace-over-budget state and broken Hyprland
keybindings straight onto `main`.

## Decision

Three channels enforce strict promotion:

- **devel** holds every component's `main` head; `devel.lock` covers all nineteen components
  (stable plus canary plus devel). It is daily development and may break.
- **canary** runs daily canary CI (`.github/workflows/canary.yml`) on the Arch/Fedora/Ubuntu
  matrix plus `e2e-canary.sh` covering all sixteen MCPs; `canary.lock` covers sixteen
  components and soaks for 24 hours.
- **stable** receives only `shesh-desktop` (the desktop) after a verified Btrfs snapshot, and
  is promoted manually after MANUAL_VERIFICATION.

The rules are mechanical. `resolve()` filters by rank: stable allows rank 0, canary rank 1 or
lower, devel rank 2 or lower. Promotion happens only through a pull request that includes
green CI and lock regeneration (`make check`). The installer supports
`--channel stable|canary|devel` with a pre-install Btrfs subvolume snapshot and a rollback
boot entry.

## Consequences

### Benefits

- Nothing reaches stable without canary end-to-end tests going green.
- The `channels/*.lock` files are SHA256-auditable.
- A developer can test canary in a VM or Distrobox before touching the laptop.

### Costs

- Three lockfiles must stay in sync; `make check` performs that work.
- Rollback depends on Btrfs, as documented — not on ext4.

## Links

- `channels/`, `scripts/e2e-canary.sh`, `Makefile`
- [ADR-0003: Federated Repos + Manifest](0003-federated-repos.md)
