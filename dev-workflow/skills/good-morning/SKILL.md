---
name: good-morning
description: "Generic morning kick-off for a git repo: fetches and fast-forward-pulls the current branch and the main dev branch, catches the user up on what changed since they were last active (on main and on their branch), surfaces whether their branch was merged or has an open PR, optionally builds, and closes with a dev joke of the day. Keeps it short — only what's relevant. Use when the user says 'good morning', '/good-morning', \"let's start the day\", 'boot me up', or any morning kick-off phrase."
license: MIT
metadata:
  author: plumpudding
  stage: alpha
  source: ORIGINAL
  tags: [morning, startup, sync, catch-up, daily, routine, kickoff, git]
  keywords: [good-morning, morning, start the day, boot me up, sync, catch up]
---

# good-morning — Morning Kick-off

A short morning ritual for whatever repo the user is in: sync git, tell them what
they missed since they were last active, flag anything about their branch (merged?
open PR?), optionally build, and end on a dev joke + a nudge to start the day.

Generic on purpose — detect the repo's conventions, never hard-code a project's
layout. Single-repo focus (the current repo); multi-repo is out of scope.

## Prime directive: don't overwhelm

The whole response should be **short and scannable**. Show only what's relevant:

- **Omit empty sections entirely.** "Nothing new on main" gets one line or is
  dropped — never a heading with nothing under it.
- **Attribution only for big things.** Name *who* did something (e.g. "Anna
  finished the export feature") only for notable changes — a shipped feature, a
  breaking change, a big PR. Routine commits stay anonymous and aggregated.
- **PRs / issues / releases: only if something major happened.** Otherwise a
  one-liner ("5 new issues, 8 closed") or nothing at all.
- Prefer a few highlight bullets over exhaustive logs. If in doubt, cut it.

## Opening line

Open with one short, friendly line before any tool calls — e.g. *"Morning! Let me
sync up and see what changed while you were away."* Keep it light; no fixed
persona.

## Safety rules (never violate)

- **Never** stash, rebase, force-pull, merge, reset, or otherwise touch
  uncommitted work. A dirty working tree or a diverged branch is a *skip-and-flag*,
  not something to "fix".
- **Never** commit, push, or open PRs.
- **Never** delete a branch without asking in text first.
- If `gh` is missing, there's no remote, or the remote isn't GitHub, **skip** the
  affected sections silently — don't error out.

## Procedure

### 1. Orient (silent — gather facts, don't print them raw)

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)" || { echo "Not a git repo."; exit 1; }
BRANCH="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)"
EMAIL="$(git -C "$REPO_ROOT" config user.email)"
NAME="$(git -C "$REPO_ROOT" config user.name | awk '{print $1}')"; NAME="${NAME:-there}"

# Main dev branch: origin/HEAD → gh default → main/master fallback
MAIN="$(git -C "$REPO_ROOT" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')"
[ -z "$MAIN" ] && MAIN="$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null)"
[ -z "$MAIN" ] && { git -C "$REPO_ROOT" show-ref --verify -q refs/heads/main && MAIN=main; }
[ -z "$MAIN" ] && { git -C "$REPO_ROOT" show-ref --verify -q refs/heads/master && MAIN=master; }
MAIN="${MAIN:-main}"

# "Since you were last active" = your most recent commit on any branch.
# Guard an unset email (--author="" would match everyone → anchor = today),
# and use a portable 48h fallback (BSD `date -v` then GNU `date -d`).
ANCHOR=""
[ -n "$EMAIL" ] && ANCHOR="$(git -C "$REPO_ROOT" log --all --author="$EMAIL" -1 --format=%cI 2>/dev/null)"
[ -z "$ANCHOR" ] && ANCHOR="$(date -u -v-48H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '48 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null)"

# Is the tree clean? (decides whether pulls / auto-switch are safe)
DIRTY="$(git -C "$REPO_ROOT" status --porcelain)"
```

Keep `REPO_ROOT`, `BRANCH`, `MAIN`, `EMAIL`, `NAME`, `ANCHOR`, `DIRTY` for later.

### 2. Fetch

```bash
git -C "$REPO_ROOT" fetch --all --prune --tags 2>&1 | tail -3
```

No remote / fetch fails → note it in one line and continue with local state only.

### 3. Pull the current branch (fast-forward only, safe)

Only pull if the branch has an upstream, the tree is **clean**, and it can
fast-forward. Capture the pre-pull SHA so step 5 can show exactly what arrived.

```bash
BR_OLD="$(git -C "$REPO_ROOT" rev-parse HEAD)"
if [ -n "$DIRTY" ]; then
  echo "skip: working tree has uncommitted changes — not pulling $BRANCH"
