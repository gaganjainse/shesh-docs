# 11. Canary / releases

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 11 of 16.

- [ ] The daily canary GitHub Actions run is green
      (https://github.com/gaganjainse/shesh-ecosystem/actions)
- [ ] If you switch to **stable**, `btrfs snapshot` is taken before install
- [ ] Rollback works: boot the snapshot from grub/btrfs-grub
- [ ] Component versions in `manifests/components.toml` match what's installed

---
