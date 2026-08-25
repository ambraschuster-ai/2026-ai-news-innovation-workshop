# Tasks

Current, open work only. Check here before starting work; update here when a
task starts, completes, or changes scope. Kept short on purpose — full
history and reasoning for anything below (or already done) lives in
[`CHANGELOG.md`](CHANGELOG.md); architecture decisions live in
[`project/adr/`](adr/). See [`specifications.md`](specifications.md) for
what this product actually is.

Status: `[ ]` not started · `[~]` in progress

## Content

- [ ] **Day 1 line-by-line edit pass.** 6 of 9 pages (`04-product-discussion`
      through `09-project-assignments`, excluding the 3 already rewritten
      research-first) are still queued for the user's own editorial pass
      against `project/copy-drafts/day-1/*.md`. See
      `project/copy-drafts/day-1/README.md` for the cross-page pattern
      decisions to make once (voice, citation density, bare question
      lists) before editing page by page.
- [ ] **Instructors page bio copy.** `docs/instructors.html` and
      `project/copy-drafts/instructors.md` are scaffolded with placeholder
      fields for Andrew and Adiel — actual bios, titles, and (optionally)
      photos not yet supplied.
- [ ] **Site-wide workshop-name sweep.** The correct name is inconsistent
      across `<title>` tags and body copy on several pages (spot-checked
      via grep, not yet fully audited or fixed).
- [ ] **Site-wide em-dash sweep.** Standing style rule: no em-dashes,
      periods/colons/commas instead. Still present across most of Day 1
      and `docs/day-2/03-claude-md.html`; clean everywhere else that's had
      an editorial pass already.
- [ ] **Known Overview/Slides parity mismatches**, found by
      `project/scripts/check-slide-parity.js` but not yet fixed (some are
      long-standing, pre-date this list): `01-state-of-ai.html` (s2, s4,
      s5), `03-use-cases.html` (s3), `06-ai-tools.html` (s2), all Day 1;
      `03-claude-md.html` (s3), `05-spec-driven-dev.html` (s3), Day 2;
      `03-ai-human-design.html` (s1), Day 3.

## Student submissions

- [ ] **Add a live-URL field to `SUBMISSION.md` and the auto-generated
      cards.** Day 3's Build Time session now walks students through
      deploying their own project to Vercel and saving the live URL (see
      `docs/day-3/04-build-time.html` s1) — `SUBMISSION.md`'s field set and
      `docs/js/submissions-gallery.js`'s parser/render logic need a
      matching field so that URL actually surfaces on the student's
      submission card instead of just living in their own notes. See
      [ADR 0023](adr/0023-auto-generated-submission-cards.md) for how the
      card pipeline currently works.
- [ ] **`SUBMISSION.md` field set is still provisional.** Flagged as
      wanting to be seen in real use before finalizing — now that
      rendering is automated (ADR 0023), a field rename has a real
      downstream parsing cost, so batch any further field changes rather
      than iterating one at a time.
- [ ] **Demo-path field decision.** Was in the original submission-card
      scope, dropped from the current field set — unclear if that was
      deliberate. Revisit once the live-URL field above is added, they may
      turn out to be the same thing.

## Infrastructure

- [ ] **Phase 2: serverless Claude proxy, still paused.**
      `api/claude-proxy.ts`, Upstash Redis rate limiting, Vercel env vars,
      a `max_tokens` cap and pinned cheaper model for public-proxy
      traffic, and a verify-the-limit-actually-works check — none built
      yet. Paused since 2026-08-04 to prioritize content; see
      [ADR 0007](adr/0007-serverless-claude-proxy.md). Do not build
      anything that calls the Claude API from a page until this is done.
- [ ] **Confirm Vercel deploy is actually wired up**: repo connected,
      live URL confirmed, and a PR produces an automatic preview
      deployment. Maintainer action (needs Vercel account access), not
      something verifiable from inside a session.
- [ ] **Decide on a standalone test for `docs/js/submissions-gallery.js`'s
      GitHub API dependency.** It's the site's only runtime call to a
      service this project doesn't control, with two edge cases (an empty
      `docs/submissions/` folder 404s rather than returning an empty
      array; a renamed `SUBMISSION.md` field breaks parsing for that
      field) only caught by hand so far. A parser unit test (plain Node,
      matching `check-slide-parity.js`'s shape) would add no new
      dependency; a Playwright integration test would — that's a real
      new-`devDependency` decision needing its own ADR if committed to,
      left open on purpose rather than decided here.

## Not yet scoped

- [ ] **Model selection / token usage / subagent guardrails content.**
      Whether this becomes its own Day 2 section or folds into existing
      ones is still an open question for a planning conversation, not
      something to design cold. A first-draft explainer of Claude Code's
      own context controls (`/clear`, `/compact`, Rewind, auto-compact,
      background agents as a token-management technique) already exists
      in `CHANGELOG.md`'s 2026-08-22 entry, reusable once this gets
      scoped.
