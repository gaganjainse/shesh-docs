---
name: coding
description: Write, test, and refactor code safely. Always read before editing, run tests, and never push without review.
---

# Coding Skill

Code is changed with care, not conviction. This skill sets the house discipline for writing,
testing, and refactoring: understand first, move in small steps, and let the tests and the
reviewer be the gate.

## The rules

1. **Understand first.** Read the relevant files. Use `git_status` and `git_log` to see
   context.
2. **Plan the diff.** State the files and approach before editing for non-trivial changes.
3. **Match the house style.** Rust: `cargo fmt` and `clippy`. Python: `ruff`. Lua: `stylua`.
   QML: `qmlformat`. Bash: `shellcheck` and `shfmt`.
4. **Small steps.** One logical change per commit; Conventional Commit messages
   (`feat:`, `fix:`, `docs:`, `chore(ci):`, `refactor:`).
5. **Test.** Run the component's `make test`, `pytest`, or `cargo test`. Add a test for the
   fix.
6. **Never** force-push `main`, never `rm -rf`, never `sudo` unless explicitly asked.
7. For new dependencies, prefer the standard library; justify each new dependency and verify
   its license is GPL-3-compatible.

Model routing: implementation work goes to a code model (`qwen2.5-coder:3b`); review and
planning go to the primary model.

> **Warning —** A green test suite is not permission to push. This skill says "never push
> without review" — the reviewer, not the automated gate, is the final authority on `main`.
