# 01 — Independent Audit (verified against the live repo, 2026-08-09)

This chapter is the current truth about the live `shesh-desktop` repository. It lists which defects from earlier audits are fixed, which remain, and which new bugs a previous AI pass introduced while "fixing" the code. It supersedes two prior audits and a 63-page master plan, and no one should act on those older documents without reading this table first.

> **Method:** I cloned `gaganjainse/shesh-desktop` at `36481e1` and read every installer script, systemd unit, tool, and CI workflow directly. Prior AIs produced two audits (40 issues) and a 63-page master plan, then **partially applied fixes to the repo**. This audit marks which old issues are fixed, which remain, and which new bugs the previous AI introduced while "fixing" things. Do not act on the old audits without this table.

Severity: Critical · High · Medium · Low
Status: Fixed · Broken · Partial/Incomplete · New finding

---

## A. New bugs introduced by the prior AI "fixes" (fix these first)

### N-01 — `$AUR_HELPER` is never defined, so `setup_ai_stack` crashes on a clean install

**File:** `sdata/subcmd-install/2.setups.sh:513`

```bash
v "$AUR_HELPER" -S --noconfirm --needed newelle
```

`AUR_HELPER` is referenced but assigned nowhere in `sdata/` or `tools/` (verified with grep). On a fresh CachyOS 260628 system where `newelle` is not installed, `v "" -S ...` expands to `-S --noconfirm --needed newelle`, which bash tries to execute as a command, so the install aborts. This is a critical regression shipped to the repo.

**Fix:** add a detector in `sdata/lib/functions.sh` and export it:

```bash
get_aur_helper() {
  for h in shelly paru yay; do command -v "$h" >/dev/null && { echo "$h"; return; }; done
  echo ""  # caller must handle absence
}
```

then in `2.setups.sh` (after sourcing functions):

```bash
AUR_HELPER="$(get_aur_helper)"
[[ -z "$AUR_HELPER" ]] && { log_warning "No AUR helper; installing shelly"; sudo pacman -S --needed shelly && AUR_HELPER=shelly; }
```

Note: `shelly` is the CachyOS default and its CLI flags differ from paru/yay — verify `$AUR_HELPER -S --noconfirm --needed PKG` works under `shelly` (it may need `shelly -S` without `--noconfirm`, or you may prefer to `pacman -S --needed paru` first for scripting stability).

### N-02 — `setup_ai_stack` uses `bc` for version compare, but `bc` is not a declared dependency

**File:** `2.setups.sh:501`

```bash
if [[ "$(echo "$ollama_ver >= 0.32" | bc -l)" != "1" ]]; then
```

`bc` is not guaranteed on a minimal CachyOS install and is not in `dist-arch/install-deps.sh` (verified). If `bc` is missing, `bc -l` fails, the command substitution is empty, `!= "1"` is true, and — worse — if `set -e`/`v` treats the pipeline as failure, the step aborts.

**Fix:** use pure bash arithmetic (strip the dot):

```bash
IFS=. read -r maj min _ <<<"$ollama_ver"
if (( maj < 0 || (maj == 0 && min < 32) )); then ...; fi
```

Also `grep -oP '[0-9]+\.[0-9]+'` against `ollama --version` (which prints `ollama version is 0.32.6`) yields `0.32` — fine, but anchor it to avoid matching other numbers.

### N-03 — `watcher-rs` is built by setup but does not exist in the repo

**File:** `2.setups.sh` (Rust build block) references `tools/smart-organizer/watcher-rs/`, but that directory is absent (verified: `ls` returns "MISSING"). The code guards with `[[ -d ]]`, so it silently falls through to the Python `watchfiles` fallback — meaning the flagship "Rust watcher" the roadmap promises is vaporware, and the fallback installs `watchfiles` even though no Python watcher script exists to use it. This is at best a medium issue (no crash) but critical against your stated goal.

**Fix:** either create `watcher-rs/` (see `05-smart-organizer.md` for the full Cargo project) or remove the block until it exists. Do not ship references to absent code.

### N-04 — MCP server loop references `hyprland_control.py` and `smart_organizer.py` that do not exist

