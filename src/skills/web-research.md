---
name: web-research
description: Research a topic using web search and fetch. Cite sources, prefer primary docs, stay local-first.
---

# Web Research Skill

Good research is a trail of citations, not a pile of assertions. This skill turns a question
into a sourced answer: search broadly, fetch the few authoritative pages, and cite every
claim with its URL.

## The protocol

1. `web_search(query)` to skim titles and URLs. Prefer official docs, release notes, the Arch
   wiki, and GitHub.
2. For two or three authoritative results, `fetch_url(url)` and extract the relevant section.
3. **Cite every claim** with its URL. Prefer primary sources over blogs.
4. Note the date of the source and flag outdated information.
5. Save useful findings with `append_note("research/<topic>", ...)`.
6. If the cloud is off (the default), never call an external API; DuckDuckGo HTML plus fetch
   are allowed.
7. Distinguish fact from recommendation, and end with a concrete next step.

Avoid SEO spam and content farms. For code libraries, use Context7-style up-to-date docs when
available (a separate MCP server), not the model's training cutoff.

> **Note —** The 2026-08-15 audit (finding F-12) flagged `fetch_url` for server-side request
> forgery: a crafted URL could reach internal services. The intended control is URL
> allowlisting; F-12 is tracked and not yet closed. Until then, treat fetched URLs as
> untrusted input and avoid internal or metadata addresses.

> **Tip —** A source's date is part of the answer. A correct fact from 2021 may be wrong today;
> say so rather than letting the reader assume currency.
