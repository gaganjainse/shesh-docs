# Foolproof Swarm Prompts — Bootstrapping Five Agents From an Empty Workspace

A new session starts with an empty home directory, which means the encrypted credential file from
the last machine is simply not there — and a password alone cannot decrypt a file that does not
exist. This chapter gives the setup sequence that solves that, plus five copy-paste prompts that
bring an orchestrator and four role workers online from nothing.

## Summary

- The encrypted token lives in the factory repository at `secrets/github.pat.enc`, so any clean
  workspace can fetch it and then ask for the password.
- Common setup is seven steps: clone both repositories, fetch the encrypted token, decrypt,
  verify, clone selectively, gate, and read the anchors.
- Each of the five prompts targets one role, and each role clones only the repositories it needs.
- The platform role clones nothing beyond the ecosystem repository and therefore sustains the
  longest session.
- Claims are atomic through a lock ref, so five sessions cannot collide on one task.

## Why the credential step used to fail

The design intent was always that the token stay encrypted at rest and never appear in a
repository in plain form. What broke was continuity: `~/.config/shesh/github.pat.enc` lived in a
home directory on one machine, and nothing carried it to the next sandbox.

The fix takes advantage of the fact that an encrypted file is safe to publish. The ciphertext now
lives in `gaganjainse/shesh-workspace` at `secrets/github.pat.enc`, a clean workspace fetches it
over raw HTTPS, and the session then asks for the password through the interface prompt. The
password never enters a chat message and the plaintext token never enters the repository.

> **Warning —** Publishing ciphertext means the password is the only remaining secret, so it must
> be strong and must never be pasted into a transcript. Token rotation following the 2026-08-11
> and 2026-08-12 transcript exposures remains an owner action tracked in `TODO.md`; see
> [the incident post-mortem](../audits/incident-2026-08-11-multi-tab-swarm.md) and the
> [security policy](../policies/security-policy.md).

## Common setup for any clean workspace

Run these in order. Every one of the five prompts below assumes this sequence has succeeded.

```bash
# 1. Clone the product and the factory
cd /home/user
git clone --depth 1 https://github.com/gaganjainse/shesh-ecosystem.git
git clone --depth 1 https://github.com/gaganjainse/shesh-workspace.git
cd /home/user/shesh-ecosystem

# 2. Fetch the encrypted token
mkdir -p ~/.config/shesh && chmod 700 ~/.config/shesh
curl -s https://raw.githubusercontent.com/gaganjainse/shesh-workspace/main/secrets/github.pat.enc \
  -o ~/.config/shesh/github.pat.enc
chmod 600 ~/.config/shesh/github.pat.enc
ls -lh ~/.config/shesh/github.pat.enc   # expect roughly 341 bytes

# 3. Decrypt — the session prompts for the password through the interface
python tools/secure_pat.py --prompt

# 4. Verify the load without printing the value
python tools/github_auth.py --check     # e.g. PAT found: gith**** len 93

# 5. Clone selectively rather than fetching 22 repositories
python tools/setup_worker.py --clean
du -sh . && find . -type f | wc -l      # target under 100 MB and 8000 files

# 6. Gate
make check

# 7. Read the anchors
head -n 60 docs/SESSION_HANDOFF.md
head -n 40 docs/SESSION_PROTOCOL.md
grep -E "⬜|🔴|🟡" TODO.md | head -n 20
```

If the fetch fails because the network is unavailable, fall back to `gh auth login` or set
`GITHUB_PAT` directly.

## The five prompts

Each prompt names a role, its repositories, and the one command that starts its work loop. Open
the orchestrator first; the workers depend on the issues it seeds.

### Session one: orchestrator

```text
--- ORCHESTRATOR — CLEAN WORKSPACE ---

You are ORCHESTRATOR for shesh-ecosystem: https://github.com/gaganjainse/shesh-ecosystem
Factory repo (holds secrets/github.pat.enc): https://github.com/gaganjainse/shesh-workspace

Treat /home/user as empty. Run the common setup, then:

python tools/setup_worker.py --role platform --clean   # 0 repos, most efficient
make check                                             # expect GATE OK, 63 tests

head -n 80 docs/SESSION_HANDOFF.md
head -n 40 docs/SESSION_PROTOCOL.md
grep -E "⬜|🔴|🟡" TODO.md | head -n 20

# Seed GitHub Issues from TODO (atomic lock backend)
SWARM_USE_GITHUB=1 python tools/swarm/orchestrator.py --seed TODO.md --dashboard

# Monitor loop — leave open; requeues claims stale beyond 10 minutes
python tools/swarm/orchestrator.py --monitor

On HOP: python tools/session_guard.py --handoff (deletes plain token, keeps encrypted),
commit, push, close the session, open a new one with this same prompt.
```

