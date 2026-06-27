# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer>=0.12.0",
#     "rich>=13.0.0",
# ]
# ///
"""Scaffold a new asset domain: DOMAIN.md, CHANGELOG.md, and the standard folders.

Run from the repo root:

    uv run scripts/scaffold_domain.py <domain-name> "<one-sentence purpose>"
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.tree import Tree

app = typer.Typer(
    help="Scaffold a new asset domain (DOMAIN.md + standard folders).",
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
    domain_name: str = typer.Argument(..., help="Domain name in kebab-case (e.g. knowledge-research)"),
    description: str = typer.Argument(..., help="One-sentence purpose of this domain"),
    base_path: Path = typer.Option(Path("."), "--base-path", "-b", help="Repo root (parent of the new domain)"),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing domain (only after user confirmation)"),
) -> None:
    sanitized = domain_name.replace("-", "").replace("_", "")
    if not sanitized.isalnum() or domain_name != domain_name.lower():
        typer.secho(f"Error: domain name must be lowercase kebab-case (got: {domain_name!r})", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)

    domain_path = base_path.resolve() / domain_name
    if domain_path.exists() and not force:
        typer.secho(
            f"Error: domain '{domain_name}' already exists at {domain_path}\n"
            "Use --force to overwrite (only after explicit user confirmation).",
            err=True, fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    title = to_title(domain_name)

    domain_md = f"""\
---
name: {domain_name}
description: "{description}"
type: domain
building_blocks:
  contracts: "Shared conventions all domain skills read before operating."
  skills: "Invocable agent skills — user-facing, trigger-driven workflows."
  agents: "Autonomous / subagent-dispatched agents."
  prompts: "Reusable prompt fragments — personas, instruction blocks."
  tools: "uv-runnable CLI scripts skills invoke as shell commands."
  docs: "Domain-level architecture notes and reference material."
stage: alpha
---

# {title}

{description}

<!-- TODO: 2-3 sentences on scope, what problems it solves, and who uses it. -->

## Building Blocks

| Folder       | Purpose                                                          |
| ------------ | ---------------------------------------------------------------- |
| `skills/`    | Invocable skills — user-facing, trigger-driven agent workflows.  |
| `contracts/` | Shared contracts read by all domain skills.                      |
| `agents/`    | Autonomous / subagent-dispatched agents.                         |
| `prompts/`   | Reusable prompt fragments.                                       |
| `tools/`     | `uv`-runnable CLI tools.                                         |
"""

    changelog_md = f"# Changelog — {domain_name}\n\n## [Unreleased]\n"
    skills_readme = (
        f"# {title} — Skills\n\nInvocable agent skills for the `{domain_name}` domain. "
        "Each skill lives in its own subdirectory with a `SKILL.md`.\n\n"
        f"Scaffold one with:\n\n```bash\nuv run scripts/scaffold_skill.py {domain_name} <skill-name> \"<description>\"\n```\n"
    )

    write_file(domain_path / "DOMAIN.md", domain_md)
    write_file(domain_path / "CHANGELOG.md", changelog_md)
    write_file(domain_path / "skills" / "README.md", skills_readme)

    console.print(f"\n[bold green]✓ Domain scaffolded:[/bold green] [cyan]{domain_name}[/cyan]")
    console.print(f"  Path: {domain_path}\n")
    tree = Tree(f"[bold]{domain_name}/[/bold]")
    tree.add("[yellow]DOMAIN.md[/yellow]  ← domain manifest")
    tree.add("CHANGELOG.md")
    tree.add("skills/  ← scaffold skills here")
    console.print(tree)

    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  1. Fill in the TODO in [cyan]{domain_name}/DOMAIN.md[/cyan]")
    console.print(f"  2. Scaffold a skill: [bold]uv run scripts/scaffold_skill.py {domain_name} <name> \"<desc>\"[/bold]")
    console.print(f"  3. (Optional) add a [cyan]{domain_name}/{domain_name}.bundle.yaml[/cyan] to group the skills")


if __name__ == "__main__":
    app()
