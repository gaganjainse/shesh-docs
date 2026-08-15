---
title: Reference
type: reference
summary: "An index of factual reference material: schemas, catalogues, and checklists."
audience: operator
status: current
verified: 2026-08-15
---

# Reference

Reference pages state facts. They contain no instructions and no rationale. Pages
marked as generated are produced from a source file in the repository and must
not be edited by hand.

## System composition

| Page | Contents |
|---|---|
| [Component catalogue](components.md) | Every component, its layer, channel, and owning repository. Generated from the manifest. |
| [Manifest schema](manifest-schema.md) | The fields of `components.toml` and their permitted values. |
| [Release channels](release-channels.md) | The three channels and the gates between them. |
| [Models](models.md) | Each model, its role, context window, and residency budget. |
| [Upstreams](upstreams.md) | Tracked third-party projects and the reason each is tracked. |
| [Licences and sources](licences.md) | Licence of every bundled or forked dependency. |
| [Cloud model providers](cloud-providers.md) | Network providers reachable through the gateway. |

## Behaviour

| Page | Contents |
|---|---|
| [Skills](skills/index.md) | The behaviour library and the rules governing it. Served by `shesh-skills`. |
| [Verification checklist](verification-checklist.md) | Every manual check, by area. |
| [Desktop verification checklist](desktop-checklist.md) | Desktop-specific checks. |
| [Related projects](related-projects.md) | Adjacent repositories that are not part of the installed system. |

## Related

- [How-to guides](../how-to/index.md) — the procedures that use these values.
- [Architecture](../explanation/index.md) — why the system is composed this way.
- [Governance](../governance/security-policy.md) — the policies these values must
  satisfy.
