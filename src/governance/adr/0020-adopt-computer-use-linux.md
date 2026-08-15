---
title: "ADR-0020: Adopt computer-use-linux for desktop automation"
type: explanation
summary: "Adopt computer-use-linux for desktop automation."
audience: maintainer
status: current
verified: 2026-08-15
---

# ADR-0020: Adopt computer-use-linux for desktop automation

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-08-15 |
| **Deciders** | Fleet maintainer |
| **Tags** | adopt-vs-build, soma, desktop, licensing |

## Context

`GAPS.md` records the capabilities an operator reaches for that the fleet
cannot serve. After `shesh_desktop_ctl` closed Bluetooth, networking,
brightness, clipboard, session control, services, and notifications, the
largest remaining gap is genuine desktop automation: reading the accessibility
tree, targeting windows across compositors, and injecting input.

That gap is not a weekend of work. It requires AT-SPI bindings, per-compositor
window backends for GNOME, KDE, Hyprland, i3, and COSMIC, Wayland portal
handling, and a uinput driver for input injection. Each is a separate,
long-lived maintenance burden, and getting any of them subtly wrong produces
an agent that clicks the wrong thing.

[computer-use-linux](https://github.com/agent-sh/computer-use-linux) already
does this. It is a Rust Model Context Protocol server, MIT licensed, with a
backend registry that tries the GNOME Shell extension, GNOME Introspect, the
COSMIC helper, KWin scripting, `hyprctl`, i3 IPC, and generic X11 in order.
It was extracted from a shipping product and carries a documented safety
contract and a `doctor` readiness command.

[ADR-0018](0018-adopt-vs-build.md) requires preferring a maintained upstream
where one exists.

## Decision

Adopt `computer-use-linux` as the desktop automation backend rather than
writing an equivalent.

- **Licence.** MIT, which is compatible with distribution under
  GPL-3.0-or-later. Recorded in the manifest and in
  [Licences and sources](../../reference/licences.md).
- **Integration.** It runs as a separate process speaking the Model Context
  Protocol over standard input and output. It is not linked into any Shesh
  package, consistent with the process-boundary rule in
  [ADR-0001](0001-five-languages.md).
- **Governance.** It is not exposed to agents directly. `shesh-core` proxies
  it through `shesh_desktop_ctl`, so every call passes the policy engine and
  is recorded in the audit log exactly like a first-party tool
  ([ADR-0015](0015-guard-policy.md)). Direct configuration of the upstream
  server in a client is unsupported, because it would bypass the guard.
- **Version.** Pinned in the manifest and tracked by the upstream job like any
  other fork.
- **Scope.** Adopted for the accessibility tree, window targeting, screen
  capture, and input injection. The capabilities already covered by
  `shesh_desktop_ctl` are not re-delegated; one owner per capability.

Rejected in the same review:

- `mcp-linux-desktop` — overlaps heavily with `shesh_desktop_ctl`, and its
  licence was not clearly declared at the time of review. Reconsider if that
  changes.
- `hyprmcp` — narrower than the chosen option, and `shesh_shell` already covers
  compositor control for the reference configuration.

## Consequences

### Benefits

- The largest remaining capability gap closes without the fleet taking on
  AT-SPI, five compositor backends, and a uinput driver.
- Compositor coverage extends beyond the reference configuration, which the
  fleet would not otherwise have attempted.
- Upstream absorbs the maintenance as compositors change.

### Costs and risks accepted

- A Rust binary joins the runtime dependencies. It is not built from the
  workspace, so it is fetched and pinned like any other upstream.
- Desktop automation is inherently high-risk: an agent that can click and type
  can do anything the user can. Every call is therefore policy-gated and
  logged, and input injection defaults to confirm rather than allow.
- The upstream is a single-maintainer project. If it stops being maintained,
  the fork already exists and the proxy boundary means only one package
  changes.
- The accessibility service must be enabled on the machine. The upstream
  `doctor` command reports readiness; a first-boot check surfaces it.

## References

- [ADR-0018](0018-adopt-vs-build.md) — adopt over build.
- [ADR-0015](0015-guard-policy.md) — everything passes the guard.
- [GAPS.md](https://github.com/gaganjainse/shesh-skills/blob/main/GAPS.md) — the
  capability register this closes against.
