# Canary builds and releases

The daily canary is the heartbeat that proves the fleet still builds and passes after
each change. This chapter confirms the canary is green and that a bad release can be
rolled back to a snapshot.

> **Note —** This chapter is section 11 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Canary health

- [ ] The daily canary GitHub Actions run is green:
      https://github.com/gaganjainse/shesh-ecosystem/actions.

## Safe installs and rollback

- [ ] If you switch to **stable**, a `btrfs` snapshot is taken before install.
- [ ] Rollback works: boot the snapshot from grub or btrfs-grub.
- [ ] Component versions in `manifests/components.toml` match what is installed.
