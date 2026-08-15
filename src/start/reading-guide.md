---
title: How to read these documents
type: explanation
summary: "How the book is organised by document type, and which path to follow for your goal."
audience: operator
status: current
verified: 2026-08-15
---

# How to read these documents

This book separates documentation by the reader's need rather than by feature.
Knowing which part answers your question is faster than searching.

## The four document types

Every page is exactly one type, declared in its front matter as `type`.

| Type | It answers | It deliberately omits |
|---|---|---|
| **Tutorial** | "Teach me by doing." One guided path to a working result. | Alternatives, options, rationale |
| **How-to** | "Help me accomplish a specific task." | Teaching, background theory |
| **Reference** | "Tell me the exact fact." Tables, schemas, flags. | Steps, narrative, opinion |
| **Explanation** | "Help me understand why it works this way." | Instructions to follow |

A page that mixes types is a defect. Report it as a documentation issue.

## Choose a path

**You want to install and run Shesh.**
[Install Shesh](install.md), then work through the
[verification checklist](../reference/verification-checklist.md) on the machine.

**You want to understand the design.**
Start at [The Agentic Body](../explanation/agentic-body.md), then
[Repository topology](../explanation/repository-topology.md) and
[Agent protocols](../explanation/protocols.md). The reasoning behind each
load-bearing choice is recorded in the
[architecture decision records](../governance/adr/index.md).

**You have a specific task.**
Go to [How-to guides](../how-to/index.md). Guides are titled by goal, so scan the
list rather than reading in order.

**You need an exact value.**
Go to [Reference](../reference/index.md): the
[manifest schema](../reference/manifest-schema.md),
[release channels](../reference/release-channels.md),
[component catalogue](../reference/components.md), and
[model list](../reference/models.md).

**You are working on Shesh itself.**
[Development environment](https://github.com/gaganjainse/shesh-workspace/blob/main/docs/index.md) covers the contributor
workflow, the parallel-agent tooling, and the evaluation harness. This material
is separate from the operator documentation because it describes tooling that is
not part of what you install.

**You are auditing the system.**
[Security policy](../governance/security-policy.md),
[Threat model](../governance/threat-model.md), and
[Dependency policy](../governance/dependency-policy.md).

## Trusting a page

Two fields in the front matter tell you how much to rely on a page:

- `status: current` — the page describes committed behaviour and is maintained.
- Superseded material is not kept in this book. It moves to
  [shesh-docs-archive](https://github.com/gaganjainse/shesh-docs-archive), where
  every page carries a banner. Do not follow instructions from an archived page.
- `verified: <date>` — when a maintainer last checked the page against the code.

## Searching

The rendered book includes a full-text index. Press <kbd>S</kbd> to focus the
search field and <kbd>?</kbd> for the keyboard shortcuts. Search matches page
titles and body text, so searching for an exact flag or field name is usually
faster than browsing.

## Related

- [Introduction](introduction.md) — what the system is and how the parts fit.
- [Glossary](glossary.md) — terms and acronyms used throughout.
- [Documentation policy](../governance/documentation-policy.md) — the rules that
  govern what may be written here.