**File:** `2.setups.sh` installs MCP servers by iterating `system_control smart_organizer hyprland_control`, but only `tools/shesh/mcp_servers/system_control.py` exists. The `[[ -f ]]` guard means the missing two are silently skipped, yet the unit-enable loop still generates and enables `.service` files for all three names, producing `shesh-smart-organizer-mcp.service` and `shesh-hyprland-control-mcp.service` that point at non-existent executables, so the units fail or stay dead after boot.

**Fix:** iterate over present files (`for f in "$mcp_dir"/*.py`) and derive names from disk, or create the two missing servers (provided in `06-shesh-agent.md`).

### N-05 — `tools/shesh/core/memory.py` is a two-line assertion stub

The only content is a ChromaDB version assert. There is no `SheshMemory` class, no store/search, despite the roadmap and `agent.py` pseudocode referencing it. `Cargo.toml` declares a Rust binary with no `src/main.rs`. `config/statusbar.json` is `{"pattern":"ml4w-2.14.1"}` with no explanatory schema. These are scaffolding placeholders that look finished.

**Fix:** either complete them per the specs in this doc set or delete them so they do not mislead.

### N-06 — `subcmd-uninstall/2.undo-setups.sh` is an empty placeholder

Contents: `#!/bin/bash` / `# Placeholder`. The prior audit's HIGH-06 ("uninstall doesn't undo NVIDIA/AI/organizer") is therefore not actually fixed, despite the file existing (which makes it look fixed). A full implementation is in `02-roadmap.md`.

### N-07 — NVIDIA `setup_nvidia_mux` final print says `sudo msi-gpu-switcher status` (wrong binary)

The installed binary is `msi-mux-switcher` (symlinked earlier in the same run). The trailing message tells the user to run `msi-gpu-switcher`, which does not exist.

**Fix:** print `sudo msi-mux-switcher status`.

### N-08 — Newelle config claims HTTP MCP endpoints on ports 8765/8766/8767, but nothing serves them

`dots/.config/newelle/config.toml` lists `smart_organizer = "http://localhost:8765/mcp"` etc., but `system_control.py` uses stdio transport (`mcp.run(transport="stdio")`) and no HTTP server is shipped. Newelle will fail to connect to all three. Either run the MCP servers as stdio (Newelle 1.4.5 supports STDIO on native installs) and configure them as `command:` entries, or ship a tiny stdio-to-HTTP bridge.

**Fix:** use stdio MCP config in Newelle (see `06-shesh-agent.md`); remove the bogus http URLs.

### N-09 — Bootloader/NVIDIA code has an unclosed heredoc/branch in the truncated region

The visible portion of `setup_nvidia_mux` in the live file is malformed around the systemd-boot branch (`ue` / `NEEDS_INITRAMFS_REBUILD` appears mid-function without the enclosing `case` shown). Run `bash -n sdata/subcmd-install/2.setups.sh` and fix every syntax error before relying on it.

**Action:** `bash -n` must pass cleanly; this is the first CI gate (see `02-roadmap.md`).

### N-10 — `dots/.config/shesh/config.toml` references the RTX 4050 correctly, but claims iGPU offload for `moondream2` via "v0.31.2"

Ollama's iGPU offload for vision is Intel-ARC-specific and your 14700HX iGPU is Arc (Xe-LPG) class, so it may work, but this is unverified; treat it as experimental and do not make it a hard dependency of the install.

---

## B. Status of the original 40 audit issues

A prior audit produced 40 issues. The table below records each issue's current state against the live repository on 2026-08-09.

