# shesh-omniroute

> **Shesh wrapper around the OmniRoute gateway.** A self-hosted, OpenAI-compatible
> LLM gateway for the whole Shesh stack. It runs our OmniRoute fork in a rootless
> podman container and exposes `http://localhost:20128/v1` to every client.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python) ![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue) ![Tests](https://img.shields.io/badge/Tests-17-success) ![CI](https://github.com/gaganjainse/shesh-omniroute/actions/workflows/ci.yml/badge.svg)

- **License:** GPL-3.0-or-later
- **Owner:** Gagan Jain ([@gaganjainse](https://github.com/gaganjainse))
- **Layer:** Soma (gateway — optional cloud fallback)
- **Part of:** [shesh-ecosystem](https://github.com/gaganjainse/shesh-ecosystem)

---

## Quick start

```bash
pipx install .
shesh-omniroute start            # pulls image, starts container, waits for health
shesh-omniroute status           # endpoint + health + routing-ready check
export SHESH_OMNIROUTE_BASE_URL=http://localhost:20128/v1
```

The gateway API key is generated on first start and stored with `0600`
permissions at `~/.config/shesh/omniroute/api.key`, or pushed into
shesh-secrets as `omniroute:api-key` when shesh-secrets is installed.

## Layout

- `src/shesh_omniroute/` — the whole wrapper (standard library only)
- `templates/` — container environment and routes configuration, rendered on start
- `tests/` — full offline test suite (mocked container backend and health server)
- `Containerfile` — builds the gateway image from our fork

## Status

Component CI is green (reusable ecosystem pipeline). For the security posture
and vulnerability reporting, see
[SECURITY.md](https://github.com/gaganjainse/shesh-omniroute/blob/main/SECURITY.md).

## Where this fits

`shesh-omniroute` is the Shesh-side face of the optional cloud layer described in
the [gateway overview](overview.md) and the [OmniRoute study](omniroute-study.md).
It is a planned, opt-in component of the
[shesh-ecosystem](https://github.com/gaganjainse/shesh-ecosystem) product.

## License

GPL-3.0-or-later — see
[LICENSE](https://github.com/gaganjainse/shesh-omniroute/blob/main/LICENSE).
