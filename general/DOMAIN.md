---
name: general
description: "General-purpose personal skills and assets that don't yet warrant their own domain."
type: domain
building_blocks:
  contracts: "TBD — shared conventions all skills in this domain read before operating."
  skills: "Invocable agent skills — user-facing, trigger-driven workflows."
  agents: "TBD — autonomous / subagent-dispatched agents."
  prompts: "TBD — reusable prompt fragments."
  tools: "TBD — uv-runnable CLI scripts skills invoke as shell commands."
  docs: "TBD — domain-level architecture notes and reference material."
stage: alpha
---

# General

General-purpose personal skills and assets. This is the catch-all domain for
things you build before they grow into a focused domain of their own. When a
cluster of related skills emerges here, promote it: scaffold a dedicated domain
with `scripts/scaffold_domain.py` and move the skills over.

## Building Blocks

| Folder      | Purpose                                                              |
| ----------- | ------------------------------------------------------------------- |
| `skills/`   | Invocable skills — user-facing, trigger-driven agent workflows.     |
| `contracts/`| Shared contracts read by all domain skills (add when ≥2 skills share rules). |
| `agents/`   | Autonomous / subagent-dispatched agents.                            |
| `prompts/`  | Reusable prompt fragments — personas, instruction blocks.           |
| `tools/`    | `uv`-runnable CLI tools skills invoke as shell commands.            |

`example-skill/` is a working template — read it to see the exact SKILL.md
shape, then delete it once you have real skills.
