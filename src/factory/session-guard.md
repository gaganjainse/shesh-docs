# session_guard.py — The Session Health Monitor

The guard is the smoke detector of a development session: it watches for the conditions that
preceded past context overflows and produces the handoff artifacts before answer quality drops.
This chapter lists what it measures, what it writes, and why two of its behaviors are
deliberately conservative.

Status: living · last verified 2026-08-13
Source: `tools/session_guard.py` · Protocol: [Session Protocol](session-protocol.md)

## What it measures

Every tick appends a record to `~/.local/share/shesh/session_guard.jsonl`. A single breach is
enough to recommend a hop.

| Metric | HOP threshold |
|---|---|
| Workspace size (`du -sh /home/user`) | > 100 MB |
| File count | > 8000 |
| Session age (first guard log to now) | > 60 min |
| Average tool latency, last 10 calls | > 5 s |
| Uncommitted changes | > 20 files |
| `make check` failing | Immediate HOP |

## Commands

```bash
python tools/session_guard.py --status    # read-only health report
python tools/session_guard.py --tick      # autopilot tick: log, alert if hot
python tools/session_guard.py --handoff   # write NEXT_SESSION_PROMPT + handoff.json
python tools/session_guard.py --clean     # drop caches to shrink the workspace
```

## Two deliberate restraints

The guard writes `docs/SESSION_HOP_ALERT.md` on a breach, and that file is untracked by design.
A committed alert becomes a lie within hours, so `.gitignore` excludes it and an archived
example is kept under `docs/history/attic/` for reference.

`--status` and `--tick` are strictly read-only. Credential cleanup happens only under an
explicit `--handoff`, because during the 2026-08-11 multi-tab incident a status call past the
60-minute mark deleted the plain personal access token out from under running daemons. See
[the incident post-mortem](../audits/incident-2026-08-11-multi-tab-swarm.md) for the full
chronology and [secure_pat.py](secure-pat.md) for the credential flow it touches.
