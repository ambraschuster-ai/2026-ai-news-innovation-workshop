# Specifications

What this product is and what it requires. Changes rarely — when it does,
that's usually worth its own dated note in [`CHANGELOG.md`](CHANGELOG.md).
For what's currently open, see [`tasks.md`](tasks.md). For why a past
technical decision was made, see [`project/adr/`](adr/).

## What this is

A public website for a 3-day, in-person AI workshop for journalists (state
of AI → prompting, Claude Code, and configuration → responsible design and
shipping), built and maintained by Claude Code sessions working on this
repo. Students use the site during class and build their own project
alongside it, submitting their work into the same repo.

## Audience

Two distinct readers, kept deliberately separate (see
[ADR 0009](adr/0009-separate-maintainer-claude-md.md)):

- **Workshop students**, using the site day-of and referencing
  `STUDENT_CLAUDE_GUIDE.md` while they build their own project.
- **Claude Code sessions maintaining this repo** (this file's actual
  reader), who need `CLAUDE.md`, this file, `tasks.md`, and `project/adr/`
  — never the student-facing content.

## Structure

- `docs/` — the entire deployed site (Vercel, static). The only directory
  that ends up live at the public URL.
- `docs/data/schedule.json` — the single source of truth for every
  session's time, duration, type, and title across all three days. Every
  page's displayed schedule info, prev/next navigation, and timeline view
  reads from this file at runtime; nothing hardcodes a session time except
  each Slides deck's `cover-meta` (a deliberate simplification, see
  [ADR 0011](adr/0011-split-overview-and-slides.md) — `deck.js` has no
  fetch, so this needs a matching manual edit whenever a schedule change
  touches a session with a Slides deck).
- Each real content session ships as a pair: an **Overview** page (normal
  scrolling article, shared nav/footer) and a **Slides** deck (paginated,
  self-contained chrome, no schedule fetch) — see
  [ADR 0011](adr/0011-split-overview-and-slides.md). Keep both in sync;
  `project/scripts/check-slide-parity.js` checks structural parity (same
  section ids, same item counts) but not wording.
- `project/copy-drafts/day-N/*.md` — an editable markdown mirror of each
  live Overview page, one file per session, used for direct human editing
  before porting changes into the live HTML. See
  `project/copy-drafts/README.md` for the format convention.
- `docs/submissions/your-name/` — one continuous folder per student for
  the whole workshop (not per-day), created during Day 1's Fork & Submit,
  holding their own project plus copies of `SUBMISSION.md` and
  `STUDENT_CLAUDE_GUIDE.md`-as-`CLAUDE.md`. See
  [ADR 0022](adr/0022-continuous-student-folder.md).
- `docs/students/index.html` — auto-generates submission cards client-side
  from `docs/submissions/` on `main`, via GitHub's public API, parsing
  each student's `SUBMISSION.md`. No backend, no build step. See
  [ADR 0023](adr/0023-auto-generated-submission-cards.md).
- `api/` — one serverless function (a Claude proxy), paused, not yet built
  — see [ADR 0007](adr/0007-serverless-claude-proxy.md) and `tasks.md`.
  Never put secrets in this directory's source; they're Vercel environment
  variables.
- `project/adr/` — numbered architecture decision records, the durable
  "why" behind any non-trivial technical decision. Read before proposing
  an approach to something already decided; if a past decision needs to
  change, write a new ADR that supersedes it, don't edit the old one.

## Core requirements

- **`schedule.json` is authoritative.** A session's time, duration, or
  title lives there and only there (Slides `cover-meta` excepted, see
  above) — never hardcode it a second place that could drift.
- **One shared deployment, one live site.** There is no per-student
  hosting inside this project; students who want their own live URL
  deploy independently (Day 3's Build Time session walks them through a
  free Vercel account of their own) — that's separate from, not a
  replacement for, this site's own single Vercel deployment.
- **No secrets committed.** Anything sensitive is a Vercel environment
  variable, never source in `api/` or anywhere else in the repo.
- **Every non-trivial technical decision gets an ADR** before or
  immediately after it ships — new dependency, changed data flow,
  hosting/infra change, a deviation from a previous plan.
- **Ordered day content stays renumbered and cross-referenced correctly.**
  When a session is added, cut, or reordered within a day: update
  `schedule.json`, the day's `nav.html` flyout, `resources.html`
  attributions, each affected Slides deck's hardcoded "Next section" link
  chain, and any Overview page that names a since-moved session by title.
- **Cut content is archived, not deleted**, unless the user explicitly
  says otherwise — moved to `project/removed-sessions/` (gitignored, not
  deployed, recoverable) rather than dropped from disk.

## Explicitly out of scope (for now)

- A backend beyond the one paused serverless proxy function.
- A full portfolio page per student — the auto-generated card is the
  display unit (see [ADR 0023](adr/0023-auto-generated-submission-cards.md)).
- Standalone automated tests beyond `check-slide-parity.js`, until the
  open testing-strategy decision in `tasks.md` is resolved.
