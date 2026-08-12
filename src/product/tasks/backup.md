# 6. Backup

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 6 of 16.

- [ ] `shesh-backup-mcp` → `run_backup` completes (after a manual first
      `restic init`)
- [ ] First backup verified: `restic -r <repo> snapshots` lists it
- [ ] `check_system_updates` reports pending pacman/AUR packages (read-only)
- [ ] **System update is never automatic** — it only notifies; you run `pacman -Syu`
- [ ] `clean_system_caches("user")` frees space without error
- [ ] A scheduled backup timer is enabled if you want daily unattended runs
- [ ] **Test a restore** to a temp dir before trusting backups

---
