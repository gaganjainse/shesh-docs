# Introduction

Imagine owning a small city of software: dozens of autonomous services, each with its
own mind, memory, and hands, all expected to cooperate on a single machine. That is the
Shesh fleet. This book is the map.

Shesh is a federated, local-first artificial-intelligence body built on a
CachyOS/Hyprland Linux machine. Rather than a single monolithic program, it is a
federation of repositories — components that together form one coherent system. This
repository, `shesh-docs`, is the **reading edition**: a single, well-ordered compilation
of the documentation that lives across every component repository, gathered here so the
whole can be understood without jumping between thirty-one separate projects.

## What this book is

This is a compiled reference, not the source of truth. The authoritative documentation
for any component continues to live in that component's own repository. Here, those
documents are copied, organized, and kept in sync so you can read the ecosystem as one
continuous work. Think of it as the bound volume of a newspaper whose sections are
otherwise scattered across the newsroom.

The compilation is generated and maintained with [mdBook](https://rust-lang.github.io/mdBook/),
a documentation toolchain modeled on the Rust programming language's own books. Navigation
is driven by a single table of contents (`SUMMARY.md`), and every chapter is cross-linked
to the section that surrounds it.

## How the fleet is organized

The fleet is deliberately separated into three planes so that experimental tooling never
leaks into the product a person actually runs:

- **Product** — `shesh-ecosystem` and its components. This is what runs on the machine:
  the agent, its body, and its safeguards. It is clean, versioned, and installable.
- **Factory** — `shesh-workspace`. The development harness: session protocols, swarm
  orchestration, secure credentials, and efficiency tooling. It is intentionally kept
  apart from the product so that builder workflows do not complicate the running system.
- **Gateway** — `shesh-omniroute` and the OmniRoute fork. An optional cloud layer that
  brokers access to large hosted models, always secondary to the local Ollama primary.

A fourth area, **Desktop** (`shesh-desktop`), is the styling and performance layer — the
look and feel of the system on real hardware.

## What you will find

The book is divided into twelve parts. After this introduction and a short guide to using
these docs, the parts proceed from the product outward: architecture and concepts, the
manual verification tasks, the reference material, tutorials, then the factory and gateway
planes, the desktop, the architecture decision records, audits and roadmaps, verification
and handoff, skills and policies, the decision trail, the portfolio projects, and finally
the SheshAOS operating system.

A [glossary](./glossary.md) defines the fleet's vocabulary, and a [style guide](./STYLE_GUIDE.md)
records the editorial standards every chapter follows, so the compilation reads as one
voice rather than a pile of unrelated notes.

## A note on accuracy

Because this is a living compilation, individual chapters carry their own dates and status.
The fleet audit of 2026-08-15 established the current factual baseline — license
(GPL-3.0-or-later), component counts, and test status — and this book follows it. Where a
chapter describes work in progress, that status is stated plainly.

**Owner:** Gagan Jain ([@gaganjainse](https://github.com/gaganjainse)) · **License:**
GPL-3.0-or-later.
