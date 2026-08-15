# Tutorial — organize Downloads with Smart Organizer v2

Status: living · last verified 2026-08-13

The Smart Organizer turns `~/Downloads` from a pile into routed folders. Think of it as a sorting
clerk: something notices a new file arrives, something else decides where it belongs, and a third
piece actually moves it. Full reference lives in
[05_SMART_ORGANIZER_V2](https://github.com/gaganjainse/shesh-desktop/blob/main/docs/SHESH/05_SMART_ORGANIZER_V2.md)
inside `shesh-desktop`.

## How the pipeline flows

The work splits into three layers so that a bad decision can never destroy a file:

1. A **Rust watcher** notices new files in `~/Downloads`.
2. A **Python classifier** decides the destination and records which rule fired.
3. A **Bash apply layer** is the only mover — the layers that decide never touch your files
   themselves.

## Walkthrough

1. **Dry-run first.** The classification output shows the proposed destination for each file and
   the rule that fired. Nothing moves until the apply layer confirms.
2. **Override with the rules file.** Your editable rules file beats every heuristic — your rule
   always wins over the classifier.
3. **Go continuous.** Enable the systemd units (canonical unit files ship in the repository, so
   there are no here-doc installs) to watch Downloads around the clock.

## Verify it works

- [ ] Drop a known-type file, such as a `.pdf`, into Downloads and watch it land in the expected
  folder within seconds.
- [ ] Edit the rules file with an obvious override and confirm it preempts the classifier on the
  next matching file.
- [ ] Check that the apply layer logged each move — moves without log lines are a bug; report
  them.

This corresponds to [MANUAL_VERIFICATION §5](../../verification/manual-verification.md) (the
desktop section) on the hardware checklist.
