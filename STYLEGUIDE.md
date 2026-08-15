# Shesh documentation style guide

This guide governs every Markdown file in the Shesh fleet: the `shesh-docs` book,
component READMEs, ADRs, and policy documents. It derives from the
[Google developer documentation style guide](https://developers.google.com/style),
with project-specific rules added where Google is silent.

When this guide and a local convention disagree, this guide wins. When this guide
is silent, follow Google. When both are silent, choose the option that a reader
encountering the page for the first time would find least surprising.

## 1. Voice and tone

Write for a competent engineer who has not seen this system before.

| Rule | Do | Don't |
|---|---|---|
| Address the reader as "you" | `Run make check before you promote a build.` | `We run make check before we promote.` |
| Use present tense | `The resolver writes shesh.lock.` | `The resolver will write shesh.lock.` |
| Use active voice | `The guard rejects the call.` | `The call is rejected by the guard.` |
| State facts, not history | `Components are declared in components.toml.` | `We decided to move components into components.toml.` |
| Describe behaviour, not intent | `The scheduler retries three times.` | `The scheduler should retry three times.` |

Prohibited constructions:

- **First person.** No `I`, `we`, `our`, `us`, `my`. The project has no narrator.
  Attribute decisions to the artefact: "ADR-0019 consolidates the sub-services",
  not "we consolidated the sub-services".
- **Quoted user requests.** Never paste a chat prompt into a document. If the
  prompt contains a requirement, state the requirement.
- **Acquisition metaphors.** Do not write "steal", "stolen", or "steal-map" about
  other projects. Write "adapted from", "modelled on", or "derived from", and
  link the source with its licence.
- **Self-assessment.** Do not write "proper system", "not messed up", "foolproof",
  "clean", or "messy" about the project's own design. These claims are unverifiable
  and age badly. Describe the property instead: "each service owns its own
  release cadence".
- **Filler intensifiers.** Remove "simply", "just", "obviously", "of course",
  "easy", "powerful", "seamless", "robust".
- **Exclamation marks** in body text.

## 2. Headings

- One `#` H1 per file, matching the `SUMMARY.md` entry.
- **Sentence case**: capitalise the first word and proper nouns only.
  `## Release channels`, not `## Release Channels`.
- No emoji, no numeric prefixes, no trailing punctuation.
- Do not skip levels. Never go deeper than H4.
- Headings are noun phrases (`## Failure modes`) or imperatives in how-to guides
  (`## Configure the resolver`). Never questions.

## 3. Document types

Every chapter is exactly one Diátaxis type, declared in its front matter. Do not
mix types in one page; link instead.

| Type | Answers | Voice | Must not contain |
|---|---|---|---|
| **Tutorial** | "Teach me by doing" | Imperative, one happy path | Options, alternatives, rationale |
| **How-to** | "Help me accomplish X" | Imperative, goal in the title | Teaching, background theory |
| **Reference** | "Tell me the exact facts" | Declarative, tabular | Steps, narrative, opinion |
| **Explanation** | "Help me understand why" | Declarative, discursive | Instructions the reader should follow |

Required front matter on every chapter:

```yaml
---
title: Release channels
type: reference          # tutorial | how-to | reference | explanation
summary: The three promotion channels and the gates between them.
audience: operator       # operator | contributor | maintainer
status: current          # current | historical
verified: 2026-08-15     # date the claims were last checked against code
---
```

`status: historical` marks a document that records a past state. Historical
documents are never edited to look current; they carry a banner (§7).

## 4. Structure of a chapter

1. H1 title.
2. One or two sentences stating what the page covers and who it is for. No
   preamble before this.
3. For how-to and tutorial pages: a **Prerequisites** section listing exact
   versions and prior steps.
4. Body.
5. For how-to and tutorial pages: a **Verify** section with a command and its
   expected output.
6. **Related** — three to five links, each with a clause explaining why to follow it.

Keep chapters under roughly 1,200 words. Split longer material by task.

## 5. Code, commands, and paths

- Fence every block and always declare the language: `bash`, `python`, `toml`,
  `json`, `rust`, `yaml`, `text`.
- Commands appear without a `$` prompt, one command per line, so they can be copied.
- Show expected output in a separate `text` block, not interleaved with the command.
- Long flags over short ones in documentation: `--channel canary`, not `-c canary`.
- Never hard-code a personal path. Use `~/`, `$XDG_CONFIG_HOME`, or a documented
  placeholder such as `<workspace>`. `/home/gagan/...` must not appear.
- Placeholders use angle brackets and kebab-case: `<component-name>`.
- Inline code for: file names, paths, commands, flags, environment variables,
  field names, and literal values. Not for emphasis and not for product names.

## 6. Facts, numbers, and claims

Documentation states only what is true of the committed code at the `verified`
date.

- **No counts in prose or badges** that a change can invalidate — test counts,
  component counts, provider counts, repository counts. Either omit the number
  or generate the page from the source of truth.
- Generated pages carry a first line reading
  `<!-- Generated from <path>. Do not edit by hand. -->`.
- Do not document unimplemented behaviour in a reference or how-to page.
  Unbuilt work belongs on the roadmap, phrased as a plan and dated.
- Every claim about an external project needs a link and, where licensing
  matters, its SPDX identifier.
- Do not embed dynamic shields.io badges for volatile metrics. A CI status badge
  on a repository README is acceptable; `Tests-63` is not.

## 7. Historical documents

Audits, incident reports, session logs, and superseded ADRs are historical. They
are preserved, never silently rewritten, and never presented as current guidance.

Each begins with:

```markdown
> **Historical record.** This document describes the state of the system on
> <date> and is retained for provenance. It is not maintained. For current
> behaviour, see [<page>](<link>).
```

Superseded ADRs keep `Status: Superseded by ADR-NNNN` and are not deleted.

## 8. Cross-references and single sourcing

- **One canonical location per fact.** A page either owns a topic or links to
  the page that owns it. Copying prose between repositories is prohibited;
  duplicated files drift and become contradictory.
- Link text describes the destination: `see [release channels](...)`, never
  `see [here](...)` or a bare URL.
- Links between chapters are relative paths ending in `.md`.
- Component READMEs are canonical in their own repository. The book links to
  them; it does not mirror them.

## 9. Terminology

Use these spellings exactly and consistently.

| Correct | Never |
|---|---|
| Shesh (the project) | shesh, SHESH |
| `shesh-core` (a repository) | Shesh Core, shesh core |
| SheshAOS | Shesh AOS, sheshaos |
| Agentic Body | agentic body, the Body |
| Brain, Mind, Soma (the three layers) | brain/mind/soma in prose |
| Model Context Protocol (MCP) | MCP protocol |
| Agent Client Protocol (ACP) | ACP protocol |
| repository | repo (in prose; `repo` is fine as a field name) |
| directory | folder |
| Expand every acronym on first use per page | — |

## 10. Formatting mechanics

- Wrap prose at 90 columns. Do not wrap tables or links.
- Bulleted lists for unordered sets; numbered lists only for ordered steps.
- Lists have parallel grammar: all fragments or all sentences.
- Tables need a header row; align the pipes.
- Use an em dash sparingly, unspaced (`text—text`). Prefer a comma, colon, or
  full stop. A paragraph with two em dashes is over-punctuated.
- Blockquotes are for callouts only, prefixed with a bold label:
  `> **Warning.** This deletes the lockfile.` Permitted labels: Note, Warning,
  Caution, Historical record.
- Dates are ISO 8601: `2026-08-15`.
- Files and directories are kebab-case: `release-channels.md`.

## 11. Review checklist

A documentation change is ready to merge when:

- [ ] Front matter is present and `verified` is today's date.
- [ ] The page is exactly one Diátaxis type.
- [ ] No first person, no "steal", no self-praise, no quoted prompts.
- [ ] Headings are sentence case with no emoji.
- [ ] Every command was run and every output pasted is real.
- [ ] No volatile counts, no personal paths, no `TODO` markers.
- [ ] Every fact is stated in exactly one place across the fleet.
- [ ] `markdownlint` and the link checker pass.
