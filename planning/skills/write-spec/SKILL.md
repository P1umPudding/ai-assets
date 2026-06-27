---
name: write-spec
description: "Interview the user to uncover the real goal, then write a self-contained spec sheet for a feature/project/change — requirements, precise acceptance criteria, and an embedded implement-and-verify workflow that a fresh agent can execute end to end. Use when the user wants to specify something before building, or says 'write a spec', 'spec this out', 'schreib ein spec', or '/write-spec'. This skill ONLY writes the spec; it never implements."
license: MIT
metadata:
  author: plumpudding
  stage: alpha
  source: ORIGINAL
  tags: [spec, planning, requirements, interview, workflow, acceptance-criteria]
  keywords: [write-spec, spec, specification, requirements, plan, interview, criteria]
  reads_from: ["the current codebase / environment"]
  writes_to: ["specs/<name>.md (auto-detects an existing convention first)"]
---

# Write Spec

You produce a **spec sheet** — a single markdown file precise enough that a
*fresh agent with none of this conversation's context* can implement it and
verify its own work. **You do not implement.** Your only deliverable is the spec.

## Operating principles

- **Find the real goal, not the stated solution.** Interview past the surface
  request. People ask for a solution; spec the underlying need.
- **Every question leads with a recommendation.** Never ask an open question.
  Give your recommended answer/default first, then alternatives, and **always**
  let the user type a custom answer or add extra context. If a question can be
  answered by reading the codebase, read the codebase instead of asking.
- **One thing at a time.** Don't dump a wall of questions. Walk the decision tree;
  resolve dependencies between decisions one by one.
- **Lock key decisions explicitly.** Before writing, replay the decisions you've
  settled and have the user confirm them, so nothing is silently assumed.
- **Be concrete; decide now, don't defer.** Everything that's been decided goes
  into the spec in specific terms — exact names, values, copy, states, data
  shapes, behavior. Leave nothing to the planner's or implementer's imagination.
  *You* are the one interviewing, so when you're unsure how something should be,
  that's a question for the user **now** — don't punt the decision downstream. The
  only thing you leave open is the code-level HOW (which files/functions, in what
  order); that's the implementer's job. Everything else: pin it down.
- **Tailor everything to THIS environment.** The verification plan must use the
  tools that actually exist here — real commands, real test files, real URLs.
- Interview in the user's language; write the spec in the repo's documentation
  language (default English).

## Procedure

### 1. Orient — ground yourself before asking anything

Read the environment so your questions are sharp and your verification plan is
real. Do **not** ask the user what you can find out yourself:

- **Stack & commands:** language, frameworks, package manager; the actual
  `build` / `test` / `run` / `lint` commands (read `package.json`, `Makefile`,
  `CLAUDE.md`, CI config).
- **Verification surface:** Is there a UI? Can it be driven (Chrome MCP / a dev
  server / Playwright)? Is there a unit/e2e test runner? A CLI to invoke? This
  decides what "practical verification" means in the spec.
- **Format to match:** look for an existing spec/plan to mirror — `specs/*.md`,
  `docs/plan.md`, `docs/specs/`, prior specs. If one exists, match its structure
  and its acceptance-criteria style.
- **Output path:** where specs live → write there. Default `specs/<kebab-name>.md`;
  use the detected convention if there is one.
- **Project conventions:** read `CLAUDE.md` / `AGENTS.md` / `README` for rules the
  spec and the implementer must respect (UI component lib, styling rules, etc.).

Then state, in 3–5 lines, what you found (stack, test/verify options, format
you'll match, target path) before interviewing.

### 2. Interview — one focused question at a time

Use the platform's structured-question UI when available. In Claude Code use
**AskUserQuestion**: put your recommended option **first**, suffixed
`(recommended)`; it already gives the user an *Other* free-text + notes field, so
the "custom answer / add info" path is always present. Outside Claude Code, ask in
prose: state your recommendation, give alternatives, invite a custom answer.

Walk the tree. Cover at least these, skipping what's already answered by Orient:

- **Real goal & why now** — the outcome the user actually wants; the problem
  behind the request.
- **Scope** — what's explicitly IN, and what's explicitly OUT (non-goals).
- **Users / triggers / inputs → outputs** — who/what invokes it, and what it
  produces.
- **Functional requirements** — concrete, observable behaviors.
- **Non-functional constraints** — only the ones that matter here (perf, a11y,
  security, compatibility, design tokens, error handling).
- **Data / contracts / state** — APIs, schemas, files, or state touched.
- **Edge cases & failure behavior** — what happens when things go wrong / empty /
  large / offline.
- **UX specifics** (if UI) — states, copy, and which existing components to reuse
  (don't hand-roll what a component library already provides).

End the interview by **replaying the locked key decisions** and asking the user to
confirm or correct them.

### 3. Define precise success criteria

Turn the agreed behavior into a **numbered list of acceptance criteria**, each one
independently checkable (binary pass/fail) and tied, where possible, to a concrete
verification (a test, a command, a Chrome-MCP assertion). If a past spec set a
criteria format, match it. These criteria are the contract the implementer is
graded against — vague criteria are a bug.

### 4. Write the spec

Fill in `references/spec-template.md` and write it to the output path. **Size each
section to the work — there is no length cap.** A large feature may need Goal,
Non-goals, Context, and Requirements that each run to many paragraphs with their
own sub-headings (a 1000-line spec is fine if the feature warrants it); a small
change stays terse. Add as much sub-structure as the content needs — what matters
is that it stays readable and self-contained, not short. Two parts are
non-negotiable:

- A **Verification Plan** with *concrete, executable* steps for THIS environment
  (real commands; for a UI, real Chrome-MCP navigation + assertions; for a CLI,
  real invocations + expected output). No generic placeholders.
- The **Implementation Workflow** section, embedded verbatim from the template, so
  a fresh agent self-executes: plan → fresh-subagent plan review (+fix) →
  fresh-subagent implement → fresh-subagent review (+fix) → loop until clean →
  cross-check every acceptance criterion → practical verification → final
  independent check.

### 5. Self-check — the second pass

Before declaring done, re-read the spec twice: once as the fresh implementer
("could I build this with only this file?"), once as a skeptical reviewer
("what's ambiguous, unverifiable, or missing a criterion?"). Fix what you find;
ask the user about anything you can't resolve. For a high-stakes spec, dispatch a
**fresh subagent** to critique it and fix the relevant findings — this is the
"second AI checks the output" gate applied to the spec itself.

Finish by reporting the spec's path and a 3-line summary (goal, scope, how it
gets verified).

## Hard rules

- **Inspect, don't implement.** Read and verify the existing code as much as you
  need to ground the spec — confirm that files, APIs, components, and patterns
  actually exist and understand how they work. But write no production code, and
  do **not** pre-write the implementer's plan: no file-by-file or
  function-by-function code plan. The spec defines WHAT and the acceptance
  criteria; deciding the exact code-level HOW is the implementer's job
  (Implementation Workflow, step 1). If the user wants to build, point them there.
- **Don't fabricate what exists; do design what's new.** Never state as fact
  something about the *current* codebase you didn't verify in Orient — existing
  commands, paths, components, or test tooling. But you absolutely *may* invent
  and propose *new* things the feature needs (a new component, command, endpoint,
  or approach). When you do: confirm the shape with the user, then write it into
  the spec concretely — name, behavior, interface, defaults — so the implementer
  builds what you specified instead of re-deciding it. Just keep the two visibly
  separate: what already exists vs. what this spec introduces.
- **The spec must be self-contained.** Assume the implementer gets only this file.
