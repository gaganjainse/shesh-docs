# Gateway — optional cloud, local-first by default

Shesh is local-first (ADR-0005): the Ollama 6 GB stack on the laptop is the
primary brain. The gateway parts exist for one reason — sometimes a bigger
model is worth a network call, and that must never cost money or privacy
without an explicit choice.

- [OmniRoute study](omniroute-study.md) — 291 providers surveyed, 90+ free,
  numbers re-verified and CI-gated.
- [Free providers](free-providers.md) — the usable free tier, extracted.
- [Shesh-Omniroute wrapper](shesh-omniroute.md) — the ecosystem component
  that speaks to the fork.

The OmniRoute fork itself lives at
[gaganjainse/OmniRoute](https://github.com/gaganjainse/OmniRoute); enabling
any cloud route is a user choice, off by default.
