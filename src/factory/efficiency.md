# Efficiency — Longer Sessions for No Money

Cloning 22 repositories into every session cost minutes of setup and cut session life to under
an hour, all to edit one component. This chapter collects the free techniques that took the
working set from 36 MB to 2 MB and stretched a session from 60 minutes to two or three hours,
with no paid API involved.

## Summary

- Selective, shallow, blob-filtered cloning is the single largest win: 36 MB and about 3000
  files become 2 MB and a few hundred.
- Running only the gates that matter for the component you touched saves roughly 80 percent of
  gate time.
- Deterministic stubs keep every component testable offline, so no session ever needs a paid
  model.
- Offline file queues beat the GitHub Issues API on a phone with poor network.
- GitHub Actions carries the long unattended work for free on public repositories, so browser
  tabs do not have to.

## The core problem: a workspace that outgrows its session

A session workspace behaves like a suitcase with a weight limit. Everything you pack is
available, but past a certain weight the airline stops cooperating — and in this case the
airline is the sandbox, which slows down and eventually declares the workspace over budget.

Before selective cloning, every worker ran a full clone of all 22 repositories, including the
largest: `shesh-voice` at 41 MB, `shesh-desktop` at 22 MB, `SheshAOS` at 7.5 MB, and
`shesha-kernel` at 4.5 MB. The `src/` tree reached 36 MB across roughly 3000 files, the workspace
reached 88–113 MB, and the guard called a hop after 30 to 60 minutes.

## Selective clone: the largest single win

`tools/setup_worker.py` clones only the repositories a role touches, using
`--depth 1 --single-branch --filter=blob:none`. The blob filter matters most for the large
repositories, because it fetches commits and trees while deferring file contents until something
actually reads them.

| Role | Before | After | Size | Files | Session length |
|---|---|---|---|---|---|
| Brain | 22 repos, 36 MB | `shesh-audit`, `shesh-secrets`, `SheshAOS` — 3 repos | ~8 MB | ~600 | 120–180 min |
| Mind | 22 repos, 36 MB | audit plus memory, mind, harness, orchestrator, skills, calendar — 7 repos | ~2 MB | ~500 | 120 min |
| Soma | 22 repos, 36 MB | audit plus files, shell, system, backup, phone, containers, mcp-bundle, acp — 9 repos | ~2 MB | ~700 | 120 min |
| Platform | 22 repos, 36 MB | none — only the ecosystem repository itself | 0 MB | no extra | 150 min |
| Single component (`shesh-memory`) | 22 repos | audit plus memory — 2 repos | ~0.6 MB | ~200 | 150 min |

```bash
python tools/setup_worker.py --role mind --clean
python tools/setup_worker.py --component shesh-memory
du -sh src/ && find src/ -type f | wc -l
```

The swarm worker calls `setup_worker` before starting work when you pass `--setup`. Full detail
lives in [setup_worker.py](setup-worker.md).

## Keeping the toolchain out of the sandbox

A Rust toolchain — `~/.cargo` plus `~/.rustup` — costs roughly 1 GB and puts the workspace over
budget immediately. The session handoff document therefore forbids installing Rust in the
sandbox; CI has it instead. Brain work that genuinely needs `cargo test` runs in the
`Containerfile` image, or tests only the component that changed rather than the whole workspace.

## Cleaning caches, and cleaning them often

```bash
python tools/session_guard.py --clean
# removes __pycache__, .pytest_cache, .ruff_cache, .venv, src/*/target, src/*/dist
```

`session_guard.py --tick` logs workspace size and file count and calls a hop when either passes
its threshold; cleaning resets both. `setup_worker.py --clean` performs the same cleanup as part
of workspace setup.

## Running only the gates that apply

The full `make check` runs ruff, 30 ecosystem tests, the license gate, and resolution of three
channel locks in about 10 seconds. When work is confined to one component, a narrower set answers
the same question far faster.

```bash
python -m pytest tests/test_manifest.py -q       # ~1 s
python -m ruff check src/shesh-memory/           # ~0.5 s
cd src/shesh-memory && python -m pytest tests/ -q  # ~1 s
```

