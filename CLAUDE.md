# CLAUDE.md

Guidance for Claude Code (and any agent) working in this repo. Read this fully
before creating or wiring up an asset — the rules here are what make assets
**Skaile-conform** and publishable to skaile.store.

## What this is

A personal, public collection of **AI assets** — skills, domains, agents, and
shared resources — authored to the Skaile / agentskills.io conventions so they
can be published to [skaile.store](https://skaile.store) under the publisher
**`plumpudding`**.

Pure content. No application code, no backend, no secrets. The only executable
bits are the `uv`-runnable scaffolders in `scripts/`.

## Asset kinds

| Kind       | Lives at                                  | Identity                          |
| ---------- | ----------------------------------------- | --------------------------------- |
| `skill`    | `<domain>/skills/<name>/SKILL.md`         | `skill:<name>@plumpudding`        |
| `bundle`   | `<domain>/<domain>.bundle.yaml`           | `bundle:<name>@plumpudding`       |
| `agent`    | `<domain>/agents/<name>/agent.yaml`       | `agent:<name>@plumpudding`        |
| `contract` | `<domain>/contracts/<name>/CONTRACT.md`   | `contract:<name>@plumpudding`     |

Everything ships from a **domain** folder. Even a single skill needs a domain
to live in. Group related skills into a domain, and spin up a new one when a
cluster grows (scaffold with `scripts/scaffold_domain.py`).

## Golden rules

1. **`name:` in frontmatter MUST equal the parent directory name.** kebab-case,
   1–64 chars, lowercase. This is enforced on publish.
2. **`description:` is the routing signal.** Write it third-person and specific
   about *when to use this* — it's how agents and the store decide relevance.
   1–1024 chars.
3. **Never invent paths, function names, or API endpoints** in a prompt body.
   If `metadata.reads_from` / `writes_to` are declared, they must match what the
   body actually references.
4. **Keep SKILL.md bodies under ~500 lines.** Move long reference material into
   `references/` and load it on demand (progressive disclosure).
5. **One publisher: `plumpudding`** (set in `skaile.yaml`). Don't change it —
   it's baked into every asset's canonical identity.
6. Use `@postxl/ui-components`-style discipline only applies to app repos — N/A
   here. This repo is content, not UI.

## Creating a new asset

### Always prefer the scaffolders

```bash
# New domain (DOMAIN.md + CHANGELOG.md + skills/)
uv run scripts/scaffold_domain.py <domain> "<one-sentence purpose>"

# New skill inside an existing domain (SKILL.md; add --cli for CLI.md)
uv run scripts/scaffold_skill.py <domain> <skill-name> "<trigger description>" [--cli]
```

The scaffolders emit the exact frontmatter and folder layout this repo expects.
After scaffolding, fill in the body and the TODOs.

### Skill anatomy

```
<domain>/skills/<skill-name>/
├── SKILL.md          ← REQUIRED. frontmatter + agent-prompt body
├── CLI.md            ← optional. slash-command / CLI usage
├── references/       ← optional. loaded on demand
├── examples/         ← optional. worked examples
├── scripts/          ← optional. uv-runnable single-file tools
└── validator.py      ← optional. output validation
```

**SKILL.md frontmatter** (minimum = `name`, `description`, `metadata.stage`):

```yaml
---
name: my-skill                 # MUST match the directory
description: "Third-person, trigger-focused. When should an agent use this?"
license: MIT                   # optional
metadata:
  author: plumpudding
  stage: alpha                 # alpha | beta | stable
  source: ORIGINAL             # ORIGINAL | MERGED | MIGRATED
  tags: [search, pdf]
  keywords: [summarize, extract]   # for store/CLI discovery
  version: 1.2.0               # OPTIONAL — overrides the repo-wide git-tag version for THIS asset
  requires: []                 # other skill:/contract: deps this skill reads
  reads_from: []               # file paths the body reads (keep accurate)
  writes_to: []                # file paths the body writes (keep accurate)
---
```

Body convention: imperative mood; lead with the agent's **role**, then its
procedure and the hard rules (a **Role / Reads / Writes / Must / Never** shape
works well for tool-like skills; a **principles / procedure / hard-rules** shape
fits procedural ones). See `planning/skills/write-spec/SKILL.md` and
`dev-workflow/skills/good-morning/SKILL.md` for worked examples.

### Domain anatomy

```
<domain>/
├── DOMAIN.md                  ← REQUIRED. frontmatter below
├── CHANGELOG.md               ← "# Changelog — <domain>" + "## [Unreleased]"
├── <domain>.bundle.yaml       ← optional. groups skills for one-shot install
├── skills/                    ← the skills
├── contracts/                 ← optional. shared rules (do_not_invoke: true)
└── agents/                    ← optional. agent.yaml + persona/rules
```

**DOMAIN.md frontmatter** (required: `name`, `description`, `type: domain`,
`building_blocks`, `stage`):

```yaml
---
name: my-domain
description: "One sentence on the domain's purpose."
type: domain
building_blocks:
  contracts: "…"   # use "TBD" where empty
  skills: "…"
  agents: "TBD"
  prompts: "TBD"
  tools: "TBD"
  docs: "TBD"
stage: alpha
---
```

### Bundle (optional but recommended per domain)

A bundle groups a domain's assets so a consumer installs them in one go:

```yaml
name: my-domain                # MUST match the domain directory
description: "What this bundle gives you."
dependencies:
  - skill:my-skill
  - skill:other-skill
  - contract:my-domain-contract   # if present
  - agent:my-agent                # if present
```

### Contracts (only when ≥2 skills share rules)

A contract is shared, non-invocable context. `CONTRACT.md` frontmatter must set
`metadata.do_not_invoke: true`. Skills declare it under `metadata.requires`.

### Agents (advanced)

`<domain>/agents/<name>/agent.yaml` (gitagent `spec_version: '0.1.0'`), with
optional `SOUL.md` (persona) and `RULES.md` (ruleset). Shared personas/rules can
live in a top-level `_agent-parts/{personas,rules}/` and be referenced from
`agent.yaml` via relative paths. Only add this when you actually ship an agent.

## Wiring an asset up

After creating an asset, decide whether to **register** or **auto-discover** it:

- **Auto-discovery (default, zero config):** a skill at
  `<domain>/skills/<name>/SKILL.md` and a `<domain>/<domain>.bundle.yaml` are
  found automatically by the agentskills.io filename convention. For most
  skills, you do nothing else.
- **Lock identity (optional):** add the asset to `skaile.yaml` under `assets:`
  to pin its canonical identity even if the directory layout later changes:

  ```yaml
  - { kind: skill,  name: my-skill, root: my-domain/skills/my-skill }
  - { kind: bundle, name: my-domain, root: my-domain, files: [my-domain.bundle.yaml] }
  ```

- If the skill belongs in a domain bundle, add it to that bundle's
  `dependencies:`.
- Add a one-line entry to the domain's `CHANGELOG.md` under `## [Unreleased]`.

## Versioning

Repo-wide version comes from `git describe --tags`. To release a new version of
**every** asset, cut a tag:

```bash
git tag v0.2.0
git push --tags        # only when the user says to push
```

To version a **single** asset independently, set `metadata.version:` in its
SKILL.md — that overrides the repo-wide tag for that asset only.

## Publishing to skaile.store

Published via the **`skaile-store`** CLI (the store doesn't store bytes — it
records a pointer to a git commit + per-file hashes, then serves them from
GitHub). Typical flow:

```bash
skaile-store login                          # Keycloak device flow → ~/.skaile/auth.json
skaile-store whoami                         # verify identity + roles

# First time: register THIS repo as a source
skaile-store sources add https://github.com/P1umPudding/ai-assets --ref main
skaile-store sources list                   # note the <sourceId>

# Index the repo's assets at the current ref
skaile-store sources sync <sourceId>        # async job; discovers SKILL.md / bundles

# Review what was discovered, then publish
skaile-store candidates <sourceId>
skaile-store publish preview <assetId>      # dry run
skaile-store publish <assetId> --ref main   # or: publish --all <sourceId> --ref main
```

All commands take `--json` for scripting. To retract: `skaile-store unpublish
<assetId>`. There is **no CI auto-publish** in this repo — publishing is a
deliberate manual step the maintainer runs.

## Before you call an asset done — checklist

- [ ] `name:` matches the directory; kebab-case.
- [ ] `description:` is specific and trigger-focused.
- [ ] `metadata.stage` set (alpha/beta/stable).
- [ ] `reads_from` / `writes_to` (if declared) match the body; no invented paths.
- [ ] SKILL.md body under ~500 lines; references moved to `references/`.
- [ ] Domain's `DOMAIN.md` and `CHANGELOG.md` updated if you added/removed a skill.
- [ ] Added to bundle `dependencies:` and/or `skaile.yaml` `assets:` if you want
      it bundled / identity-locked.
- [ ] No duplicate skill covering the same use case in the same domain.

## Git

Commit locally freely. **Only push when the user explicitly says "push"** in
that request — approval doesn't carry to later changes. Do not add a
`Co-Authored-By` / AI co-author trailer to commits.

## Reference

The conventions here mirror Skaile's canonical `ai-assets` repo. If something is
ambiguous, the source of truth is `skaile.yaml` (publisher + identity) and the
agentskills.io filename convention (`<domain>/skills/<name>/SKILL.md`).