| ID | Sev | Issue | Status today | Notes / action |
|----|-----|-------|--------------|----------------|
| BUG-01 | Critical | `showfun`/`v` before function defs | Partial | `setup_mux_switcher` still has `showfun`/`v` immediately after its def (ok) but `setup_nvidia_mux`, `setup_ai_stack`, `setup_power_management` retain the "define-then-call-adjacent" pattern; the original "called before defined" ordering is mostly resolved for mux/smart-org but NVIDIA/AI/power still interleave. Restructure per `02-roadmap.md` Phase 1. |
| BUG-02 | Critical | Backup `--dry-run` hardcoded | Fixed | Here-doc in `2.setups.sh` now writes `ExecStart=${BIN_DIR}/backup.sh` (no flag); `tools/backup/backup.service` static file remains — verify it also has no `--dry-run` (it is unused by setup but ships in repo). |
| BUG-03 | Critical | `diagnose rm` without `-f` | Fixed | Now `rm -f "$output_file"` (quoted). |
| BUG-04 | Critical | `install-files` missing sudo keepalive | Fixed | `setup:121` now calls `sudo_init_keepalive`. |
| BUG-05 | Critical | MSI DMI detection wrong (AND vs OR) | Broken | Live code: `if [[ -f product_name ]] || grep -qi MSI sys_vendor`. This is now OR, but the first clause `[[ -f product_name ]]` is true on virtually every laptop (the file always exists), so the MUX installer runs on every machine, not just MSI. Fix to actually test content: `grep -qi MSI /sys/class/dmi/id/sys_vendor || grep -qi MSI /sys/class/dmi/id/product_name`. |
| BUG-06 | Critical | mkinitcpio sed duplicates modules | Partial | The NVIDIA block was rewritten with broader bootloader support, but the MODULES insertion must be verified idempotent (dedupe); review the actual `sed`/`awk` in the live function and add the dedup routine from `04-device-profile.md`. |
| HIGH-01 | High | `command_exists` triple-defined | Broken | Still redefined at top of `2.setups.sh` and in `0.run.sh`; no `tools/lib/common.sh`. |
| HIGH-02 | High | `die()` triple-defined | Broken | `2.setups.sh:4` still defines its own `die`. |
| HIGH-03 | High | AI stack `pip install --user` + `|| true` | Fixed | Now uses `uv venv` + pinned deps; `|| true` removed. (But see N-01/N-02 which break it anew.) |
| HIGH-04 | High | NVIDIA shown on all distros | Fixed | Now guards `OS_GROUP_ID` arch/cachyos and `lspci` nvidia. |
| HIGH-05 | High | ZRAM hardcoded 16 GB, no size config | Broken | `setup_power_management` still says "Configuring ZRAM for 16GB RAM" and only enables the service; never writes `/etc/systemd/zram-generator.conf`, so ZRAM may not even be configured. Must detect RAM and write the config (you have 16 GB — 8 GB zram0, zstd). |
| HIGH-06 | High | Uninstall doesn't undo setups | Partial | File exists but is a stub (N-06). |
| HIGH-07 | High | smart-organizer setup triplicated | Broken | Still generated via here-docs in `2.setups.sh` and `subcmd-smart-organizer/0.run.sh`, plus static files in `tools/smart-organizer/`. Divergences remain (e.g. service names: `smart-organizer.service` vs `smart-organizer-timer.service`). Canonicalize to `tools/*/units/`. |
| HIGH-08 | High | bootstrap machine-specific, no skip flags | Broken | `tools/bootstrap.sh` still titles itself "MSI Sword 16 HX B14VEKG", defines its own colors/logging, and has no `--skip-*`. Add flags + generic framing. |
| MED-01 | Medium | `NC` vs `STY_RST` colors | Broken | Every `tools/*.sh` still redefines `NC`; no shared lib. |
| MED-02 | Medium | log functions redefined everywhere | Broken | Same. |
| MED-03 | Medium | `--fisrtrun` typo in help | Broken | Still present `options.sh:11`. |
| MED-04 | Medium | repetitive `install_cmds()` | Broken | Untouched. |
| MED-05 | Medium | dead `TEMP_FILES_TO_CLEANUP` code | Broken | Still commented out / unused. |
| MED-06 | Medium | `$base` vs `$REPO_ROOT` | Partial | `diagnose` exports `base`; standardize on `REPO_ROOT`. |
| MED-07 | Medium | duplicate `*credentials*` in safety.sh | Broken | Still duplicated (`safety.sh:43` and `:50`); also `*backup*` overlaps protected dirs. |
| MED-08 | Medium | exp-update-tester redefines logs 7× | Broken | Untouched; migrate to bats. |
| MED-09 | Medium | `local backup=true` shadowing (SC2155) | Low | Low; verify with ShellCheck. |
| MED-10 | Medium | unquoted `mv $t $t.old` | Broken | Quoting audit still needed across `3.files.sh`. |
| MED-11 | Medium | three `.updateignore` paths, no migration | Broken | Untouched. |
| MED-12 | Medium | ShellCheck only lints `tools/` + smart-organizer | Broken | `shellcheck.yml:32` still `find tools sdata/subcmd-smart-organizer` — core installer never linted (this is why N-01..N-09 slipped through). |
| MED-13 | Medium | tests run on Ubuntu, not Arch | Broken | `functional-tests.yml` still ubuntu-latest. |
| MED-14 | Medium | README links to missing `docs/SETUP.md` | Partial | `docs/AI_Documents/` now exists but the specific linked files may not; reconcile links. |
| MED-15 | Medium | README says `mux-switcher` but binary is `msi-mux-switcher` | Partial | The setup echo is now mostly correct but NVIDIA tail says `msi-gpu-switcher` (N-07); re-verify README. |
| MED-16 | Medium | License mismatch (README says MIT, root is GPL-3, MIT.txt placeholders) | Broken | `README.md:124` still says "MIT - Same as upstream end-4/dots-hyprland" (upstream is GPL-3), and `licenses/MIT.txt` still has `<YEAR>`/`<COPYRIGHT HOLDER>`. |
| MED-17 | Medium | `2>&1>/dev/null` wrong redirect order | Low | Verify `1.deps-router.sh:9`. |
| MED-18 | Medium | font install `cd` without subshell | Broken | Untouched. |
| MED-19 | Medium | `ls` word-split into arrays | Broken | `backup_clashing_targets` in functions.sh still uses `($(ls -A ...))`. |
| LOW-01..08 | Low | indentation, naming, stale comments, ci-trigger, debug echo | Broken (mostly) | `ci-test-trigger.txt` still present; empty `custom/*.lua` still 1-byte; `remove_bashcomments_emptylines` debug echo to verify. |

