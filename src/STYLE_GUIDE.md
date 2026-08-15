# Shesh Documentation Style Guide

*The single source of truth for how every page in this book is written. Follow it
without exception so the 125-chapter compilation reads as one coherent voice rather
than a pile of unrelated notes.*

The target voice is that of a serious engineering publication — clear, authoritative,
and quietly confident. Think of the prose in a flagship IEEE *Spectrum* feature: it
opens with a concrete hook, explains hard ideas through plain-language analogy, keeps
paragraphs short, and never wastes a sentence. We are not writing marketing copy and
we are not writing a lab notebook. We are writing documentation that an intelligent
reader can trust.

---

## 1. Voice and tone

- **Active voice, present tense.** Write "Shesh records every action" rather than
  "Every action is recorded by Shesh." The system is alive; describe what it does.
- **Authoritative, not breathless.** State facts directly. Avoid hype words
  (*revolutionary*, *magical*, *seamless*, *effortless*) and avoid emoji as
  decoration in headings or body text.
- **Accessible.** Assume the reader is technically literate but not fluent in every
  subsystem. Define a term on first use, then use it freely.
- **Concrete over abstract.** Prefer specific nouns. "The policy engine rejects the
  call" beats "There is a rejection mechanism that handles disallowed operations."
- **One idea per paragraph.** Paragraphs run three to six sentences. If a paragraph
  grows past eight lines, split it.

## 2. Structure of a chapter

Every chapter follows the same anatomy so readers always know where they are.

1. **Title (H1).** A specific noun phrase. No emoji. Examples: *The Agentic Body*,
   *Promotion Pipeline*, *Rootless Containers*, *Catch-Up Scheduling*.
2. **Lede.** One or two sentences stating what the reader will learn and why it
   matters. This is the chapter's thesis, like the opening of a feature article.
3. **Summary (for chapters longer than ~400 words).** A short bullet block of the
   key takeaways, placed right after the lede. Keep it to three to six items.
4. **Body.** H2 for major sections, H3 for subsections. Use descriptive headings,
   not labels — *Why this exists* is better than *Overview*.
5. **Closure.** For substantial chapters, end with a short "Where this fits" or
   "What's next" line that connects to adjacent chapters.

## 3. Making hard ideas clear

- **Lead with analogy when the concept is abstract.** The fleet already uses a body
  metaphor — Brain, Mind, Soma, Physique. Lean on it. Explain a protocol the way you
  would explain plumbing: it moves something from one place to another and fails
  loudly when blocked.
- **Show the flow before the detail.** A short sentence of what happens, then the
  mechanism. Readers remember the shape of a system before they remember its fields.
- **Tell the reader why a decision was made.** A documented decision is more useful
  than a rule stated in isolation.

## 4. Formatting rules

- **Prose wrapping.** Wrap source lines around 100 characters for readability. This
  is a courtesy to editors, not a hard contract.
- **Code blocks.** Fence every block and tag its language (`bash`, `python`,
  `toml`, `json`, `text`). Keep blocks short and purposeful; a wall of shell is a
  sign the prose should carry more of the explanation.
- **Tables.** Use them for comparisons and reference data, not for narrative. Align
  columns meaningfully.
- **Lists.** Convert a pile of facts into sentences or a small table where possible.
  When a list is genuinely needed, keep its items grammatically parallel.
- **Callouts.** Use a blockquote with a leading label: `> **Note —**`,
  `> **Warning —**`, `> **Tip —**`. One sentence, no emoji.
- **Cross-links.** Link related chapters with relative paths so the book stays
  navigable after a build.
- **Diagrams.** Keep Mermaid diagrams; precede each with a one-line caption. Ensure
  they render in the mdBook HTML output.
- **Dates.** ISO format: `2026-08-15`.
- **Numbers.** Spell out one through nine in prose; use figures for data and
  measurements (23 components, 63 tests, 6 GB). Be consistent within a sentence.

## 5. Correctness policy (per the 2026-08-15 fleet audit)

Documentation must not contradict the code or the audit's verified findings.

- **License.** The body is **GPL-3.0-or-later**. Do not state MIT anywhere.
- **Upstreams.** Do not present `gaganjainse/SheshOS` as a live, reachable source.
  Mark it unpublished or conceptual. Validate owned upstream URLs in CI.
- **Facts.** Preserve the technical facts you find — test counts, versions, model
  names, hardware specs. Do not invent new ones. If a figure is flagged as stale or
  uncertain in the audit, soften it ("as of the last audit") or flag it explicitly.
- **Status.** Label active versus archived repositories accurately, per
  `audit-manifest.tsv`. Archived packages are not executable products.
- **History versus live.** Keep historical audits, query logs, and incident reports
  clearly separated from live reference material with a visible banner.

## 6. Things to avoid

- Emoji as decoration in titles or prose (status badges in existing READMEs are
  grandfathered; do not add new ones).
- Filler openings: "Here is…", "In this document we will…", "Welcome to…".
- Repeating "this repo is for reading only" more than once (state it in the
  introduction, then move on).
- Inconsistent capitalization: **Shesh** in prose, **shesh-** for repos and
  packages, **SheshAOS** for the OS.
- Mixed voices within one page — pick the essay voice and hold it.

## 7. Before and after

**Before (note style, emoji, label headings, no flow):**

> # 🐍 Shesh Ecosystem
> ## Why this repo exists
> We fork every upstream we depend on and keep those forks rolling; we integrate the
> best parts as Shesh components and only let tested combinations reach the daily
> driver. That gives us latest upstream without waiting for releases, safety
> (breakage is caught in canary, not on your machine), coherence (one manifest, one
> lockfile, one audit log, one policy engine), and ownership (the integrated whole is
> Shesh, not a pile of someone else's brands).

**After (Spectrum voice, concrete lede, defined terms):**

> # The Shesh Ecosystem
>
> Shesh is a federated, local-first AI body for a CachyOS/Hyprland machine. This
> chapter explains what the ecosystem is, why it is built as a federation of pinned
> forks rather than a single application, and how a change travels from an upstream
> project to the machine on your desk.
>
> Most AI desktops are a loose collection of someone else's tools. Shesh takes a
> different path: it forks every upstream it depends on, keeps those forks rolling
> with upstream, and integrates the best parts as first-class Shesh components. Only
> combinations that survive testing reach the daily driver.
>
> This discipline buys four things. *Latest upstream* — new work lands without waiting
> for a release. *Safety* — breakage is caught in canary, not on your laptop.
> *Coherence* — one manifest, one lockfile, one audit log, one policy engine. And
> *ownership* — the integrated whole is Shesh, not a pile of other people's brands.
