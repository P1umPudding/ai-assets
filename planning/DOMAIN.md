---
name: planning
description: "Skills for turning a vague idea into something a fresh agent can build — specs, plans, and the interview/verify workflows around them."
type: domain
building_blocks:
  contracts: "TBD — shared spec/plan conventions all planning skills read."
  skills: "Invocable skills that interview the user and produce planning artifacts (specs, plans)."
  agents: "TBD."
  prompts: "TBD."
  tools: "TBD."
  docs: "TBD — notes on the spec format and the implement-and-verify loop."
stage: alpha
---

# Planning

Skills that turn a vague request into a precise, self-contained artifact a fresh
agent can execute. The emphasis is on **interviewing the user to find the real
goal**, locking key decisions explicitly, and writing down a verification loop so
the result can be checked against what was actually asked for.

## Building Blocks

| Folder      | Purpose                                                           |
| ----------- | ---------------------------------------------------------------- |
| `skills/`   | Invocable planning skills (e.g. `write-spec`).                   |
| `contracts/`| Shared spec/plan conventions (add when ≥2 skills share rules).   |
| `agents/`   | Autonomous planning agents.                                      |
| `prompts/`  | Reusable interview / criteria-definition prompt fragments.       |
| `tools/`    | `uv`-runnable helpers.                                           |

## Skills

| Skill        | Purpose                                                                  |
| ------------ | ------------------------------------------------------------------------ |
| `write-spec` | Interview the user, then write a self-contained spec sheet with requirements, acceptance criteria, and an embedded implement-and-verify workflow. |
