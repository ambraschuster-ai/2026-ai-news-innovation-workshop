# CLAUDE.md — Maintainer / Build Guide

This file is for Claude Code sessions working **on** this repository —
building the workshop website itself. It is not shown to workshop students.
Their day-by-day guidance lives in `STUDENT_CLAUDE_GUIDE.md` (see
[ADR 0009](project/adr/0009-separate-maintainer-claude-md.md) for why these
are separate files).

## Before starting work

- Read [`project/tasks.md`](project/tasks.md) for what's currently open.
- Read [`project/specifications.md`](project/specifications.md) for what
  this product is and what it requires — read on the first session working
  on this repo, or whenever a task's context isn't already clear from
  `tasks.md` alone. Changes rarely, so a fresh session doesn't need to
  re-read it every time if it's already been read recently in this thread.
- Read [`project/adr/`](project/adr/) for existing architecture decisions
  before proposing a new approach to something already decided. If a past
  decision needs to change, write a new ADR that supersedes it — don't edit
  the old one.
- [`project/CHANGELOG.md`](project/CHANGELOG.md) holds the historical
  record (what happened, in what order, and why) — consult it like
  `project/adr/`, when investigating the reasoning behind something past,
  not as standing context read every session.

## While working

- Check off tasks in `project/tasks.md` as they're completed. Add newly
  discovered tasks there rather than letting them go untracked. Keep it
  short — a task's full history and reasoning belongs in a dated
  `project/CHANGELOG.md` entry, not piled into `tasks.md` itself.
- Any non-trivial technical decision (new dependency, changed data flow,
  hosting/infra change, a plan deviation) gets a new numbered file in
  `project/adr/`, following the existing format (Context / Decision /
  Consequences). If it also changes what this product fundamentally does
  or requires, update `project/specifications.md` to match.
- Keep a local dev server running against `docs/` for the length of the
  session (`python3 -m http.server <port> --directory docs`, run in the
  background) so pages can be spot-checked as they're edited, rather than
  starting one only at the end to verify finished work. Start one at the
  beginning of a session touching `docs/` if one isn't already up.

## Repo layout

- `docs/` — the deployed static site (Vercel). This is the only directory
  that ends up live at the public URL.
- `project/` — internal build tracking (this file's companions). Never
  linked from the public site.
- `api/` — the one serverless function (Claude proxy, see
  [ADR 0007](project/adr/0007-serverless-claude-proxy.md)). Never put
  secrets in this directory's source — they're Vercel environment variables.
- `STUDENT_CLAUDE_GUIDE.md`, `SUBMISSION.md` — content students copy
  into their own workflow. Treat as content-fill deliverables, not this
  file's concern.
