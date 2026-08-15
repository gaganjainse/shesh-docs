# Travel Mode — One Tab on a Phone, Two Days Without a Laptop

Away from the laptop with only a phone, a browser tab is the weakest link in the whole system:
mobile operating systems suspend background tabs within a minute. This chapter explains honestly
what keeps running under those conditions, what does not, and how to shift the long hours onto
GitHub Actions instead.

## Summary

- Agent sessions in a browser are not daemons. They advance only while the tab is alive, so a
  locked phone stalls them.
- A sidebar full of worker tabs is the least reliable arrangement on mobile; one orchestrator tab
  is more useful than five stalled ones.
- GitHub Actions runs on GitHub's infrastructure and is the only component that genuinely runs
  unattended for days.
- Three workflows cover continuous integration, auto-merge of swarm branches, and an hourly
  janitor pass.
- The practical pattern is to push branches before leaving, then let auto-merge and the janitor
  work through them.

## What actually keeps running on a phone

Each agent chat is a server-side session that makes its tool calls through a WebSocket owned by
your browser tab. That distinction is the whole story: the session's state lives on a server, but
its forward motion depends on a socket in a tab that a mobile operating system is free to freeze.

In practice, iOS and Android throttle timers and may suspend the tab within 30 to 60 seconds of
the screen locking. Safari on iPhone is the most aggressive; Chrome on Android is somewhat better
but still throttles interval timers.

The sidebar creates a misleading impression. Chats opened earlier on a laptop still exist
server-side and still appear in the list, but their Python loops — `while True: sleep(45)` —
advance only when the model issues its next tool call, and the model issues that call only after
the previous tool returns. Throttle the socket and the return is delayed; delay it long enough
and the model simply pauses.

Workers in this repository make that visible. They call `time.sleep(45)` inside a loop and run
`git pull --rebase`; if the browser freezes, the shell call hangs waiting on its subprocess, the
model waits with it, and after roughly two to five minutes the session is marked idle and stops
advancing on its own. A "Continue" button appears, and someone has to tap it.

> **Warning —** A sidebar of worker tabs does not provide one or two days of unattended work. Do
> not plan around it.

One orchestrator tab is a different matter. It polls every 60 seconds, and if you keep that
single tab in the foreground and tap Continue when asked, it will keep seeding issues and
sending heartbeats. That is strictly better than five tabs competing for background time.

## Where the unattended hours actually live

GitHub Actions runs on GitHub's own Ubuntu runners, not in your browser. It can run for hours or
days with the phone switched off entirely. Three workflows carry the load.

| Workflow | Trigger | What it does while you travel | Token |
|---|---|---|---|
| `ci.yml` | Push to main, canary, devel; pull requests | ruff, 30 tests, license gate, deterministic locks, clean check | `GITHUB_TOKEN` |
| `swarm-auto-merge.yml` | Pull requests from `swarm/*` branches | Approves and squash-merges green worker PRs, deletes the branch, comments the issue, labels `swarm:done` | `GITHUB_TOKEN` |
| `swarm-scheduled.yml` | `cron: 0 * * * *`, plus manual dispatch | Resolves locks, syncs `docs/components/` from `src/`, runs ruff, pytest, and the license gate, seeds issues from `TODO.md`, requeues claims stale beyond 10 minutes, pushes changes | `GITHUB_TOKEN` |

The janitor is the piece that genuinely runs for one or two days unattended. It needs no personal
access token — `GITHUB_TOKEN` is provided automatically with `contents: write`, `issues: write`,
and `pull-requests: write` — and it runs on schedule at minute zero of every hour, or on demand
from the Actions tab. It does no model-driven coding, but it keeps locks deterministic, syncs
docs, requeues dead workers, and seeds issues so there is work waiting when you wake up.

## The pattern: push branches, then close the laptop

The reliable way to get merges while travelling is to move the work onto GitHub before you leave
and let the workflows finish it.

