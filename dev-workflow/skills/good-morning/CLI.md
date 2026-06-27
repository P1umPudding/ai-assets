# good-morning — CLI Usage

## Slash Command

```
/good-morning
```

Runs the morning kick-off for the current repo: fetch + fast-forward pull (current
branch and the main dev branch), a short catch-up on what changed since you were
last active, branch status (merged / open PR), an optional build, and a dev joke of
the day. Ends by offering to switch you to the main branch if you're not on it.

Also triggers on natural phrases: "good morning", "let's start the day", "boot me
up".

## Arguments

None. The skill auto-detects the repo, the main dev branch, your identity, and the
build command.

## Examples

```
/good-morning
good morning
```
