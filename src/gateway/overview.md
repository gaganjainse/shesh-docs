# Gateway — optional cloud, local-first by default

![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue)

Shesh is local-first by design (ADR-0005): the Ollama 6 GB stack on the laptop
is the primary brain. The gateway plane exists for one reason — sometimes a
bigger model is worth a network call, and that choice must never cost money or
leak privacy without an explicit opt-in.

The three chapters below survey the optional cloud layer, document the free
capacity it can reach, and describe the wrapper that brings it into the fleet.

- [OmniRoute study](omniroute-study.md) — 291 providers surveyed, 90+ free,
  numbers re-verified and CI-gated.
- [Free providers](free-providers.md) — the usable free tier, extracted.
- [Shesh-Omniroute wrapper](shesh-omniroute.md) — the ecosystem component that
  speaks to the fork.

The OmniRoute fork lives at
[gaganjainse/OmniRoute fork](https://github.com/gaganjainse/OmniRoute). Enabling any
cloud route is a user choice, off by default.
