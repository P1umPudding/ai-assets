---
name: example-skill
description: "Template skill that demonstrates the canonical SKILL.md shape — frontmatter, ROLE/READS/WRITES/MUST/NEVER body, and progressive disclosure. Use as the starting point when authoring a real skill; delete once you have your own."
license: MIT
metadata:
  author: plumpudding
  stage: alpha
  source: ORIGINAL
  tags: [example, template, scaffold]
  keywords: [example, template, starter, how-to-author]
---

# Example Skill

This file is a living template. It shows the structure every skill in this repo
follows. Replace the body with your real instructions, or scaffold a fresh skill
with `uv run scripts/scaffold_skill.py <domain> <name> "<description>"`.

## Role

You are an agent performing <the skill's job>. State the role in one or two
sentences — what outcome the user gets when this skill triggers.

## Reads

- `<path/or/input>` — what you read and why. Keep this in sync with the real
  `metadata.reads_from` if you declare it.

## Writes

- `<path/or/output>` — what you produce. Mirror in `metadata.writes_to`.

## Must

- Use imperative mood and concrete steps.
- Keep this body under ~500 lines; move long reference material to `references/`
  and load it only when needed (progressive disclosure).

## Never

- Never invent file paths, function names, or API endpoints. If unsure, verify
  first.
- Never overwrite the user's files without explicit confirmation.

## Notes

Optional supporting folders (all optional): `CLI.md` (slash-command usage),
`references/` (loaded on demand), `examples/`, `scripts/` (uv-runnable),
`validator.py` (output validation).