That saves roughly 80 percent of the time. Workers accept a `--component` filter so they run
only the tests for the component they claimed.

> **Note —** Narrow gates are for iteration. The full `make check` still runs before a push,
> and the auto-merge workflow runs it again on GitHub.

## File queue versus the Issues API

The two swarm backends trade differently, and the right choice depends on the network you are
on rather than on which is more sophisticated.

| Backend | Strengths | Costs |
|---|---|---|
| GitHub Issues API | True atomicity, visible in the web interface | Needs a token and network; 5000 requests per hour; added latency |
| File queue (`swarm/queue/*.json`) | Offline, no API calls, no rate limit, faster | Coordination relies on atomic `git push` |

Travelling with one tab on a weak connection, prefer the file queue:
`python tools/swarm/worker.py --component shesh-memory`, without `--github`. It uses only
`git push`. The hourly janitor workflow uses the file-queue requeue logic for the same reason.
See [Swarm](swarm/README.md) for both backends in full.

## Credentials that survive a hop without being rewritten

The encrypted token at `~/.config/shesh/github.pat.enc` (mode 600) persists across sessions,
because `.gitignore` only excludes it from Git, not from the workspace snapshot. The plain copy
is deleted on handoff, so the next session reports `need_password=true` and prompts once through
the interface rather than on every tool call. No external secret manager is needed; see
[secure_pat.py](secure-pat.md).

## Free models, and no model at all

Every component ships a deterministic stub, which is why the test suite is green with no model
available. `shesh-orchestrator` calls Ollama when it is present and otherwise falls back to a
stub that returns valid JSON steps; `shesh-memory` uses a local hash embedder offline and
`nomic-embed-text` when available; `shesh-harness` uses `make_ollama_responder()` when Ollama is
reachable and a stub when it is not.

```bash
ollama pull phi4-mini qwen2.5-coder:3b moondream2 nomic-embed-text
# all 6 GB-safe, free, no API key
```

In a sandbox with no GPU, the stubs keep the system working at zero cost. GitHub Models is the
other free path: the inference endpoint at `https://models.github.ai/inference` accepts
`GITHUB_TOKEN` and is free for public repositories, and a small `tools/llm_free.py` calling
`https://models.inference.ai.azure.com` with that token would need no paid key at all. The
gateway chapter on [free providers](../gateway/free-providers.md) surveys the rest.

## Two habits that cost nothing

A platform worker — docs, decision records, `Containerfile`, `install.sh`, CI, swarm tooling —
needs no `src/` clones whatsoever, and works directly in the ecosystem repository. That is the
most efficient configuration available, and `ROLE_MAP["platform"] = []` encodes it.

The workspace also persists between sessions apart from caches, so a repository cloned once is
still there next time. `clone_repo()` checks for an existing directory and runs
`git pull --ff-only --depth 1` instead of cloning again. The first worker to run a selective
clone pays the cost; every later session reuses it.

## Unattended hours on GitHub, not in a browser tab

GitHub Actions is free for public repositories at 2000 Ubuntu minutes per month.
`swarm-scheduled.yml` runs hourly for three to five minutes on `GITHUB_TOKEN` rather than a
personal token, so it costs nothing. Three workflows do useful unattended work: `ci.yml` for
ruff, tests, license, and locks; `swarm-auto-merge.yml` to merge green `swarm/*` pull requests;
and `swarm-scheduled.yml` to seed issues, requeue stale claims, and push refreshed locks and
docs. Keep one orchestrator tab and let the workflows carry the hours — see
[Travel Mode](travel-mode.md).

## The travelling checklist

- Use `tools/setup_worker.py --role mind --clean` rather than cloning 22 repositories.
- Prefer the file-queue worker when the network is poor.
- Run only the relevant tests while iterating on a single component.
- Keep the token encrypted and enter the password once per session.
- Rely on deterministic stubs offline; use free local Ollama models on the laptop.
- Keep one orchestrator tab open and let Actions handle the janitor and merge work.
- On handoff, run `session_guard --handoff` to delete the plain token and clean caches.

Together these take a session from 60 minutes to 120–180 minutes, the workspace from 113 MB to
40–60 MB, and the file count from about 3400 to about 800 — with no money spent.
