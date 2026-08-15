# Release Channels

A channel is a release filter, much like the `core`, `testing`, and `devel` repositories of a
Linux distribution. Shesh routes every component through one of three channels so that
experimental work can never reach the machine you depend on.

## What each channel contains

| Channel | Contains | Promoted when | Runs on |
|---|---|---|---|
| `stable` | only components tagged `stable` in the manifest | canary soaks N days, no regressions, manual sign-off | your MSI Sword (production) |
| `canary` | `stable` + `canary` components | each component passes its own tests and the integration suite | a VM / secondary account |
| `devel` | everything (`stable` + `canary` + `devel`) | component works on a developer branch | development only |

The `stable` channel is the only one that touches the production laptop, the MSI Sword. `canary`
runs in a virtual machine or a secondary account where breakage is cheap, and `devel` holds
development work that has not yet earned a channel of its own.

## Channel-specific lockfiles

Each channel resolves to its own lockfile, which pins exact versions so a reinstall is
reproducible.

```bash
python scripts/resolve_manifest.py --channel stable  --out channels/stable.lock
python scripts/resolve_manifest.py --channel canary  --out channels/canary.lock
python scripts/resolve_manifest.py --channel devel   --out channels/devel.lock
```

## How promotion is gated

A change earns its way upward through a sequence of gates: lint, then unit tests, then
integration tests on an Arch/CachyOS container, then a hardware smoke test for display, GPU, and
audio, then a soak timer. No component reaches `stable` without clearing every gate, and every
promotion writes a btrfs snapshot before it applies, so a bad promotion is always reversible.

> **Note —** The gate scripts under `scripts/gates/` are planned; today the discipline is
> enforced manually and by CI.
