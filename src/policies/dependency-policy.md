# Dependency Policy — Rolling With the River, Never Drowning in It

CachyOS, the fleet's operating system, is rolling-release: the packages it depends on move
underneath it every week. This chapter sets the discipline for staying near latest without
drowning in breakage.

- Depend on near-latest by default, with deliberate ceilings, not floating pins.
- Automation moves versions; humans and CI approve the move.
- A breaking release is held back one version, at most twice, before replacement.
- Warnings are CI failures, so tomorrow's deprecation is caught today.

## Why this exists

The OS beneath Shesh is rolling. Packages move weekly, and a static lockfile would quietly
rot. The policy is to **design for motion** — stay near latest in a controlled way, with gates
that catch breakage early and a written protocol for when they do.

## The rules

1. **Near-latest by default.** Python dependencies pin minimums plus a curated ceiling (for
   example, `fastmcp>=3.4.7,<4`); ceilings lift deliberately, not by accident.
2. **Automation moves versions, humans approve.** Dependabot (pip and github-actions, weekly,
   grouped) opens the pull requests; CI gates answer "is it safe"; a human or session merges.
   Pins without a mover rot; movers without gates are roulette. The fleet has both.
3. **Conflict protocol (user-specified):** a new release breaks the fleet → land the rest,
   hold the offender back ONE version with a dated comment naming the failure. Still broken
   next cycle → hold again, at most twice. A fundamental break (upstream removed the
   behavior) → **replace the dependency**; never indefinite pinning, never impulsive forking.
   All three outcomes are recorded in `TODO.md` as they happen.
4. **Deprecation watch:** no dependency on a project archived upstream (gap check quarterly);
   no Python or Rust standard-library-deprecated APIs (`pytest -W error` and clippy enforce
   this continuously — warnings are CI failures here).
5. **New dependencies are a decision, not an accident:** check `SOURCES.md` and the steal-
   first rule first; record in `manifests/components.toml` for ecosystem components; license
   must be declared (`scripts/check_licenses.py` gates). License must be GPL-3-compatible.
6. **Rust:** `cargo update` is a deliberate act run at the quarterly review with the full gate
   chain (deny, machete, `clippy -D warnings`, tests); `Cargo.lock` is committed so runners
   and machines agree.

## Rolling resilience, concretely

"Resistant, not break" means a specific set of defenses:

- **`canary.yml` plus scheduled full-matrix CI** give early warning: upstream drift breaks the
  canary first, not the user.
- **Warnings-as-errors fleet-wide** (`pytest -W error`): deprecation warnings are tomorrow's
  breakage, caught at deprecation time.
- **The desktop never hard-depends on a specific glibc or pacman behavior**: components probe
  (`shutil.which`, capability flags) and fail *loudly and honestly* rather than fabricate
  (SF-audited).
- **`shesh-backup` plus [Recovery](./recovery.md)**: pre-upgrade snapshots are the rollback,
  the runbook is the restore, and `tools/dr_check.sh` verifies readiness.
- **Kernel and driver moves (CachyOS plus NVIDIA class):** vendor quirks stay behind the
  `shesh-system` capability layer, so a kernel change degrades one tool honestly instead of
  crashing a stack.

## Better-alternative reviews

The quarterly review asks, per dependency: is there a maintained, license-clean, measurably
better alternative worth stealing? Adoptions are recorded as ADRs. The bar for switching:
maintained momentum, real gain, and migration cost below the gain within a month of
engineering time.

> **Tip —** When a dependency breaks, resist the urge to pin forever. The policy's hold-twice
> limit exists to force a decision, not to paper over a fundamental incompatibility.
