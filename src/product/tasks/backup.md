# Backup with restic

Backups are the safety net under every risky action the Shesh body takes. This chapter
confirms the restic vault is initialized, runs on schedule, and can actually be
restored.

> **Note —** This chapter is section 6 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Run and verify a backup

- [ ] `shesh-backup-mcp` → `run_backup` completes, after a manual first `restic init`.
- [ ] The first backup is verified: `restic -r <repo> snapshots` lists it.
- [ ] A scheduled backup timer is enabled if you want daily unattended runs.
- [ ] **Test a restore** to a temp directory before you trust the backups.

## System updates stay manual

The body may look at pending updates, but it never installs them on its own.

- [ ] `check_system_updates` reports pending pacman and AUR packages (read-only).
- [ ] System updates are **never automatic** — the body only notifies; you run
      `pacman -Syu`.
- [ ] `clean_system_caches("user")` frees space without error.
