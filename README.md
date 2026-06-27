# ai-assets

Personal collection of AI agent skills, domains, agents, and shared resources —
authored to be **Skaile-conform** so they can be published to
[skaile.store](https://skaile.store).

Pure content: SKILL.md prompts, manifests, and a couple of `uv`-runnable
scaffolding scripts. No app code, no secrets.

## Quick start

```bash
# Scaffold a new domain (a folder that groups related skills)
uv run scripts/scaffold_domain.py my-domain "One sentence on what it's for"

# Scaffold a new skill inside an existing domain
uv run scripts/scaffold_skill.py my-domain my-skill "When the agent should use this"
```

Then fill in the generated `SKILL.md`. See **CLAUDE.md** for the full authoring
and publishing rules.

## Layout

```
skaile.yaml                       ← publication manifest (publisher: plumpudding)
.skaile-source.yaml               ← source sidecar (default ref + sync trigger)
scripts/                          ← uv-runnable scaffolders
<domain>/
├── DOMAIN.md                     ← domain manifest (required per domain)
├── CHANGELOG.md
├── <domain>.bundle.yaml          ← optional: groups the domain's skills
└── skills/<skill-name>/SKILL.md  ← the skill (required); + optional CLI.md, references/, scripts/
```

`general/` ships as a starter domain with `example-skill/` as a working
template — read it, then delete it once you have real skills.

## Publishing to skaile.store

Assets are published with the `skaile-store` CLI (register this repo as a
source, sync, then publish). Identity is `<kind>:<name>@plumpudding#<version>`;
version comes from `git describe --tags`, so cut a tag to release. Full
step-by-step in **CLAUDE.md → Publishing**.
