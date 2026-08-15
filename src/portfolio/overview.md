# Portfolio — completely automatic

![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue)

The portfolio lives at
[gaganjainse/portfolio](https://github.com/gaganjainse/portfolio) (Astro,
deployed to Vercel via `vercel.json`). This chapter states the house rules that
keep the site self-maintaining and the quality floor that enforces them.

House rules, in priority order:

1. **No forks** — original work only; nothing padded.
2. **Proper priority** — projects are ordered by real signal, not recency.
3. **Zero manual upkeep** — the site regenerates from the GitHub API (see
   [Auto-Update](auto-update.md)); stale project data is treated as a bug, to
   the same standard as stale docs.

## Quality floor

The floor is enforced by scripts, not intentions:

- `npm run check` (astro check), `npm run lint` (eslint), `npm test`
  (vitest), `npm run format:check` (prettier) — all wired into the `auto`
  pipeline and CI.
- Generated assets (favicons, OpenGraph image, résumé PDF) are reproducible from
  `npm run generate:all` — never hand-edited binaries.
