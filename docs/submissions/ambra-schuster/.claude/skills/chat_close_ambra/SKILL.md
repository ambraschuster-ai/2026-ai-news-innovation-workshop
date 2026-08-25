---
name: chat_close_ambra
description: End-of-session wrap-up for Ambra Schuster's Documented NY project in docs/submissions/ambra-schuster/. Updates the active sub-project's tasks.md (checkboxes, newly discovered work), amends requirements.md or architecture.md if scope or a technical decision changed, refreshes SUBMISSION.md so it reflects current project status, updates CLAUDE.md if it went stale, then splits the session's work into logical commits and pushes them to the current branch. Use when the user says they're wrapping up, switching tasks, done for now, or invokes /chat_close_ambra.
---

# Chat close (Ambra's)

> Named `chat_close_ambra` so it can never be confused with the workshop's
> own `/chat_close`, which belongs to Andrew and wraps up the site repo's
> `project/` files. This one is only about
> `docs/submissions/ambra-schuster/`.

Run this at the end of a session, before switching tasks, so nothing worked
on this session only lives in the conversation. Docs first, then commits, so
the doc updates ride along in the push.

Everything in this skill is scoped to `docs/submissions/ambra-schuster/`.
Per that folder's `CLAUDE.md`, it is the whole workspace — the site's own
directories (`docs/` outside that folder, `project/`, `api/`, root-level
config) belong to the workshop maintainers. If wrap-up seems to require
touching a file outside the folder, stop and say what and why instead of
reaching outside.

## Step 0 — Establish what actually happened

Don't work from memory of the conversation alone. Run `git status` and
`git diff` (staged and unstaged) to see the real, current change set —
conversation recall and actual diffs drift, especially in a long session.
Note anything that was tried and reverted versus what's actually still in
the tree.

If `git status` is clean and nothing was discussed that maps to docs work
either, say so and stop — don't manufacture busywork on a session that
didn't change anything.

Also check that nothing outside `docs/submissions/ambra-schuster/` is
modified. If something is, flag it before committing rather than sweeping
it into the push.

## Step 1 — The active sub-project's `tasks.md`

The project table in `docs/submissions/ambra-schuster/CLAUDE.md` says which
of the five sub-projects under `documented-answers/` is active. That
project's `tasks.md` is the live list of what's open:

- Check off (`- [x]`) tasks completed this session — but only against the
  specific *Done when* line. If that line isn't literally true yet, the
  task isn't finished; leave it unchecked and say so.
- Add work discovered but not done to the right stage, rather than letting
  it float.
- Keep entries short.

Don't touch a non-active project's `tasks.md`. Projects written at planning
depth get rewritten before they start.

## Step 2 — `requirements.md` and `architecture.md`, if relevant

Per `CLAUDE.md`, these are the source of truth for the active project, and
stale entries get fixed in the same commit as the work that made them stale.

- If the session changed **what the project does or requires** — not just
  what's left to do — update `requirements.md` to match. This should be
  rare; only on a real scope change.
- If a decision in `architecture.md` turned out to be wrong, or the session
  made a non-trivial technical decision (new dependency, changed data flow,
  hosting change, a deviation from what the file describes), update
  `architecture.md` so it describes what was actually built. Don't leave the
  file describing something different from the code.
- If the work drifted past what `requirements.md` allows, or into another
  project's scope, say so rather than quietly widening the file to fit.

Skip this step if nothing decision-worthy happened — most sessions won't
need it.

## Step 3 — `SUBMISSION.md`, and `CLAUDE.md` if it went stale

- **Every run, update `docs/submissions/ambra-schuster/SUBMISSION.md` so it
  reflects the current state of the project** — replace any remaining
  `TODO` placeholders, and revise the hypothesis, what you're building, and
  solution fields if the session moved them. Keep it concise: roughly one
  to two sentences per field, plain language, describing what actually
  exists now rather than what's planned. This is a public showcase card,
  not a status log — no changelog entries, no task lists, no session
  history. If nothing about the project's direction or state changed this
  session, leave the file alone and say so.
- If the same correction came up more than once this session, or the same
  mistake was made twice, add a line to `CLAUDE.md` — that's the signal the
  file names for when to grow it.
- If the status of a sub-project changed (paused, started, finished), update
  the status column in `CLAUDE.md`'s project table.

## Step 4 — Commit and push

- Group the diff into logically separate commits (e.g. a code change and an
  unrelated docs fix are two commits, not one). Doc updates from Steps 1-3
  can ride in their own commit or the last content commit, whichever reads
  more naturally.
- Write each commit message around *why*, matching the existing log style
  (`git log --oneline`) — short, imperative, specific.
- Stage files by name, not `git add -A`/`.` — review `git status` after
  staging to make sure nothing unintended (stray temp files, `.DS_Store`,
  unrelated edits) is included.
- Before the first commit of anything new, confirm `.gitignore` actually
  covers `.env`, `corpus.json`, and any credentials file. Never commit an
  API key, token, or password — if one is about to go in, stop and say so.
- Push to the current branch: `git push -u origin <branch-name>`. Retry on
  network failure only. Never force-push, rewrite history, or skip hooks to
  get a push through — if a hook fails, fix the underlying issue and commit
  again.
- If an open PR already exists for this branch, pushing is enough — don't
  open a duplicate.

Report back concisely: what got updated in each step (or skipped, and why),
and the resulting commits/push outcome.
