# shesh-docs

The documentation source for the Shesh fleet, published as an mdBook.

- **Licence:** GPL-3.0-or-later
- **Owner:** Gagan Jain ([@gaganjainse](https://github.com/gaganjainse))
- **Style:** [Google developer documentation style guide](https://developers.google.com/style),
  with project rules in [STYLEGUIDE.md](STYLEGUIDE.md)
- **Structure:** [Diátaxis](https://diataxis.fr/)

## Scope

This repository owns the conceptual material, operating procedures, reference
tables, and governance records for the whole fleet. It is the canonical location
for everything except component build instructions, which stay in each
component's own README and are linked from here.

## Build

```bash
mdbook serve --open
```

The book is written to `book/`. The build requires
[mdBook](https://rust-lang.github.io/mdBook/) and Python 3.11 or later for the
front-matter preprocessor.

## Validate

```bash
python3 tools/check_docs.py
```

The checker enforces the style guide mechanically: required front matter,
navigation integrity, link resolution, heading rules, and the prose
prohibitions. It exits non-zero on any error, and continuous integration runs it
on every change.

## Regenerate derived pages

Pages that project a machine-readable source are generated, not written. Each
carries a comment naming its generator.

```bash
python3 tools/generate_components.py ../shesh-ecosystem/manifests/components.toml
```

Continuous integration regenerates these pages and fails if the committed output
differs, so the manifest and the catalogue cannot drift apart.

## Organisation

| Part | Contents | Diátaxis type |
|---|---|---|
| `src/start/` | Orientation and installation | Tutorial |
| `src/explanation/` | Design and reasoning | Explanation |
| `src/how-to/` | Task-oriented procedures | How-to |
| `src/reference/` | Schemas, catalogues, checklists | Reference |
| `src/development/` | Contributor tooling | Mixed |
| `src/governance/` | Policies and decision records | Reference |
| `src/history/` | Preserved records, not maintained | Historical |

Every page declares its type, audience, status, and a `verified` date in front
matter. Pages under `src/history/` carry a banner and are exempt from the prose
rules, because they are preserved verbatim as a record.

## Contributing

1. Read [STYLEGUIDE.md](STYLEGUIDE.md).
2. Make the change, keeping each page to a single Diátaxis type.
3. Update the `verified` date only if you checked the claims against the code.
4. Run `python3 tools/check_docs.py` and `mdbook build`.

A page whose claims can no longer be verified moves to `src/history/` with a
banner rather than being left in place looking current.

## Security

Vulnerability reporting and the security posture are documented in the
[ecosystem security policy](https://github.com/gaganjainse/shesh-ecosystem/blob/main/SECURITY.md).

## Licence

GPL-3.0-or-later — see [LICENSE](LICENSE).