elif git -C "$REPO_ROOT" rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  # NB: don't pipe the pull — a pipe's exit code is the last stage (tail), which
  # always succeeds, so a real `|| echo` flag would be dead code.
  if git -C "$REPO_ROOT" pull --ff-only >/dev/null 2>&1; then
    echo "pulled: $BRANCH (fast-forward)"
  else
    echo "skip: $BRANCH has diverged — left untouched"
  fi
fi
```

A diverged branch or dirty tree is a **skip + one-line flag**, never a stop.

### 4. Pull / fast-forward the main dev branch

If `BRANCH` == `MAIN`, step 3 already covered it. Otherwise update the local
`MAIN` ref to `origin/MAIN` **only if it fast-forwards** (no checkout, no merge):

```bash
if [ "$BRANCH" != "$MAIN" ]; then
  git -C "$REPO_ROOT" fetch origin "$MAIN:$MAIN" >/dev/null 2>&1 \
    || echo "note: local $MAIN didn't fast-forward (has its own commits) — using origin/$MAIN for the summary"
fi
```

The catch-up summary reads `origin/$MAIN` regardless, so this is just keeping the
local ref tidy.

### 5. Catch-up summary (the core — keep it tight)

**What changed on `MAIN` since your anchor.** Categorize lightly by
conventional-commit prefix; show counts + a few highlights, author named only for
notable ones:

```bash
git -C "$REPO_ROOT" log "origin/$MAIN" --since="$ANCHOR" --no-merges \
  --format='%h%x09%an%x09%s' | head -40
```

Render compactly. Examples of the *right altitude*:

> **On `main`:** 12 commits since you last pushed — 3 features, 2 fixes, rest chores.
> Notable: Anna shipped CSV export (`feat: csv export`); one breaking change to the
> auth payload (`feat!: ...`).

If nothing: a single line *"`main`: nothing new since your last commit."* — or drop
it if you're already saying a lot.

**What changed on your branch** (if not `MAIN`): list what arrived in the pull.

```bash
git -C "$REPO_ROOT" log "$BR_OLD"..HEAD --oneline 2>/dev/null | head -20
```

If empty: "your branch is unchanged since you left." One or two lines — no dump.

### 6. Branch status — merged? open PR? (needs `gh`)

```bash
if [ "$BRANCH" != "$MAIN" ] && command -v gh >/dev/null 2>&1; then
  gh pr list --head "$BRANCH" --state all \
    --json number,state,title,url,mergedAt,author -q '.[]' 2>/dev/null
fi
```

- **Merged** (`state == MERGED`): tell the user, and handle the switch in step 9.
- **Open PR**: tell the user with the **URL**.
- No `gh`: fall back to `git merge-base --is-ancestor HEAD "origin/$MAIN"` to guess
  merged-ness (note: squash/rebase merges won't show as ancestors — only claim
  "merged" when confident).

### 7. PRs / issues / releases — only the major stuff (needs `gh`)

Glance, don't dredge. Report a line only when something **notable** happened since
the anchor; otherwise a terse count, or omit.

```bash
SINCE_DATE="${ANCHOR%%T*}"  # gh search wants YYYY-MM-DD
# PRs merged since the anchor
gh pr list --state merged --search "merged:>=$SINCE_DATE" --limit 50 --json title,url,author -q '.[]' 2>/dev/null
# Issue deltas — new vs closed (two queries; --limit so the count isn't capped at 30)
gh issue list --state all    --search "created:>=$SINCE_DATE" --limit 200 --json number -q '.[]' 2>/dev/null | wc -l
gh issue list --state closed --search "closed:>=$SINCE_DATE"  --limit 200 --json number -q '.[]' 2>/dev/null | wc -l
# Releases — list carries no author; attribute a notable one separately
gh release list --limit 5 2>/dev/null
# gh release view <tag> --json author,name,publishedAt   # only for a notable release
```

- **PRs:** name a merged PR + author only if it's a sizable/feature one; else
  "3 PRs merged, 2 opened" or nothing.
- **Issues:** terse only — e.g. *"5 new issues, 8 closed."* (the two counts
  above). Highlight one only if it's clearly major.
- **Releases (GitHub Releases):** mention a new release/tag whose `publishedAt` is
  ≥ the anchor (`gh release list` has no date filter — eyeball it). For a notable
  one, attribute the author via `gh release view <tag> --json author`. Else omit.

### 8. Build (auto-detect, non-blocking)

Detect a build command from the repo; run it only if found; report the result in
**one line**. A failure is flagged, never a stop.

```bash
cd "$REPO_ROOT"
PM=npm
[ -f bun.lockb ] || [ -f bun.lock ] && PM=bun
[ -f pnpm-lock.yaml ] && PM=pnpm
[ -f yarn.lock ] && PM=yarn
if [ -f package.json ] && grep -q '"build"' package.json; then
  $PM run build >/tmp/gm-build.log 2>&1 && echo "build: ✓ clean" || echo "build: ✗ failed (see /tmp/gm-build.log)"
