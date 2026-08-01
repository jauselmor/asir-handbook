# Apuntes CFGS ASIR — documentation project

Teaching material for two (soon three) FP modules, published as a versioned
bilingual MkDocs site.

## Python — NON-NEGOTIABLE

uv only. NEVER use pip, python -m venv, pipx, or bare `python`.

- Project dependencies: `uv add <pkg>` / `uv remove <pkg>`
- Run anything: `uv run <cmd>` — never activate a venv
- Ephemeral tools: `uvx <tool>`
- Standalone scripts: PEP 723 inline metadata + `uv run script.py`.
  Do NOT add a one-off script's dependencies to pyproject.toml.
- After changing dependencies, commit the updated `uv.lock`.

## Structure

```
docs/
├── index.{en,es}.md
├── redes/     Planificación y Administración de Redes
├── marcas/    Lenguajes de Marcas y Sistemas de Gestión de Información
└── comun/     shared material referenced by both subjects
scripts/       ingestion and maintenance helpers
```

Cross-link between subjects rather than duplicating an explanation. If a concept
is already covered in another subject's folder, link to it.

## Languages

**English is the source of truth.** Write `.en.md` first.
**Spanish is required for regulatory compliance** — it is not optional and not
a nice-to-have. Every `.en.md` must have a corresponding `.es.md`.

Spanish files carry front matter:

```yaml
---
translated_from: vlan.en.md
source_sha: a3f9c21ab412
reviewed: true
---
```

- Never edit `.es.md` content independently — retranslate from the English source.
- After translating, run `uv run scripts/check_translations.py --update-hashes`.
- Set `reviewed: true` ONLY when a human has approved it. Never set it yourself.
- `uv run scripts/check_translations.py` must pass before any commit.

### Glossary — respect exactly

| English | Español |
|---|---|
| routing | enrutamiento |
| switch | conmutador |
| trunk link | enlace troncal |
| firewall | cortafuegos |
| default gateway | puerta de enlace predeterminada |
| stylesheet | hoja de estilo |
| tag (XML/HTML) | etiqueta (never "label") |
| markup language | lenguaje de marcas |
| spreadsheet | hoja de cálculo |

Do not translate: command names, file paths, code blocks, CLI output, RFC titles.
Keep heading anchors stable so cross-links survive translation.

## Workflow

1. Ingest sources (PDF/docx/web) into `scratch/` as markdown first. `scratch/` is gitignored.
2. Write the English page, then the Spanish translation.
3. Run `uv run scripts/check_translations.py`.
4. Run `uv run mkdocs build --strict` — it fails on broken links.
5. Commit with a descriptive message.

NEVER commit directly to `main`. Work on a branch (`tema/…`, `fix/…`).
NEVER push without explicit approval.

## Versioning

`mike` publishes one version per academic year (`2025-26`, `2026-27`), aliased
to `latest`. Do not run mike locally; CI deploys on merge to `main`.
Publishing a version is a deliberate act at a course boundary, not a routine edit.

## Writing conventions

- Sentence case headings. Formal register in both languages.
- Every page opens with a one-paragraph summary of what it covers.
- Code blocks always specify a language.
- Prefer admonitions (`!!! note`, `!!! warning`) over bold-text asides.
- Diagrams as Mermaid fenced blocks, not images, so they stay diffable.
