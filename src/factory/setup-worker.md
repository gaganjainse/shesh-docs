# setup_worker.py — Cloning Only What a Role Touches

A swarm worker assigned to the Mind layer has no use for the desktop repository, yet early
sessions cloned the entire fleet anyway and paid for it in setup time and session length. This
tool clones exactly the repositories a role needs, shallow and blob-filtered, so a fresh
workspace is ready in seconds.

Status: living · last verified 2026-08-13
Source: `tools/setup_worker.py` · Rationale: [Efficiency](efficiency.md)

## Usage

```bash
python tools/setup_worker.py --role brain --clean
python tools/setup_worker.py --role platform --clean
```

Four roles are defined — `brain`, `mind`, `soma`, and `platform` — and each maps to a fixed
component list held in one place, the role table inside `setup_worker.py`. The `--clean` flag
resets the workspace layout before cloning.

Every clone uses `--depth 1 --filter=blob:none`. Measured on 2026-08-11, that took a full
checkout from 36 MB to roughly 1.3–3.3 MB and from about 3000 files to about 300; the
measurement is recorded in
[the incident chronology](../audits/incident-2026-08-11-multi-tab-swarm.md), Tab 2.

## What it repairs on boot

Two failures during that incident traced back to workspace state rather than code, so the tool
now fixes both as it sets up. It writes a repository-local Git identity, because a missing
identity produced silent empty-commit failures that surfaced only as HTTP 422 responses when
opening pull requests. It also wires credentials through the secure token loader, so a worker
that cannot authenticate fails closed instead of pushing nothing and reporting success.

See [Efficiency](efficiency.md) for the per-role size and session-length figures, and
[github_auth.py](github-auth.md) for the credential path.
