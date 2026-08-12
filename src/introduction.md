# Introduction — Shesh Docs Complete Reading Compilation

> **Purpose:** This repo is a **copy for reading only** — compilation of **all docs** from `shesh-ecosystem`, `shesh-desktop`, `shesh-workspace`, `shesh-omniroute`, `OmniRoute` fork, and all `shesh-*` components — properly organised so you have no issues in navigation.

**Why this repo exists (user request):**

> "Make a docs repo and copy every docs there for my reading only as I need to understand what is going on. Add that in the live update flow too. It is a copy meaning docs are updated to other places as intended but for my knowledge, they are updated in the repo, but keep one point in mind, the docs in the repo should be properly organised as they are the compilation of all the docs and I should not have issues in navigation. Do a proper deep research on it, learn from other sources as every big project makes docs, understand the structure. Steal every good point from them. Also find out what other documentations we have missed to make. Then make them and updated on both is intended place and the docs repo. And properly separate factory and the product in three docs as I don't want a messed up system. I want you to make a good system."

**What we stole for docs structure (deep research):**

- **Docusaurus** (Meta, 3M weekly downloads, React/Jest/Prettier docs) — `docs/` + `blog/` + `src/components` + `static/` + `docusaurus.config.js` + `versioned_docs/` + `versions.json` + i18n, grouping pages by subfolder inside `docs/`, Algolia/local search, built-in versioning/themes
- **VitePress** (Vue Team, 2M) — Vue + Vite, local MiniSearch, built-in i18n
- **Starlight** (Astro, 200K) — Astro-powered modern docs, Pagefind offline search, built-in i18n — we already use Astro 7.2 in portfolio, so Starlight is natural
- **Nextra** (Next.js) — file-system docs, Flexsearch
- **Kubernetes Docs** — Concepts (architectural overviews), Tasks (step-by-step), Tutorials (guided learning), References (API/CLI details) — separation makes sense but you jump between all three to configure a Service: read Concepts to understand, Tasks to create, Reference to know all fields — we use same
- **Rust Book** — rustdoc `///` outer + `//!` inner, Examples early, cross-link aggressively, module-level `//!` overview, `#[doc(hidden)]`, mdBook `SUMMARY.md` load-bearing file defines navigation, prefix/numbered/suffix chapters, validation duplicate paths, `book.toml` config, `src/SUMMARY.md` table of contents required
- **mdBook** — `book/` output, `book.toml` config, `src/SUMMARY.md` + `chapter_1.md`, `watch`, `serve`, `test` code samples compile

**Our structure (stealing every good point):**

- **mdBook** `SUMMARY.md` as load-bearing navigation — like Rust book, with `# Summary`, `- [Introduction]`, parts ` # Part I: Product`, etc., prefix/numbered/suffix chapters, validation duplicate paths, `book.toml` with `additional-css`, `git-repository-url`, `edit-url-template`, `search.limit-results=20`
- **Docusaurus** grouping by subfolder inside `docs/` — `getting-started/`, `architecture/`, `concepts/`, `tasks/`, `tutorials/`, `reference/`, `factory/`, `gateway/`, `desktop/`, `adr/`, `audits/`, `verification/`, `skills/`, `policies/`, `queries/`, `portfolio/`
- **Kubernetes** Concepts/Tasks/Tutorials/Reference separation — we have Product Overview, Getting Started, Architecture, Concepts (Brain/Mind/Soma/Physique, Protocols, Learning, Containers, Linux Layout), Tasks (Manual Verification Checklist split into First Boot, Accounts, MCP Mesh, Voice, GPU, Display, Backup, Phone, Containers, Agent Behavior, Security, Canary), Tutorials (Organize Downloads, Voice+Settings+Organizer Flow, RAG+Vector), Reference (Manifest, Channels, Components, Models, Upstreams)
- **Rust** Examples early, cross-link aggressively, module-level overview, hide implementation noise
- **Docs as Code** — version-controlled, reviewed via PRs, GitHub Actions checks broken links/outdated examples, tie docs to releases, docs-needed label, mention contributors in release notes

**Three docs separation (factory vs product vs gateway) — proper system, not messed up:**

- **Product — shesh-ecosystem (clean):** `src/product/` — what user installs on MSI Sword, no session protocol, no swarm dev tooling
- **Factory — shesh-workspace (messy dev):** `src/factory/` — session protocol, swarm file+Issues atomic lock+PR auto-merge, secure PAT password, efficiency selective clone, model-agnostic, travel mode, steal infrastructure, live update system
- **Gateway — shesh-omniroute + OmniRoute fork (optional cloud):** `src/gateway/` — free big models gateway 291 providers 90+ free, optional to local Ollama primary where enable is user choice
- **Desktop — shesh-desktop (illogical-impulse + CachyOS):** `src/desktop/` — style + performance non-negotiable, backend that integrates into look

**Live update flow:** Added to `docs/LIVE_UPDATE_SYSTEM.md` — `tools/live_update.py --docs ALL --swarm` called automatically by `autopilot/runner.py`, `supervise.sh`, `session_guard.py`, `swarm/orchestrator.py`, workers, and GitHub Actions `ci.yml`, `swarm-*.yml`. So docs in intended place (ecosystem) and copy in docs repo both updated automatically.

**What other documentations we missed and now made:**

- `STYLE_PERFORMANCE.md` — style + performance non-negotiable (illogical-impulse look + CachyOS performance)
- `STEAL_INFRASTRUCTURE.md` — so you don't have to write many times
- `LIVE_UPDATE_SYSTEM.md` — automatic live update
- `MODEL_AGNOSTIC.md` — 5-layer guard for quality consistency across free models
- `OMNIROUTE_STUDY.md` — 291 providers 90+ free
- `EFFICIENCY.md` — 10 strategies selective shallow clone 36M→2M
- `TRAVEL_MODE.md` — 1 orchestrator tab + Actions true hours
- `WORKSPACE_SEPARATION.md` — product vs factory
- `SITUATION_REPORT.md` — 5 agents started all stopped analysis
- `FOOLPROOF_SWARM_PROMPTS.md` — 5 agents prompts with GitHub links, no password in open
- `AUDIT_EXHAUSTIVE.md` + JSON — 54 repos audited
- `SKILL_MARKETPLACE.md`, `UPDATE_MIRROR.md` — P2 future now minimal docs
- `SECURITY.md`, `CONTRIBUTING.md` — missing, now created as placeholders

This repo is **reading only** — source of truth remains in `shesh-ecosystem` and `shesh-workspace` and `shesh-desktop`, but this repo compiles all for easy navigation.
