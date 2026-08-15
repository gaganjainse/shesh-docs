# Next Session Prompt

Copy this whole file into a new Arena.ai Agent Mode chat to continue the Shesh
build. It hands the next session the fleet summary, the rules it must respect,
the secured PAT flow, and the first commands to run.

> **Note —** This prompt was generated around 2026-08-13 and is preserved as a
> working record. It is retained as a record, not as live reference. The
> authoritative factual baseline is the
> [2026-08-15 fleet audit](../../../FLEET_AUDIT_2026-08-15.md): the body is
> **GPL-3.0-or-later** (not MIT), SheshAOS reports **877 passing tests with 1
> ignored** at the baseline, and `gaganjainse/SheshOS` is an unpublished,
> conceptual project rather than a live upstream. The "53-repo fleet" and "872
> SheshAOS tests" figures below are historical; rely on the baseline.

## Summary

- Shesh is a federated, local-first AI OS for CachyOS/Hyprland on an MSI Sword 16 HX (i7-14700HX, RTX 4050 6 GB, 1920×1200 @ 144 Hz).
- Owner is Gagan Jain (@gaganjainse); main repo is shesh-ecosystem; target OS is CachyOS + Hyprland + Quickshell.
- Language policy is Rust, Python 3.11+, Lua, QML/JS, and Bash only — talking over MCP/JSON.
- The PAT is encrypted at rest and decrypted on demand via a password prompt; it is never echoed.
- Read SESSION_HANDOFF first, then the audit/roadmap, TODO, manual verification, session protocol, swarm, and the query log.

---

You are continuing **Shesh** — federated local-first AI OS for CachyOS/Hyprland
MSI Sword 16 HX B14VEKG (i7-14700HX, RTX 4050 6GB, 1920x1200@144).

**Owner:** Gagan Jain (@gaganjainse) — fleet https://github.com/gaganjainse
**Main repo:** shesh-ecosystem **Target OS:** CachyOS 260628 + Hyprland 0.55 + Quickshell
**Lang policy:** Rust, Python 3.11+, Lua, QML/JS, Bash only — MCP/JSON (ADR-0001)

**Federation:**
- 23 components (organs) in `manifests/components.toml` (brain/mind/soma); 3 channels — 16 ship from the single `shesh-core` repo (ADR-0019)
- Locks: stable 1, canary 19, devel 23 — SHA256 audited
- Component repos (6): shesh-core, shesh-memory, shesh-orchestrator, shesh-harness, shesh-phone, shesh-omniroute + SheshAOS/shesha-kernel
- MCP servers: `shesh-*-mcp`; 9 in `servers.json` with containers/secrets/calendar available
- Tests (2026-08-13 snapshot): 61 ecosystem, 235+ component, 26 desktop, 872 SheshAOS (Rust) — all green. **Baseline note:** the 2026-08-15 audit reports SheshAOS at 877 passing with 1 ignored.

**Stack must respect:**
- `docs/SESSION_HANDOFF.md` — read first, live anchor
- `docs/history/AUDIT_AND_ROADMAP.md` — decisions D1–D19
- `TODO.md` — ⬜ todo, ✅ done, 🟡 in-progress, 🔴 blocked
- `docs/MANUAL_VERIFICATION.md` — 16-section checklist (hardware + rolling deps + security + recovery drill)
- `SECURITY.md` + `docs/THREAT_MODEL.md` + `docs/RECOVERY.md`
- `docs/policies/DEPENDENCY_POLICY.md` — rolling-release ownership
- `docs/policies/DOCUMENTATION_POLICY.md` + `docs/STYLE_GUIDE.md` + `docs/INDEX.md`
- `tools/book_build.py` — shesh-docs pure projection
- `docs/history/queries/QUERYLOG.md` — full trail, newest first
- `docs/SESSION_PROTOCOL.md` — 60-second hop protocol
- `docs/history/adr/` — 19 ADRs
- `docs/GETTING_STARTED.md` — full install + Ollama 6 GB stack
- `Containerfile`, `distrobox.ini`, `tools/install.sh --channel`

**GitHub PAT — secured with a password (auto prompt):**
- Encrypted file: `~/.config/shesh/github.pat.enc` (0600) — PBKDF2HMAC 200k + Fernet
- Plain file: `~/.config/shesh/github.pat` (0600) — auto-deleted on handoff
- Flow in a new session: the guard detects the enc file but no plain file →
  NEED_PASSWORD → the agent asks for the password via the ask_user UI →
  `tools/secure_pat.py` decrypts to a 0600 plain file → `tools/github_auth.py`
  loads it and never logs the value.
- Do **not** echo the PAT. The tool redacts it.

**Commands first in a new session:**
```bash
cd /home/user
git pull origin main
python tools/session_guard.py --status
python tools/github_auth.py --check
make check   # GATE OK
ls src/ | wc -l
cat docs/SESSION_HANDOFF.md
cat TODO.md | grep -E "⬜|🔴|🟡" | head -n 40
```

**Autopilot rules:**
1. Pick the highest ⬜ not blocked from TODO.md.
2. Branch `feat/THING` — small change, one component.
3. Tests — never push red — `pytest -q -p no:cacheprovider`.
4. GuardedMCP from shesh-audit.
5. No secrets in config — via shesh-secrets `env:`, `gopass:`, `file:0600`.
6. After each user message: append to QUERYLOG.md, update TODO.md.
7. Before push: `session_guard --tick` — if a hop is needed, hand off, do not start a new task.
8. Archive, not delete; no force-push to main.

**Swarm parallel:**
- `docs/SWARM.md` — GitHub as bus via `swarm/` queue/claims/heartbeats.
- Orchestrator: `python tools/swarm/orchestrator.py --seed TODO.md --monitor`.
- Workers: `python tools/swarm/worker.py --component shesh-memory` or
  `python tools/swarm/worker_github.py --component shesh-memory --github`.
- PAT needed for push/PR — decrypted via the password flow above.

**Message to give you:** "Continue Shesh — read SESSION_HANDOFF first, TODO top-to-bottom, next ⬜. PAT encrypted at ~/.config/shesh/github.pat.enc — the agent will ask for the password and decrypt. Run session_guard --status and make check."

---
Generated 2026-08-11T16:49:08 by `tools/session_guard.py --handoff` · hand-refreshed 2026-08-13 (numbers/canon); regenerates on next hop.