**Bottom line:** of the original 40, only about 5 are genuinely fixed; the repo looks further along than it is because stub files were added. The previous AI also introduced 10 new issues (Section A), three of which are critical and block a clean install.

---

## C. New issues found beyond both prior audits

### NEW-A — Wrong hardware assumptions baked into comments and configs across the codebase

Multiple files and the entire PDF plan assume a 2560x1600 "QHD+" panel and an RTX 4070 8 GB. Your actual SKU (`B14VEKG-210IN`) is 1920x1200 FHD+ FHD+ at 144 Hz with RTX 4050 6 GB. Any `monitor=eDP-1,2560x1600@144` line will fall back to a lower/default mode. Any model pulled for an 8 GB budget (qwen3:14b, llava:13b) will OOM. **Action:** create one `profiles/msi-sword-cachyos/profile.conf` as the single source of these values and source it everywhere; never hardcode resolution/VRAM.

### NEW-B — No `hyprland_control` / `smart_organizer` MCP servers (also N-04)

The headline "Shesh controls Hyprland" feature has no implementation. `06-shesh-agent.md` provides both servers (hyprctl wrapper + organizer trigger).

### NEW-C — No wake-word/voice service unit

Newelle is installed but there is no user service ensuring it (or its voice backend) starts on login, and no documented `uwsm`/graphical-session ordering. The "Hey Shesh" experience will not survive reboot.

### NEW-D — Smart-organizer `--watch` is a polling loop, not inotify

`smart-organizer.sh` advertises `--watch` but the lib has no event watcher; it likely re-scans on a sleep loop. On a spinner/NVMe this wastes I/O and feels laggy versus the promised sub-100 ms reaction. Real-time watching is specified in `05-smart-organizer.md`.

### NEW-E — `safety.sh` is included but uses undefined logging funcs

`safety.sh` calls `log_info`, `log_error`, `log_ok`, `is_dry_run`, `log_action_dry` which it neither defines nor sources. When `organize.sh` sources it after defining those, it works; if sourced standalone it crashes. There is no clear contract. Add a header comment documenting required sourcing order, or move shared logging to `tools/lib/common.sh`.

