# secure_pat.py — A GitHub Token Encrypted at Rest

The fleet's GitHub personal access token never sits in a repository, a transcript, or a
world-readable file. This chapter describes how it is stored under a password, how a new session
recovers it, and which failure modes count as compromise.

Status: living · last verified 2026-08-13
Source: `tools/secure_pat.py` · Loader: [github_auth.py](github-auth.md)

## Where the token lives

Two files, both mode 600, in `~/.config/shesh/` (directory mode 700).

| File | Purpose |
|---|---|
| `github.pat.enc` | Encrypted token — PBKDF2HMAC with 200,000 iterations, then Fernet; survives sessions |
| `github.pat` | Decrypted plain token; deleted on handoff |

## How a new session recovers it

The design assumes the plain file is gone and the encrypted one is not, which is exactly the
state a clean handoff leaves behind.

1. The session guard finds `github.pat.enc` present and `github.pat` missing, and reports
   `NEED_PASSWORD`.
2. The agent asks for the password through the interface prompt, never in a chat message.
3. `secure_pat.py` decrypts to the plain file at mode 600.
4. `tools/github_auth.py` and `tools/git_askpass.py` read from there, redacting the value.

```bash
python tools/secure_pat.py --prompt        # decrypt via hidden password prompt
python tools/secure_pat.py --handoff       # delete plain, keep encrypted
python tools/github_auth.py --check        # verify load and redaction
```

## Rules that are not negotiable

Tools print a redacted length and nothing more; neither the token nor the password is ever
echoed. If the plain file is ever found world-readable, treat it as a compromise and rotate.

> **Warning —** Token rotation following the transcript exposures of 2026-08-11 and 2026-08-12
> remains an owner action tracked in `TODO.md`. See
> [the incident post-mortem](../audits/incident-2026-08-11-multi-tab-swarm.md) and the
> [security policy](../policies/security-policy.md).
