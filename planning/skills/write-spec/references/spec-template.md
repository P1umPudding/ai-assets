# Spec template

Fill every section. Delete the parenthetical hints. Replace `<…>` placeholders.
If a past spec in this repo set a format, match it instead and only borrow the
**Implementation Workflow** section below verbatim. The finished file is the only
context the implementing agent gets, so keep it self-contained.

**Sections scale with the work — there is no length cap.** Goal, Non-goals,
Context, and Requirements can each grow to many paragraphs with their own
sub-headings (`###`) for a large spec, or stay a few lines for a small one. Add
sub-structure freely; the only rule is that it stays readable and self-contained.

---

# Spec — <Feature / Project name>

> One-line summary of what this delivers.

## Goal

(The real outcome the user wants — the problem behind the request, not just the
asked-for solution. For a large spec, split this into `###` sub-sections —
e.g. background, motivation, target users, the vision of "done".)

## Non-goals

(What is explicitly OUT of scope, so the implementer doesn't drift.)

- <non-goal>

## Context

(What exists today, where this plugs in, relevant files/modules, and the project
conventions that apply — link `CLAUDE.md`/`AGENTS.md` rules the implementer must
follow, e.g. UI component library, styling rules.)

## Requirements

(Concrete, observable behaviors. Numbered so criteria can reference them.)

1. R1 — <requirement>
2. R2 — <requirement>

### Constraints

(Non-functional things that matter here: perf, a11y, security, compatibility,
design tokens, error handling. Only list what's real.)

- <constraint>

### Data / contracts

(APIs, schemas, files, state touched. Message shapes, types, endpoints.)

## Edge cases & failure behavior

- <case> → <expected behavior>

## Acceptance criteria

(Each one binary pass/fail and, where possible, tied to a concrete check. These
are the contract the implementation is graded against.)

- [ ] AC1 — <observable, checkable outcome>  → _verified by:_ `<test / command / Chrome-MCP assertion>`
- [ ] AC2 — <observable, checkable outcome>  → _verified by:_ `<…>`

## Verification plan

(Concrete and executable in THIS environment — real commands, real test files,
real URLs/selectors. Filled in by the spec author from what actually exists.)

- **Automated:** `<e.g. npm test -- path/to/file>` — expect <result>.
- **Build/lint:** `<e.g. npm run build>` — expect clean.
- **Practical / manual:** `<e.g. Chrome MCP: navigate to http://localhost:5173/x,
  assert element Y shows Z>` _(only if a UI / runnable surface exists; otherwise
  state why none applies)_.

---

## Implementation Workflow (for the implementing agent)

You are a **fresh agent**. This file is your full brief. Implement the spec above
by following these steps in order. Do not skip the reviews, and use a **fresh
subagent** for each review so it brings unbiased eyes.

0. **Read & sanity-check.** Read this whole spec. If anything is ambiguous, or
   contradicts the codebase, stop and ask before writing code.
1. **Plan.** Produce a concrete, step-by-step implementation plan (files to
   touch, order, risks). Write it next to this spec (e.g. `<spec>.plan.md`).
2. **Plan review.** Dispatch a fresh subagent to review the plan against this
   spec — gaps, wrong assumptions, missed acceptance criteria, risky steps. Fix
   every relevant finding.
3. **Implement.** Dispatch a fresh subagent to implement the (fixed) plan step by
   step, keeping changes aligned with the plan and the project's conventions.
   Where the codebase already has a similar feature, use it as the example/format
   to match rather than inventing a new shape.
4. **Implementation review.** Dispatch a fresh subagent (fresh eyes — hasn't seen
   the implementation happen) to review the diff for correctness against the plan
   and this spec.
5. **Fix & loop.** Fix every relevant finding from step 4. Repeat steps 3–4 until
   a review pass returns **no relevant findings**.
6. **Cross-check against this spec.** Go through the **Acceptance criteria** above
   one by one. Mark each ✅ / ❌ with the evidence that proves it. Any ❌ → return
   to step 3.
7. **Practical verification.** Run the **Verification plan** above for real —
   tests, build, CLI, or Chrome MCP as applicable. Capture the evidence (output,
   screenshots, assertions).
8. **Final independent check.** Dispatch a fresh agent to check the finished
   result against this spec end to end. Fix anything it surfaces.
9. **Done.** Only when every acceptance criterion is ✅, verification is green, and
   the final check passed. Report with evidence — no unverified "it works" claims.
