# Shesh Docs — Complete Reading Compilation

![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue)
![CI](https://github.com/gaganjainse/shesh-docs/actions/workflows/ci.yml/badge.svg)

This repository is the **reading edition** of the Shesh fleet's documentation: a single,
ordered compilation of the docs that live across `shesh-ecosystem`, `shesh-desktop`,
`shesh-workspace`, `shesh-omniroute`, the OmniRoute fork, and every `shesh-*` component.
It exists so the whole can be read and navigated as one book rather than thirty-one
separate projects.

- **License:** GPL-3.0-or-later
- **Owner:** Gagan Jain ([@gaganjainse](https://github.com/gaganjainse))
- **Built with:** [mdBook](https://rust-lang.github.io/mdBook/)

## Why this repository exists

The request that began it was simple: gather every document into one place for reading,
organize it so navigation is never a chore, and keep it in sync with the source
repositories. A live-update flow copies documentation from the component repos into this
one automatically, so the compilation tracks the fleet as it evolves.

## How it is structured

The compilation borrows the best ideas from documentation systems that scale:

- **mdBook** provides the navigation backbone — a single `SUMMARY.md` table of contents,
  numbered parts and chapters, and a search index.
- **Kubernetes-style separation** divides material into concepts (how things work),
  tasks (how to do things), tutorials (how to learn by doing), and reference (precise
  detail).
- **Docs-as-code** keeps every page in version control, reviewed through pull requests,
  with link and build checks in continuous integration.

The fleet is separated into three planes so builder tooling never complicates the product:

- **Product** — `shesh-ecosystem` and its components: what runs on the machine.
- **Factory** — `shesh-workspace`: the development harness, kept apart from the product.
- **Gateway** — `shesh-omniroute` and the OmniRoute fork: an optional cloud model layer.
- **Desktop** — `shesh-desktop`: the styling and performance layer on real hardware.

## Building the book

This is a pure mdBook project. There is no `package.json`; the book is built with the
mdBook toolchain:

```bash
mdbook build
mdbook serve   # serves at http://localhost:3000
```

## Live update

Although this repository is for reading, a live-update flow copies documentation from
`shesh-ecosystem`, `shesh-desktop`, `shesh-workspace`, and the other sources into this
repository automatically. The source of truth remains in each component's own repository;
this book is its organized projection.

## Security

Security posture and vulnerability reporting follow the canonical ecosystem security
policy in [`shesh-ecosystem`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/SECURITY.md).

## License

GPL-3.0-or-later — see [LICENSE](LICENSE).
