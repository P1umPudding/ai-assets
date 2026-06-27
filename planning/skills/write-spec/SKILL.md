---
name: write-spec
description: "Interviews the user to uncover the real goal, then writes a self-contained spec sheet for a feature/project/change — requirements, precise acceptance criteria, and an embedded implement-and-verify workflow that a fresh agent can execute end to end. Use when the user wants to specify something before building, or says 'write a spec', 'spec this out', 'schreib ein spec', or '/write-spec'. This skill ONLY writes the spec; it never implements."
license: MIT
metadata:
  author: plumpudding
  stage: alpha
  source: ORIGINAL
  tags: [spec, planning, requirements, interview, workflow, acceptance-criteria]
  keywords: [write-spec, spec, specification, requirements, plan, interview, criteria]
  reads_from: ["references/spec-template.md"]
  writes_to: ["specs/<name>.md"]
---

# Write Spec

You produce a **spec sheet** — a single markdown file precise enough that a
*fresh agent with none of this conversation's context* can implement it and
verify its own work. **You do not implement.** Your only deliverable is the spec.

## Operating principles

- **Find the real goal, not the stated solution.** Interview past the surface
  request. People ask for a solution; spec the underlying need.
- **Bias to asking over assuming.** When a decision could reasonably go more than
  one way and guessing wrong would be costly or annoying to unwind, **ask** — don't
  assume. A few extra confirmed details beat one wrong assumption the user only
  discovers in the built result. Interview *relentlessly*: walk every branch of the
  design tree, drill each answer down to specifics, and keep going until there's no
  consequential unknown left. Err on the side of one question too many. (The one
  thing you still decide yourself, not ask about, is the technical HOW — see below.)
- **Every question leads with a recommendation.** Never ask an open question
  (the one exception is the opening "what do you want built?" if the user hasn't
  said yet). Give your recommended answer/default first, then alternatives, and
  **always** let the user type a custom answer or add extra context. If a question
  can be answered by reading the codebase, read the codebase instead of asking.
- **Batch related questions; sequence dependent ones.** When the platform has a
  structured multi-question UI (Claude Code: AskUserQuestion, up to ~4 at once),
  use it — asking several questions together is good, *especially* when they
  belong to the same topic, because the user can step through them in order. What
  to avoid is an unstructured wall of free-text questions. When one decision
  genuinely depends on the answer to another, ask the first, then follow up — don't
  ask a question whose answer an earlier, still-open one would settle.
- **Lock key decisions explicitly.** Before writing, replay the decisions you've
  settled and have the user confirm them, so nothing is silently assumed.
- **Be concrete; decide now, don't defer.** Everything that's been decided goes
  into the spec in specific terms — exact names, values, copy, states, data
  shapes, behavior. Leave nothing to the planner's or implementer's imagination.
  When you're unsure about something *the user cares about* (a goal, a behavior, a
  product or UX choice), that's a question for the user **now** — don't punt it
  downstream. The only thing you leave open is the code-level HOW (which
  files/functions, in what order); that's the implementer's job. Everything else:
  pin it down.
- **Interview about intent; decide the tech yourself.** Your questions are for the
  things only the user can answer — goals, scope, behavior, product/UX choices.
  Do **not** interrogate the user on implementation details (library choices,
  internal structure, data-shape mechanics, naming). Decide those yourself the way
  you judge best and write them into the spec concretely. Escalate a technical
  choice to a question only when it is a genuine **major architectural decision**
  (hard to reverse, costly, cross-cutting), when the spec is **explicitly a
  technical one**, or when the user has signalled they want to **co-decide the
  tech**. The goal isn't to keep technical decisions out of the spec — it's to
  make them yourself instead of via a hundred questions.
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

### 2. Interview — structured, recommendation-led questions