elif [ -f Makefile ] && grep -qE '^build:' Makefile; then
  make build >/tmp/gm-build.log 2>&1 && echo "build: ✓ clean" || echo "build: ✗ failed"
else
  echo "build: (no build script detected — skipped)"
fi
```

Adapt the detection to the stack you actually see (cargo, go, etc.). On failure,
show just the first error line in the heads-up — don't dump the whole log.

### 9. Sign off — joke, switch question, closing line

First get the joke (step 10). Then assemble the closing block in this order, with
the motivational line **always the literal last line**.

**If the branch was merged (step 6) and the tree is clean** → switch now, then tell
them:

```bash
git -C "$REPO_ROOT" checkout "$MAIN" && git -C "$REPO_ROOT" pull --ff-only
```

…and offer (in text) to delete the merged local branch. If it was merged but the
tree is **dirty**, do **not** switch — just say it's merged and let them deal with
their changes.

**If still not on `MAIN`** (and not auto-switched) → end with a plain-text question
so a quick reply works — no tool call:

> You're on `feature-x`, not `main`. Want me to switch you over? Just say the word.

**Closing block shape:**

> ☕ Good morning, `<NAME>`. Synced `feature-x`; `main` has 12 new (3 feats, 1
> breaking). Build clean.
>
> *Heads-up:* your branch has an open PR → <url>
>
> **Today's joke:** `<joke>`
>
> You're on `feature-x`, not `main` — want me to switch you over? Just say the word.
>
> Go build something amazing! ☕

Rules for the block:
- `Go build something amazing!` is the **literal last line**, always.
- The joke sits above it; the switch question (if any) between them.
- Fold any warnings (skipped pull, dirty tree, build fail, detached state) into one
  short *Heads-up* line — don't scatter them.
- If you're already on `MAIN`, drop the switch question.

### 10. Dev joke of the day

Same architecture as the reference skill: one two-part programming joke from
JokeAPI, with a baked-in fallback. Never blocks, never repeats except the fallback.

```bash
JOKE="$(
  curl -fsS --max-time 5 'https://v2.jokeapi.dev/joke/Programming?safe-mode&type=twopart' 2>/dev/null \
  | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    if d.get('error'): sys.exit(1)
    print(d['setup'].strip() + ' — ' + d['delivery'].strip())
except Exception:
    sys.exit(1)
" 2>/dev/null
)"
[ -z "$JOKE" ] && JOKE="There are 10 kinds of people in the world: those who understand binary and those who don't."
echo "$JOKE"
```

One joke, one line, never explained. `?safe-mode` filters server-side. Any
failure (offline, rate-limit, bad JSON) → the fallback one-liner.

## What this skill never does

- Never stashes, rebases, force-pulls, merges, or resets — dirty/diverged is
  skip-and-flag.
- Never commits, pushes, or opens PRs.
- Never deletes a branch without asking in text.
- Never auto-switches to `MAIN` when the tree is dirty.
- Never dumps full logs or floods the user — only the relevant, short version.
- Never blocks on a build failure or a joke-API failure.
- Never switches branches via a tool-confirmation dialog for the end question — it
  asks in plain text so the user can reply "yes" in one breath.
