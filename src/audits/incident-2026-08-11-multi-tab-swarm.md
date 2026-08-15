# Incident Post-Mortem — 2026-08-11: Five-Tab Swarm Collision

On 2026-08-11, five parallel agent tabs plus GitHub Actions drove one swarm bus
for a day. This chapter explains what broke, why, and how each weakness became a
permanent control — a clean example of fixing the system through the system.

> **Historical record —** This post-mortem covers an incident on 2026-08-11 and
> is preserved as a factual record. It is retained as a record, not as live
> reference. The authoritative factual baseline is the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md): the body is
> licensed **GPL-3.0-or-later**, and `gaganjainse/SheshOS` is an unpublished,
> conceptual project rather than a live upstream.

## Summary

- Five agents plus GitHub Actions shared one swarm bus; the day surfaced real bugs and several self-inflicted wounds.
- A placebo worker merged placeholder "work" and closed real issues; missing git identity and credential auth broke every pull request.
- Lint debt in `tools/` blocked every swarm PR from auto-merging until it was paid down.
- Each root cause received a concrete control; the incident became the system's best stress test.
- Five harmless placeholder commits remain in history by policy (no force-push); the residue is institutional memory.

## What happened

Five parallel agent tabs (an orchestrator plus brain, mind, soma, and platform
workers) and GitHub Actions drove one swarm bus for a day. The net effect was
mixed: real bugs were found and fixed, but duplicate and noisy issues were
seeded (#19–34), placeholder "work" pull requests were merged to main (five
commits of marker files from a stub `do_work`), claim and PR closure
cross-talked through the shared issue/PR number space, and a PAT was exposed in
a transcript.

## Root causes and their controls

1. **Worker placebo.** `do_work()` marker-filed every claim and auto-merge
   closed real issues. Workers now fail closed without an `--executor` and
   release claims (`release_issue_claim`) — PR #39.
2. **Loose TODO seeder.** Any line containing ⬜/🟡 became an issue. A strict
   bullet parser with blocked-ancestor inheritance replaced it — PR #38.
3. **Shared working tree with daemon commits.** Heartbeat commits raced manual
   rebases. Daemons were isolated to their own clone via
   `tools/swarm/daemon.sh`, and the orchestrator refuses swarm commits off-main
   — PR #40.
4. **Gate gaps.** `ruff` did not cover `tools/` locally (29 pre-existing
   errors), and the workflow used the forbidden `gh pr review --approve`. Both
   were fixed on main the same day; local `make check` and CI now match.
5. **Session guard self-nuke.** `--status` past 60 minutes deleted the plain
   PAT under running daemons. Status became read-only; only explicit `--handoff`
   deletes it — PR #40.
6. **Credential hygiene.** A PAT was visible in a tool transcript. A rotation
   task was opened (owner action), and askpass-style auth was added to workers
   — PR #39.

## What went right

Atomic claim refs, the auto-merge gate, the heartbeat bus, and the hop protocol
all behaved under multi-agent load once the fixes above landed. The incident was
the best stress test the system had seen; its findings became code the same day.

## Residue

Five placeholder commits remain in main's history (no force-push, by policy).
They are harmless inert markers under `swarm/artifacts/`; their content was
removed in `c421f32613bd33745b641878338ff1d3436da08f`, and this note is the
institutional memory.

---

## Appendix A — Original situation report

The report below was preserved verbatim (quotes included) when
`docs/history/SITUATION_REPORT.md` was fused into this incident record on
2026-08-13 under the "one topic, one home" rule. Two findings here extend the
root-cause list: the **queue fallback defect** (claiming blocked kernel tasks
when no matching issue existed — fixed to a strict filter that waits) and
**heartbeat files as the reliable liveness signal** (buffered stdout of
long-running processes is not). The per-tab chronology is the source evidence
for the post-mortem.

> **User said:** "I just gave them the start as a prompt. Leave that aside the main point is that the five agents I started all stopped, not a good look for a autocomplete but these are the outputs of them."

The PDF outputs showed five tabs. The orchestrator seeded issues, fixed the
weakest link (`do_work()` placebo) by dogfooding the full pipeline, and merged
PR #37 (`fb2fc03614c44b9320577f21b695e200d0c78a18`, closing #31). A brain
worker booted a clean workspace, hit silent `git commit` failures from a
missing identity, then silent push failures from missing credential auth, fixed
both, and produced PR #19. Lint debt in `tools/` had blocked every swarm PR
from auto-merging; that was cleared in `45150db5397bd01058c7f535c0e54f49eef54c`
(16 auto-fixed, 15 manual). The session guard's `--status` had deleted the plain
PAT mid-session; that was restricted to `--handoff`. Shared working trees caused
rebase races, and heartbeat files proved to be the dependable liveness signal.

The session ended with all five agents stopped — expected on a phone after the
60-minute hop threshold deleted the plain PAT. The controls above made the next
run durable.

> **Where this fits —** The [session handoff](../verification/session-handoff.md)
> and [next session prompt](../queries/next-session-prompt.md) describe the
> hardened swarm and autopilot that emerged from this incident.