```bash
git checkout -b swarm/issue-42/test-agent
# edit src/shesh-memory/... or docs/...
make check
git add -A && git commit -m "feat(shesh-memory): implement ..."
git push origin swarm/issue-42/test-agent
gh pr create --title "[swarm] issue 42" --body "Closes #42" \
  --base main --head swarm/issue-42/test-agent --label swarm
```

Because the head branch starts with `swarm/`, `swarm-auto-merge.yml` triggers on that pull
request. It checks the branch out on a GitHub runner, runs `make check` — ruff, pytest, license,
locks, and component tests — and if everything is green it merges with
`gh pr merge --squash --auto --delete-branch`, comments on issue 42, and labels it `swarm:done`.
The run takes about three to five minutes on GitHub's infrastructure, with no tab open anywhere.

The limitation is honest: someone still has to push the branch. A janitor pass cannot write code
on its own. So the travel plan divides by day.

| Phase | What happens |
|---|---|
| Day 0, before leaving | Run the orchestrator, seed issues, and have one or two workers push a handful of branches and pull requests |
| Days 1–2, travelling | The hourly janitor keeps the repository healthy; auto-merge lands the pushed pull requests as gates pass; one orchestrator tab seeds more issues when you tap Continue |
| On return | `git pull` — every janitor and auto-merge result is already on `main` |

## Why the supervise loop is not the answer

`scripts/supervise.sh --loop` reads the next unchecked item from `TODO.md`, expects an agent to
implement it, then runs the gates and commits. In a chat session it loops as long as the agent
keeps making tool calls, and hits the hop threshold after roughly 60 minutes.

Inside a workflow the loop has a different problem: the runner has no model to do the
implementing, so it would pick tasks it cannot complete. That is exactly why the janitor workflow
was scoped to non-model work — locks, doc sync, requeueing — which can genuinely run for hours
unattended.

> **Note —** This chapter originally closed by proposing a model-driven workflow as future work.
> That workflow now exists as `swarm-llm-worker.yml`, running every two hours on the free GitHub
> Models tier through `GITHUB_TOKEN`; see [Factory Overview](overview.md) and
> [Swarm](swarm/README.md). No paid provider key is required, though setting `OPENAI_API_KEY` or
> `ANTHROPIC_API_KEY` remains an option.

## The recommended travel setup

Before leaving the laptop, hand off cleanly and push.

```bash
python tools/secure_pat.py --handoff   # delete the plain token, keep the encrypted one
git push origin main
```

On the phone, open one orchestrator tab, keep the site in the foreground where possible, and tap
Continue when it appears.

```bash
cd /home/user && git pull
python tools/session_guard.py --status
# reports NEED_PASSWORD → supply the encryption password through the interface prompt
python tools/secure_pat.py --prompt
python tools/github_auth.py --check
make check
SWARM_USE_GITHUB=1 python tools/swarm/orchestrator.py --seed TODO.md --dashboard
python tools/swarm/orchestrator.py --monitor
```

Worker tabs are optional and unreliable. If you open one or two —
`python tools/swarm/worker_github.py --component shesh-memory --github --poll 60` — keep the
phone plugged in, disable battery optimization for the browser, and expect to tap Continue every
10 to 20 minutes.

Enable the janitor from the repository's Actions tab. It then runs hourly regardless of the
phone's state, seeding issues from `TODO.md`, requeueing stale claims, and pushing refreshed
locks and doc syncs.

Back at the laptop, pick the state up from GitHub:

```bash
git pull origin main
python tools/session_guard.py --status
make check
python tools/swarm/orchestrator.py --dashboard
```

## The honest bottom line

Keep one orchestrator tab and tap Continue when it asks. Do not depend on four or five sidebar
workers, because the mobile operating system will pause them. Rely on the janitor and auto-merge
workflows for the real unattended hours, and on `git pull` when you return.

That is the best arrangement the platform's limits allow. For the efficiency measures that make
each session last longer, see [Efficiency](efficiency.md); for the handoff itself, see
[Session Protocol](session-protocol.md).
