---
name: chat_close
description: End-of-session wrap-up for this repo. Updates project/tasks.md (checkboxes, newly discovered tasks) and project/CHANGELOG.md (dated entry) if relevant, adds a new ADR under project/adr/ if a non-trivial technical decision was made this session, then splits the session's work into logical commits and pushes them to the current branch. Use when the user says they're wrapping up, switching tasks, done for now, or invokes /chat_close.
---

# Chat close

Run this at the end of a session, before switching tasks, so nothing worked
on this session only lives in the conversation. Four steps, in order —
docs first, then commits, so the doc updates ride along in the push.

## Step 0 — Establish what actually happened

Don't work from memory of the conversation alone. Run `git status` and
`git diff` (staged and unstaged) to see the real, current change set —
conversation recall and actual diffs drift, especially in a long session.
Note anything that was tried and reverted (worth a line in the changelog per
existing convention below) versus what's actually still in the tree.

If `git status` is clean and nothing was discussed that maps to docs work
either, say so and stop — don't manufacture busywork on a session that
didn't change anything.

## Step 1 — Task tracker: `project/tasks.md`, if relevant

Per `CLAUDE.md`'s "While working" section, this is the current, actively
maintained list of what's open. Update it when this session's work maps
onto it:

- Check off (`- [x]`) or remove any task completed this session.
- If a task was discovered but not done, add it under the relevant header
  rather than leaving it untracked.
- Keep entries short — full history and reasoning belongs in the dated
  `project/CHANGELOG.md` entry (Step 3), not piled into `tasks.md` itself.

Skip this step (leave the file untouched) if the session's work genuinely
doesn't map to anything tracked here — don't force an edit.

If this session changed what the product fundamentally does or requires
(not just what's left to do), also update `project/specifications.md` to
match — that file changes rarely, so only touch it on a real scope change.

## Step 2 — Architecture: `project/adr/`, if relevant

Per `CLAUDE.md`: any non-trivial technical decision (new dependency,
changed data flow, hosting/infra change, a deviation from an existing
plan or ADR) gets a new numbered ADR, not an edit to an old one.

- Read `project/adr/README.md`'s index and the most recent ADR (highest
  number) to match numbering and format.
- New file: `project/adr/00NN-short-slug.md` with `Status`/`Date` header
  and `## Context` / `## Decision` / `## Consequences` sections (see any
  existing ADR, e.g. `0024-nav-home-redesign.md`, for depth and tone).
- If a decision supersedes an earlier ADR, say so in both the new ADR and
  by updating that old ADR's Status in `project/adr/README.md`'s table —
  never edit the superseded ADR's own body.
- Add the new row to `project/adr/README.md`'s table.

Skip this step if nothing decision-worthy happened this session — most
sessions (content edits, bug fixes, copy passes) won't need one.

## Step 3 — Changelog: `project/CHANGELOG.md`

Add one dated entry under this file's `## Change log` section
(reverse-chronological, newest entries directly under the header):

- `- YYYY-MM-DD — **Bold one-line summary.** ` then 2-5 sentences: what
  changed, why, and anything explicitly excluded or left open.
- Keep it concise. Some existing entries run long (multi-paragraph, full
  audit trail) because they were written for high-stakes structural passes
  — don't match that length by default. A few tight sentences is the right
  size for a normal session; only go longer if the session itself was
  unusually complex and the detail is load-bearing.
- Use today's actual date, not a placeholder.

## Step 4 — Commit and push

- Group the diff into logically separate commits (e.g. a content change
  and an unrelated bug fix are two commits, not one) rather than a single
  catch-all commit. Doc updates from Steps 1-3 can ride in their own
  commit or the last content commit, whichever reads more naturally.
- Write each commit message around *why*, matching this repo's existing
  log style (`git log --oneline`) — short, imperative, specific.
- Stage files by name, not `git add -A`/`.` — review `git status` after
  staging to make sure nothing unintended (stray temp files, unrelated
  edits) is included.
- Push to the current branch: `git push -u origin <branch-name>`. Retry
  on network failure only (exponential backoff), per standing git
  guidance. Never force-push, rewrite history, or skip hooks to get a
  push through — if a hook fails, fix the underlying issue and commit
  again.
- If an open PR already exists for this branch, pushing is enough — don't
  open a duplicate. If none exists and one seems warranted, follow the
  repo's normal PR flow (check for a template, draft PR) rather than
  leaving pushed commits with no PR.

Report back concisely: what got updated in each of the four steps (or
skipped, and why), and the resulting commits/push outcome.
