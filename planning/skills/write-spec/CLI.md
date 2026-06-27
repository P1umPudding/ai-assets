# Write Spec — CLI Usage

## Slash Command

```
/write-spec [what you want built]
```

Starts an interview to uncover the real goal, then writes a self-contained spec
sheet (requirements, acceptance criteria, verification plan, and an embedded
implement-and-verify workflow) to `specs/<name>.md` — or to the repo's existing
spec location if one is detected. It does **not** implement.

## Arguments

- `[what you want built]` (optional): a one-line description of the feature /
  project / change. If omitted, the skill asks for it first.

## Examples

```
/write-spec add a dark-mode toggle to the settings page
/write-spec
```