Use the platform's structured-question UI when available, and prefer grouping
related questions into one ask. In Claude Code use **AskUserQuestion** (up to ~4
questions at once): put your recommended option **first**, suffixed
`(recommended)`; it already gives the user an *Other* free-text + notes field, so
the "custom answer / add info" path is always present. Outside Claude Code, ask in
prose: state your recommendation, give alternatives, invite a custom answer.

Walk the tree. Cover at least these — they're about intent and behavior, not
implementation mechanics (decide those yourself per the principle above). Skip
what's already answered by Orient:

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

**Don't accept vague answers.** If an answer leaves a real decision open ("make it
look nice", "handle errors gracefully", "the usual"), drill in: which states
exactly, what copy, what happens on each failure, what the defaults are. Push each
topic to specifics you could hand an implementer verbatim — a vague answer is just
a deferred question.

**Assumption sweep — before you write.** List every assumption you'd otherwise bake
into the spec. For each, ask yourself: *if I guessed wrong here, would the user
notice and care?* If yes → turn it into a question now. Only silently assume the
trivial, easily-reversible things. Surfacing a half-dozen "I'm going to assume X,
Y, Z — correct any of these?" is exactly the right move; it's cheaper than a spec
built on a guess that unravels at implementation time.

End the interview by **replaying the locked key decisions** and asking the user to
confirm or correct them.

### 3. Define precise success criteria

Turn the agreed behavior into a **checklist of acceptance criteria** (the `- [ ]`
form the template uses, labelled AC1, AC2, …), each one
independently checkable (binary pass/fail) and tied, where possible, to a concrete
verification (a test, a command, a Chrome-MCP assertion). If a past spec set a
criteria format, match it. These criteria are the contract the implementer is
graded against — vague criteria are a bug.

### 4. Write the spec

Write the spec to the output path using `references/spec-template.md` as the
structure. **Everything in that template above the first `---` divider is guidance
for you, the author — do not copy it into the spec.** The spec itself starts at the
`# Spec — <name>` heading. Name the file after the feature in kebab-case (e.g.
`dark-mode-toggle.md`). Copy the `## Implementation Workflow` section — its heading
through the end of the file — **verbatim**; fill in and clean every section above it (drop the
parenthetical hints and any unused `<…>` placeholders). If you instead match a past
spec's format (per Orient), you must still emit sections literally titled
**Acceptance criteria** and **Verification plan** and keep the Implementation
Workflow as the final section — its steps reference those sections by name and
position.

**Size each section to the work — there is no length cap.** A large feature may need Goal,
Non-goals, Context, and Requirements that each run to many paragraphs with their
own sub-headings (a 1000-line spec is fine if the feature warrants it); a small
change stays terse. Add as much sub-structure as the content needs — what matters
is that it stays readable and self-contained, not short. Two parts are
non-negotiable:

- A **Verification plan** with *concrete, executable* steps for THIS environment
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
  Boundary: specify *interfaces and contracts* fully (message shapes, types,
  endpoints, public signatures) — those are part of WHAT — but leave the *internal*
  mechanics (call sequence, file layout, helper breakdown) to the implementer.
- **Don't fabricate what exists; do design what's new.** Never state as fact
  something about the *current* codebase you didn't verify in Orient — existing
  commands, paths, components, or test tooling. But you absolutely *may* invent
  and propose *new* things the feature needs (a new component, command, endpoint,
  or user-facing approach). Confirm anything user-facing or architectural with the
  user — fold it into the locked-decisions replay rather than asking per item — and
  decide purely-internal approaches yourself. Then write it into the spec
  concretely — name, behavior, interface, defaults — so the implementer builds what
  you specified instead of re-deciding it. Just keep the two visibly separate: what
  already exists vs. what this spec introduces.
- **Self-contained for every decision.** The reader must be able to act without
  having seen *this conversation* — every decision lives in the spec. You may
  reference repo files the implementer can open (e.g. `CLAUDE.md`), but any rule
  that's load-bearing for this work must be **copied into the spec**, not just
  linked, so it can't be missed.
