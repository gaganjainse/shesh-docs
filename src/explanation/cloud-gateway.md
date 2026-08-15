---
title: The cloud gateway
type: explanation
summary: "Shesh is local-first (ADR-0005): the Ollama 6 GB stack on the laptop is the."
audience: operator
status: current
verified: 2026-08-15
---

# The cloud gateway

Shesh is local-first (ADR-0005): the Ollama 6 GB stack on the laptop is the
primary brain. The gateway parts exist for one reason — sometimes a bigger
model is worth a network call, and that must never cost money or privacy
without an explicit choice.

- [OmniRoute study](https://github.com/gaganjainse/shesh-docs-archive/blob/main/src/omniroute-study.md) — a large provider set surveyed, a free subset,
  numbers re-verified and CI-gated.
- [Free providers](../reference/cloud-providers.md) — the usable free tier, extracted.
- [Shesh-Omniroute wrapper](../how-to/enable-cloud-routing.md) — the ecosystem component
  that speaks to the fork.

The OmniRoute fork itself lives at
[gaganjainse/OmniRoute](https://github.com/gaganjainse/OmniRoute); enabling
any cloud route is a user choice, off by default.
