---
name: dev-workflow
description: "Everyday developer-routine skills — daily kick-off, sync, catch-up, and the small rituals around starting and ending a work session."
type: domain
building_blocks:
  contracts: "TBD — shared conventions for the routine skills."
  skills: "Invocable routine skills (e.g. good-morning)."
  agents: "TBD."
  prompts: "TBD."
  tools: "TBD."
  docs: "TBD."
stage: alpha
---

# Dev Workflow

Skills for the daily rhythm of working in a repo — syncing, catching up on what
changed while you were away, and getting set to build. Generic by design: they
detect the repo's conventions rather than hard-coding any one project's layout.

## Building Blocks

| Folder       | Purpose                                                       |
| ------------ | ------------------------------------------------------------- |
| `skills/`    | Invocable routine skills (e.g. `good-morning`).               |
| `contracts/` | Shared conventions (add when ≥2 skills share rules).          |
| `agents/`    | Autonomous routine agents.                                    |
| `prompts/`   | Reusable prompt fragments.                                    |
| `tools/`     | `uv`-runnable helpers.                                        |

## Skills

| Skill          | Purpose                                                                       |
| -------------- | ----------------------------------------------------------------------------- |
| `good-morning` | Morning kick-off: fetch/pull, catch you up on what changed since you were last active, surface merged/open PRs, optional build, and a dev joke of the day. |
