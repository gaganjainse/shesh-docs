# Portfolio auto-update — GitHub API, gates, and Vercel

Everything below is wired in the
[portfolio repo](https://github.com/gaganjainse/portfolio) today. The site
regenerates itself: project data is pulled from the GitHub API, assets are
rebuilt, and the result is gated before it ships.

## The pipeline

```bash
npm run auto
# = update:projects  (scripts/auto-update-projects.mjs — GitHub API pull)
#   + generate:all   (favicons, og-image, résumé PDF)
#   + check && lint && test && build
```

Two GitHub Actions workflows carry it:

| Workflow | Job |
|---|---|
| `auto-update.yml` | scheduled refresh of project data from the GitHub API |
| `ci.yml` | check + lint + test + build gate on every push |

Deploys target Vercel, configured by `vercel.json` — the main branch is
production.

## What to verify by hand, quarterly

- [ ] The last `auto-update.yml` run is green and its commit landed.
- [ ] The projects shown match the real pinned order on the GitHub profile.
- [ ] `npm run auto` exits 0 locally end-to-end — if any stage fails, the
      pipeline must fail loudly. A green run with a broken stage is the one
      outcome this design exists to prevent.
