---
name: docs-writer
description: Write and convert documentation and notes in Markdown. Keep them organized, linked, and dated.
---

# Docs and Notes Skill

Notes are only useful if you can find them again. This skill keeps the fleet's writing in one
format, one place, and one index — Markdown everywhere, linked by wikilinks, dated by day.

## The habits

- **Capture first:** `append_note("inbox", ...)` for quick thoughts.
- **Structure:** notes live under `~/Notes/{Daily,Tech,Ideas,Meetings,SHESH}`. Daily notes are
  named `YYYY-MM-DD.md`.
- **Markdown everywhere:** use headings, tables for comparisons, and language-tagged code
  fences.
- **Convert docs:** `convert_to_markdown(path)` for PDF, DOCX, and XLSX (via pandoc).
- **Link notes:** use relative `[[wikilinks]]`; tag with `#tag` at the bottom.
- **Keep an index:** maintain `~/Notes/README.md` with links to active notes.
- When answering from notes, run `search_notes` first and cite the file.
- Never put secrets in notes. Use `~/Vaults` (KeePassXC) instead.

> **Tip —** A daily note named by ISO date sorts itself and survives years of accumulation.
> Pair it with the `~/Notes/README.md` index so the whole tree stays navigable.
