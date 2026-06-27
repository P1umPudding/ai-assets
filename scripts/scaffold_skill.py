# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer>=0.12.0",
#     "rich>=13.0.0",
# ]
# ///
"""Scaffold a new skill at <domain>/skills/<name>/ with a canonical SKILL.md.

Run from the repo root:

    uv run scripts/scaffold_skill.py <domain> <skill-name> "<description>"

The domain must already exist (scaffold it with scaffold_domain.py first).
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.tree import Tree

app = typer.Typer(
    help="Scaffold a new skill (SKILL.md + optional supporting folders).",
    add_completion=False,
)
console = Console()


def to_title(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


@app.command()
def main(
    domain: str = typer.Argument(..., help="Existing domain folder (e.g. general)"),
    skill_name: str = typer.Argument(..., help="Skill name in kebab-case (e.g. summarize-pdf)"),
    description: str = typer.Argument(..., help="Third-person trigger description (used for routing)"),
    author: str = typer.Option("plumpudding", "--author", help="Author handle for frontmatter"),
    cli: bool = typer.Option(False, "--cli", help="Also scaffold a CLI.md"),
    base_path: Path = typer.Option(Path("."), "--base-path", "-b", help="Repo root"),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing skill (only after user confirmation)"),
) -> None:
    if skill_name != skill_name.lower() or not skill_name.replace("-", "").isalnum():
        typer.secho(f"Error: skill name must be lowercase kebab-case (got: {skill_name!r})", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)

    root = base_path.resolve()
    domain_path = root / domain
    if not (domain_path / "DOMAIN.md").exists():
        typer.secho(
            f"Error: domain '{domain}' not found at {domain_path} (no DOMAIN.md).\n"
            f"Create it first:  uv run scripts/scaffold_domain.py {domain} \"<purpose>\"",
            err=True, fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    skill_path = domain_path / "skills" / skill_name
    if skill_path.exists() and not force:
        typer.secho(
            f"Error: skill '{skill_name}' already exists at {skill_path}\n"
            "Use --force to overwrite (only after explicit user confirmation).",
            err=True, fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    title = to_title(skill_name)

    skill_md = f"""\
---
name: {skill_name}
description: "{description}"
license: MIT
metadata:
  author: {author}
  stage: alpha
  source: ORIGINAL
  tags: []
  keywords: []
---

# {title}

<!-- One or two sentences on what the user gets when this skill triggers. -->

## Role

You are an agent performing <the skill's job>.

## Reads

- `<path/or/input>` — what you read and why.

## Writes

- `<path/or/output>` — what you produce.

## Must

- Use imperative mood and concrete steps.
- Keep this body under ~500 lines; move long reference material to `references/`.

## Never

- Never invent file paths, function names, or API endpoints — verify first.
- Never overwrite the user's files without explicit confirmation.
"""

    write_file(skill_path / "SKILL.md", skill_md)

    if cli:
        cli_md = f"""\
# {title} — CLI Usage

## Slash Command

```
/{skill_name}
```

## Arguments

- `--arg <value>`: description.

## Examples

```
/{skill_name} --arg value
```
"""
        write_file(skill_path / "CLI.md", cli_md)

    console.print(f"\n[bold green]✓ Skill scaffolded:[/bold green] [cyan]{domain}/skills/{skill_name}[/cyan]\n")
    tree = Tree(f"[bold]{skill_name}/[/bold]")
    tree.add("[yellow]SKILL.md[/yellow]  ← fill in the body")
    if cli:
        tree.add("CLI.md")
    console.print(tree)

    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  1. Write the body of [cyan]{domain}/skills/{skill_name}/SKILL.md[/cyan]")
    console.print(f"  2. (Optional) lock its identity by adding it to [cyan]skaile.yaml[/cyan] under `assets:`")
    console.print(f"  3. (Optional) add it to [cyan]{domain}/{domain}.bundle.yaml[/cyan] dependencies")


if __name__ == "__main__":
    app()