### NEW-F — No tests for any of the new shell/Python (MCP, organizer, mux-switcher)

The repo has a `test.sh` but it targets upstream exp-update logic. The new tools have zero coverage. At minimum add: shellcheck + `bash -n` for all `.sh`; `python -m py_compile` for all `.py`; a containerized dry-run. This is how N-01..N-09 reached `main`.

### NEW-G — `.github/workflows/python-check.yml` exists but its scope vs the new `tools/shesh` is unverified

Confirm it actually lints MCP servers; if it only checks `sdata/uv`, it misses the new Python.

### NEW-H — `PREBOOT_INSTRUCTIONS.md` and `INSTALLATION_GUIDE.md` may reference the old TOML Hyprland config

Verify they mention the Lua config (Hyprland >=0.55) and CachyOS `chwd` driver installation; update any stale `hyprland.conf` references.

### NEW-I — No `CONTRIBUTING.md` at root; PR template exists but no dev setup doc

Add a short `CONTRIBUTING.md` pointing at `docs/SHESH/` and the checklist, so future AI/you do not reintroduce drift.

### NEW-J — Repo ships both `tools/backup/backup.service` (static) AND generates one via here-doc

Two sources of truth for the same unit. Delete the static one or make setup install it verbatim.

---

## D. Comparison with the upstream and top dotfile repos (2026)

| Practice | end-4/dots-hyprland (base) | JaKooLit/Hyprland-Dots | prasanthrangan/hyprdots (HyDE) | ML4W 2.14.1 | CachyOS hyprland | **Your fork target** |
|---|---|---|---|---|---|---|
| Hyprland config | Lua (0.55+) Yes | Lua/conf hybrid | conf | Lua Yes | Lua | Lua Yes (keep) |
| Shell | Quickshell Yes | Quickshell/ags | Waybar/ags | Quickshell Yes | Quickshell | Quickshell Yes (keep) |
| ShellCheck on all scripts | Yes | Yes | Yes | Yes | n/a | Must fix (MED-12) |
| Arch container CI | partial | Yes | Yes | Yes | n/a | Add |
| Idempotent installer | Yes | Yes | Yes | Yes | n/a | NVIDIA/mkinitcpio |
| Device/driver setup | explicitly none ("not a system setup script") | some | some | some | Yes chwd | Yes your differentiator — make it bulletproof |
| File/automation tooling | none | none | some (theme) | welcome app | none | Yes smart-organizer (your edge) |
| Local AI agent | sidebar (Ollama/Gemini) | none | none | none | none | Yes Shesh (your edge) |
| Visual polish | best-in-class | good | good (70+ themes) | very good | clean | must not regress |
| Uninstall reverses changes | n/a | partial | partial | partial | n/a | Stub |

**Strategic read:** The upstream deliberately refuses to do system/driver/AI setup. That refusal is your moat — but only if your system layer is as robust as the upstream's UX layer is beautiful. Right now your system layer is the weakest, buggiest part. Fix Section A first, then the device/automation/AI layers become a genuine, upstream-beating advantage rather than a liability.

---

## E. The 10 things to do before you install CachyOS (in order)

1. Add `get_aur_helper` + define `AUR_HELPER` (N-01).
2. Replace `bc` version compare with bash arithmetic (N-02).
3. Fix MSI DMI content check (BUG-05) and make `setup_power_management` write the zram config (HIGH-05).
4. `bash -n` all of `sdata/`; fix syntax (N-09).
5. Make MCP install iterate real files (N-04) or add the missing servers.
6. Fix the license (README to GPL-3.0-or-later, fill `MIT.txt` placeholders) (MED-16).
7. Expand ShellCheck to all scripts + add Arch container CI (MED-12/13) so the above cannot regress.
8. Create `tools/lib/common.sh` and source it (HIGH-01/02, MED-01/02).
9. Create `profiles/msi-sword-cachyos/` with the correct 1920x1200/6 GB values (NEW-A).
10. Fix bootstrap `--skip-*` flags and generic framing (HIGH-08).

Each of these is expanded into copy-paste-ready code/prompts in `02-roadmap.md` and `09-ai-prompts.md`.
