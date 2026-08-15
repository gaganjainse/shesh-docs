#!/usr/bin/env python3
"""mdBook preprocessor: consume YAML front matter and render page metadata.

Front matter is authoring metadata. Without this preprocessor mdBook renders it
as body text. This strips the block, emits a compact metadata line, and prepends
a banner to any page marked `status: historical`.

Registered in book.toml as [preprocessor.frontmatter].
"""
import json
import re
import sys

FM = re.compile(r'\A---\r?\n(.*?)\r?\n---\r?\n', re.S)

TYPE_LABEL = {
    "tutorial": "Tutorial",
    "how-to": "How-to guide",
    "reference": "Reference",
    "explanation": "Explanation",
}

HISTORICAL_BANNER = (
    "> **Historical record.** This page describes the state of the system when it "
    "was written and is retained for provenance. It is not maintained and may "
    "contradict current behaviour. Do not follow its instructions.\n\n"
)


def parse_front_matter(text):
    """Return (metadata dict, remaining body). Tolerates absent front matter."""
    m = FM.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).split("\n"):
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, text[m.end():]


def render(meta, body):
    if not meta:
        return body

    if meta.get("status") == "historical" and "Historical record" not in body[:400]:
        body = HISTORICAL_BANNER + body.lstrip()

    bits = []
    label = TYPE_LABEL.get(meta.get("type", ""))
    if label:
        bits.append(label)
    if meta.get("audience"):
        bits.append(f"Audience: {meta['audience']}")
    if meta.get("verified"):
        bits.append(f"Verified: {meta['verified']}")
    if not bits:
        return body

    meta_line = f'<div class="page-meta">{" · ".join(bits)}</div>\n\n'

    # Place the metadata line directly beneath the H1 so the title stays first.
    m = re.search(r'^(#\s+.+?)$', body, re.M)
    if m:
        return body[:m.end()] + "\n\n" + meta_line + body[m.end():].lstrip("\n")
    return meta_line + body


def walk(section):
    chapter = section.get("Chapter")
    if not chapter:
        return
    if chapter.get("content"):
        meta, body = parse_front_matter(chapter["content"])
        chapter["content"] = render(meta, body)
    for sub in chapter.get("sub_items", []):
        walk(sub)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        sys.exit(0)  # supports every renderer
    context, book = json.load(sys.stdin)
    del context
    for section in book.get("sections", []):
        walk(section)
    json.dump(book, sys.stdout)


if __name__ == "__main__":
    main()
