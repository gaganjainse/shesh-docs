# github_auth.py and git_askpass.py — Loading a Token Without Leaking It

Two small loaders share one contract: GitHub credentials are resolved at the moment they are
needed, never stored in repository files, and never printed. This chapter gives the resolution
order and explains how Git itself is wired to the same secure source.

Status: living · last verified 2026-08-13
Sources: `tools/github_auth.py`, `tools/git_askpass.py`

## Resolution order

`github_auth.py` tries three sources in turn and stops at the first that works.

1. The `GITHUB_PAT` or `GH_TOKEN` environment variables.
2. `~/.config/shesh/github.pat`, which **must** be mode 600. A world-readable file is refused
   loudly — and it is the refusal that gets logged, never the token.
3. An authenticated `gh auth login` session, if the GitHub CLI holds one.

## Wiring Git to the same source

`git_askpass.py` is the Git-native half. Set `GIT_ASKPASS=tools/git_askpass.py` together with
`GIT_TERMINAL_PROMPT=0`, and every `git fetch` or `git push` over HTTPS is answered from the
same secure file. Nothing is embedded in remote URLs, and no `.git-credentials` file appears on
disk.

## What is verified

`make check` covers the loader, with both the refusal path and value redaction under unit test.
Fleet CI checkouts pass `persist-credentials: false`, so runner-side tokens are not written to
disk either; see the [security policy](../policies/security-policy.md). The encrypted-at-rest
half of the story is [secure_pat.py](secure-pat.md).