### Session two: Worker-Brain

```text
--- WORKER-BRAIN — CLEAN WORKSPACE ---

You are WORKER-BRAIN. Repositories: shesh-audit, shesh-secrets, shesh-brain, SheshAOS
(all under https://github.com/gaganjainse/).

Run the common setup, then:

python tools/setup_worker.py --role brain --clean   # 3 repos, ~8 MB
python tools/swarm/worker_github.py --component shesh-audit --github --setup --poll 45

On HOP: session_guard --handoff, push, close, reopen with this prompt, refetch the
encrypted token, supply the password again.
```

> **Note —** `SheshAOS` is the governance and runtime repository, and it is a real component.
> Do not confuse it with `gaganjainse/SheshOS`, the model-routing brief named as an upstream by
> `shesh-mind`, which is unpublished and conceptual rather than a reachable repository.

### Session three: Worker-Mind

```text
--- WORKER-MIND — CLEAN WORKSPACE ---

You are WORKER-MIND. Repositories: shesh-memory, shesh-mind, shesh-harness,
shesh-orchestrator, shesh-skills, shesh-calendar (all under https://github.com/gaganjainse/).

Run the common setup, then:

python tools/setup_worker.py --role mind --clean    # 7 repos, ~2 MB
python tools/swarm/worker_github.py --component shesh-memory --github --setup --poll 45
```

### Session four: Worker-Soma

```text
--- WORKER-SOMA — CLEAN WORKSPACE ---

You are WORKER-SOMA. Repositories: shesh-files, shesh-shell, shesh-system, shesh-backup,
shesh-phone, shesh-containers, shesh-mcp-bundle, shesh-acp, shesh-media, shesh-messaging
(all under https://github.com/gaganjainse/).

Run the common setup, then:

python tools/setup_worker.py --role soma --clean    # 9 repos, ~2 MB
python tools/swarm/worker_github.py --component shesh-system --github --setup --poll 45
```

### Session five: Worker-Platform

```text
--- WORKER-PLATFORM — CLEAN WORKSPACE ---

You are WORKER-PLATFORM. Scope: shesh-ecosystem itself — docs, decision records,
Containerfile, install.sh, CI, swarm tooling, and portfolio updates at
https://github.com/gaganjainse/portfolio (no forks; owned repositories take priority).

Run the common setup, then:

python tools/setup_worker.py --role platform --clean  # 0 repos, ~150 min session
python tools/swarm/worker_github.py --component general --github --setup --poll 60
```

## Why these prompts hold up

Eight properties turn a fragile setup into a repeatable one, and each addresses a specific failure
seen in earlier sessions.

| Property | Mechanism |
|---|---|
| Credentials survive a new sandbox | The encrypted file is fetched from the factory repository over raw HTTPS; no file from a previous machine is needed |
| The password is asked for, not typed into chat | `secure_pat.py --prompt` uses `getpass`, which surfaces an interface prompt; the value is redacted in all output |
| The workspace stays small | `git clone --depth 1` plus `setup_worker.py --role X --clean`; Brain takes 3 repositories and roughly 8 MB instead of 22 and 36 MB |
| No wasted clones | Platform clones nothing, Mind 7 repositories at about 2 MB; existing clones are refreshed with `git pull --ff-only --depth 1` |
| Claims are atomic | `claim_issue_atomic()` creates `refs/heads/swarm/claims/issue-N` via POST `/git/refs`; GitHub returns 422 if it exists, so the first claimant wins — verified against issues #1 and #2 |
| Work is isolated | One branch per task, `swarm/issue-N/agent-id`, gated by `make check` before the pull request |
| Hours run without a session | `swarm-scheduled.yml` hourly and `swarm-llm-worker.yml` every two hours, both on `GITHUB_TOKEN` with no paid key; `swarm-auto-merge.yml` lands green work |
| Handoff is secure | `session_guard.py --handoff` deletes the plain token, keeps the encrypted one, and writes `NEXT_SESSION_PROMPT.md` with `need_password=true` |

## Where this fits

The routine is always the same: treat the workspace as empty, clone the product and the factory,
fetch the ciphertext, decrypt, clone selectively, gate, read `SESSION_HANDOFF.md`, and pick the
next unchecked task. [Swarm](swarm/README.md) explains the coordination bus these prompts drive,
[Efficiency](efficiency.md) explains the clone sizes, and [Session Protocol](session-protocol.md)
covers the handoff at the other end of the session.
