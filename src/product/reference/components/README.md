# Components — all shesh-* repositories

This table is a projection of [`manifests/components.toml`](../manifest.md); the manifest is the
single source of truth and this page is derived from it. It lists the 23 components that make up
the product, grouped by the body layer they serve.

| Component | Layer | Channel | Archived | Repo |
|---|---|---|---|---|
| `shesh-acp` | soma | canary | Yes | [shesh-acp](https://github.com/gaganjainse/shesh-acp) |
| `shesh-audit` | brain | canary | Yes | [shesh-audit](https://github.com/gaganjainse/shesh-audit) |
| `shesh-backup` | soma | canary | Yes | [shesh-backup](https://github.com/gaganjainse/shesh-backup) |
| `shesh-brain` | brain | devel | Yes | [shesh-brain](https://github.com/gaganjainse/shesh-brain) |
| `shesh-calendar` | mind | canary | Yes | [shesh-calendar](https://github.com/gaganjainse/shesh-calendar) |
| `shesh-containers` | soma | canary | Yes | [shesh-containers](https://github.com/gaganjainse/shesh-containers) |
| `shesh-desktop` | soma | stable | No | [shesh-desktop](https://github.com/gaganjainse/shesh-desktop) |
| `shesh-ebpf` | soma | canary | Yes | [shesh-ebpf](https://github.com/gaganjainse/shesh-ebpf) |
| `shesh-files` | soma | canary | Yes | [shesh-files](https://github.com/gaganjainse/shesh-files) |
| `shesh-harness` | mind | canary | No | [shesh-harness](https://github.com/gaganjainse/shesh-harness) |
| `shesh-mcp-bundle` | soma | canary | Yes | [shesh-mcp-bundle](https://github.com/gaganjainse/shesh-mcp-bundle) |
| `shesh-media` | soma | canary | Yes | [shesh-media](https://github.com/gaganjainse/shesh-media) |
| `shesh-memory` | mind | canary | No | [shesh-memory](https://github.com/gaganjainse/shesh-memory) |
| `shesh-messaging` | soma | canary | Yes | [shesh-messaging](https://github.com/gaganjainse/shesh-messaging) |
| `shesh-mind` | mind | canary | Yes | [shesh-mind](https://github.com/gaganjainse/shesh-mind) |
| `shesh-omniroute` | mind | devel | No | [shesh-omniroute](https://github.com/gaganjainse/shesh-omniroute) |
| `shesh-orchestrator` | mind | devel | No | [shesh-orchestrator](https://github.com/gaganjainse/shesh-orchestrator) |
| `shesh-phone` | soma | devel | No | [shesh-phone](https://github.com/gaganjainse/shesh-phone) |
| `shesh-secrets` | brain | canary | Yes | [shesh-secrets](https://github.com/gaganjainse/shesh-secrets) |
| `shesh-shell` | soma | canary | Yes | [shesh-shell](https://github.com/gaganjainse/shesh-shell) |
| `shesh-skills` | mind | canary | Yes | [shesh-skills](https://github.com/gaganjainse/shesh-skills) |
| `shesh-system` | soma | canary | Yes | [shesh-system](https://github.com/gaganjainse/shesh-system) |
| `shesh-voice` | soma | canary | No | [shesh-voice](https://github.com/gaganjainse/shesh-voice) |

## Reading the archive column

The `Archived` column reflects the 2026-08-15 fleet audit (`audit-manifest.tsv`) — the GitHub
archive state of each repository. This is distinct from the manifest's own `archived` flag on
`shesh-desktop`, which marks that repository as a read-only provenance snapshot excluded from
clone lists and audits, even though its GitHub repository is not archived.

Component READMEs stay canonical in their own repositories (policy: ecosystem links, never copies
prose).
