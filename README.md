# shesh-docs — Complete Reading Compilation for Shesh Ecosystem

> **Purpose:** Copy for reading only — compilation of all docs from `shesh-ecosystem`, `shesh-desktop`, `shesh-workspace`, `shesh-omniroute`, `OmniRoute` fork, and all `shesh-*` components — properly organised so you have no issues in navigation.

- **License:** GPL-3.0-or-later
- **Owner:** Gagan Jain ([@gaganjainse](https://github.com/gaganjainse))
- **Built with:** [mdBook](https://rust-lang.github.io/mdBook/)

![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue?style=for-the-badge) ![CI](https://img.shields.io/github/actions/workflow/status/gaganjainse/shesh-docs/ci.yml?style=for-the-badge&label=CI)

**Why this repo exists:** User said: "Make a docs repo and copy every docs there for my reading only as I need to understand what is going on. Add that in the live update flow too. It is a copy meaning docs are updated to other places as intended but for my knowledge, they are updated in the repo, but keep one point in mind, the docs in the repo should be properly organised as they are the compilation of all the docs and I should not have issues in navigation. Do a proper deep research on it, learn from other sources as every big project makes docs, understand the structure. Steal every good point from them. Also find out what other documentations we have missed to make. Then make them and updated on both is intended place and the docs repo. And properly separate factory and the product in three docs as I don't want a messed up system."

**Structure (stealing every good point from big projects):**

- **mdBook** - `SUMMARY.md` load-bearing, `book.toml`, prefix/numbered/suffix chapters, validation duplicate paths, additional-css, git-repository-url, edit-url-template, search limit 20 - like Rust book
- **Docusaurus** - grouping by subfolder inside docs/, blog/, src/components, static/, versioned_docs/, versions.json, i18n, Algolia/local search, built-in versioning/themes - Meta's battle-tested, 3M weekly downloads
- **Kubernetes** - Concepts (architectural overviews), Tasks (step-by-step), Tutorials (guided learning), References (API/CLI details) - separation makes sense, cross-linking, targeted search, version matching
- **Rust** - Outer doc comments `///`, inner `//!`, Examples early, cross-link aggressively, module-level overview, hide implementation noise `#[doc(hidden)]`, mdBook multi-page tutorials with own URLs, sidebar custom navigation
- **Docs as Code** - version-controlled, reviewed via PRs, GitHub Actions checks broken links/outdated examples, tie docs to releases, docs-needed label

**Three docs separation (proper system, not messed up):**

- **Product — shesh-ecosystem (clean):** `src/product/` — what user installs on MSI Sword, no session protocol, no swarm dev tooling
- **Factory — shesh-workspace (messy):** `src/factory/` — session protocol, swarm file+Issues atomic lock+PR auto-merge, secure PAT password, efficiency selective clone, model-agnostic, travel mode
- **Gateway — shesh-omniroute + OmniRoute (optional):** `src/gateway/` — free big models gateway 291 providers 90+ free, optional to local Ollama primary where enable is user choice
- **Desktop — shesh-desktop (illogical-impulse + CachyOS):** `src/desktop/` — style + performance non-negotiable, backend that integrates into look

**Live update flow:** Added to `shesh-ecosystem/docs/LIVE_UPDATE_SYSTEM.md` — `tools/live_update.py --docs ALL --swarm` called automatically by autopilot, supervise.sh, session_guard, swarm orchestrator/workers, and GitHub Actions ci.yml, swarm-*.yml. So docs in intended place and copy in this repo both updated automatically.

**What other documentations we missed and now made:**

- `STYLE_PERFORMANCE.md` — style + performance non-negotiable
- `STEAL_INFRASTRUCTURE.md` — so you don't have to write many times
- `LIVE_UPDATE_SYSTEM.md` — automatic live update
- `MODEL_AGNOSTIC.md` — 5-layer guard quality consistency
- `OMNIROUTE_STUDY.md` — 291 providers 90+ free
- `EFFICIENCY.md` — 10 strategies selective shallow clone
- `TRAVEL_MODE.md` — 1 orchestrator tab + Actions true hours
- `WORKSPACE_SEPARATION.md` — product vs factory
- `SITUATION_REPORT.md` — 5 agents started all stopped analysis
- `FOOLPROOF_SWARM_PROMPTS.md` — 5 agents prompts
- `AUDIT_EXHAUSTIVE.md` + JSON — 54 repos audited
- `SKILL_MARKETPLACE.md`, `UPDATE_MIRROR.md` — P2 future
- `SECURITY.md`, `CONTRIBUTING.md` — missing, now placeholders

**Build:**

```bash
# mdBook
mdbook build
mdbook serve  # serves at http://localhost:3000

# Or Astro Starlight (since portfolio uses Astro 7.2)
npm install
npm run dev
```

**Live update:** This repo is reading only, but live update flow copies docs from `shesh-ecosystem`, `shesh-desktop`, `shesh-workspace` etc into here via `tools/live_update.py --docs ALL` + `scripts/sync-docs.sh` (to be added).

**Links:**
- Product: https://github.com/gaganjainse/shesh-ecosystem
- Factory: https://github.com/gaganjainse/shesh-workspace
- Gateway: https://github.com/gaganjainse/shesh-omniroute + https://github.com/gaganjainse/OmniRoute
- Desktop: https://github.com/gaganjainse/shesh-desktop

## Security

Security posture and vulnerability reporting: [canonical ecosystem security
policy](https://github.com/gaganjainse/shesh-ecosystem/blob/main/SECURITY.md).

## License

GPL-3.0-or-later — see [LICENSE](LICENSE).
