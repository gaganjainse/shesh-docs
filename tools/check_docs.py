#!/usr/bin/env python3
"""Validate the documentation against the style guide.

Checks structure (front matter, navigation, links) and the prose prohibitions
that reviewers cannot reliably catch by eye. Exits non-zero on any error.

Usage:
    python3 tools/check_docs.py [--src src]
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict

REQUIRED_FIELDS = ("title", "type", "summary", "audience", "status", "verified")
VALID_TYPES = {"tutorial", "how-to", "reference", "explanation"}
VALID_STATUS = {"current", "historical"}
VALID_AUDIENCE = {"operator", "contributor", "maintainer"}

# Prose rules applied to current pages only. Historical pages are preserved
# verbatim as a record and are exempt.
PROSE_RULES = [
    (r"\b(?:steal|stole|stolen|stealing)\b",
     "acquisition metaphor; write 'adapted from' or 'derived from'"),
    (r"(?<![\w`/-])(?:we|our|us)(?![\w-])",
     "first person plural; attribute to the system or the artefact"),
    (r"(?<![\w`/-])(?:I|my)(?![\w-])",
     "first person singular"),
    (r"\b(?:foolproof|proper system|no issues|messed up)\b",
     "unverifiable self-assessment; describe the property instead"),
    (r"^> *\"", "quoted user request; state the requirement instead"),
    (r"img\.shields\.io",
     "volatile badge; counts go stale and nothing detects it"),
    (r"/home/[a-z]", "personal filesystem path; use ~/ or a placeholder"),
    (r"\b(?:TODO|FIXME|TBD|XXX)\b(?!\.md)(?![\w-])",
     "unfinished marker; documentation must not ship placeholders"),
    (r"\b\d+ tests\b", "volatile count; give the command that reports it"),
    (r"\b(?:simply|just|obviously|seamless|robust)\b", "filler intensifier"),
]

FENCE = re.compile(r"```.*?```", re.S)
INLINE = re.compile(r"`[^`\n]*`")
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")


def strip_code(text: str) -> str:
    """Blank out code so prose rules never fire on commands or identifiers."""
    text = FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return INLINE.sub("", text)


def parse_front_matter(text: str):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, text[m.end():]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="src")
    args = ap.parse_args()
    src = args.src

    errors: list[str] = []
    warnings: list[str] = []

    chapters = sorted(
        os.path.relpath(os.path.join(r, f), src)
        for r, _d, fs in os.walk(src)
        for f in fs
        if f.endswith(".md") and f != "SUMMARY.md"
    )
    if not chapters:
        print(f"no chapters found under {src}", file=sys.stderr)
        return 1

    # ---- navigation ----
    summary_path = os.path.join(src, "SUMMARY.md")
    summary = open(summary_path, encoding="utf-8").read()
    listed = [t.split("#")[0] for _l, t in LINK.findall(summary) if t.endswith(".md")]

    for orphan in sorted(set(chapters) - set(listed)):
        errors.append(f"{orphan}: not listed in SUMMARY.md")
    for missing in sorted(set(listed) - set(chapters)):
        errors.append(f"SUMMARY.md: entry has no file: {missing}")
    dupes = {p for p in listed if listed.count(p) > 1}
    for d in sorted(dupes):
        errors.append(f"SUMMARY.md: listed more than once: {d}")

    # ---- per chapter ----
    titles: dict[str, list[str]] = defaultdict(list)
    for rel in chapters:
        path = os.path.join(src, rel)
        raw = open(path, encoding="utf-8").read()
        meta, body = parse_front_matter(raw)

        if meta is None:
            errors.append(f"{rel}: missing YAML front matter")
            continue

        for field in REQUIRED_FIELDS:
            if not meta.get(field):
                errors.append(f"{rel}: front matter missing '{field}'")

        if meta.get("type") and meta["type"] not in VALID_TYPES:
            errors.append(f"{rel}: type '{meta['type']}' not in {sorted(VALID_TYPES)}")
        if meta.get("status") and meta["status"] not in VALID_STATUS:
            errors.append(f"{rel}: status '{meta['status']}' not in {sorted(VALID_STATUS)}")
        if meta.get("audience") and meta["audience"] not in VALID_AUDIENCE:
            errors.append(f"{rel}: audience '{meta['audience']}' not in {sorted(VALID_AUDIENCE)}")
        if meta.get("verified") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["verified"]):
            errors.append(f"{rel}: verified must be ISO 8601 (YYYY-MM-DD)")

        if meta.get("title"):
            titles[meta["title"]].append(rel)

        # exactly one H1, matching the front-matter title (ignore code fences)
        nocode = strip_code(body)
        h1s = re.findall(r"^# (.+)$", nocode, re.M)
        if len(h1s) != 1:
            errors.append(f"{rel}: expected exactly one H1, found {len(h1s)}")
        elif meta.get("title") and h1s[0].strip() != meta["title"]:
            errors.append(f"{rel}: H1 '{h1s[0].strip()}' does not match title '{meta['title']}'")

        # heading hygiene
        for level, text in re.findall(r"^(#{2,6}) (.+)$", nocode, re.M):
            if len(level) > 4:
                warnings.append(f"{rel}: heading deeper than H4: {text}")
            if text.rstrip().endswith(":"):
                errors.append(f"{rel}: heading ends with a colon: {text}")
            if re.match(r"^\d+[.)]", text):
                errors.append(f"{rel}: heading has a numeric prefix: {text}")

        # historical pages must carry the banner
        if meta.get("status") == "historical" and "Historical record" not in body[:600]:
            errors.append(f"{rel}: historical page missing the 'Historical record' banner")

        # generated pages must declare themselves
        if "Generated by" in body[:400] and "Do not edit" not in body[:600]:
            warnings.append(f"{rel}: generated page should say 'Do not edit by hand'")

        # prose rules: current pages only
        if meta.get("status") == "current":
            prose = strip_code(body)
            for pattern, why in PROSE_RULES:
                for m in re.finditer(pattern, prose, re.M):
                    line = prose[:m.start()].count("\n") + 1
                    errors.append(
                        f"{rel}:{line}: {why} -> {m.group(0)!r}"
                    )

        # links resolve
        for _label, target in LINK.findall(body):
            if target.startswith(("http://", "https://", "mailto:", "#", "//")):
                continue
            if not target.endswith(".md"):
                continue
            resolved = os.path.normpath(
                os.path.join(src, os.path.dirname(rel), target.split("#")[0])
            )
            if not os.path.exists(resolved):
                errors.append(f"{rel}: broken link -> {target}")

    for title, where in sorted(titles.items()):
        if len(where) > 1:
            warnings.append(f"duplicate title {title!r}: {', '.join(where)}")

    # ---- report ----
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")

    print(
        f"\n{len(chapters)} chapters checked, "
        f"{len(errors)} errors, {len(warnings)} warnings"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
