# Changelog

This file is the historical record of how this repo got built: dated
narrative, decisions made and later reconsidered, review passes, what broke
and how it got fixed. It is **not** the place to check current status —
that split off on 2026-08-25 into two current, actively-maintained files:

- [`specifications.md`](specifications.md) — what this product is and what
  it requires. Changes rarely.
- [`tasks.md`](tasks.md) — what's actually open right now. Changes often,
  stays short on purpose.

Durable architecture *decisions* (the "why") live in [`project/adr/`](adr/),
unchanged by this split.

This file is kept for reference, not read by default at the start of a
session (unlike `specifications.md`/`tasks.md`) — consult it the same way
you'd consult `project/adr/`, when you need the reasoning behind something
past, not as standing context. Everything below this line predates the
split and was formerly `project/REQUIREMENTS.md` in its entirety, including
its own now-superseded Phase 1-5 build checklist and "Newly identified
tasks" list — both kept here for the historical detail baked into each
entry (dates, what was tried and reconsidered), even though the current,
clean version of what's still open now lives in `tasks.md` instead. Where
the two disagree on whether something is done, trust `tasks.md`, not this
file — several items below were resolved by later work without their
checkbox being updated to match, which is exactly the kind of drift the
split was meant to fix.

---

# Requirements & Task Log (historical, superseded — see note above)

**Current focus (2026-08-04, status updated 2026-08-15):** paused backend
work (Phase 2, and the remaining Vercel-connection item in Phase 1) to
prioritize frontend/content — need the site visibly clickable and ready for
content to be added. Backend items below are fully scoped and not forgotten;
resume after the content pass. Do not build anything that calls the Claude
API from a page until Phase 2 (the proxy) is actually done — see
[ADR 0007](adr/0007-serverless-claude-proxy.md).

**Where things stand (2026-08-16):** all three days now have real,
scheduled content, currently on `review/full-site-audit-3` (branched from
`full-site-audit-2`) — Day 1 (8/9 sessions, only
`09-project-assignments` still a placeholder), Day 2 (8/8), Day 3 (7/7).
`live` (production, minimal) is untouched by the Day 2/3 work and still
only serves `setup.html`/`setup-day-2.html`, by design — see
[ADR 0018](adr/0018-live-branch-for-partial-production-deploy.md).
Day 2's round-3 audit is done and implemented (see the 2026-08-16 change
log entry) — all 8 sessions reviewed page by page, 7 of them edited (only
`08-show-tell` untouched), plus two new reusable components (a file
viewer, a starter-prompt code block). **Next step**: Day 3's round-3
audit hasn't started yet. Known open threads, not yet scheduled: the
workshop-name and em-dash sweeps are still only done on pages that got
touched directly, not site-wide; VS Code/Claude Code/Git content has no
scheduled home on any of the 3 days (see the Day 3 change log entry);
`STUDENT_CLAUDE_GUIDE.md` is still unwritten; a real visual/Playwright
check of the two new Day 2 components is still outstanding (no browser
automation tool was available during the round-3 implementation pass).

**2026-08-19**: Adiel's [PR #8](https://github.com/AndrewRCalderon/2026-ai-news-innovation-workshop/pull/8)
(Day 2 & 3 review notes) read, digested, and implemented — see
"Collaborator feedback — Adiel, PR #8" below. Done: the
`docs/day-3/04-ai-human-design.html` rewrite (new human-in-the-loop/
automate framework, new §05 coding-judgment section), the §05 condense +
Day 3 schedule reorder (`docs/data/schedule.json`), the Product Design
§02 citation refresh, and `STUDENT_CLAUDE_GUIDE.md` (new file, repo root)
plus its linked Day 2 §03 exercise rework. **Still open**: 3-5 additional
media-industry role examples for §05 slide 2 (background research
launched, not yet merged in), and a citable public source for the
Capelouto example on that same slide. The line-by-line copy edit pass is
still queued after this.

**2026-08-20**: the media-industry role research from 08-19 got merged into
§05 slide 2 (Business Insider, NPR, NYT added; Capelouto citation still
outstanding, flagged inline in the file). Then the line-by-line copy edit
pass happened: Day 2's 8 `project/copy-drafts/day-2/*.md` files got a full
user edit pass, and Day 3 was ported fresh (`project/copy-drafts/day-3/*.md`,
all 7 sessions, from current post-PR-#8 site content) and given the same
treatment. Both days then got a citation-integrity pass (a script checking
every `**Sources**` list against actual `[n]` usage — orphaned citations
removed or relocated to where they fit, per standing rule: user removes a
sentence, its citation goes too; new unsourced content is fine if an
existing citation "somewhat supports" it), plus typo fixes, two missing
section-numbers restored (`04-ai-human-design.md`, `07-final-show-and-tell.md`,
both confirmed intentional content cuts), an "AI-Human Design" →
"Human-AI Design" rename (in the copy-drafts only, not yet live — see
task below), and three new researched citations added to
`04-ai-human-design.md` (Vaccaro et al. 2024, Bainbridge 1983 "Ironies of
Automation," Green & Chen). See
[content-architecture-notes.md](content-architecture-notes.md) for
editorial patterns pulled from this pass, kept for the Day 1 rewrite.

**2026-08-20, continued: copy-draft re-implementation done, all 15 pages.**
All of Day 3 (7/7 pages: `01-recap` through `07-final-show-and-tell`) and
all of Day 2 (8/8, including `04-skills-best-practices`, implemented in a
follow-up pass once its draft was reviewed and confirmed) had their live
Overview HTML and Slides companions rebuilt from the edited copy-drafts,
matching the established Day 2 round-3 pattern (prose/citations/components
carried over, page skeleton — nav, breadcrumb, masthead, TOC, footer —
untouched unless the draft's own structure changed). `project/scripts/
check-slide-parity.js` runs clean across all of it except three known,
pre-existing false positives where Slides condenses a long list into a
single `.pull-question` paragraph (`03-claude-md` s3, `06-spec-driven-dev`
s3, `04-ai-human-design` s1 — the last one new this pass, same pattern).
Riding along in the same files: the "AI-Human Design" → "Human-AI Design"
rename cascaded fully (`schedule.json`, HTML, Slides, and
`docs/partials/nav.html`'s dropdown, which the original task scoping
missed); the Day 3 schedule 15-minute reallocation applied to
`schedule.json` (Final Coding Time 60→75 min, Where Can You Take This
45→30 min); the Capelouto citation gap closed (Press Gazette source,
softened to what it actually confirms); and Arlyn Gajilan added back to
`05-where-you-can-take-this`'s roster on a moderate-confidence trade-press
source (TVNewsCheck, syndicated republish, direct quote) after her earlier
exclusion for weak sourcing.

Two structural content cuts were confirmed with the user rather than
assumed from the draft alone, since removing a whole section is bigger
than a wording diff: `06-spec-driven-dev` dropped its "Why This Connects
to Skills" section entirely (confirmed intentional), and
`07-final-show-and-tell` dropped its "What to Actually Say" section
(pattern-matched against the confirmed case, not re-asked). `03-claude-md`
additionally got its Batch 7 corrections applied (haddock3 sentence
removed, user examples woven into the closing paragraph) and its
file-viewer bug actually fixed, not just relocated: root cause was a CSS
specificity collision (`.briefing code`'s `white-space: nowrap` beating
the parent `<pre>`'s `pre-wrap`), diagnosed and fixed via Playwright,
documented in [ADR 0020](adr/0020-file-viewer-inline-collapsible.md)
(supersedes [ADR 0019](adr/0019-file-viewer-dialog.md), swapping the
`<dialog>` popup for a native `<details>` disclosure in the process).

`04-skills-best-practices.html`'s structural rewrite (new §2 non-technical
scenario, §3's advice folded in and reframed around directing Claude to
build the skill rather than hand-authoring `SKILL.md`, new §4 testing
section replacing the old failure-pattern list) is now implemented into
both Overview and Slides, parity-clean, verified visually. This closes out
the entire Day 2 + Day 3 copy-draft re-implementation initiative.

**Still open**: the codebase hygiene sweep, the model-selection/token-usage content
idea (now also covering subagent/consumption-guardrail content, see the
Newly Identified Tasks entry below), Day 1's still-nonexistent copy-drafts,
and the site-wide workshop-name/em-dash/colon sweeps (deferred to Day 1's
eventual line-edit pass, not this one) remain unscheduled.

**2026-08-20, continued: `STUDENT_CLAUDE_GUIDE.md`'s three open threads
resolved in one pass.** User asked to prioritize this file specifically.
Closed: the line-1716 Claude-Desktop-vs-Claude-Code tooling gap (new
"Where this file kicks in" section), the submission-card file-structure
idea (new `SUBMISSION.md` template shipped at repo root, see
[ADR 0021](adr/0021-student-submission-metadata-file.md)), and the
model-selection/subagent-guardrail content seed (new "Choosing the right
model for the task" section, deliberately AI-in-the-loop after an early
draft put the burden on the student instead and was corrected mid-review).
Also reworked, per direct user request mid-pass: "How to explain things to
me" changed from Claude assuming the student's vocabulary level to Claude
asking the student directly via a short onboarding question set. Three
things intentionally left open rather than forced to a premature answer:
the `SUBMISSION.md` field set (provisional, two rounds of user edits mid-
review, explicitly to be revisited once seen in real use), the
demo-path-field question, and the harvesting mechanism for
`docs/students/index.html` — see the "Student submission cards" and
"Live-test `STUDENT_CLAUDE_GUIDE.md`" entries below. The guide itself is
not marked fully done until that live test happens.

**2026-08-20, continued: the above `SUBMISSION.md` work corrected after
missing prior ADRs.** Walking through how a student's fork would actually
work in Claude Desktop surfaced that this session's `SUBMISSION.md`/
`ADR 0021` work hadn't checked `project/adr/` first, and conflicted with
three already-accepted decisions:
[ADR 0003](adr/0003-daily-merge-branch-workflow.md) (per-day submission
folders), [ADR 0004](adr/0004-submissions-inside-docs.md) (path inside
`docs/`), and [ADR 0008](adr/0008-readme-driven-portfolio-data.md)
(README-driven portfolio data, hand-built pages). Reconciled directly with
the user and written up as
[ADR 0022](adr/0022-continuous-student-folder.md), which supersedes 0003's
folder-namespacing, 0008's data-source decision, and 0021 entirely. Net
result: one continuous folder per student
(`docs/submissions/your-name/`, replacing the per-day scheme), created
during Day 1's Fork & Submit, where both `SUBMISSION.md` and
`STUDENT_CLAUDE_GUIDE.md`-as-`CLAUDE.md` get **copied** (not moved, since
the root copies are linked from live pages) alongside the actual project
work. This also fixed a pre-existing bug in
`docs/day-1/08-fork-and-submit.html`/its Slides (missing `docs/` prefix on
the submissions path) and required reframing the Day 2 §03 `CLAUDE.md`
exercise (`docs/day-2/03-claude-md.html` + Slides +
`project/copy-drafts/day-2/03-claude-md.md`), since the file now arrives a
day earlier than that exercise originally assumed. Full detail in the
Phase 5 `STUDENT_CLAUDE_GUIDE.md` bullet and the "Student submission
cards" Newly Identified Task below.

**2026-08-20, end of day — session stopped on daily usage limit, picking up
tomorrow.** Quick orientation for next session, so it doesn't need to
re-read this whole file cold:

1. ~~First thing to do: finish validating the "Modulate how much the guide
   makes Claude ask vs. just act" fix.~~ **Done 2026-08-21** — redesigned,
   re-ran, confirmed passing with ground-truth-verified evidence. See the
   task itself in "Newly identified tasks" below for detail.
2. **Next up**: per the priority order worked out with the user on
   2026-08-20 (still valid, nothing since has changed it): **Day 1
   copy-drafts** is the biggest real content gap — Days 2/3 both got full
   copy-draft edit passes, Day 1 never started, and
   `09-project-assignments.html` is still a placeholder. Everything else
   in "Newly identified tasks" below (model-selection/subagent content
   planning, codebase hygiene sweep, workshop-name/em-dash sweep) can wait
   behind that. This hasn't been scoped yet — treat it as its own planning
   pass first (same pattern as the Day 2/3 copy-draft pilot got), not
   something to start implementing cold.
3. Also logged 2026-08-21, not yet scoped: a Claude-model comparison table
   (task fit, cost, consumption) as an idea for the still-unscoped
   model-selection content task below — not something to design now.

**2026-08-21, continued: quick-wins batch done, plus a real architecture
change (student submission cards go auto-generated).** Took stock of the
whole file and, per the user's choice, worked the small independent items
before Day 1 copy-drafts:

- **Spec-driven-dev content bug found and fixed**: the copy-pasteable
  starter prompt in `docs/day-2/06-spec-driven-dev.html` §3 had an
  `Implement` line ("Pieces that should probably get built and checked
  separately: [your answer]") that didn't tell a student what to actually
  write there, worded three different ways across the live HTML, Slides,
  and copy-draft (drift, not intent). Reworded to directly answer the
  checklist question above it in the same section: "The pieces I'll build
  and check one at a time, in the order I'd tackle them: [your answer]."
  Also renamed the code block's `starter-prompt.md` label to
  `spec-driven-starter-prompt.md` (all three files) so a student can find
  it later among their own files, and fixed a stray "architecutre" typo in
  the copy-draft.
- **`docs/setup-day-2.html` deleted** — confirmed fully orphaned (zero
  inbound links) and fully superseded by `setup.html`'s own "Days 2 and 3"
  section, which already covers the same install steps.
- **`docs/resources.html` Day 2 and Day 3 sections populated**, same
  prose-link style as Day 1's section, pulled from citations already
  live-verified inline on those days' pages (not fresh research) — 10
  Day 2 links across all 5 sessions including Plan Mode and Spec-Driven
  Development (missed on the first draft), 8 Day 3 links across all 4
  cited sessions including Human-AI Design's Google PAIR Guidebook and
  Vaccaro et al. meta-analysis (also missed on the first draft, then
  added after the user flagged it). Deliberately broad — user may trim.
- **`.github/pull_request_template.md` created** — a native GitHub
  feature, auto-populates the PR description box for anyone opening a PR
  against the repo with a short checklist matching Fork & Submit's actual
  flow (day-numbered branch, work confined to the student's own folder,
  `SUBMISSION.md` updated, no secrets).
- **`SUBMISSION_GUIDE.md` reconsidered, not built.** Original reason
  (ADR 0009) was stale — `setup.html`/`08-fork-and-submit.html` already
  point students to `STUDENT_CLAUDE_GUIDE.md` directly. Instead, enriched
  `SUBMISSION.md` itself: a note that it becomes a public card once
  merged, plus one example under each field's existing prompt — guidance
  lives where a student is already looking, no new file to maintain.
- **Real architecture change, not just a quick win**: mid-session the user
  asked to verify the submissions pipeline with a mock folder, which
  surfaced that no card-rendering mechanism existed at all yet
  (`docs/students/index.html` was a TODO stub). User wants cards
  **auto-generated live from `main`**, reversing ADR 0008/0022's
  hand-built-rendering decision (their `SUBMISSION.md`-as-data-source
  decision is unchanged). Written up as
  [ADR 0023](adr/0023-auto-generated-submission-cards.md): the site's
  first client-side use of GitHub's own public API — `docs/students/index.html`
  now discovers folders under `docs/submissions/` via the Contents API and
  renders each student's `SUBMISSION.md` as a card via new
  `docs/js/submissions-gallery.js`, same "fetch and render, no backend"
  pattern as `project-ideas.js` (ADR 0017). Full detail, including the
  named coupling/rate-limit/availability tradeoffs, in the ADR and in the
  "Student submission cards" task below.
- **Pipeline verified end-to-end, the original ask**: built a mock
  `docs/submissions/example-student/` (real `CLAUDE.md` + filled-in
  `SUBMISSION.md`, built the same way Fork & Submit's own instructions
  would produce one), confirmed via direct `curl` that the GitHub Contents
  API actually behaves as expected against this repo (including a real
  surprise: an empty `docs/submissions/` returns **404**, not an empty
  array — the renderer treats that as the empty state, not an error), unit
  -tested the field parser against hardcoded strings (filled, untouched
  placeholder, and missing-field cases), then ran a full browser
  (Playwright) test of the real page and script with the network calls
  mocked to return the mock student's data — confirmed the card renders
  with correct field values, the empty-state message shows on a 404, the
  error-state message shows on a real failure, and a missing field renders
  "Not yet filled in." instead of breaking the card. Mock folder deleted
  after verification, per the plan's default (not shipping a fake entry
  into what real students will see).
- **New task logged, not built**: per the user's request once this test
  wrapped, "Newly identified tasks" below now has a testing-strategy task
  — identify which of this project's bigger architecture bets (GitHub API
  dependency chief among them) warrant standalone, repeatable unit/
  integration tests, using today's ad-hoc verification (parser unit test +
  Playwright mocked-route integration test) as the proven starting
  pattern.

**2026-08-21, continued: Day 1 copy-drafts ported** (the biggest
remaining content gap named above), plus `resources.html` quick wins,
testing-strategy scoping, and a codebase-hygiene-sweep re-scope, all
worked in one session per the user's "all of it" call — em-dash sweep
dropped from scope since the user already did that manually.

- **Day 1 ported to `project/copy-drafts/day-1/*.md`**: all 9 real-content
  pages (`01-state-of-ai` through `08-fork-and-submit`, plus the bonus
  `people-to-follow` resource page), ~1,122 lines total, following the
  Day 2/3 convention in `project/copy-drafts/README.md`. Two recon passes
  ran first so the user could see impact before approving: a porting-
  scope pass (all 9 files, plus confirming `09-project-assignments.html`
  is still a TODO stub and not a port target) and a content-architecture
  audit checking Day 1 against the 6 patterns logged in
  `content-architecture-notes.md` from the Day 2/3 pass. That audit found
  Day 1's biggest gap is voice, not incidental drift — `01-state-of-ai`'s
  §1 heading and `04-product-discussion`'s §1 heading both bake first-
  person-plural directly into the `<h2>` ("The Moment We're In," "Why We
  Start Out Loud"), a structural choice, not a wording tweak. Per the
  copy-drafts workflow (Claude drafts a faithful mirror, the human makes
  editorial calls), these hotspots were flagged inline as `<!-- -->`
  comments in the affected files rather than silently resolved during
  porting, plus a new `project/copy-drafts/day-1/README.md` summarizing
  all the cross-page patterns (voice, citation-density-by-page-type,
  4 bare self-directed-question-lists, thin grounding on the 3 explainer
  pages) for the user to decide once before the line edit, per
  `content-architecture-notes.md`'s own ask. Three new components not yet
  in the copy-drafts convention (`.stat-pull`, `.stakes`, `.process-wheel`,
  `.chip-strip`, and a markdown-table mapping for `.resource-table`) got
  a documented representation added to `project/copy-drafts/README.md`'s
  Format section. Spot-checked 3 drafts against source HTML (citation
  counts, section counts, table row counts) — all matched exactly.
  **Line-by-line edit itself is still open** — that's the user's own pass,
  intentionally done last, not part of this porting step. See the "New
  workflow" task below for the updated status.
- **`resources.html` quick wins, `testing-strategy` scoping, and
  `codebase-hygiene-sweep` re-scoping**: see their own task entries below
  for what changed in each.

**2026-08-21, continued: home page & nav redesign implemented**, from a
design handoff delivered outside the repo (`Home.dc.html` + `README.md`).
Rebuilt `docs/index.html` (masthead, jump-to strip, numbered Workshop-Days
row list, Getting-Started cards — new `.home-*` classes in `style.css`, no
`briefing.css` dependency added) and `docs/partials/nav.html` (Day 1/2/3
collapsed into one "Days" menu with a second-level per-day flyout;
click+hover+outside-click+Escape all wired in `docs/js/nav.js`; logo moved
from nav to footer). See [ADR 0024](adr/0024-nav-home-redesign.md) for the
implementation decisions (single shared nav markup instead of the
handoff's duplicate desktop/mobile trees; day labels link to `/day-N/`
directly with a separate caret toggling the flyout; new `.is-active`
current-page state). Verified with Playwright against a local static
server (desktop click/hover, mobile tap-accordion, outside-click close,
active-link state, day-page navigation) — screenshots matched the
handoff's fidelity bar; zero console errors.

- **Found and fixed in the same pass, not part of the original handoff
  scope**: every nav/footer link rendered in `briefing.css`'s accent
  purple on every day/setup page (any `<body class="briefing">` page),
  regardless of state, because `.briefing a`'s specificity beat the nav's
  own link-color rules — invisible before because nothing contrasted
  against it; visible now that `.is-active` needed to actually stand out.
  Root cause and fix are in ADR 0024.
- **Follow-on, same session, after the user reviewed the live result**: a
  nav-brand emoji (🤖 + 🧠, picked via AskUserQuestion, moved from
  right-of-wordmark to robot-left/brain-right after a first pass put both
  on the right) and a new Instructors page — see the "Nav-brand emoji" and
  "Instructors page" entries below for what shipped vs. what's still open.
- **Two real Days-menu bugs found and fixed after the user tried it live,
  not caught in the original verification pass**: (1) clicking "Days" (or
  a day's caret) with a real mouse could silently close the menu instead
  of opening it — a genuine click-vs-hover event-ordering race, not the
  Playwright-only artifact it was first assumed to be; fixed by detecting
  hover-capable pointers and making click idempotent-open there instead of
  toggling. (2) A separate bug where clicking into the menu left it stuck
  visually open (via `:focus-within` in CSS) even after JS correctly
  closed it on mouseleave; fixed by removing the now-redundant
  `:focus-within` rule. Full root-cause writeup in the "Update, same day"
  section of [ADR 0024](adr/0024-nav-home-redesign.md) — including the
  admission that the first bug's symptom was actually seen during initial
  testing and wrongly dismissed instead of flagged.
- **Small fun addition, user-requested**: `docs/js/click-effect.js` — on
  any click anywhere on the site, a 🤖/🧠 pair pops at the cursor and
  fades over ~0.6s (skips the drift animation under
  `prefers-reduced-motion`). Wired onto all 59 real HTML pages (every
  Overview page and every Slides deck, not just partial-having pages) via
  a one-time batch script-tag insertion before `</body>`, verified none
  were double-inserted and every file still has exactly one `<body>`/
  `</body>` pair after.

**2026-08-21**: on `review/full-site-audit-6`. User felt `01-state-of-ai.md`
and `02-industry-conversation.md` (Day 1's first-ported copy-drafts,
predating the research-first discipline) read repetitive and shallower
than Day 2/3, and asked for a from-scratch, research-first rewrite of
both, explicitly not repeating Day 3's material. Both rewritten via 5
parallel background research agents plus a follow-up 6th for citation
currency; `03-use-cases.md` §4/§5 also grounded with real incidents per a
mid-pass user request. Full detail in the matching 2026-08-21 "Change
log" entry below. **Drafts only, awaiting user review** before any
`docs/day-1/*.html` implementation. Also drafted `project/copy-drafts/
instructors.md`'s two bios from public sources, pending the user's edit
pass (separate change-log entry).

Source of truth for build progress on this repo. Check here before starting
work; update here when a task starts/completes, or when new work is
discovered that wasn't in the original scope. Architecture *decisions* (the
"why") live in [`project/adr/`](adr/) — this file tracks the "what" and
"is it done."

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done

---

## Phase 1 — Foundation

- [x] Repo scaffold: `docs/` directory structure created
- [x] `docs/partials/nav.html`, `docs/partials/footer.html`
- [x] `docs/js/partials.js` loader script
- [x] `docs/css/style.css` (base reset, watercolor palette variables)
- [x] `docs/index.html`, `docs/resources.html` skeletons; `docs/setup.html` has real content now — see Phase 5
- [x] `vercel.json` + `package.json` deploy config
- [ ] Connect repo to Vercel and confirm live URL (requires account access —
      maintainer action, not something done from this session)
- [ ] Confirm a PR produces an automatic Vercel preview deployment

## Phase 2 — Proxy & rate limiting

- [ ] `api/claude-proxy.ts` serverless function
- [ ] Upstash Redis project created; rate limiting wired via `@upstash/ratelimit`
- [ ] Env vars configured in Vercel (`ANTHROPIC_API_KEY`, `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`)
- [ ] `max_tokens` cap + pinned cheaper model for public-proxy traffic
- [ ] Verify: request past rate limit returns a graceful error, not a pass-through to Anthropic

## Phase 3 — Content structure

- [x] `docs/data/schedule.json` authored (single source of truth for session times/types/titles) — **Day 1 times confirmed 2026-08-11**, **Day 2 times confirmed 2026-08-13**, **Day 3 times confirmed 2026-08-13** (10am–5pm, one AM break, matching Day 1's shape exactly on all three days — see the Day 3 change log entry below)
- [x] `docs/css/timeline.css`, `docs/js/timeline.js`
- [x] `docs/js/topic-metadata.js` — populates each topic page's time/duration/type badges and prev/next links from `schedule.json`
- [x] Day 1/2/3 `index.html` (timeline view, driven by `schedule.json`) — pattern works for all three; Day 2 and Day 3 both now have real learning-outcomes copy (2026-08-13)
- [~] Topic page template + topic pages — **Day 1 renumbered/renamed 2026-08-11** (Claude Desktop pivot — see below): `01-state-of-ai`, `02-industry-conversation`, `03-use-cases`, `04-product-discussion`, `05-problem-statement-discussion`, `06-ai-tools`, `07-explore-claude-desktop`, `08-fork-and-submit` all have real content; `09-project-assignments` is still a placeholder. `people-to-follow.html` also has real content but is unlisted/unscheduled (a resource page, not a numbered session — see below). **Day 2, all 8 topics built 2026-08-13. Day 3, all 7 topics built 2026-08-13** (see below). Every day now has real, scheduled content, except Day 1's `09-project-assignments` placeholder.
- [x] Briefing template, Overview page (`docs/css/briefing.css` Overview rules, `docs/js/reveal.js`) — normal scrolling page, shared nav/footer restored, reuses `topic-metadata.js`. See [ADR 0011](adr/0011-split-overview-and-slides.md) (supersedes [0010](adr/0010-briefing-template.md)'s toggle).
- [x] Briefing template, Slides page (`docs/css/briefing.css` deck rules, `docs/js/deck.js`) — paginated-only, self-contained chrome linking back to its Overview page, no schedule.json fetch. **8/8 Day 1 content-complete topics have a Slides companion** (Topics 1–5, 7, 8, 9); **all 8 Day 2 topics and all 7 Day 3 topics also have one**, built 2026-08-13, parity-checked against `project/scripts/check-slide-parity.js` (clean).
- [ ] Slides system for the *generic* template (`docs/css/slides.css`, `docs/js/slides.js`) — the original Part 6b plan; **not needed for briefing-template pages**, which get their slides via the deck pattern above instead. Only relevant if a generic-template page ever wants slides.
- [~] Responsive layout — handled via media queries inside `style.css`/`timeline.css`/`briefing.css` rather than a separate `responsive.css` file (simpler given how little CSS exists so far); revisit splitting it out if it gets unwieldy

## Phase 4 — Student showcase

- [x] `docs/students/index.html` hub page — **built 2026-08-21**, cards
      auto-generated client-side from `docs/submissions/` on `main` via
      GitHub's API, see [ADR 0023](adr/0023-auto-generated-submission-cards.md)
      and the "Student submission cards" task below.
- [x] ~~Student portfolio page template~~ — **superseded 2026-08-21**: per
      ADR 0023, a full page per student is explicitly out of scope for
      now. The card itself is the display unit, linking out to each
      student's fork via the Fork URL field.
- [x] ~~Extended `README.md` submission template (adds title/pitch + demo path fields)~~ — **superseded 2026-08-20** by `SUBMISSION.md` as its own dedicated file (see [ADR 0022](adr/0022-continuous-student-folder.md), which supersedes [ADR 0008](adr/0008-readme-driven-portfolio-data.md)'s README-based approach). Nothing left to build here.
- [x] `.github/pull_request_template.md` — **built 2026-08-21**, a short
      checklist matching Fork & Submit's actual flow.
- [x] ~~`SUBMISSION_GUIDE.md`~~ — **reconsidered 2026-08-21, not built**:
      the original reason (ADR 0009) was stale; guidance enriched directly
      into `SUBMISSION.md`'s own inline field prompts instead.

## Phase 5 — Content fill

- [~] Real content written for each of the 24 topic pages (originally scoped
      as 24, actual final count differs per day since each day's session
      count was recomposed during planning, not a fixed 8/day) — **Day 1:
      8/9 scheduled sessions done** (only `09-project-assignments` still a
      placeholder), plus `people-to-follow.html` as a bonus resource page.
      **Day 2: all 8/8 scheduled sessions done (2026-08-13). Day 3: all 7/7
      scheduled sessions done (2026-08-13)** — see the Day 2 and Day 3
      change log entries below for the full session lists and sourcing.
- [x] Slides populated per topic — **true for every Day 1 topic that has
      real content** (all 8 scheduled + `people-to-follow`), **every Day 2
      topic** (all 8), **and every Day 3 topic** (all 7), all built
      2026-08-13.
- [x] `docs/setup.html` — **rebuilt 2026-08-11 as Day 1 only**, with a real
      interactive checklist, ready to send to students. Day 2's setup
      content moved to a new, currently-unlinked `docs/setup-day-2.html`.
- [~] `STUDENT_CLAUDE_GUIDE.md` written (day-specific guidance students
      paste into their own Claude sessions — see
      [ADR 0009](adr/0009-separate-maintainer-claude-md.md) for why this
      isn't named `CLAUDE.md`). **Implemented 2026-08-19**, growing out of
      Adiel's PR #8 glossary note (see "Collaborator feedback — Adiel,
      PR #8" below) — three required sections, all written:
      1. Pedagogical-explanation instructions for Claude: don't
         over-explain; insert reflection checkpoints inviting the
         student to check their own understanding and ask for a simpler
         explanation if something didn't land.
      2. Common vibe-coding pitfalls: security/credential hygiene (never
         commit secrets, use env vars, check `.gitignore`), folder/code
         hygiene, using Plan Mode before going deep on an approach,
         testing with a smaller/cheaper model and matching model choice
         to task size, smart credential management generally.
      3. Using `gh`/git effectively for their own product repo — distinct
         from the Day 1 fork-and-submit *workshop-submission* flow
         already covered in `docs/day-1/08-fork-and-submit.html`:
         committing regularly, using PRs, general practices supporting
         good product design and development.
      **Linked task, implemented 2026-08-19**: reworked the Day 2 §03
      exercise in `docs/day-2/03-claude-md.html` (Overview + Slides) and
      `project/copy-drafts/day-2/03-claude-md.md:93-100`. New version:
      students copy `STUDENT_CLAUDE_GUIDE.md` in as their `CLAUDE.md` and
      ask Claude to update it based on what it observed about how they
      worked on Day 1, instead of generating cold via `/init`. The
      pending Batch 7 edits on that same page (file-viewer popup fix,
      paragraph weave, both in section 2, not section 4) were left
      untouched, as planned.
      **Revised 2026-08-20**, closing the three open threads logged
      against this file (see "Newly identified tasks" below for their
      full history): added a "Where this file kicks in" section
      orienting students to the Day 1 (Claude Desktop) → Day 2 (VS Code /
      Claude Code / GitHub Desktop) tooling shift, resolving the line-1716
      gap below; reworked "How to explain things to me" from
      assumption-based instructions into onboarding questions Claude asks
      the student directly; replaced the single model-choice bullet in
      "Things to watch for" with a new "Choosing the right model for the
      task" section, AI-in-the-loop (Claude surfaces model options and
      tradeoffs in plain language, student picks — not the student
      justifying a choice unprompted); added a "Keeping submission info
      current" section pointing at the new `SUBMISSION.md` (see task
      below); "Using git and GitHub" gained a line naming GitHub Desktop
      and Claude-Code-runs-git-directly as the two real paths, replacing
      the previous tool-agnostic phrasing. See
      [ADR 0021](adr/0021-student-submission-metadata-file.md) for the
      `SUBMISSION.md` decision specifically.
      **Corrected, same day, still 2026-08-20**: the above `SUBMISSION.md`/
      `ADR 0021` work didn't check existing architecture first and
      conflicted with it — [ADR 0003](adr/0003-daily-merge-branch-workflow.md)
      already had students working in a per-day folder
      (`submissions/day-N/name/`), [ADR 0004](adr/0004-submissions-inside-docs.md)
      already placed that inside `docs/`, and
      [ADR 0008](adr/0008-readme-driven-portfolio-data.md) already decided
      portfolio data comes from an extended `README.md`, not a separate
      file. Reconciled via [ADR 0022](adr/0022-continuous-student-folder.md),
      which supersedes 0003's folder-namespacing, 0008's data-source
      decision, and 0021 entirely: one continuous folder per student for
      the whole workshop (`docs/submissions/your-name/`, not per-day),
      `SUBMISSION.md`'s field set kept (superseding 0008's), and both
      `STUDENT_CLAUDE_GUIDE.md`-as-`CLAUDE.md` and `SUBMISSION.md`
      **copied** (not moved) into that folder during Day 1's Fork & Submit
      — moving would delete the root copies that `docs/setup-day-2.html`
      and `docs/day-2/03-claude-md.html` already link to. `STUDENT_CLAUDE_GUIDE.md`'s
      "Where this file kicks in" and "Keeping submission info current"
      sections updated to name the folder explicitly. This also meant
      reframing the Day 2 §03 `docs/day-2/03-claude-md.html` exercise
      (Overview + Slides + `project/copy-drafts/day-2/03-claude-md.md`):
      since `CLAUDE.md` now arrives Day 1, not Day 2, the exercise shifted
      from "copy it in" to "review and update what's already there,"
      including explicitly asking students to reconsider whether every
      guardrail still earns its place after a day of real use.
      **Not yet considered complete**: needs a live test on a real project
      (not just a read-through) before this bullet closes for good — see
      the "Newly identified tasks" entries below.
- [x] `resources.html` populated with real links — established pattern:
      when a topic's review turns up a genuinely useful external
      compilation/reference (not something we'd host/maintain ourselves),
      link it from the relevant day's section here as it's found, rather
      than waiting for a dedicated content-fill pass. Day 1 entry: the
      newsroom AI policies index (from Topic 2). **Day 2 and Day 3
      populated 2026-08-21** (10 and 8 links respectively, drawn from
      citations already live-verified inline on those days' pages) —
      deliberately broad first drafts, flagged as open to trimming.
- [x] ~~Sample/placeholder student portfolio pages created for 2-3
      students to validate the template~~ — **superseded 2026-08-21**: no
      separate page template exists anymore (ADR 0023, cards are the
      display unit). Validated instead via a mock
      `docs/submissions/example-student/` run through a full Playwright
      render test, then deleted rather than left as a permanent sample —
      see the "Student submission cards" task below.
- [x] **`resources.html`'s "AI Tools Landscape" wrapped in a collapsible.**
      Raised 2026-08-21 — the ~20-tool, 7-category list was dominating the
      page above the fold. **Built**: a new `.collapsible`/`.collapsible-body`
      component in `docs/css/style.css` (native `<details>`/`<summary>`,
      closed by default, matches the `.file-viewer-inline` disclosure
      pattern already used elsewhere per
      [ADR 0020](adr/0020-file-viewer-inline-collapsible.md), though a
      separate component since `resources.html` doesn't load
      `briefing.css`). Verified open/closed states visually via
      Playwright.
- [x] **Wrap `resources.html`'s other sections in the same collapsible.**
      Raised 2026-08-21, right after the AI Tools Landscape collapsible
      shipped — user liked the pattern and wants Day 1/2/3 Resources
      (each a plain `<section>` today) converted to the same
      `.collapsible`/`.collapsible-body` disclosure. **Built 2026-08-21**:
      all three sections converted, defaulted **open** (`<details
      class="collapsible" open>`) unlike AI Tools Landscape's closed
      default — per the reasoning logged when this was raised, these
      lists are shorter and more likely something a visitor wants to see
      immediately. Verified via a local static server + Playwright: all
      three open by default, toggle closed on click, no JS dependency
      (the `.collapsible` CSS is pure `<details>`/`<summary>`, already
      confirmed as the only usage pattern in `docs/`).
- [x] **Remove `resources.html`'s "Tools & Setup" section entirely.**
      Raised 2026-08-21. It's two placeholder link-TBD entries (GitHub,
      Claude Code / VS Code setup) that were never filled in and are now
      redundant with `setup.html`'s actual install instructions. **Removed
      2026-08-21**, confirmed via Playwright that the section no longer
      renders on the page.
- [x] **Review the AI Tools Landscape list for currency.** Raised
      2026-08-21, alongside the collapsible change above. Pricing and
      tool relevance in that list (Claude, ChatGPT, Gemini, Perplexity,
      Cursor, Midjourney, etc.) haven't been re-verified since originally
      written and drift fast — needs a research pass to confirm the list
      is accurate before treating it as final, not just a copy edit.
      **Researched and updated 2026-08-21** (background research agent,
      all 22 tools checked against current pricing pages): 9 of 22 had
      drifted and were corrected — **DALL-E** was retired by OpenAI in
      May 2026 and replaced with **GPT Image 2** (swapped in, with a note
      explaining the replacement, since this is a bigger change than a
      price tweak); **Replit**'s "Boost" tier was renamed "Core" and its
      price rose $13→$25/mo ($20 annual); **Airtable**'s "Pro" tier was
      renamed "Team" and priced per-seat, roughly doubling from the
      site's stated figure; **Canva** Pro rose $13→$18/mo; **Synthesia**'s
      range shifted $30–60→$29–89/mo; **Gemini**'s paid tier was renamed
      "Advanced"→"Google AI Pro" ($19.99/mo, the price itself was already
      close); **Descript**'s "Pro" tier was renamed "Hobbyist" ($16/mo
      annual); **ElevenLabs** Starter dropped $11→$6/mo; **Make** Pro rose
      $15→$16/mo. The other 13 tools (Claude, ChatGPT, Perplexity, Claude
      Code, GitHub Copilot, Cursor, Midjourney, Zotero, Google Scholar,
      Jupyter + Claude, Zapier) checked out as current, no changes made.

---

## Newly identified tasks

Tasks discovered during build that weren't in the original plan. Add here as
found; promote into a phase above once scoped, or leave here if it doesn't
map cleanly to one.

- [ ] **Day 1 citation-grounding rework.** Raised 2026-08-21 — the user
      wants Day 1 to go through the same editorial discipline Day 2/3 got:
      research surfaces real sources → prose gets rewritten to match
      *exactly* what the source supports (named people/orgs/numbers,
      hedged confidence where sourcing is weaker) → each page's
      **Sources** list gets reconciled against its inline `[n]` usage.
      Not "bolt citations onto what's already written" — verify and
      tighten to match. This is the user's own line-by-line pass, done in
      a fresh session — this entry is the scoped brief for that session,
      not a scoping task itself. Everything below is already documented
      in `project/copy-drafts/day-1/README.md` and
      `project/content-architecture-notes.md` (both written during the
      2026-08-21 porting pass) — re-read those two files first; this is a
      pointer into them, not a duplicate.
      - **Triage** (a recommendation, confirm/adjust before editing):
        - *Tier 1 — verify existing citations against sources, add
          workshop-specific framing*: `01-state-of-ai` (24 citations,
          already specific/traceable — furthest from voice target, bakes
          first-person-plural into its §1 heading), `03-use-cases` (25
          citations, verified specific/traceable by reading the live
          page — flagged "generic/theoretical" in-draft, which on
          inspection means thin workshop framing, not weak sourcing; its
          two example lists were also just collapsible-wrapped, see the
          "Use-cases collapsible" entry below — that's a structural
          change only, doesn't touch the citation work here).
        - *Tier 2 — needs new/better sourcing*: `02-industry-conversation`
          (one citation explicitly self-flagged "no URL — reflects
          general perception, not a formal study" — the clearest case for
          new research), `05-problem-statement-discussion` (1 citation),
          `people-to-follow` (1 citation, thin grounding).
        - *Tier 3 — skip, working as designed*: `04-product-discussion`
          (voice/heading fix only, zero citation work needed),
          `06-ai-tools`, `07-explore-claude-desktop`,
          `08-fork-and-submit` (all zero-citation activity pages, already
          closest to the target pattern).
      - **Cross-cutting decisions to make once, up front**, not
        page-by-page: voice (facilitator "we" vs. the declarative
        narrator voice used elsewhere — affects `01`§1/`04`§1 headings
        specifically, smaller instances in `02`/`05`/`07`);
        citation-density-vs-conciseness (if trimming, keep the Sources
        list in sync); named sub-headings for the 3 remaining bare
        self-directed-question lists (`02`§5, `05`§3, `06`§2 — Day 2's
        `01-debrief.md` "### Self Reflection" is the model).
      - **Not started** — no line-by-line editing, no new source
        research done yet.
- [x] **Use-cases collapsible.** Raised 2026-08-21, same planning session
      as the task above, while scoping it — the user separately wanted
      `docs/day-1/03-use-cases.html`'s two long example lists (§s2, 9
      rows; §s3, 11 rows) to stop reading as clunky embedded content.
      **Done same day**: wrapped each `<dl class="roster">` in
      `<details class="collapsible"><summary>See all N examples</summary>
      <div class="collapsible-body">...</div></details>`, closed by
      default — the exact pattern already used for `resources.html`'s "AI
      Tools Landscape" block, no new CSS needed. `.block-head`
      (eyebrow/`<h2>`) and section IDs (`#s2`/`#s3`) were left untouched
      on purpose, since the page's own TOC and `resources.html`'s
      existing links anchor to them — verified both still work. Citation
      popovers (`<sup class="cite">`) still function inside the opened
      collapsible. No new files, no slides-deck change, no
      `resources.html` change, no copy-draft change.
- [x] **Nav-brand emoji.** Raised 2026-08-21, mid-session, during the nav/
      home redesign. User picked 🤖 + 🧠 (robot, human brain — no heart)
      via AskUserQuestion. **Done same day**: added to
      `docs/partials/nav.html`'s brand wordmark, both wrapped in
      `aria-hidden` spans (`.site-nav-brand-emoji` in `style.css`) so
      screen readers still just hear "AI News Innovation Workshop."
      **Repositioned same day**: first pass put both emoji on the right;
      corrected to robot on the left, brain on the right
      (`.site-nav-brand-emoji--left`/`--right` for the differing margins).
- [~] **Instructors page.** Raised 2026-08-21, same session — profiles for
      Andrew and Adiel. User confirmed it should be linked from the end of
      the top-level nav, and picked the "stub page + copy-draft" option
      via AskUserQuestion over "nav link only." **Scaffolding done same
      day**: `docs/instructors.html` (two `.idea-card` placeholders,
      reusing the existing generic card component rather than inventing a
      new one), nav link added at the end of `docs/partials/nav.html`
      (after Setup), `project/copy-drafts/instructors.md` created with
      placeholder title/bio fields for both — flagged inline as not a
      normal Overview-page-mirror draft (no citations/sections) since this
      isn't a schedule-tied topic page. **Still open**: actual bio copy,
      titles, and (optionally) photos — none supplied yet. Once
      `instructors.md` is filled in, port it into the two `.idea-card`
      blocks in `docs/instructors.html` per the usual copy-drafts
      workflow (see [copy-drafts/README.md](copy-drafts/README.md)).
- [~] **Student submission cards, auto-populated from a standardized fork
      file structure.** Raised 2026-08-20, mid-session, while working on the
      copy-drafts re-implementation pass. **Scoped and implemented
      2026-08-20, then corrected same day**: a single pre-built template
      file, `SUBMISSION.md`, shipped at repo root so every student fork
      inherits it. First pass (`ADR 0021`) put it in a `submissions/day-N/`-
      style scheme without checking prior art; that conflicted with
      already-accepted [ADR 0003](adr/0003-daily-merge-branch-workflow.md)/
      [0004](adr/0004-submissions-inside-docs.md)/[0008](adr/0008-readme-driven-portfolio-data.md)
      and was corrected via [ADR 0022](adr/0022-continuous-student-folder.md)
      (supersedes 0003's folder-namespacing, 0008's data-source decision,
      and 0021 entirely). Current state: one folder per student,
      `docs/submissions/your-name/`, used across all three days (not
      per-day); both `SUBMISSION.md` and `STUDENT_CLAUDE_GUIDE.md`-as-
      `CLAUDE.md` copied (not moved) into it during Day 1's Fork & Submit,
      root copies left intact since they're linked from live pages.
      `STUDENT_CLAUDE_GUIDE.md`'s "Keeping submission info current" section
      instructs Claude to help students fill `SUBMISSION.md` in early and
      keep it updated through restructures.
      **Confirmed scale**: 5–7 student forks, not dozens.
      **Reversed 2026-08-21**: ADR 0008/0022's "hand-built, not
      auto-generated" rendering stance is superseded by
      [ADR 0023](adr/0023-auto-generated-submission-cards.md) — the user
      asked for a live pipeline test (a mock folder run through Fork &
      Submit's own instructions, checked against a rendered card), which
      surfaced that no rendering mechanism existed at all yet, and decided
      cards should auto-generate from `main` instead of being transcribed
      by hand. `SUBMISSION.md` stays the data source (0008/0022's
      unchanged part); only the rendering mechanism changed. Built:
      `docs/js/submissions-gallery.js` (GitHub Contents API to discover
      `docs/submissions/` folders, `raw.githubusercontent.com` to fetch
      each `SUBMISSION.md`, parsed client-side — no manifest, no CI, no
      backend, same pattern as `project-ideas.js`/ADR 0017) and
      `docs/students/index.html`, now wired to it.
      **Pipeline verified end-to-end 2026-08-21**: a mock
      `docs/submissions/example-student/` (real `CLAUDE.md` copy + a
      filled-in `SUBMISSION.md`) exercised the actual fetch → parse →
      render path via a Playwright browser test with the network calls
      mocked to the mock student's data — confirmed the card renders
      correctly, an empty `docs/submissions/` (real finding: this 404s,
      not an empty array) shows the empty-state message, a real API
      failure shows the error-state message, and a missing/unfilled field
      renders "Not yet filled in." instead of breaking. Mock folder
      deleted afterward rather than kept as a permanent sample.
      **New coupling risk, named in ADR 0023**: `SUBMISSION.md`'s field
      set is still provisional (see below) — a field *rename* breaks
      parsing for that field until `submissions-gallery.js` is updated to
      match, mitigated by matching on field-label text rather than line
      position and failing per-field rather than breaking the whole card,
      but the coupling itself is real, not eliminated. Worth weighing
      before the field set changes again.
      **Still open, not resolved by this pass**:
      - The field set (see `SUBMISSION.md` itself — the user has been
        revising it directly) is **provisional**, flagged as wanting to be
        seen in real use before finalizing. Revisit once students have
        actually filled one in — and now that rendering is automated, a
        field-set change has a real downstream cost, see above.
      - Whether a demo-path field should be added back — it was in the
        original Phase 4 scope and earlier drafts of this task, but isn't
        in the current field set; unclear if that was deliberate.
      - A separate full portfolio page per student (distinct from the
        card) is explicitly out of scope per ADR 0023, not just
        unresolved — the card is the display unit for now.
- [ ] **New: identify standalone unit/integration tests for this
      project's bigger architecture bets.** Raised 2026-08-21, right after
      the submission-cards pipeline test above. User's reasoning: as this
      site takes on real external dependencies (GitHub's API being the
      first, via ADR 0023) rather than just static HTML/CSS/JS, there
      should be a repeatable way to notice when something breaks and fix
      it, not just discover it live. **Not scoped or built yet** — this is
      a planning task: go through the project's architecture decisions
      (`project/adr/`) and identify which ones are actually load-bearing
      enough to warrant a standalone, repeatable test, versus which are
      static enough that a test would just be overhead.
      `docs/js/submissions-gallery.js`'s dependency on GitHub's public API
      is the clearest current candidate — it's the site's only runtime
      call to a service this project doesn't control, and its two edge
      cases (an empty `docs/submissions/` 404ing rather than returning an
      empty array; a missing/renamed `SUBMISSION.md` field) were only
      caught by hand this session, not by anything repeatable.
      `check-slide-parity.js` is the one precedent already in the repo for
      what a standalone, repeatable check looks like here, though it
      checks content parity, not runtime behavior.
      **Concrete starting pattern, proven this session but not yet saved
      to the repo** (built as scratch verification, not committed): a
      parser unit test (hardcoded `SUBMISSION.md` strings — fully filled,
      untouched placeholder, missing field entirely — checked against
      expected parsed output, no network) plus a Playwright integration
      test (real page, real script, network calls mocked via
      `page.route()` to return canned responses) covering the populated,
      empty-404, error, and missing-field states. When this gets scoped:
      decide whether to formalize these into `project/scripts/` (matching
      `check-slide-parity.js`'s precedent) and whether Playwright becomes
      a tracked project capability (it was available this session via
      `npx`, not as a project dependency) or stays an ad-hoc tool.
      **Scoped 2026-08-21** (still not built — this pass is the recon and
      recommendation, not the implementation): `package.json` currently
      has zero `devDependencies`/`dependencies`/`scripts` at all, so
      adding repeatable tests means introducing tooling from scratch, not
      extending something that already exists. `project/adr/` has 23
      entries; ADR 0023 (GitHub API dependency) is the clear standout —
      it's the only ADR describing a runtime call to a service this
      project doesn't control, with two edge cases (the empty-folder 404,
      a renamed `SUBMISSION.md` field) that were only caught by hand.
      Everything else in `project/adr/` describes static HTML/CSS/JS
      structure or one-time build decisions — not load-bearing in the
      same way, so not recommending standalone tests for those.
      **Recommendation**: formalize the parser-unit-test half of this
      session's proven pattern into `project/scripts/` now, matching
      `check-slide-parity.js`'s shape exactly (plain Node, no framework,
      run manually via `node project/scripts/<name>.js`) — that part adds
      no new dependency. The Playwright integration-test half is a real
      **new-dependency decision** (`package.json` goes from nothing to a
      tracked `devDependency`), which per this repo's own CLAUDE.md
      warrants an ADR if committed to, not something to slip in as a side
      effect of a scoping pass. **Left as an open yes/no for the user**:
      keep Playwright ad-hoc (`npx`, as used this session and for the
      resources.html Playwright checks in the same 2026-08-21 session) or
      commit it as a tracked devDependency with its own ADR. Neither the
      parser script nor Playwright-as-dependency has been built yet —
      this entry is the scoping conclusion only.
- [x] **Rename "AI-Human Design" to "Human-AI Design," site-wide.** Decided
      2026-08-20 while editing `project/copy-drafts/day-3/04-ai-human-design.md`
      (its H1 already reads "Human-AI Design"; `01-recap.md`'s summary
      updated to match). **Implemented 2026-08-20**, as part of that page's
      full copy-draft re-implementation (see the Day 3 §04 restructure
      below): `docs/data/schedule.json` (`"title"`),
      `docs/day-3/04-ai-human-design.html` (title tag, H1, breadcrumb,
      masthead), `docs/day-3/slides/04-ai-human-design-slides.html` (title,
      chrome-eyebrow, cover-title), and `docs/partials/nav.html`'s dropdown
      entry, which the original scoping missed. Filename left unchanged, as
      planned.
- [x] **Day 3 schedule: shift 15 min from Where Can You Take This to Final
      Coding Time.** Raised 2026-08-20. **Implemented 2026-08-20** as part
      of the copy-draft re-implementation pass: `docs/data/schedule.json`
      updated, Final Coding Time 60→75 min (2:00-3:15 PM), Where Can You
      Take This 45→30 min (3:15-3:45 PM), Final Show & Tell unchanged at
      3:45 PM. Both pages' Overview and Slides cover-meta updated to match
      (Slides hardcodes this per ADR 0011, so it needed a manual edit, not
      just the JSON change). §05's content (3 slides, including the
      reflection/discussion slide) was carried over as-is, not further
      trimmed for the shorter 30-minute slot — worth a facilitator's eye
      the first time it's actually run at this length, since that's not
      something a copy pass alone can validate.
- [x] **Day 3 schedule: Final Show & Tell must start at 4:00 PM, not
      3:45 PM.** Raised 2026-08-21. Faculty were invited for 4:00 PM
      specifically, so the schedule had to move to match. **Implemented
      2026-08-21**: `docs/data/schedule.json` updated. Final Coding Time
      and Where Can You Take This are unchanged (2:00-3:15 PM, 3:15-3:45 PM).
      A new 15-minute break (`day-3/break-2`) was inserted at 3:45 PM.
      Final Show & Tell now starts at 4:00 PM, compressed 60→50 min.
      Closing & Celebration now starts at 4:50 PM, compressed 15→10 min.
      Total PM span still ends 5:00 PM. §07's Slides cover-meta was
      updated to match by hand (Slides hardcodes this per ADR 0011); the
      Overview page's masthead-meta and both pages' prev/next nav read
      schedule.json directly, so no manual edit was needed there. The new
      break needed no timeline/CSS changes, `docs/js/timeline.js` already
      renders any session with `url: null` as a break-styled item,
      established by the existing `day-3/break-1`.
- [ ] **New content: model selection, token usage, choosing smaller models
      for sub-tasks, and now also subagent/consumption guardrails.**
      Raised 2026-08-20 while reviewing
      `project/copy-drafts/day-3/04-ai-human-design.md`. **Not scoped —
      explicitly deferred to a planning conversation later, not something
      to design now.** Open question from the user, unresolved on
      purpose: does this need its own section (replacing something), or
      can it be sprinkled into existing Day 2 sections instead? User's
      instinct leans toward the latter, but wants to explore/plan it
      together before deciding. Note for that future conversation: there's
      already a small seed of this idea in `STUDENT_CLAUDE_GUIDE.md`'s
      pitfalls section ("testing with a smaller/cheaper model and
      matching model choice to task size") — worth checking for overlap
      before scoping this further, so the two don't end up saying the
      same thing in two places.
      **Extended, same day, still 2026-08-20**: a live example of this
      exact topic came up mid-session (this repo's own build work), when
      the user asked Claude to introspect on whether its own subagent
      spawning was judicious, given a large share of session usage was
      coming from the Agent/Task subsystem. That exchange (a self-
      assessment of actual agent-call costs in this session, plus
      guardrail advice: explicit effort caps in agent prompts, preferring
      Explore over general-purpose for read-only tasks, cheaper-model
      overrides for simple lookups, and checking Claude Code's actual
      cost-breakdown/settings mechanics rather than guessing) is exactly
      the kind of practicable guidance this future content should cover,
      not just "smaller models exist." When this gets planned: decide
      whether subagent/guardrail management is its own beat within this
      content or folded into the model-selection material, and where it
      fits relative to the existing `STUDENT_CLAUDE_GUIDE.md` pitfalls
      seed.
      **`STUDENT_CLAUDE_GUIDE.md` side implemented 2026-08-20**: the old
      passive pitfalls-seed bullet was replaced with a standalone
      "Choosing the right model for the task" section — deliberately
      **AI-in-the-loop**, not student-burdened: Claude surfaces the model
      options and their tradeoffs in plain language before a subtask, and
      the student picks, rather than being expected to justify a choice
      unprompted (an earlier draft got this backwards and was corrected
      mid-review). **Still open**: the broader in-class content question
      (a dedicated Day 2 lesson vs. just this guide content) — this pass
      only closes the guide-side seed, not the bigger unscoped idea above.
      **New idea, 2026-08-21, still not scoped — address in the future
      planning conversation, not now**: a reference table of Claude models
      (Haiku, Sonnet, Opus, etc.) with the practical decision-making
      information students would actually use — what kind of task each is
      best suited for, relative cost, how token-consumptive it is, and
      whatever else practitioners typically weigh (context window, speed,
      reasoning depth). Would live somewhere in this same model-selection
      content once it's actually scoped — exact placement (its own
      section, a resource-page table, folded into Day 2) is part of what
      that future planning conversation needs to decide, same as the rest
      of this task.
      **New idea, 2026-08-22, still not scoped**: a plain-language
      explainer of Claude Code's own context/token-management controls
      came up in this session (the user was actively confused about how
      to use them) and is worth folding into this same content once it's
      scoped, since it's the same underlying skill ("manage your usage
      deliberately") as model selection. What was actually explained,
      reusable as a first draft when this gets built:
      - **`/clear`**: wipes the conversation entirely and starts fresh
        (CLAUDE.md/memory/skills reload automatically). Use when the next
        task is genuinely unrelated to the current thread.
      - **`/compact`**: condenses the conversation so far into a summary
        and keeps going in the same session, continuity preserved, detail
        traded away. Use at a natural task boundary when staying in the
        same thread but not needing the full blow-by-blow of what led here.
      - **Rewind** (Esc Esc): an undo, not a token-management move, rolls
        conversation and/or file state back to an earlier checkpoint. Use
        to correct a wrong turn, not to save tokens (though it has that
        side effect).
      - **Auto-compact**: happens automatically near the context limit, no
        user action needed, worth saying explicitly so students don't
        think they have to manage this by hand.
      - **Background agents/subagents** as a token-management technique in
        their own right, not just a delegation tool: a subagent's search/
        fetch noise stays in its own context, only its summary lands in
        the main thread. This is arguably the highest-leverage lever for a
        long working session and ties directly to the existing subagent-
        guardrail material already logged above (2026-08-20 entry).
      Also worth deciding when this gets scoped: whether this belongs in
      `STUDENT_CLAUDE_GUIDE.md` itself (a natural fit alongside "Choosing
      the right model for the task") or in Day 2's in-class content, same
      open question as the rest of this task.
- [x] **Live-test `STUDENT_CLAUDE_GUIDE.md` on a real project.** Raised
      2026-08-20, right after the guide's onboarding-questions/model-choice/
      submission-info rework (see the Phase 5 bullet above).
      **Done 2026-08-20**: ran a fresh subagent session with `CLAUDE.md`
      (copied from `STUDENT_CLAUDE_GUIDE.md`) in a scratch project, given a
      plausible Day 1/2 student request (an RSS headline summarizer, no
      coding background). What worked: all three onboarding questions
      asked verbatim-in-spirit, genuinely stopped rather than guessing
      answers and continuing; credential hygiene flagged proactively before
      it was relevant; `SUBMISSION.md` correctly left unfilled rather than
      guessed, since there was no real project direction yet.
      **Surfaced two real gaps, not yet fixed — see the new task right
      below**: the guide gives no guidance on safe pre-work scaffolding
      (a folder, `.gitignore`, stub script) before onboarding questions are
      answered, so the test session defaulted to 100% asking, zero
      building; and the "more than a file or two" Plan Mode trigger has no
      real line, a first scaffold is often 4-5 trivial files that's still
      one small conceptual unit. Caveat: this validates the *instructions*
      produce the intended behavior once read, not whether Claude Desktop/
      Code actually auto-discovers `CLAUDE.md` the way documented — that
      mechanism is still unverified directly.
- [x] **Modulate how much the guide makes Claude ask vs. just act, based on
      the onboarding-question answers themselves.** Raised 2026-08-20,
      directly off the live-test findings above. User's concern: the
      guide's current asking-first instinct is correct in spirit
      (students shouldn't have to make every choice, Claude should suggest
      and explain) but shouldn't fully stall real development either.
      **Designed and implemented 2026-08-20**, same day, once the user
      came back to it: broadened "How to explain things to me"'s second
      onboarding question from just "when something breaks" to also cover
      "when we're starting something new" — one question now covers both
      error-handling explanation depth *and* general build-vs-ask pacing,
      with an explicit line stating the answer is the default for how much
      to build before checking in generally, not just for explanations.
      Deliberately reused the existing question rather than adding a
      fourth one, to keep the file from growing.
      Resolves both concrete gaps the live test found: **(1) pre-work
      scaffolding ambiguity** — now governed directly by the broadened
      question's answer, instead of being unaddressed. **(2) the fuzzy
      Plan-Mode file-count trigger** — reworded to be explicitly about risk/
      reversibility only ("expensive or awkward to undo"), a hard safety
      net that holds regardless of the calibration answer, with an
      explicit carve-out that a first rough scaffold isn't what it's about
      even if it's more than a file or two — deferring that specific case
      to the calibration question instead of counting files.
      **Live-test finished and confirmed working, 2026-08-21.** First
      attempt (2026-08-20) was inconclusive: the two-turn structure
      (spawn agent → get turn 1 → `SendMessage` a resumed/backgrounded
      agent with turn 2 answers) produced a truncated-looking response
      that only did model-selection research and created no files,
      despite a "just go" instruction — never resolved whether that was
      the guide's wording or a test-methodology artifact. Redesigned the
      test to close that gap: one **single foreground agent call**
      presenting the full exchange (opening request + calibration answers)
      in one shot, rather than a resumed background turn — and per the
      user's request, run on **Haiku 4.5** (`model: "haiku"`) to avoid
      burning tokens on a repeat test, on the reasoning that this is
      primarily an instruction-following check, not a deep-reasoning one.
      **Clean pass, ground-truth verified** (checked the scratch
      directory directly, not just the agent's self-report): given a
      "just go, build a rough first version" pace answer, it actually
      created a real, appropriately-rough scaffold (`summarize_feed.py`,
      `requirements.txt`, `.env.example`, `.gitignore`, `README.md`) and
      made one `git commit`, unprompted, matching "Using git and GitHub."
      `.gitignore` correctly excluded `.env` (credential hygiene). Model
      choice was handled silently, correctly citing "only when
      non-obvious" from the student's own answer, rather than turning
      into a blocking question. Plan Mode correctly did not trigger, and
      the agent's self-assessment quoted the exact "Things to watch for"
      line that justified skipping it. `SUBMISSION.md` was filled in with
      real, relevant project content once there was an actual direction,
      matching "Keeping submission info current." **This closes out the
      task — the fix works as designed.**
      **Noted but not acted on**: the same "make Claude suggest instead of
      asking for every choice" principle could arguably extend to
      "Choosing the right model for the task" too (still always asks
      before proceeding), but that wasn't a live-test finding, so left
      alone rather than scope-creeping this pass.
- [ ] **Codebase hygiene sweep: non-functional breadcrumbs and AI slop.**
      User noticed, while reviewing the Day 2 copy-draft edit pass, that
      the repo has accumulated HTML comments and other non-functional
      artifacts left behind by AI-assisted editing (pending-edit notes,
      structural TODOs, dangling comments that now describe an already-
      resolved state — see the 2026-08-20 review of the Day 2 copy-draft
      edits for concrete examples in `03-claude-md.md` and
      `04-skills-best-practices.md`). **Deferred, not scoped yet.** When
      picked up: sweep `docs/` and `project/copy-drafts/` for HTML
      comments and other non-functional markers that are stale, resolved,
      or were never meant to ship; distinguish "genuinely still pending"
      from "leftover scaffolding" before deleting anything. Same pass
      should look more broadly for other AI-slop patterns (dead code,
      unused citations left in a Sources list after the sentence citing
      them was cut, orphaned components) since the effect is the same:
      wasted tokens on every future session that reads these files, on
      top of being confusing to a human reader. Also see
      [content-architecture-notes.md](content-architecture-notes.md) for
      editorial (not code) patterns from the same review, kept for the
      eventual Day 1 pass rather than as a task here.
      **Re-scoped 2026-08-21** (recon only, nothing swept yet): grepped
      `docs/` and `project/copy-drafts/` for `<!-- -->` HTML comments —
      found almost none. Only two real hits, both false positives: a JS
      regex literal in `docs/js/submissions-gallery.js` that merely
      contains the string `<!--`, and one line in this project's own
      `project/copy-drafts/README.md` that mentions HTML comments as a
      category, not an actual comment. So the "stale/resolved comment"
      framing this task was raised under doesn't describe a real backlog
      — by the time of this recon, the Batch-7-era comments the user
      originally flagged (in `03-claude-md.md`/`04-skills-best-practices.md`)
      had already been cleared during the Day 2/3 copy-draft
      implementation pass. **What the sweep actually found instead**: 7
      literal `TODO` placeholders visible on live pages —
      `docs/day-1/index.html:16,20` (the day's summary copy) and
      `docs/day-1/09-project-assignments.html:27,32,33,41,45` (already a
      known-unwritten placeholder page, tracked separately in Phase 3/5
      above). Not fixing either today: `index.html`'s summary depends on
      Day 1's content actually being finalized, which this session's
      copy-draft port is a step toward but doesn't complete, and
      `09-project-assignments` is already correctly tracked elsewhere.
      **Note for whoever picks this up next**: the Day 1 copy-drafts
      ported this same session (`project/copy-drafts/day-1/*.md`)
      intentionally carry new `<!-- -->` comments flagging content-
      architecture hotspots (voice, bare question lists) per the
      established convention — those are exactly the "genuinely still
      pending" kind this task's own framing says to leave alone, not
      examples of the slop it's meant to catch.
- [~] **New workflow: `project/copy-drafts/`, markdown copy drafts for
      direct editing.** User found dictating copy edits turn by turn (the
      pattern used for the round-3 audit's Batches 1–7) slow and lossy.
      Pilot: all 8 Day 2 Overview pages ported to
      `project/copy-drafts/day-2/*.md` (2026-08-16), one file per topic,
      with a documented convention (see `project/copy-drafts/README.md`)
      for citations, comparison columns, term/definition rosters,
      numbered steps, and exercises. Pages with pending Batch 7 feedback
      (`01-debrief`, `02-prompting`, `03-claude-md`, `04-skills-best-practices`)
      carry inline HTML-comment notes pointing back to that feedback
      rather than pre-guessing final wording. Slides decks aren't
      ported, still a Claude-authored condensation of Overview at
      implementation time. **Deferred to a new branch, not
      `review/full-site-audit-3`** — tracked as part of the broader
      full-site line-by-line edit pass,
      [GitHub issue #6](https://github.com/AndrewRCalderon/2026-ai-news-innovation-workshop/issues/6)
      (Adiel tagged there for visibility; supersedes the earlier, now
      closed, issue #5, which scoped this too narrowly to just Day 2).
      This branch ships with the drafts present but unedited/unimplemented.
      **Extended to Day 3, 2026-08-19**: pilot held up, so all 7 Day 3
      Overview pages ported to `project/copy-drafts/day-3/*.md`, same
      convention, no new structural cases needed except a `[Stat
      callout: ...]` bracketed note for `.stat-pull` (not seen in Day 2,
      first used on `02-product-design.md` and `04-ai-human-design.md`).
      Ported from current (post-PR-#8-implementation) site content, not
      the pre-rewrite version, so `02-product-design`,
      `04-ai-human-design`, and `05-where-you-can-take-this` already
      reflect this session's rewrites — the Capelouto citation gap on
      `05` is flagged inline in its draft too, same as the live page.
      **Extended to Day 1, 2026-08-21**: all 9 real-content pages ported
      to `project/copy-drafts/day-1/*.md` (the biggest remaining content
      gap named at the top of this file). New structural cases this time:
      `.stakes` (same markdown shape as `.roster`, flagged inline since
      they'd otherwise be ambiguous), `.process-wheel` (same shape as
      `.history`, same reason), `.chip-strip`, and a markdown-table
      mapping for `.resource-table`/`.filter-pills` (`people-to-follow.md`).
      All five now documented in this README's Format section above.
      Also shipped: `day-1/README.md`, a cross-page pattern summary (voice,
      citation density, bare question lists, grounding) pulled from
      `content-architecture-notes.md`, so the user can make those calls
      once before editing instead of per-page. Full detail in the
      2026-08-21 change-log entry near the top of this file. **Update,
      same day**: rather than a line-by-line prose edit, `01-state-of-ai.md`
      and `02-industry-conversation.md` got a full research-first rewrite
      instead (see the matching 2026-08-21 "Change log" entry below) after
      the user felt they read shallower and more repetitive than Day 2/3.
      `03-use-cases.md` §4/§5 got a lighter, targeted pass in the same
      session. The other 6 Day 1 pages are still queued for the user's own
      line-by-line pass, unchanged by this. **Update, 2026-08-22**:
      `01`/`02`/`03`'s corresponding `docs/day-1/*.html` pages were
      regenerated from these drafts ahead of the line-by-line pass (the
      user wants to edit against the live rendered site, not the raw
      markdown) — full detail in the matching 2026-08-22 change-log
      entry. **Resolved 2026-08-21**: this
      research-first discipline (now used 4 times: Day 2, Day 3, this Day 1
      rewrite, and its own follow-up grounding pass) is now a project skill,
      [`.claude/skills/ground-content/SKILL.md`](../.claude/skills/ground-content/SKILL.md)
      — invoke it directly for future grounding passes instead of
      re-deriving the process.
- [x] Resolved: the org/repo is confirmed
      (`github.com/AndrewRCalderon/2026-ai-news-innovation-workshop`, this
      repo's own remote) — `setup.html` now links directly to it. **New
      caveat**: `STUDENT_CLAUDE_GUIDE.md` itself doesn't exist yet (still a
      Phase 5 deliverable), so that specific link 404s on GitHub until it's
      written. Fine for now since setup.html isn't live/sent to students
      yet, but write that file before it actually goes out.
- [ ] Decide which remaining topic pages should use the new briefing template
      (rich, structured content) vs. stay on the generic topic-header/sidebar
      template — currently only `day-1/01-state-of-ai.html` uses briefing;
      the other 5 built Day 1 pages are still on the generic template with
      placeholder content. See [ADR 0011](adr/0011-split-overview-and-slides.md).
- [x] Resolved: user wants a Slides companion for every topic that has real
      content — 4/4 built so far (Topics 1–4). Keep building one alongside
      each new Overview page going forward rather than deciding per-topic.
- [ ] Slides pages hardcode their cover-meta (time/duration/type) as static
      text instead of reading `schedule.json` like Overview pages do
      (`topic-metadata.js`) — a deliberate simplification in
      [ADR 0011](adr/0011-split-overview-and-slides.md) since deck.js has no
      fetch. Real cost: caught once already — Topic 1's slides page still
      said "45 MIN" after the schedule retiming moved it to 15 min, and had
      to be fixed by hand. Worth reconsidering if this happens again as more
      slides pages accumulate; the fix would be a small schedule-fetch added
      to `deck.js` for just the cover-meta fields.
- [x] ~~"After class: end-of-day resources email (including recommended
      newsletters)" is real Day 1 content but isn't an in-class scheduled
      session, so it isn't in `schedule.json`. Currently just a static note
      on `day-1/index.html`. The actual newsletter list it should send
      belongs in `resources.html`'s Day 1 section once that's populated
      (Phase 5) — right now that section is still a TODO placeholder.~~ —
      **Removed 2026-08-23**: user asked to drop the static note from
      `day-1/index.html` entirely rather than build the feature it was a
      stand-in for. Nothing to build here anymore.
- [x] Resolved: "Your Workshop Tech Stack" and "How They Work Together"
      moved out of `07-ai-tools.html` into `08-explore-tech-stack.html`
      (both Overview and Slides). AI Tools is now a clean 5-section, 30-min
      survey (landscape, quick reference, evaluation criteria, required/
      optional for this workshop); Explore Tech Stack owns the hands-on
      deep dive plus a new facilitator roadmap (see change log).
- [ ] `project/scripts/check-slide-parity.js` (added 2026-08-06, see
      Batch 7 below) found two pre-existing Overview/Slides content
      mismatches on topics not yet reached in the full-scale review — not
      fixed, just flagging so they're not lost: `05-project-ideation.html`
      s2 (Overview 12 `<li>`s vs. Slides 7) and `07-ai-tools.html` s2
      (Overview 22 `.roster-row`s vs. Slides 12). Address when the review
      reaches those topics.

### `live` vs `review/full-site-audit-2` divergence — consolidated follow-ups

`live` (see [ADR 0018](adr/0018-live-branch-for-partial-production-deploy.md))
was the active surface for iterating on `setup.html` and a visual-design
exploration (fonts, colors, spacing) with Adiel and the user. On
2026-08-13 everything below was ported into `review` so it isn't lost
when `review` eventually merges to `main`. `live` stays live/deployed
independently; this is a one-way port (`live` → `review`), not a merge,
so the two branches still diverge — `live` has no Day 1 content, `review`
has no production URL.

- [x] **`setup.html`/`setup-day-2.html` content, final version.** Ported
      wholesale from `live`, including Adiel's PR #3 (retitled
      "Pre-Workshop Setup," checklist 7 → 18 items, Day 2/3 tooling
      folded into the single page, new "Git" section — the Code tab
      won't open without Git installed locally and GitHub Desktop's
      bundled copy doesn't count — corrected connector path, corrected
      tab count confirmed via live install, 7 new screenshots) and all
      of the prior `live`-only copy edits (GitHub connector walkthrough,
      contact info split out, "workshop account" → "email account," Git/
      GitHub-Desktop blockquote removed, redundant "Setup" breadcrumb
      removed). **`docs/setup-day-2.html` was orphaned on both branches**
      — nothing linked to it since setup.html absorbed its content.
      **Deleted 2026-08-21** after confirming zero inbound links anywhere
      in `docs/` or `STUDENT_CLAUDE_GUIDE.md`.
- [x] **Checklist label flex bug.** Fixed as a side effect of the
      `setup.html` port (the fix was in the markup — text wrapped in a
      `<span>` inside each label — not a standalone CSS change).
- [x] **Tow-Knight Center logo.** Added to `review`'s `nav.html` (new
      `.site-nav-brand` wrapper) and `docs/assets/images/` (created
      fresh, didn't exist on `review` before). `review`'s nav keeps its
      full dropdown menu, unlike `live`'s stripped single-link version,
      so the markup differs slightly from `live`'s copy even though the
      CSS is identical.
- [x] **Design exploration (fonts, colors, spacing), applied site-wide.**
      This went further than "port `live`'s files" — the token changes
      live in shared `style.css`/`briefing.css`, so they now affect
      every page on `review` (Day 1 topics, home, resources, students),
      not just setup. Space Grotesk headings / Plus Jakarta Sans body
      (loaded via one `@import` in `style.css` instead of per-page
      `<link>` tags, since `review` has far more pages than `live`);
      purple `#955af5` / coral `#e8664a` / off-white `#fdfbf7` palette
      replacing the old pastel watercolor tones; heading margin added
      (was `margin: 0`, headings sat flush against surrounding text).
      Worth a look across a few Day 1 pages, not just setup, since this
      is the first time the new look has touched them.
- [ ] **Workshop name.** Fixed in `setup.html`, `setup-day-2.html`, and
      `nav.html`'s brand link (all touched during this port anyway).
      Still wrong in `footer.html` and every other page's `<title>`/body
      copy — needs a full site-wide find/replace, not yet done.
- [ ] **Em-dashes.** Standing rule (saved to memory, not in this repo:
      `feedback_no-em-dashes`). Clean on `setup.html`/`setup-day-2.html`
      (ported from `live`, already swept there). Every other page on
      `review` still has them throughout, untouched by this pass.

---

## Full-scale site review (in progress — 2026-08-06)

User is reviewing the live site page by page and passing notes in batches.
Logging each batch here as it arrives; not prioritized or implemented yet —
that happens once the review is complete. See change log for batch history.

### Batch 1 — Home, Students, Day 1 index, Topic 1 (State of AI)

- [ ] **Home page**: harmonize styles to match the briefing template adopted
      for Day 1 content pages (`docs/css/briefing.css`). User chose a
      **light visual pass** (align colors/type/spacing tokens), not a full
      retemplate — in progress.
- [ ] **Student submissions**: verify the fork → clone → branch → commit →
      push → PR flow actually works end-to-end, not just that
      `09-fork-and-submit.html` describes it correctly. **Deferred**: user
      wants to finish writing all of Day 1's content first, then come back
      to this. When it happens: user will do the fork/PR themselves under
      their own GitHub account and report back (their choice over doing it
      together live in-session), since opening a real PR is a visible,
      public action.
- [ ] **Day 1 index page** (`docs/day-1/index.html`): once all Day 1 topic
      content is finished, add a 1–2 sentence summary of what the day
      covers plus a short learning-outcomes list. Blocked on Topics 6
      (`06-problem-statement-discussion`) and 10 (`10-project-assignments`)
      still being placeholders.
- [x] **Topic 1 (State of AI) slides — cover slide**: removed the
      `"→ or click to begin"` hint site-wide from all 8 existing slide
      decks (Topics 1, 2, 3, 4, 5, 7, 8, 9), not just Topic 1.
- [x] **Topic 1 "The Moment We're In" copy edits** — done in both
      `docs/day-1/01-state-of-ai.html` and
      `docs/day-1/slides/01-state-of-ai-slides.html`:
      - Bullet 1: "overnight" dropped.
      - Bullet 2: em dash replaced with a period.
      - Timeline chips: `.chip` given left padding
        (`docs/css/briefing.css:120`) so years no longer crowd the divider.
      - ChatGPT paragraph reworded to the shorter version.
      - Stat pull "1,000,000 users in 5 days" verified accurate (see
        research findings below) — left as plain text for now, not yet
        wired into an interactive citation (that's the item right below).
- [ ] **New architecture idea raised by the citation need above**: an
      inline citation/footnote system — superscript markers on factual
      claims that reveal a source link (and maybe a short description) when
      clicked. Would touch the shared briefing template used by every
      topic page, so this is ADR-sized, not a copy fix. Interaction design
      (inline popover vs. bottom footnote list) still needs to be worked
      out with the user — revisit once the review batches are done.

### Batch 2 — Topic 1 (State of AI), "What's Actually Changed" section

Applies to both `docs/day-1/01-state-of-ai.html` (§s2, lines ~60–86) and
`docs/day-1/slides/01-state-of-ai-slides.html` (duplicated content, ~line
75+).

- [x] Dropped "Here's the honest split." from the intro paragraph.
- [x] Renamed "Still True" → "Caveat" (user's choice among Caveat/
      Caution/Warning options).
- [x] Resolved: asked the user to clarify "deeper/more probative" (longer
      per-item explanations vs. more items vs. both) — answer was that the
      column is fine as-is. No content change needed.
- [x] Column parity: added a "Privacy tooling" item to the Changed column
      to pair with the existing "Privacy and data security remain
      genuinely thorny" caveat (exact wording was drafted by Claude, not
      dictated by the user — worth a closer read).
- [x] Done — all 12 items in both columns now have `.cite` citations (see
      ADR 0012 and the research findings entry below).

### Batch 3 — Topic 1 (State of AI), "Key Moments in Recent History" section

Applies to both `docs/day-1/01-state-of-ai.html` (§s3, lines ~88–97) and
`docs/day-1/slides/01-state-of-ai-slides.html` (duplicated content,
~line 106+). Six-item `<ol class="history">` timeline: 2012, 2016,
2018–2020, Nov 2022 (hinge), 2023–2024, 2024–2026.

- [x] Intro line reworded (polished version of the user's rough phrasing):
      "The path here wasn't sudden. It's the accumulation of decades of
      technical milestones and academic research — some at universities,
      some at big tech companies — that finally broke into public view."
- [x] 2012 item named the benchmark: AlexNet's 2012 ImageNet win (15.3%
      vs. 26.2% error), confirmed via research — see findings below.
- [x] 2016 AlphaGo item: confirmed fine as-is, no change made.
- [ ] 2018–2020 BERT/GPT-2/GPT-3 item: "GPT-3 introduces few-shot
      learning" is still unexplained — deliberately left alone pending the
      citation-system decision (user's preferred fix for this one)
      rather than half-solving it with inline text.
- [x] 2023–2024 "Copilot era" item: added a plain-text detail naming the
      NYT v. OpenAI/Microsoft lawsuit (Dec 2023) — not yet an interactive
      citation, since that system doesn't exist yet.
- [x] 2024–2026 "current moment" item: "Sober" → "Frenetic" (user's pick
      over "Adamant," which was flagged as not fitting the intended
      meaning), plus added "— people are throwing things at the wall to
      see what sticks."

### Research findings (background agent, 2026-08-06) — unblocks Batch 1/3/4 citations

- **ChatGPT "1M users in 5 days"**: verified accurate. Sam Altman and Greg
  Brockman both confirmed it on X, Dec 5 2022 (5 days after the Nov 30
  launch). High confidence. Caveat: don't confuse with a *different*,
  later 2025 Altman tweet about "1 million users in one hour" — different
  milestone.
- **2012 benchmark**: confirmed as AlexNet winning ILSVRC (ImageNet) 2012 —
  15.3% top-5 error vs. 26.2% for the next-best (non-neural) entry. Paper:
  Krizhevsky, Sutskever, Hinton, NeurIPS 2012. Source:
  <https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html>
- **Training-data lawsuits**: *The New York Times v. Microsoft and OpenAI*
  (filed Dec 27 2023, SDNY) is the clearest, most journalism-relevant pick
  — alleges unauthorized use of Times articles to train GPT models; still
  active/in discovery as of the research date. A second option: eight
  Alden Global papers (Chicago Tribune, NY Daily News, etc.) sued the same
  defendants Apr 30 2024. **Before publishing a "case status" line, verify
  against a live docket** — litigation is moving fast and the agent's
  status info may already be stale.
- **Newsroom examples**: Large — NYT's internal "Echo" tool (2025,
  summarizes/suggests headlines, cannot draft articles) and Washington
  Post's "Ember" AI writing coach for op-ed contributors (2025). Small —
  Sahan Journal (MN, AI-personalized advertiser kits + story summaries),
  Outlier Media (Detroit, AI-assisted SMS civic-info service), City
  Bureau/Documenters Network (Chicago, AI surfacing trends across public-
  meeting notes). All confirmed via named sources; full citations in the
  agent's report if needed later.
- Full agent report (with all URLs) is not persisted elsewhere — if a
  citation URL is needed and not summarized here, someone will need to
  re-derive/re-search it.

### Batch 4 — Topic 1 (State of AI), slides 4–5 + end slide

Slides 4–5 apply to both `docs/day-1/01-state-of-ai.html` (§s4/s5, lines
~101–144) and `docs/day-1/slides/01-state-of-ai-slides.html` (duplicated).
The end-slide item is a **shared deck template pattern**, confirmed present
in all 8 existing slide decks (Topics 1, 2, 3, 4, 5, 7, 8, 9) — see note
below.

- [x] Slide 4 — "You Cannot" → "You Should Not."
- [x] Same slide — pull-question reworded to: `Not "will AI replace me?"
      but "what does this let me try that I couldn't before?"` (user's
      pick among three drafted options).
- [x] Slide 5 — "Your industry" → "Our industry."
- [x] Same row — replaced the vague Adobe/Bloomberg line with real named
      examples: NYT's "Echo" tool, Washington Post's "Ember," Sahan
      Journal, Outlier Media (sourced via the research agent — see
      findings above).
- [x] Same slide, "For you" stakes item — reworded to "...as essential as
      understanding Google Docs, Slack, and spreadsheets."
- [x] **End slide**: replaced the `-30-` mark + summary line with a
      simple nav block (Restart / Back to schedule / Next section) —
      applied as a template-level change across **all 8 slide decks**
      (Topics 1, 2, 3, 4, 5, 7, 8, 9), each with a correct next-topic link
      per `schedule.json`'s Day 1 order.

### Research findings (background agent, 2026-08-06) — citations for the compare-grid ("Changed"/"Caveat") items

**Applied** — all 12 items in both `docs/day-1/01-state-of-ai.html` and its
Slides mirror now carry `.cite` markers using these sources. The two
weak/proxy items (Changed #2 "Accessibility," #5 "Public conversation")
had their copy reworded per user direction to actually match what their
Pew sources measure, rather than being cited as-is or left uncited.

**Changed column:**

1. Speed of deployment — McKinsey on generative AI's dev-time savings.
   <https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/unleashing-developer-productivity-with-generative-ai>
   Medium confidence — "minutes vs. months" is hyperbole beyond what the
   study itself claims (its real numbers: 10–50% time savings).
2. Accessibility — Pew: 49% of U.S. adults now use AI chatbots (up from
   23% in 2023). <https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/>
   **Weak/proxy citation** — shows broad adoption, not specifically "no ML
   background needed."
3. Capability scale — Stanford AI Index 2025: SWE-bench 4.4%→71.7% solved
   in one year, GPQA +48.9 pts, MMMU +18.8 pts.
   <https://hai.stanford.edu/ai-index/2025-ai-index-report> High confidence.
4. Cost — Stanford AI Index: GPT-3.5-level query cost fell ~280x in 18
   months ($20.00 → $0.07 per million tokens).
   <https://hai.stanford.edu/ai-index/2025-ai-index-report> High confidence.
5. Public conversation — Pew: 95% of U.S. adults have heard about AI;
   "heard a lot" nearly doubled 26%→47% (2022–2025).
   <https://www.pewresearch.org/science/2025/09/17/ai-in-americans-lives-awareness-experiences-and-attitudes/>
   **Weak/proxy citation** — measures awareness/usage, not literal
   "dinner-table talk." Agent suggested either softening the tooltip
   wording or skipping a citation on this one.
6. Privacy tooling — Anthropic's Aug 2025 consumer terms update: Work/
   Enterprise/Education/Government + API excluded from training; new
   consumer opt-in/opt-out controls. <https://www.anthropic.com/news/updates-to-our-consumer-terms>
   High confidence, primary source.

**Caveat column:**

1. Hallucinates — OpenAI/Georgia Tech paper arguing training rewards
   confident guessing over admitting uncertainty.
   <https://arxiv.org/abs/2509.04664> High confidence.
2. Not "thinking," pattern-matching — Apple's "The Illusion of Thinking"
   (2025): reasoning models collapse on novel/complex logic puzzles.
   <https://machinelearning.apple.com/research/illusion-of-thinking> High
   confidence, but **contested in the field** — some researchers argue the
   puzzle-based test design underestimates real reasoning ability.
3. Amplifies bias — Zhao et al. 2017, the foundational bias-*amplification*
   paper (33%→68% gender-association skew after training).
   <https://arxiv.org/abs/1707.09457> High confidence, though pre-LLM era;
   a newer companion citation exists if wanted
   (<https://arxiv.org/html/2410.15234>, 2024).
4. Best on well-defined tasks — METR: near-100% success on tasks under
   ~4 min, under 10% on tasks taking humans 4+ hours.
   <https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/>
   High confidence for task length/complexity; imperfect fit for
   "creative work" specifically (METR's tasks are mostly software
   engineering).
5. Privacy/security thorny — Stanford AI Index: privacy incidents up 56%
   YoY (233 in 2024); trust in AI companies on data protection fell
   50%→47%. <https://hai.stanford.edu/assets/files/hai_ai-index-report-2025_chapter3_final.pdf>
   High confidence.
6. Don't fully understand why models work — Dario Amodei's "The Urgency
   of Interpretability" essay. <https://darioamodei.com/post/the-urgency-of-interpretability>
   High confidence, direct primary source from a lab CEO.

### Batch 5 — Topic 2 (Industry Conversation)

Not yet implemented — logged only, per the review workflow (organize
first, implement once the user says go). Applies to
`docs/day-1/02-industry-conversation.html` and
`docs/day-1/slides/02-industry-conversation-slides.html` unless noted as
Overview-only.

- [x] **"Smart people" → "people"** — both occurrences fixed:
      - s1 lede (both files): "...understanding what people actually
        disagree about."
      - s3 (Overview only — the Slides version never had this sentence):
        rewritten (not a straight deletion, which would've broken the
        grammar) to "Nobody knows yet — both camps have people who know
        what they're talking about." (Claude's phrasing — worth a check.)
- [x] **s2 "The Journalism Conversation" — citations, done in both files**.
      Before wiring in citations, independently re-verified every
      candidate source URL by fetching it directly (several of the
      research agent's suggested links turned out dead or blocked —
      caught before publishing, not after):
      - The agent's suggested NYT source (`nytco.com/press/principles-...`)
        **404s** — not used. Its Nieman Lab backup also blocks automated
        fetches. Used **Semafor's Feb 2025 reporting** instead (confirmed
        live, content directly verified): NYT bars staff from using AI to
        draft/substantially revise articles and requires AI-generated
        images/video to be labeled. Copy changed from "if AI was used...
        readers are told" (aspirational, per the agent's own caveat) to
        this verified, concrete policy detail.
        Source: <https://www.semafor.com/article/02/16/2025/new-york-times-goes-all-in-on-internal-ai-tools>
      - **Washington Post**: dropped the unsupported "draft templated
        earnings reports" clause (that's actually AP's program) and
        rewrote around what Haystacker (2024) actually does — confirmed
        directly against the source's own text.
        Source: <https://www.editorandpublisher.com/stories/new-washington-post-ai-tool-sifts-massive-data-sets,251540>
      - **Reuters**: rewritten around Fact Genie, Reuters' real tool
        (confirmed via the source's own text: scans press releases/
        financial documents in under 5 seconds, suggests alerts,
        journalists review before publishing) — not the unverifiable
        court-filings claim that was previously on the page.
        Source: <https://wan-ifra.org/2025/04/from-lab-to-newsroom-how-reuters-builds-ai-tools-journalists-actually-use/>
      - **Associated Press**: copy kept as-is (accurate, if conservative),
        cited. Source: <https://www.poynter.org/reporting-editing/2015/robot-writing-increased-aps-earnings-stories-by-tenfold/>
- [x] **s2 copy edit, both files** — investigative-reporting sentence
      reworded to: "No major newsroom uses it to replace investigative
      reporting. However, newsrooms are using AI to augment investigative
      capacity. The tension is efficiency gains versus maintaining
      journalistic integrity." Applied to each file's own base sentence
      (the Slides version keeps its trailing "honest answer" sentence
      after the edited part).
- [x] **s3 "The Tech Industry Conversation" — intro line, both files**:
      "The scaling question — are we even on the right path?" → "The
      scaling question…"
- [x] **Structural reorder, both files** (this turned out to apply to the
      Slides deck too — it has the identical 6-section structure with the
      same "Journalism Conversation" content, not just the Overview as
      first assumed): moved "The Journalism Conversation" to directly
      after "Where Newsrooms Actually Stand," before "What's Actually at
      Stake." New order in both files: What Everyone's Talking About →
      Tech Industry Conversation → Skeptics vs. Optimists → Where
      Newsrooms Actually Stand → Journalism Conversation → What's
      Actually at Stake. Updated the TOC/cover-contents order and all
      `block-eyebrow`/`<span class="n">` numbers to match; physically
      moved the section blocks. DOM `id`s (`s1`–`s6`) left unchanged since
      they're just anchors/`data-jump` targets, not tied to visual order —
      confirmed the Slides deck's prev/next and dot-nav (which read DOM
      order) still track correctly since the actual nodes moved, not just
      their labels.

### Batch 6 — Topic 2, "Where Newsrooms Actually Stand" section

**Overview-only** — the Slides deck's version of this section has neither
the "depending on size" phrase nor the "common policies emerging" bullets
(it's a condensed roster + pull-question only), so neither addition below
has an equivalent spot there. Flagged, not assumed away.

- [x] Added a no-URL `.cite` disclaimer after "depending on size":
      "This breakdown reflects general perception, not a formal study of
      AI adoption or maturity across small, regional, mid-size, and large
      newsrooms." The citation component already supported note-only
      citations (no `data-url` → popover shows just the text, pill isn't
      clickable) without needing any code changes.
- [ ] User wants 2–3 hyperlinks to real, public newsroom AI policies
      placed right under the "common policies emerging across newsrooms"
      bullets. **Research findings (verified live, not just recalled)**:
      - **Compilation option**: <https://aifornewsroom.in/ai-guides> — an
        actively maintained, independent index of ~128 published newsroom
        AI policies across ~40 countries, each linking to the original
        document. Spot-checked 3 outbound links (ABC News Australia, EL
        PAÍS, WBEZ) — all live and on-topic. Caveat: partly newsroom-
        submitted, not independently audited.
      - **Individual-link alternative** (if preferred instead of/alongside
        the compilation), spanning sizes not already used elsewhere on
        this page: Chicago Public Media/WBEZ (mid-size,
        <https://www.wbez.org/ai-policy>), Sahan Journal (small nonprofit,
        AI guidelines embedded in its About page, not a standalone URL —
        <https://sahanjournal.com/about-sahan-journal/>), ABC News
        Australia (large, non-US alternative to the names already cited —
        <https://www.abc.net.au/about/abc-ai-principles/104036790>).
      - Rejected candidates: Journalist's Resource's 52-newsroom policy
        comparison (bot-blocked, and it's an analysis piece not a link-out
        compilation); Denver Post's policy (real per secondhand reporting,
        no direct published URL found); CNTI's policy report (a PDF
        analysis, not a browsable compilation).
      - [x] **Resolved**: went with the compilation link. Briefly
        considered hosting our own CSV-backed table page (surfaced via
        `resources.html`) instead of linking out, reasoning that we
        wouldn't maintain it ongoing — but dropped that once it was clear
        aifornewsroom.in is already a live, actively maintained index, so
        rebuilding it ourselves would just be a snapshot competing with
        the real thing. Added a single plain-prose link (not a `.cite`
        pill, since it's further reading rather than a footnote on one
        specific claim) right after the "common policies" bullets:
        "Curious what real policies look like? Browse a compiled index of
        published AI policies from newsrooms worldwide" →
        <https://aifornewsroom.in/ai-guides>.

### Batch 7 — Topic 3 (Use Cases)

Applies to `docs/day-1/03-use-cases.html` and
`docs/day-1/slides/03-use-cases-slides.html` unless noted otherwise.

- [x] **s1 "What Does AI Actually Do?"**: em dash → comma. "These are
      real, deployed use cases — not theoretical ones." → "These are
      real, deployed use cases, not theoretical ones." Done in both
      files.
- [x] **s2 "Use Cases in Journalism" — done, Overview only**. All 5
      existing items now cited (WAN-IFRA, Poynter, THE CITY's own site).
      Added 6 new examples: 4 as new rows (iTromsø/local-government
      monitoring, Chequeado/automated claim-spotting, MittMedia+United
      Robots/automated local content, DocumentCloud/FOIA analysis — all
      small/regional or mid-size, none repeating NYT/AP/WaPo/Reuters),
      plus 2 folded into existing rows as concrete named examples rather
      than duplicate-category rows (Hearst's regional dailies added to
      "Headline ideation"; Zamaneh Media added to "Accessibility"). Table
      grew from 5 to 9 rows.
- [x] **s3 "Use Cases Outside Journalism" — done, Overview only**. All 5
      existing items cited (Zendesk, an ACL bias-detection paper,
      Wikipedia's filter-bubble entry, a PNAS speech-recognition bias
      study, Brandwatch). Added all 6 new examples as new rows, each a
      distinct industry (AlphaFold/scientific research, *Mata v. Avianca*/
      legal, IDx-DR/healthcare, GitHub Copilot security study/software,
      Be My Eyes' "Be My AI"/accessibility, UPS ORION/logistics). Table
      grew from 5 to 11 rows.
- [x] **CSV download — reverted**: built a client-side "Download as CSV"
      button, then the user reconsidered given how few rows existed at
      the time and asked to drop it. Removed cleanly (buttons, the shared
      `docs/js/csv-export.js` script, its CSS, and the ADR, since it never
      shipped/was reviewed).
- [x] **Standalone-module question — resolved**: user wants an inline
      "infinite scroll" reveal (not a separate page). Built
      `docs/js/infinite-roster.js` — a `.roster.is-infinite` table shows
      its first 4 rows, then reveals more in batches as a sentinel
      element scrolls into view; all rows stay in the DOM so non-JS
      visitors see everything immediately. Applied to both of Topic 3's
      rosters (Overview only — Slides stays condensed at 5 items each,
      matching how every other topic's Slides content is already a
      trimmed version of its Overview, not a full mirror). See
      [ADR 0013](adr/0013-infinite-scroll-roster.md).
- [x] **Resources link, per user request**: rather than a second page,
      linked directly to these two sections from `resources.html`'s Day 1
      list via their existing `#s2`/`#s3` anchors — same pattern now used
      for the newsroom AI policies index (see Phase 5 above).
- [x] **s6 "The Practical Question" — reframed as a self-assessment
      checklist, done in both files**, replacing the yes/no task list.
      Mirrors s5's Works-When/Doesn't-Work-When criteria as first-person
      questions (to avoid duplicating that content) rather than repeating
      the same specific tasks (research, drafting, etc.) — the Slides
      version is condensed, same pattern as everywhere else on this page.
      Wording was Claude's draft, presented before implementing; no
      objection raised, so shipped as proposed — worth a read.

### Batch 8 — Topic 3, s6 "The Practical Question" follow-up

- [x] Dropped the "Not abstract —" lead-in (Overview only — Slides never
      had it). Now just "Before reaching for AI, ask yourself:" in both.
- [x] Bullets restyled from the site's usual em-dash marker to checkmarks
      for this specific list, via a new `.field-notes.is-checklist`
      modifier (scoped, not a global change to every field-notes list on
      the site) — done in both files.
- [x] **Checklist questions now grounded in real sources, done in both
      files**. Research found no single master framework covering all 6
      — pieced together from multiple credible sources instead (user
      explicitly said this was fine): Google's "Rules of Machine
      Learning" (task/heuristic-first question), Google's "Problem
      Framing" guide (data-quality question), AP's generative AI
      standards via Poynter (verify-before-publish question), Trusting
      News' AI Trust Kit (credibility-stakes question), and IDEO's AI
      Ethics Cards (augment-vs-replace question). The 6th question
      ("real-time information / human trust") has **no honest citation**
      — research explicitly flagged this as a gap rather than forcing a
      weak match, so it's left uncited rather than fabricated.
      Independently re-verified all 5 URLs live before using them.
- [x] **Built `docs/resources/ai-decision-frameworks.html`** — a table of
      the same 5 verified sources (org, type, description), framed as an
      ongoing collection to add to whenever future research turns up
      another good practitioner framework, not a one-off list. Linked
      from Topic 3 s6 ("See more frameworks like this →", both files) and
      from `resources.html`'s Day 1 list, matching the pattern already
      established for the newsroom AI policies index.

### Batch 9 — Topic 4 (People to Follow)

Applies to `docs/day-1/04-people-to-follow.html` and
`docs/day-1/slides/04-people-to-follow-slides.html` unless noted.

- [x] s1 renamed "Why Follow People" → "Drawing Inspiration From Others"
      (user's suggestion), done in both files.
- [x] Removed the "Hashtags" row from s6 "Communities & Events" (both
      files) — not necessary.
- [x] Deleted s7 "How to Use This List" entirely (both files) — TOC/
      cover-contents entry and the section itself. Slides deck's static
      counter placeholder updated 09→08 (interim value — will need
      re-checking once the new section below is added back in).
- [x] **Research surfaced a serious accuracy problem**: 3 of the original
      11 people appear to be entirely fabricated — no trace found under
      any method (direct search, LinkedIn, org staff pages) for **Marcus
      Whiten** (claimed WaPo AI lead — real person is Phoebe Connelly),
      **Matt Penneyacker** (claimed GNI program officer — no verifiable
      match), or **Jeremy Sleight** (claimed Hugging Face advocate — no
      trace at all). Also, **Charlie Warzel's role was outdated** — he's
      moved from NYT Opinion to The Atlantic (Galaxy Brain newsletter).
      Fixed: Whiten → Phoebe Connelly (real, verified via Nieman Lab);
      Penneyacker and Sleight dropped rather than force in a weak
      replacement; Warzel's role and link corrected. Independently
      re-verified every remaining URL live before use (all 200 except
      Nieman Lab, which 403's on direct curl — a bot-blocking pattern
      seen repeatedly this session on real, active sites, not a dead
      link).
- [x] **Look beyond big-name newsrooms**: added 3 real, verified
      small/mid-size newsroom leaders — Simon Galperin (The Jersey Bee,
      small NJ nonprofit), Angela Eichhorst (CT Mirror), Matt Boggie
      (Philadelphia Inquirer, built "Dewey").
- [x] **New content added**: 3 critical voices (Emily M. Bender, Safiya
      Umoja Noble, Karen Hao) and 3 human-centered-AI designers (Don
      Norman, Ben Shneiderman, Fernanda Viégas), all verified.
- [x] **Structural pivot mid-build**: while wiring up the new
      "Critical Voices & Designers" section as its own 7th roster
      section, the user proposed something better — collapse the whole
      page (all 6 people/resource categories) into **one unified,
      filterable table** with a Type column and filter pills, rather than
      many separate sections. Confirmed scope (everything in one table;
      collapse to one section) before rebuilding, given how costly the
      infinite-scroll guess-wrong/rebuild cycle was earlier the same day.
      Built as `.resource-table` + `.filter-pills` + new
      `docs/js/type-filter.js` (29 rows, 8 filterable types) — see
      [ADR 0015](adr/0015-filterable-type-table.md). TOC collapsed from
      7 entries to 2 in both files. Proactively added the `tr[hidden]`
      CSS fix this time (same bug class as the roster-row failure) and
      verified the whole interaction with Playwright before calling it
      done — worked correctly on the first try.
- [x] Extended `project/scripts/check-slide-parity.js` to count `<tr
      data-type="...">` rows — it had a real blind spot for table-based
      content (silently read as "no issues" the first run, since neither
      of its old checks could see table rows at all). Re-ran after the
      fix; Topic 4 confirmed clean, only the two pre-existing Topic 5/7
      mismatches remain (still not fixed, per the user's "haven't gotten
      there yet" instruction from Batch 7).
- [x] Added a `resources.html` Day 1 link to the new unified table,
      per the user's request.

---

## Infinite-scroll roster — built, debugged, then abandoned in favor of Slides pagination

Full arc, in order:

1. Built `docs/js/infinite-roster.js` (progressive reveal via
   `IntersectionObserver`) for Topic 3's two long rosters — see
   [ADR 0013](adr/0013-infinite-scroll-roster.md).
2. User reported it wasn't working (all rows displayed immediately).
   Diagnosed and fixed a real bug: `.roster-row`'s explicit `display:
   grid` was overriding the `hidden` attribute's default `display: none`.
   Verified the fix with an actual headless-Chrome session via
   Playwright (available in this environment) rather than trusting
   curl/HTML-structure checks, which can't catch a rendering bug like
   this — confirmed progressive reveal working (4→9, 4→11 rows) with
   simulated continuous scrolling.
3. Applied follow-up design feedback on the same component: removed the
   "Scroll for more examples…" sentinel text, framed the module with a
   border + `--surface` background.
4. **User still reported it not working, even in a private/incognito
   window** — ruling out caching. Real cause: on a sufficiently tall
   viewport, the sentinel is already inside the `IntersectionObserver`'s
   trigger zone the instant the page loads, so the "reveal on scroll"
   logic fires immediately in a fast cascade — no scrolling was ever
   needed to see everything, which is indistinguishable from "scroll
   doesn't work."
5. User clarified the actual goal was about the **Slides deck** getting
   too long, not the Overview page (which scrolls fine regardless), and
   said scroll didn't have to be the mechanism. **Pivoted**: Overview
   reverted to a plain roster (no special handling needed); the Slides
   deck's two long rosters split into continuation slides (`s2`/`s2b`,
   `s3`/`s3b`/`s3c`) using the deck's existing pagination instead. See
   [ADR 0014](adr/0014-slides-pagination-for-long-rosters.md), which
   supersedes 0013. Deleted `infinite-roster.js` and its CSS entirely —
   none of it shipped as a working feature.
6. Along the way, discovered Topic 3's Slides deck had silently drifted
   from item-level parity with Overview (5 items shown vs. Overview's
   9/11) — a real inconsistency with how Topics 1–2 always mirrored every
   item (just with condensed wording). Fixed by adding all the same new
   examples to Slides, condensed. Built
   `project/scripts/check-slide-parity.js` per the user's request for a
   repeatable way to catch this going forward — compares `.roster-row`/
   `<li>` counts between each topic's Overview and Slides files,
   understands the new continuation-slide pattern from ADR 0014. Running
   it immediately surfaced two more pre-existing mismatches on
   not-yet-reviewed topics (logged above, not fixed yet per the user's
   explicit "we haven't gotten past use cases" instruction).

### Batch 10 — Topic 5 (Project Ideation)

Applies to `docs/day-1/05-project-ideation.html` and
`docs/day-1/slides/05-project-ideation-slides.html` unless noted.

- [x] **s1 "The Design Process Is Circular" made actually circular**: new
      `.process-wheel` CSS component (rotate/translate/counter-rotate
      technique, 7 items at 51.43° apart, dashed ring, mobile falls back
      to a stacked list) — see [ADR 0016](adr/0016-circular-process-diagram.md).
      Verified visually with Playwright (screenshot + programmatic
      overlap check across all 7 items) rather than trusting the CSS by
      eye, at both desktop and mobile widths, and inside the Slides
      deck's more cramped per-panel layout.
- [x] Added a citation on the same lede: Nielsen Norman Group's "Design
      Thinking 101" — verified live, cleanest match to the 7-step cycle
      of the sources researched (Double Diamond, Stanford d.school, IDEO,
      and Lean Startup's Build-Measure-Learn were also checked; NN/g was
      the clearest prose match).
- [x] s2 "Start here" first question broadened: "What frustrates you
      about how journalism works (or could work)?" → "...how you access,
      share, or create information?" — both files.
- [x] "Get Specific" split out into its own section (s3), with new
      framing language: the earlier questions are "ways into a problem
      space," not something to answer perfectly yet; specificity is the
      destination, not the starting expectation; forming a hypothesis
      (next section) is one way to start closing that gap. Also fixed a
      **pre-existing** Slides/Overview parity gap while restructuring
      this section — Slides had always been missing several Start Here/
      Go Deeper questions and the entire "Think about scale" subsection
      (this is the same mismatch flagged back in Batch 7's site-wide
      scan; addressed now that the review reached this topic).
- [x] Removed "Reality Check," "Case Studies," and "Key Takeaways"
      sections entirely — both files.
- [x] Workshop Activity revised: now explicitly tells students to
      revisit the project idea they brought into the session and
      reformulate it via the exercise, and adds a closing line that
      surfacing gaps during reformulation is normal — those are places
      for more research, not a problem.
- [x] **Architecture resolved**: presented 3 options (Google Form +
      published-CSV cards / custom serverless + database / skip digital
      collection); user chose the Google Form approach specifically
      because it needs no backend, keeping the site's static architecture
      intact and not pulling Phase 2 (paused since project start) forward.
      See [ADR 0017](adr/0017-project-ideas-google-form.md).
      **Built**: an embedded-form section in Workshop Activity (Overview
      only — not the Slides deck, since submitting isn't a presentation
      action), a new `day-1/project-ideas.html` cards gallery, and
      `docs/js/project-ideas.js` (dependency-free CSV fetch + parse +
      render, header-keyword column matching so minor question rewording
      doesn't break it). **Not built by Claude, needs a human**: the
      actual Google Form and Sheet require a Google account to create —
      shipped with two literal placeholder strings
      (`REPLACE_WITH_GOOGLE_FORM_EMBED_URL` in the iframe,
      `REPLACE_WITH_PUBLISHED_CSV_URL` in the JS) that fail visibly with
      a clear message rather than silently, verified via Playwright.

### Batch 11 — Topic 7 (AI Tools)

Applies to `docs/day-1/07-ai-tools.html` and
`docs/day-1/slides/07-ai-tools-slides.html` unless noted. Not implemented —
logged only.

- [ ] Remove **s3 "Quick Reference"** entirely (both files).
- [ ] Remove **s5 "For This Workshop"** entirely (both files) —
      supersedes the earlier plan (logged in "Day 1 schedule & Claude
      Desktop pivot" below) to update this section's required-tools list
      for the Claude Desktop pivot; it's being deleted, not reworked, so
      that item is marked resolved/superseded there.
- [ ] **s2 "The Broader Landscape"** tool listings (7 categories, ~25
      tools) move out of this page into `resources.html`. Keep **s4
      "Evaluating a New Tool"** as-is — user says it's useful.
- [ ] Page reframes around two things going forward: evaluating new tools
      (existing s4 content) and **familiarizing yourself with a new
      tool** — this second angle isn't written yet; scope/content TBD
      before implementation.
- [ ] **Open implementation questions, not yet resolved:**
  - Where exactly "The Broader Landscape" lands in `resources.html` needs
    a format decision. Note this is a different case than
    `resources.html`'s established pattern so far (Phase 5: link out to
    genuinely useful *external* compilations we wouldn't host ourselves)
    — this is ~25 tools across 7 categories the site itself authored, not
    an outside link. Options: embed inline, build it as a filterable
    table like People to Follow's, or keep it a dedicated page linked
    from Resources. Not decided.
  - TOC/section numbering for `07-ai-tools.html` shrinks from 5 sections
    to 2 — renumbering question, same open item already flagged for
    People to Follow's removal above.
  - `schedule.json`'s AI Tools duration (currently 30 min) will very
    likely shrink given the content cut — folds into the Day 1 retiming
    already blocked on other content-boundary decisions.
- [ ] **Resolves Adiel's PR #1 note #21** ("tool comparison table risks
      feeling like a wall of information that goes stale fast... consider
      simplifying toward general advice") — moving the volatile tool
      roster to Resources (easier to keep current independently) while
      keeping the in-session lesson durable (an evaluation skill, not a
      point-in-time list) is exactly the fix she was pointing at.

---

## Collaborator feedback — Adiel, PR #1 (2026-08-07)

Adiel (co-instructor) opened
[PR #1](https://github.com/AndrewRCalderon/2026-ai-news-innovation-workshop/pull/1)
"Day 1 feedback" from a private fork, adding
`project/feedback/adiel-2026-08-07.md` — notes from clicking through the
live Day 1 pages. **Not merged**; digested into requirement items below.
**Not implemented, logged only**, same workflow as the review batches
above.

The PR also included a `Logistics` section on Claude account
billing/provisioning (credit-card reimbursement via a card-masking
service, CUNY's Microsoft AI subscription decision) —
**intentionally excluded from this log**, per instruction not to bring
subscription/billing specifics into `main`. That topic (student Claude
accounts need to be provisioned somehow before Day 1) still exists, but
its resolution lives in conversation with Adiel, not in this repo.

### Big-picture items (Adiel's top 4)

- [x] **Day 1 timing** — independently confirms the schedule decision
      already logged above (10am–5pm with breaks; the current
      9am–5:45pm build needs condensing). No new information, just
      corroboration from a second source.
- [x] **VS Code vs. Claude Desktop** — already being tracked above, but
      Adiel's note adds a real wrinkle: she describes a Claude Desktop
      interface where you switch between "cowork" and "claude code" via a
      tab, with panels for MCPs/skills/scheduled tasks, and says it's now
      comparable to Codex's interface and "feels like Notion" — closer to
      what students should be comfortable with than raw VS Code.
      **Resolved 2026-08-11**: "Cowork" is real, not a mishearing or
      transcription artifact — see the "Research complete" entry below
      (line ~1284) for the full verified breakdown (three tabs: Chat,
      Cowork, Code; Code is the VS-Code-like surface). Independently
      reconfirmed 2026-08-16 during the round-3 Day 2 audit while
      verifying an unrelated VS Code plan-mode detail, still accurate as
      of current docs.
- [ ] **How much GitHub to teach — conflicts with the "GitHub Desktop
      only" decision logged above.** Adiel suggests going further: use
      Claude Desktop's GitHub connector (MCP) to handle fork/PR directly
      from inside Claude Desktop, possibly bypassing GitHub Desktop and
      the terminal entirely, so the only concepts students need are
      "fork" and "PR." Needs a decision before Fork & Submit gets
      rewritten — GitHub Desktop (already logged) or the Claude Desktop
      connector (Adiel's newer suggestion). Cross-referenced in the
      Fork & Submit bullet above.
- [ ] **Pre-class email content** — to be finalized between you and Adiel;
      she wants to send it by end of week. Related existing items: the
      setup-page checklist-with-submit-button idea (#1 below) and the
      "who are you building for" pre-workshop framing question (#18
      below).

### Cross-cutting patterns Adiel flagged

Named across multiple notes; specifics logged per-page below with note
numbers for traceability back to the PR:

- Jargon students may not have yet (e.g. "your OS," "no ML background
  needed," "AGI," "weights anyone can run locally").
- Sources/examples that have aged out (some 3–5 years old) — a general
  concern beyond the specific items flagged below.
- A few sections zoom to industry-level abstraction before students have
  footing, or present a dichotomy before students form their own view
  first.
- Several "AI can't do X" claims read more absolute than current
  capability actually supports.

### Setup guide (`/setup.html`)

- [x] **Implemented 2026-08-11**: `/setup.html` is now Day 1 only, split
      into its own standalone page — see "Setup pages split for shipping"
      below for the full change. Its install steps are real interactive
      checkboxes (`.field-notes.is-interactive-checklist`, `checklist.js`)
      with a live "N of 7 steps checked off" counter. **No submission
      step** — consistent with the "no Google Form right now" decision
      from the revision-pass above; if a completion-tracking mechanism is
      wanted later, it should use whatever lightweight approach gets
      chosen for problem-statement submissions, not a one-off Google Form
      here.
- [ ] (#2) Add screenshots for install steps. **Not implemented — needs a
      human.** I can't produce real UI screenshots of Claude Desktop,
      VS Code, or GitHub; this needs someone to actually take them and
      drop them in. Applies to both `/setup.html` (Day 1) and
      `/setup-day-2.html` (Day 2).
- [x] **Implemented**: terminal/Git is already fully out of Day 1 (the
      Claude Desktop pivot removed it entirely, not just de-emphasized
      it). On Day 2, where Git still appears, softened the framing —
      added an explicit "if you're not comfortable with a command line,
      that's fine" line before the terminal step rather than presenting
      it as a bare requirement.

### Day 1 — State of AI

- [x] **Implemented 2026-08-11.** (#4) 2022 added as a fourth chip in the
      timeline strip, matching 1995/2007/2010; "1,000,000" became "1M" in
      the big stat display rather than literally "1 million" — spelling
      it out clashed with that component's numeral-styled design
      (`tabular-nums`, huge mono font), so "1M" was the readability fix
      that didn't break the component. Flagging this as a judgment call,
      not a literal application of the suggestion.
- [x] **Implemented.** (#5) Two-part fix: (1) `citations.js` now derives
      the source-site name from the citation URL's hostname for every
      citation link sitewide (`sourceLabel()` — e.g. "mckinsey.com ↗"
      instead of "Source ↗"), a systemic fix, not a per-page one. (2)
      Added month/year to State of AI's citation hover notes, derived
      confidently from each URL itself (arXiv ID month-year encoding,
      URL date-slugs) rather than guessed — e.g. arXiv `2509.04664` →
      Sept 2025. Skipped one citation (Dario Amodei's essay) where no
      date could be derived this way.
- [x] **Implemented.** (#6) AlexNet's 2012 entry reworded for a general
      audience (exact 15.3%/26.2% figures moved into the citation hover,
      not the visible prose); GPT-3's few-shot learning explanation moved
      from a citation tooltip into visible text (this also resolves an
      old pending item from Batch 3 — "GPT-3 introduces few-shot
      learning" was flagged there as unexplained). Timeline extended past
      2022 with two new entries covering the agentic escalation
      (computer use + Operator, 2024–2025; Skills + Cowork, 2025–2026),
      using dates verified by a research agent against primary sources —
      see the research summary below. **Images not added — needs a
      human**; I can't source/produce real images to embed responsibly.
- [x] **Implemented.** (#7) Split into two clearly separated groups: "Who's
      Building It" (tech giants/specialized/open-source — the model
      layer) and "Who's Using It in Journalism" (large + small newsrooms
      — the application layer), so newsrooms no longer read as parallel
      to OpenAI/Google/Meta.

### Day 1 — Industry Conversation

- [x] **Implemented.** (#8) Added a "Before You Look" prompt box asking
      students to generate their own list of disagreements before the
      prepared dichotomies list is shown, reframing it from a presented
      board of tensions into an activity.
- [x] **Implemented.** (#9) Pulled the labor-disruption line out of a
      trailing sentence into its own pull-quote, sharpened to name coding
      as the clearest current example of "work changes, doesn't
      disappear." Written as directional framing, not backed by a
      specific stat — didn't want to fabricate a number under time
      pressure.
- [x] **Implemented.** (#10) Retitled rather than reordered — "The Tech
      Industry Conversation" → "The Scaling Debate" (its actual, narrower
      scope) and "Skeptics vs. Optimists" → "The Bigger Picture: Skeptics
      vs. Optimists," with a line explicitly noting it's a wider, separate
      split from the scaling one right before it. Resolves the "which
      optimists/skeptics is this" confusion without needing to move
      content around.
- [x] **Implemented.** (#11) Reuters entry enriched with the angle Adiel
      was actually pointing at (Fact Genie was already on the page) — AI
      built into "Leon," Reuters' daily CMS (headline suggestions,
      summaries, error detection), plus the 6–8 second alert-speed stat.
      The Zapier/no-code example went into Use Cases (#12/#13 below)
      instead of here, since it's a concrete deployed example matching
      that section's pattern more than this page's policy/culture focus.

### Day 1 — Use Cases

- [x] **Implemented.** (#12) Legal example replaced: Harvey AI (142,000+
      legal professionals, ~half the Am Law 100, used for discovery —
      the direct parallel to document-heavy reporting Adiel wanted).
      Added a new **Finance** row (Mastercard's fraud-detection model,
      ~1 trillion data points, <50ms per transaction) rather than folding
      it into Legal, since Adiel raised it as a distinct example. UPS
      ORION/Logistics **dropped rather than replaced** — the research
      agent couldn't find a comparably well-sourced current alternative
      (candidates traced only to secondary SEO/consultant blogs, not
      primary sources), so this followed the site's existing pattern of
      dropping weak citations rather than forcing one in (see Batch 9).
- [x] **Implemented.** (#13) Customer service and Content moderation rows
      now explicitly note they're also business-side newsroom tools, not
      purely "outside" journalism, with an intro line on the section
      making the same point generally.
- [x] **Implemented.** (#14) Both flagged claims softened: investigative
      reporting now says AI can help with *pieces* of the process (cross-
      referencing the Data Journalism/Records & FOIA rows above it) even
      though it can't do the whole thing; the real-time item reframed
      from "can't do real-time" to "the cutoff is a workflow problem, not
      a hard wall," while keeping the real, narrower limitation (it can't
      verify a live source itself).
- [x] **Implemented.** (#15) Added "finding needles in haystacks — pattern
      recognition, lead generation" as its own line in the Works When
      column, and reframed "speed matters more than perfection" into
      "you need an 'at least this many' count, not an exhaustive one" —
      Adiel's exact framing.
- [x] **Implemented.** (#16) Reframed exactly as suggested: "does this need
      original judgment *every single time* — or can I design the
      process so judgment only happens on a smaller, surfaced set?"
- [x] **Added, not in Adiel's original list**: a new "No-code automation"
      row using Simon Galperin's Zapier-based Bloomfield Information
      Project (research-verified) — this is where the Zapier use case
      from #11 landed. **Flagging a real overlap**: Simon Galperin is
      already cited on People to Follow for the same underlying
      small-newsroom-automation story (The Jersey Bee). Cross-referenced
      the two entries explicitly rather than hiding the duplication —
      worth a look to confirm that's the right call rather than swapping
      in a different example.

### Day 1 — People to Follow

- [x] **Implemented.** (#17) Added an "Employer" column across all 27 rows
      (derived from each entry's existing, already-verified "what to
      know" text — not new research; org/publication rows get "—" since
      Employer doesn't apply). Karen Hao recategorized from "Critic" to
      "Journalist." Added the Tow-Knight Center's Substack, "(Re)Structured
      News" by Gina Chua — URL and current focus (AI's impact on
      journalism) confirmed by the research agent.

### Day 1 — Project Ideation

- [ ] (#18) Still open — clarify who students are building for before the
      "what frustrates you" prompts. Now applies to Problem Statement's
      "Finding a Problem Worth Solving" section post-restructure, not the
      original Project Ideation page (which no longer exists under that
      name — see Product Discussion above).
- [x] (#19) No action needed — hypothesis section well-received as-is.
- [ ] (#20) Still open — solo vs. pairs. **Partially resolved by the
      revision pass above**: Product Discussion (the idea-sharing part)
      is confirmed group; Problem Statement (the hypothesis/goal part) is
      confirmed individual-then-share-out. Adiel's underlying "should
      this be solo" question is answered for Problem Statement; Product
      Discussion being a group activity was a separate, explicit user
      decision, not derived from Adiel's guess.

### Day 1 — AI Tools

- [x] Already resolved earlier (Batch 11) — tool list moved to
      `resources.html`, session content simplified to evaluating +
      familiarizing. See above.

### Research agent findings applied above (2026-08-11)

A second background research agent verified: Cowork's research-preview
date (Jan 12, 2026, TechCrunch) and GA date (April 9, 2026); Skills'
launch date (Oct 16, 2025, official Anthropic post); Harvey AI's
adoption/valuation figures; Mastercard's fraud-detection stats; the
Bloomfield Information Project/Zapier case study; the Leon CMS/Fact Genie
speed stat; and the Tow-Knight Substack URL. Full findings with every
source URL and confidence level aren't persisted elsewhere — if a
citation needs re-verification later, the research would need to be
re-run rather than pulled from a saved report.

### Use-case currency rule clarified, and applied — 2026-08-11

User clarified the actual rule after reviewing the earlier "old sources"
list: sources cited as **historical facts or terminology** (AlexNet's
2012 win, "filter bubble" coined in 2011, IDx-DR's 2018 "first
FDA-authorized" milestone) are fine to stay old — the date *is* the
point. Sources cited as **live use cases** (claiming a practice is
ongoing/current) need to meet Adiel's "avoid 2023 or earlier" bar. A
third research agent checked the two remaining flagged examples against
this:

- [x] **AP's automated earnings reports — dropped entirely** (Industry
      Conversation's "Associated Press" row and Use Cases' "Routine news"
      row, both Overview + Slides). No citable 2024–2026 source exists
      confirming current scale, vendor, or even that AP still runs this
      the way the 2015 source describes — the automation vendor
      (Automated Insights/Wordsmith)'s current marketing has pivoted
      entirely to sports/betting content, a real signal the original
      arrangement may not reflect AP's current state. Followed the site's
      existing house rule (drop rather than force in a weak citation —
      see Batch 9, UPS ORION above) rather than keep it caveated as
      historical, since Use Cases' own framing explicitly claims these
      are "real, deployed use cases, not theoretical ones."
- [x] **Chequeado's Chequeabot — updated, not dropped.** Strong current
      sourcing exists (Chequeado's own May 2024 and Sept 2025 posts
      confirm it's still active, in production, and expanded since 2016
      to cover podcasts and dozens of channels). Also **corrected a
      real understatement**: the "1 in 5" figure from the old 2019
      source is stale on the *low* side — Chequeado's own reporting
      suggests roughly half of certain fact-checks now originate there.
      Rewrote to "roughly half... and growing" rather than asserting a
      precise current percentage I don't have.

### "Claude-speak" / tone pass — sample on State of AI, 2026-08-11

User flagged that Adiel's original PR feedback included a note this
project's own digest had dropped: some passages "read very claude-speak."
Combined with new guidance from the user directly: descriptions
shouldn't sound absolute; the voice should be **thoughtful and
constructively skeptical**, grounded in concrete examples, with a sense
of **curiosity and insight** rather than declarative hype. User asked for
a sample pass on State of AI first, to approve the direction before it
rolls out further — **approved, "sounds a bit better," asked to extend
it across the whole page** (done, both rounds, Overview + Slides, 7
spots total):

- Opening lede rewritten — cut "one of the most consequential technology
  shifts in decades" and "suddenly accessible to everyone" (unverifiable
  superlatives), replaced with a grounded framing that names the
  hype-vs-reality tension directly instead of only asserting the hype
  side.
- "Faster than any app in history" → "one of the fastest consumer
  product launches ever" (defensible; the original was an unverified
  superlative).
- "Impossible three years ago" → "far beyond what these models could do
  three years ago" (defensible; "impossible" overclaimed).
- "Everyone's tool" / "anyone could pick up" → "most people have at
  least tried" / "millions of people were actually trying" (removed
  unsupported absolutes; the second rewrite deliberately ties to the
  1M-in-5-days stat right below it instead of asserting an unsupported
  "most people," which the site's own later Pew citations don't actually
  support for year one).
- AlexNet/2012 entry: "this is where the modern AI boom actually starts"
  (flat causal claim) → reframed into an observation with more curiosity
  — "the shifts that turn out to matter most rarely look big while
  they're happening."
- Landscape section closer: "expect the landscape to keep shifting"
  (filler) → named the actual pattern (new capability arrives, then
  months pass before anyone knows what to do with it) instead of a
  generic closing line.
- "Essential" (stakes-for-you) → "turning into a basic job skill" —
  echoes s4's own "AI is a tool in your kit now, the way Google Docs or
  Slack is" framing instead of introducing new absolute language.
- **Not yet done**: same treatment on Industry Conversation, Use Cases,
  and People to Follow — holding for explicit go-ahead per the
  sample-first workflow the user asked for.

---

## Site-wide color palette alignment (new initiative — 2026-08-06)

User wants this site's color palette to feel *related to* their personal
site (andrewrcalderon.com) without being identical — same family, used
differently. This touches the shared root CSS variables in
`docs/css/style.css` (and their aliases in `docs/css/briefing.css`), so
it's sitewide and ADR-sized, not a page-level tweak. Not started —
logged only.

**Current workshop palette** (`docs/css/style.css`): purple `#9b7ebd` /
purple-dark `#6b4a7f`, orange `#f4a460` / orange-dark `#d97e2a`, cream
`#f5f1e8`, text `#2c2c2c`/`#666`.

**Personal site's actual palette**, pulled directly from
`andrewrcalderon.com/styles/custom.css` (not guessed):

- Purple (dominant accent, 23 uses): `rgb(149, 90, 245)` / `#955AF5` —
  notably more vivid/saturated than the workshop's muted lavender.
- Coral-red (2nd accent, 18 uses): `#E8664A` — warm, but reads as
  coral/red rather than the workshop's sandy orange.
- Near-black text: `rgb(48, 47, 47)` / `#302F2F`.
- Teal (secondary accent, 9 uses): `#1D8B8A` — **not present at all** in
  the workshop's current palette.
- Cream background: `#FFFBEF` — close in spirit to the workshop's own
  `#f5f1e8`, already similar.
- Darker purple variant: `rgb(109, 60, 200)` / `#6D3CC8`.
- Gold accent (minor use): `rgb(252, 185, 2)` / `#FCB902`.
- Light purple tints (backgrounds/borders): `#f3edff`, `#F8F5FF`,
  `#D4C8F8`.
- Dark navy (minor use): `#0D2B3A`.

**Observation**: both sites already independently land on a
purple+warm-accent+cream trio, which makes "related but not identical"
very achievable — e.g., shift the workshop's purple hue closer to the
personal site's more vivid violet while keeping it a distinct shade, warm
the orange toward coral without matching `#E8664A` exactly, and consider
introducing the teal as a new tertiary accent the workshop site doesn't
currently have. Needs a proposed derived palette (with actual hex swatches
for approval) before touching any CSS variables — not done yet.

---

## Day 1 schedule & Claude Desktop pivot (new initiative — 2026-08-11)

User is auditing Day 1 at the structural level — schedule shape and tool
stack — separate from the per-page copy batches above. Not implemented —
logged only, per the review workflow (organize first, implement once the
user says go).

### Schedule structure (applies to all three days going forward)

- [ ] Standard day shape: **10:00 AM–1:00 PM, 1-hour lunch, 2:00–5:00 PM**.
      `schedule.json`'s Day 1 times are already flagged "PLACEHOLDER"; this
      replaces that placeholder. Day 2/3 haven't been reviewed against this
      rule yet.
- [ ] **One 15-minute break in the morning only.** No afternoon break — the
      afternoon is hands-on.
- [x] **Resolved 2026-08-11 — final Day 1 timing, approved after two rounds
      of preview**:

      ```
      10:00  State of AI              15 min
      10:15  Industry Conversation    30 min
      10:45  Use Cases                30 min
      11:15  Break                    15 min
      11:30  Product Discussion       90 min   (was Project Ideation)
      1:00   Lunch                    60 min
      2:00   Problem Statement        40 min
      2:40   AI Tools                 15 min
      2:55   Explore Claude Desktop   55 min   (was Explore Tech Stack)
      3:50   Fork & Submit            25 min
      4:15   Project Assignments      45 min
      5:00   END
      ```

      Afternoon math: original session lengths totaled 250 min against a
      180-min budget. User chose to protect Project Assignments (hands-on
      buddy build time) and trim Explore Claude Desktop instead, over the
      reverse. "Nudge & Check-in" (previously a 15-min slot after 5:30pm)
      is **dropped as a separate scheduled item** — no room under the hard
      5pm end; fold a brief nudge into Project Assignments' close if
      wanted.
- [x] **Implemented 2026-08-11**: `docs/data/schedule.json` rewritten with
      the table above. Verified valid JSON and matches the approved times
      exactly.

### Remove "People to Follow" as a scheduled session

- [ ] Drop `day-1/04-people-to-follow` from `schedule.json`'s session list
      (frees ~15 min + its slot).
- [ ] Keep the page itself live at its current URL — it becomes
      resource-only, not a numbered/timed session. `resources.html`
      already links to it (`#s2`); that link keeps working since the file
      doesn't move.
- [ ] Day 1 index timeline, topic-metadata prev/next links, and the
      numbered TOC sequence (05→10) all need renumbering once this session
      drops out of the sequence — whether to renumber files 05–10 down to
      04–09, or leave a numbering gap, not yet decided.

### Project Ideation / Problem Statement split

- [x] **Resolved 2026-08-11**: "Project Ideation" (`05-project-ideation.html`)
      is **renamed "Product Discussion"** and becomes a pure discussion of
      students' own project ideas — no problem-solving framework content
      at all. It's a **group activity**.
- [x] **Resolved**: all of the problem-solving framework content moves to
      the post-lunch "Problem Statement" session
      (`06-problem-statement-discussion.html`, currently a placeholder):
      Finding a Problem Worth Solving (s2), Get Specific (s3), Form a
      Hypothesis (s4), Articulate Your Goal (s5), and the Workshop
      Activity exercise + Google Form submission (s6). Problem Statement
      is **individual work, then share out** as a group.
- [ ] "The Design Process Is Circular" (s1, the process-wheel) — which
      session it frames still isn't decided. Given Problem Statement now
      owns the whole framework arc (questions → hypothesis → goal →
      exercise), it likely belongs there as the opening frame rather than
      in Product Discussion — not yet confirmed.
- [ ] File rename still open: does `05-project-ideation.html` get renamed
      to match "Product Discussion" (e.g. `05-product-discussion.html`),
      or keep its filename with just the on-page title/nav label changed?
      Ties into the broader Day 1 renumbering question above.

### Day 1 tech stack: Claude Desktop instead of Claude Code/VS Code

- [ ] Day 1's hands-on tool session (currently `08-explore-tech-stack.html`)
      reworks around **Claude Desktop**: the app itself (not the Claude
      Code CLI/VS Code extension), giving Claude access to local files, and
      Claude Desktop's **GitHub integration/connector** (not VS Code's
      Source Control panel).
- [ ] **Confirmed 2026-08-11**: page renamed/refocused from "Explore Tech
      Stack" to an "Explore Claude Desktop" framing — a live,
      instructor-guided walkthrough of the Claude Desktop environment in
      the classroom, with **special emphasis on the code environment**.
      Exact title text and section-by-section roadmap not drafted yet —
      s1 (Why This Session), s2 (Session Roadmap), and s6 (How They Work
      Together) all need to be rewritten from scratch for Claude Desktop
      rather than moved, since they currently describe the VS Code/Claude
      Code/GitHub workflow directly (distinct from s3–s5 below, which
      relocate to Day 2 largely as-is).
- [x] **Research complete (background agent, 2026-08-11) — verifies and
      corrects Adiel's "cowork" description.** Sourced against official
      Anthropic docs (`code.claude.com/docs/en/desktop`,
      `claude.com/docs/cowork/overview`, `support.claude.com`), high
      confidence:
      - **"Cowork" is real**, not a mishearing. Claude Desktop has three
        tabs: **Chat**, **Cowork**, and **Code**. Cowork is an agentic
        workspace for document/research/spreadsheet-style work (attach
        "workspace folders," step away, come back to a deliverable) — it
        is **not** IDE-like (no file editor, no terminal, no diff view).
        **Code** is the actual coding surface and genuinely is
        VS-Code-like: file editor, integrated terminal, diff viewer with
        inline comments, multi-session sidebar, PR creation/monitoring —
        same engine as the Claude Code CLI. **This session's "special
        emphasis on the code environment" should center on the Code
        tab**, using Cowork/Chat only as needed for file access and
        connectors.
      - **Filesystem access**: Cowork uses "workspace folders" (folder
        picker, scoped access); the Code tab uses a "Project folder"
        (same unscoped model as opening a folder in VS Code); Chat/either
        tab can also add a filesystem **Connector**.
      - **"Customize" panel confirmed real** — single place for
        connectors/skills/plugins; **`/schedule`** or the Cowork sidebar
        for scheduled tasks (runs remotely, even laptop closed). Adiel's
        description of this was accurate.
      - **Hard constraint for setup/logistics**: both Cowork and Code
        **require a paid plan** (Pro/Max/Team/Enterprise) — not available
        on a free account. Doesn't change any plan (Adiel is already
        arranging paid seats — see the excluded Logistics note above),
        but must land explicitly in `setup.html`'s Day 1 prep.
      - **Windows-specific**: opening the Code tab at all requires **Git
        for Windows** to be installed (Desktop prompts for it). Relevant
        to Day 1 setup regardless of which Fork & Submit path gets
        chosen, since the Code tab itself needs it just to open.
      - Full agent report (with every source URL) isn't persisted
        elsewhere — re-run the research if a citation is needed later
        and isn't summarized here.
- [ ] VS Code walkthrough (s3), Claude Code best-practices/mindset (s4),
      and the VS Code-based GitHub walkthrough (s5) are **not deleted** —
      they move to Day 2, which already plans to introduce VS Code, Claude
      Code, and Git from the code editor. Exact Day 2 slot/page not decided
      yet (Day 2 hasn't been reviewed).
- [x] **Resolved 2026-08-11**: "Fork & Submit" (`09-fork-and-submit.html`)
      **stays on Day 1**, rebuilt entirely around **Claude Desktop's
      GitHub connector (option 2 above)** — OAuth device-flow sign-in via
      Chat/Cowork, no local Git, no `gh`, and explicitly **no GitHub
      Desktop app**. The whole fork → edit → commit → PR flow happens
      conversationally inside Claude Desktop. GitHub Desktop is dropped
      from the plan entirely, not kept as a fallback.
- [x] Superseded — see Batch 11 in the "Full-scale site review" section
      above: user decided to delete `07-ai-tools.html`'s "For This
      Workshop" section entirely rather than update its required-tools
      list.
- [x] **Implemented 2026-08-11**: `setup.html` splits into two labeled
      parts on one page (decided against a separate page, to keep one
      canonical setup URL): **Day 1 Setup** = Claude Desktop app (install,
      sign in, paid-plan note) + a GitHub account (connecting it to Claude
      Desktop is left for the live Explore Claude Desktop session, not
      pre-work). GitHub Desktop dropped entirely. **Day 2 Setup** = VS
      Code, Claude Code extension, Git — carried over close to the
      original pre-pivot content, relabeled as post-Day-1 prep.

## Implementation pass, 2026-08-11 — what actually got built

Everything above in this section is now implemented, not just logged.
Summary of the concrete changes:

- **Renumbered/renamed** all Day 1 Overview + Slides files via `git mv`
  (history preserved): `04-people-to-follow` → `people-to-follow` (dropped
  from the numbered sequence, kept as a resource, removed from the nav
  dropdown); `05-project-ideation` → `04-product-discussion`;
  `06-problem-statement-discussion` → `05-problem-statement-discussion`;
  `07-ai-tools` → `06-ai-tools`; `08-explore-tech-stack` →
  `07-explore-claude-desktop`; `09-fork-and-submit` → `08-fork-and-submit`;
  `10-project-assignments` → `09-project-assignments`.
- **`schedule.json`** rewritten with the approved Day 1 table; Day 2/3
  still placeholder.
- **`nav.html`, `resources.html`, `setup.html`, `project-ideas.html`**
  updated for the new paths/names.
- **Content rewritten**: Product Discussion (pure group discussion, no
  framework), Problem Statement (absorbed the full framework arc,
  upgraded from a placeholder to the briefing template, got a new Slides
  deck), AI Tools (trimmed to Evaluating + a new Familiarizing section),
  Explore Claude Desktop (fully rebuilt around Chat/Cowork/Code per the
  research findings), Fork & Submit (rebuilt around the GitHub connector,
  no GitHub Desktop). All six got matching Slides decks, kept in parity —
  verified with `project/scripts/check-slide-parity.js` (clean run).
- **`resources.html`** gained a new "AI Tools Landscape" section (the
  migrated tool categories) — implemented as a plain categorized list,
  not a filterable table, to match the page's existing simple style.
- Verified: valid JSON, every internal Day 1 link resolves to a real
  file, every `data-session-id` matches its `schedule.json` id, slide
  parity checker clean, HTML tag balance spot-checked.

**One honest caveat, not verified**: Fork & Submit's copy describes
asking Claude to bridge a local Code-tab project folder into a fork via
the GitHub connector, and Explore Claude Desktop describes Cowork
"handing off" to a Code session. The research confirmed the GitHub
connector's read/write capabilities and that Cowork *can* orchestrate
both local files and connectors, but didn't verify the exact click-by-
click mechanics of that hand-off. **Recommend walking through this flow
firsthand in Claude Desktop before teaching it live** — the concepts
should hold, but the precise UI steps might not match exactly.

### Revision pass, 2026-08-11 (round 2) — user reviewed the implementation

User reviewed the pages above and came back with corrections, applied
directly (not just logged):

- [x] **Product Discussion**: "The Design Process Is Circular" moved out
      entirely, into Problem Statement (see below) — Product Discussion
      is now just 2 sections (Why We Start Out Loud, Workshop Activity).
      Cut the "Good ideas rarely survive first contact with an empty
      room" line as a platitude; user's broader note: **avoid platitudes
      in the copy generally**, not just here. s1 reframed to plainly
      remind students they brought an idea in and we want to hear it, no
      flourish. Workshop Activity rewritten as literal instructions
      instead of vague description: students go around the room; since
      most will have brought more than one idea, they pick the one
      they're most excited about and talk about just that one; the group
      asks questions and reacts afterward.
- [x] **Problem Statement**: gained "The Design Process Is Circular" as
      its new opening section (s1), reframed to say the group did the
      first two steps this morning in Product Discussion and now it's
      individual work through the rest — same wheel, same citation, just
      relocated and reworded for the new context.
- [x] **No submission mechanism for now.** The Google Form
      embed/iframe and the "Submit Your Problem Statement" exercise-box
      are removed from Problem Statement entirely — **tabled, not
      cancelled**. User floated a possible lighter-weight future version
      (drop into a CSV held in the repo, surfaced somehow) instead of
      wiring up an actual Google Form, but explicitly does not want that
      built now either. `docs/day-1/project-ideas.html` and
      `docs/js/project-ideas.js` (the cards-gallery infrastructure from
      [ADR 0017](adr/0017-project-ideas-google-form.md)) are **left in
      place but now fully unlinked** — no page links to them anymore.
      Revisit ADR 0017 if/when a submission mechanism actually gets
      built, since the CSV-in-repo idea is a different architecture than
      what's there now.
- [x] **Explore Claude Desktop**: "How It All Works Together" kept (not
      deleted) but reworked into **"Building Is a Loop, Too"** — no
      longer a straight line ending at "Shipping." Now a 7-step
      `.process-wheel` (same circular component as the Design Process
      wheel, deliberately — visual callback to the same idea): Ideation →
      Planning → Building → Reviewing → Testing → Iterating (hinge) →
      Repeat. Shipping (commit + PR via the GitHub connector) is now a
      separate line noting it happens "whenever you're ready," not a
      forced final step in the loop — that's what Fork & Submit actually
      covers.
- All changes mirrored in both Overview and Slides for the three
  affected pages; re-ran `check-slide-parity.js` (clean) and re-verified
  JSON/link/tag-balance/`data-session-id` integrity after this round —
  all clean.

### Setup pages split for shipping, 2026-08-11

User needs to send students a link to Day 1 setup imminently, so
`/setup.html` had to stop being a two-day combined page and become a
single-purpose, shippable URL.

- [x] **`/setup.html` is now Day 1 setup only** — the page that's
      actually going out. Title/H1 changed to "Day 1 Setup" so a
      standalone shared link is unambiguous about scope. Confirmed no
      other page expected Day 2 content to live at this URL (`index.html`,
      `nav.html`, `footer.html`, and Explore Claude Desktop's two "do
      setup first" links all just say "(pre-workshop) setup," which
      still holds true).
- [x] **New page `/setup-day-2.html`** — the former "Day 2 Setup" half,
      moved wholesale, same content. **Not linked from nav or footer, and
      not hyperlinked from `/setup.html` either** — `/setup.html` mentions
      it exists in plain (non-clickable) text ("you'll get that link
      closer to Day 2") so students don't go looking for it early. It's
      fully built and live at its URL now, ready for whenever it needs to
      go out.
- [x] Both pages verified: tag balance, checkbox count matches the static
      "N of 7" / "N of 10" fallback text, all sitewide links still resolve
      to `/setup.html` correctly (grep-verified, none pointed at Day 2
      content).

### Downstream, not yet touched

- [x] `STUDENT_CLAUDE_GUIDE.md` reflects the Claude Desktop (Day 1) vs.
      VS Code/Claude Code/GitHub Desktop (Day 2+) tooling shift.
      **Resolved 2026-08-20** — confirmed as a real, still-open gap (not
      stale) when revisited: the guide said nothing about the shift, so a
      new "Where this file kicks in" section was added. See the Phase 5
      `STUDENT_CLAUDE_GUIDE.md` bullet above for the full change list from
      this pass.
- [ ] Adiel's 21 per-page content notes (logged in the "Collaborator
      feedback" section above) — in progress, see next section.
- [x] Resolved 2026-08-13: **Day 2 is built.** Retimed to the same
      10–1/lunch/2–5 shape as Day 1 (see the Day 2 schedule change log entry
      below). Note this landed with a different content shape than this
      line originally assumed: VS Code/Claude Code/Git didn't move into Day
      2, Day 2 stayed inside Claude Desktop/Claude Code conceptually
      (prompting, CLAUDE.md, Skills, plan mode, spec-driven development).
- [x] Resolved 2026-08-13: **Day 3 is also built** (same day as Day 2, see
      the Day 3 change log entry below), and it didn't pick up the VS
      Code/Git content either — Day 3 turned out to be product design,
      responsible/auditable AI, human-AI collaboration, industry
      application, then final build time and show & tell. **The VS
      Code/Claude Code/Git question from the line above is still genuinely
      unresolved** — that content doesn't have a home in any of the three
      days as currently built. `docs/setup-day-2.html` still carries this
      material as pre-workshop setup only; whether it needs an in-class
      home too is an open decision for whoever reviews the finished
      3-day arc next.

---

## Full-scale site review, round 3 (in progress — 2026-08-15)

User is reviewing Day 2 then Day 3 page by page and passing notes in
batches, same workflow as the first two review rounds above (see
`review/full-site-audit-2`'s "Full-scale site review" and "Collaborator
feedback" sections). Logging each batch here as it arrives; not
prioritized or implemented yet — that happens once the review is
complete and batches are grouped.

### Batch 1 — Day 2, Topic 1 (Yesterday's Debrief)

Applies to `docs/day-2/01-debrief.html`. This topic wasn't touched by the
2026-08-15 content-depth revision (logged below in the change log —
confirmed at the time as already at the right depth for a discussion
session), so this is fresh feedback, not a follow-up to that pass.

- [x] **s1 lede, closing clause** — **Implemented 2026-08-16.** Reworded
      to: "The point of a debrief isn't to compare. It's to observe what
      happened while you were working, in the code and in yourself,
      before we move on." (Overview; Slides drops the intro sentence and
      "before we move on" per that page's usual condensed pattern.)
- [x] **s2 exercise-box, "Group share-out"** — **Implemented 2026-08-16.**
      Renamed to "Talk It Through," dropped the Time/Format structure,
      now: read the questions on your own first, then open group
      conversation, jump in/build on each other/share your own moment, no
      fixed order. Applied to both Overview and Slides (Slides condensed).

### Batch 2 — Day 2, Topic 2 (Prompting)

Applies to `docs/day-2/02-prompting.html`. This topic *was* one of the 5
rewritten in the 2026-08-15 content-depth pass — this is a follow-up
polish round on top of that rewrite, not a first pass.

- [x] **Masthead dek, sentence 1 — confirmed wording.** '"Prompt
      engineering" used to mean tricks.' → **'"Prompt engineering" used to
      mean hacks."'** (confirmed via clarifying question; transcript was
      ambiguous about whether to drop the "prompt engineering" term
      entirely — user kept it, just swapped "tricks" → "hacks").
- [x] **Masthead dek, sentence 2, closing clause — implemented
      2026-08-16.** "...and knowing when Claude can help you get there" →
      "...and knowing how best to work with Claude to help you get
      there."
- [x] **s1 history, "The role-play era" (Dec 2022) item — implemented
      2026-08-16.** "...was the dominant advice for years." → "...was the
      dominant advice." per the original reading (not re-confirmed with
      the user, but low-stakes/reversible).
- [x] **s1 history, "Claude starts writing prompts for you" (2024) item —
      implemented 2026-08-16, comparable found.** Research confirmed
      OpenAI shipped a real comparable the same year: a single "Generate"
      feature in its Playground (Oct 1 2024) that both drafts and refines
      prompts, functionally covering what Anthropic split into two named
      tools. Added as a named comparison with its own citation.
- [x] **s1 history, "Less scaffolding, more curation" (2025) item —
      implemented 2026-08-16.** Replaced the vague line with the actual
      substance from Anthropic's Nov 2025 post: what matters less now
      (heavy role prompting, XML scaffolding, with the stated reasons)
      and what matters more (being explicit, explaining reasoning,
      real examples), live-verified and quoted in the citation notes.
- [x] **s4 exercise, "Rewrite One of Yours" — implemented 2026-08-16.**
      Dropped the self-rewrite step. New flow: hand a Day 1 prompt
      straight to Claude to improve, then compare against 3 questions
      pulled directly from this session's own before/after content (more
      specific? a way to check the result? dropped something
      unnecessary?), then reflect in the deliverable on what you actually
      wanted and what you could have told Claude the first time. Applied
      to both Overview and Slides.

### Batch 3 — Day 2, Topic 3 (CLAUDE.md)

Applies to `docs/day-2/03-claude-md.html`. Like Topic 2, this was one of
the 5 pages rewritten in the 2026-08-15 content-depth pass — this round
is mostly about making the page land for a non-coder audience, not a
first pass.

- [x] **s2 "A Real Example" — implemented 2026-08-16.** Added a real
      GitHub link plus a click-to-open file-viewer (new `<dialog>`
      component, see [ADR 0019](adr/0019-file-viewer-dialog.md)) holding
      the actual, byte-faithful text of this repo's `CLAUDE.md`. Closing
      paragraph now explicitly names what to emulate (point not
      duplicate, write down what Claude can't guess, organize by when
      you'll need it) and connects it to the department-decisions reframe
      below. Applied to both Overview and Slides (duplicated dialog
      markup, since Slides is a standalone page with no shared script
      state with Overview).
- [x] **s3 "What Belongs In One" — cut the two technical example
      paragraphs — implemented 2026-08-16.** Both removed from Overview
      and Slides. Kept the Include/Leave-out compare-grid columns (see
      next item).
- [x] **s3 Include/Leave-out columns — rewrite for a cross-department
      audience — implemented 2026-08-16.** Include now leads with
      design-system and audience-persona examples alongside the
      structural/gotcha ones. Leave-out grounded in Anthropic's own
      "Write an effective CLAUDE.md" table (live-verified via research):
      added "detailed documentation, link to it instead" and
      "information that changes often" as sourced, quotable categories
      that were missing before. Did not find external cross-department
      CLAUDE.md examples to cite (user later steered away from that
      search, see the s2 note above — this repo's own file became the
      running example instead).
- [x] **s3 closing stat-pull — expand into a few self-check questions —
      implemented 2026-08-16, with an honest caveat.** Research found
      only one verbatim Anthropic self-check question ("would removing
      this cause Claude to make mistakes?"). Added one more, grounded in
      the `/doctor` command's description of what it strips ("could
      Claude figure this out just by looking at the project itself?")
      rather than inventing 3-5 questions to hit a round number — the
      research agent explicitly recommended against presenting more as
      if Anthropic had framed them as self-checks, and that's the call
      made here.
- [x] **s4 exercise, "Draft Your CLAUDE.md" — implemented 2026-08-16.**
      `/init` exercise kept. 200-line requirement dropped. Deliverable
      reframed to generate-then-reflect: read what `/init` produced, and
      for a few things it summarized, ask whether it was explicit or an
      inferred abstraction. Applied to both Overview and Slides.
- [x] **Standing direction for this whole section — addressed via the
      items above**, plus the new file-viewer and department-reframed
      columns specifically aimed at making CLAUDE.md legible to someone
      outside engineering.

### Batch 4 — Day 2, Topic 4 (Skills & Best Practices)

Applies to `docs/day-2/04-skills-best-practices.html`. Also one of the 5
pages from the 2026-08-15 content-depth pass — same pattern as Topics 2–3,
a follow-up polish/practicability round, not a first pass. Also raised a
**standing punctuation preference, not scoped to this page** — see the
note at the end of this batch.

- [x] **Masthead dek — cut after "re-explaining" — implemented
      2026-08-16.** Now reads: "Package your expertise so it doesn't need
      re-explaining."
- [x] **s2 "What Actually Makes This Work" — expand each bullet into an
      explained if/then pattern — implemented 2026-08-16.** All three
      bullets rewritten as cause-and-effect (Gotchas from real vs.
      imagined failures, why skipping the no-skill baseline matters,
      vague descriptions vs. reliable activation). Overview and Slides.
- [x] **s3 "A Real Investigation" — replaced entirely — implemented
      2026-08-16.** New "Build One" section, 5 numbered steps (`.history`,
      same component now used on Spec-Driven Dev): notice the pattern →
      create the folder/file → fill in SKILL.md like an onboarding doc →
      test it two ways (auto-trigger + explicit invoke) → stress-test
      with real examples in a fresh conversation. Research confirmed the
      real mechanics (file paths, SKILL.md frontmatter, testing methods)
      live against Claude Code/Platform docs. **Hagar/MuckRock case
      study**: removed rather than relocated, no other obvious home for
      it on this page or elsewhere in Day 2 — flagging per the original
      side note, not silently dropped.
- [x] **s4 "Common Failure Patterns" — made practicable — implemented
      2026-08-16.** "The confident-looking failure" now explains the fix
      concretely (write real examples, test in a fresh conversation with
      messy input) and cites an accessible replacement source (see
      citation-hygiene item below). "The patch spiral" now includes a
      concrete self-check for when to rebuild ("could someone read the
      skill and still explain why each rule is there?"). The
      how-to-test-a-skill content gap is addressed inside the new s3
      (steps 4–5) rather than as a separate section, since it fit
      naturally into the build walkthrough.
- [x] **Drop the closing pull-question entirely — implemented
      2026-08-16.** Removed from both Overview and Slides.
- [x] **Citation hygiene, this page — implemented 2026-08-16.** (1) Moot,
      confirmed: the 3x-repeated Hagar citation was confined to the old
      s3, which no longer exists. (2) Replaced the paywalled Medium
      citation with a live-verified, confirmed-accessible source
      (`linas.substack.com/p/claudeskills`) — medium confidence fit per
      the research agent (supports the same "passes clean tests, fails on
      messy real input" claim, though with slightly different specific
      examples than the original).

**Standing style note surfaced here, applies beyond this page**: user
wants colons and dashes used sparingly in general across this site's
copy, favoring full, active sentences over colon-joined clauses (same
spirit as the existing no-em-dash rule — see
`feedback_no-em-dashes` — but this is a distinct, broader ask about
colons specifically, and dashes beyond just em-dashes). Not yet applied
anywhere; worth a site-wide pass once the audit's grouped, and worth
saving as a standing preference so future copy work defaults to it.

### Batch 5 — Day 2, Topic 5 (Your Goal & Plan Mode)

Applies to `docs/day-2/05-goal-plan-mode.html` (and its Slides deck for
the jargon item). Also one of the 5 pages from the 2026-08-15
content-depth pass.

- [x] **Resequence — reverted.** Batch 5 originally proposed moving Plan
      Mode before CLAUDE.md. User reviewed this in the round-3 plan
      (2026-08-16) and said to leave the day's order as-is for now. No
      file renumbering, `schedule.json`, or `nav.html` changes made.
- [x] **Jargon pass, both Overview and Slides — implemented 2026-08-16.**
      s2's "It compiled fine. It broke at runtime." → "Everything looked
      fine when Claude finished. It broke once someone actually used it."
      (Overview and Slides, Slides slightly more condensed).
- [x] **Restructure so the page alone is enough to actually go use Plan
      Mode — implemented 2026-08-16.** s1 now leads with the concept (2
      sentences), then a dedicated paragraph spelling out all three
      approve/review/send-back options in full sentences, then a new
      paragraph on VS Code's inline-comment-on-plan feature (see below).
      Access mechanics now read as their own block, not one clause inside
      a longer paragraph.
- [x] **Remove s4's exercise-box, defer hands-on plan-mode practice to
      `07-revisit-build.html` — implemented 2026-08-16.**
      - **Open question, resolved at implementation**: removed s4
        entirely (TOC entry + section, both Overview and Slides), rather
        than keeping its framing text with no exercise attached. The
        "state your goal, then build" idea now lives properly in Revisit
        & Build instead. Flagging this as a judgment call, easy to revert
        if the page reads as ending too abruptly after s3.
      - **Cross-file change, done**: see the `07-revisit-build.html`
        change log entry for the new integration exercise.
      - **Still open, not addressed this pass**: `schedule.json` still
        types this session `hands-on` even with its hands-on exercise
        moved out. Left as-is since the session still has an implicit
        hands-on component reading the page and using plan mode
        interactively; revisit if that stops feeling accurate.
      - **New detail added, not in the original batch**: confirmed live
        (`code.claude.com/docs/en/vs-code`) that the VS Code extension
        opens a proposed plan as a real Markdown document, letting you
        highlight text and leave an inline comment on it directly. Added
        to s1 as a practical detail. Confirmed no equivalent exists in
        Claude Desktop, so the copy doesn't imply one (also resolves the
        long-open "cowork" terminology caveat in the Adiel-feedback
        section above, see that entry's update).

### Batch 6 — Day 2, Topic 6 (Spec-Driven Development)

Applies to `docs/day-2/06-spec-driven-dev.html`. Not one of the 5 pages
from the 2026-08-15 content-depth pass in terms of scope, but the same
nontechnical-audience standard applies throughout, per the user's
explicit audience note below (saved to project memory, see
[[ai-journalism-workshop-site-build]]).

- [x] **s1 "The Core Idea" — add a "what is a spec" foundation before the
      AI-specific content — implemented 2026-08-16.** Split into a new
      s1 "What a Spec Is" (general concept, non-AI, requirements/
      constraints/acceptance-criteria) followed by s2 "The Core Idea"
      (existing AI-specific content, unchanged in substance). TOC and
      section numbering updated in both Overview and Slides.
- [x] **Jargon: explain each term once, on first use — implemented
      2026-08-16.** "Pattern completion" glossed on first use ("matching
      what you ask against patterns they've already seen"); "codebase"
      glossed on first use ("a large project's existing code, its
      codebase"); "non-determinism" replaced with plain language
      ("how unpredictable real development actually is") rather than
      glossed, since a plain synonym was available.
- [x] **s2 "The Checklist" — drop the circular diagram, make it an actual
      checklist — implemented 2026-08-16.** Replaced `.process-wheel`
      with `.history` (linear steps, already used elsewhere for
      non-chronological step sequences, e.g. Day 1's AI Tools facilitator
      roadmap) plus a nested `.field-notes.is-checklist` per step for the
      self/team questions. All original citations preserved and
      redistributed into the new structure, nothing dropped. Closing
      "Put It Together, For Use With Claude" synthesis added, leading
      into the starter-prompt block (next item). Now s3 after the new s1.
- [x] **New component: an embedded starter-prompt block — implemented
      2026-08-16.** New `.code-block`/`.code-block-label` CSS
      (`docs/css/briefing.css`), a styled `<pre><code>` block, no JS. Used
      once so far, in the new "Put It Together" step, holding a
      copy-adaptable prompt template that walks Claude through building a
      spec from the checklist's answered questions. Condensed version
      also added to the Slides deck.

**Standing audience definition, surfaced here, applies site-wide, not
just this page**: user described the workshop audience directly —
non-technical graduate students taking this workshop to learn AI
concepts well enough to bring them "into the classroom and beyond" (not
just for their own use). Capable of real conceptual complexity ("mental
heavy lifting") as long as it's well-explained in plain language, not a
reason to oversimplify. Saved to
[[ai-journalism-workshop-site-build]] as standing context for all
curriculum copy going forward, pairs with the existing
[[content-depth-over-surface-level]] research standard.

### Batch 7 — Day 2 round-3, post-implementation corrections (2026-08-16)

User reviewed the round-3 implementation (Batches 1–6, all shipped
2026-08-16, see the change log entry below) and gave a second pass of
feedback on 4 of the pages. Logged only at the time; **all of
`01-debrief.html`, `02-prompting.html`, and `03-claude-md.html`'s items
below implemented 2026-08-20** as part of the copy-draft re-implementation
pass (`04-skills-best-practices.html`'s structural rewrite is tracked
separately below, still open).

**`01-debrief.html`** — [x] s2 exercise-box ("Talk It Through") given the
same Time/Description/Deliverable structure used by every other topic's
exercise-box.

**`02-prompting.html`** — [x] s4 exercise deliverable changed: instead of
free-form reflection sentences, the deliverable is now annotating the
original prompt directly, using the three comparison questions already in
the exercise as the annotation tool.

**`03-claude-md.html`**:
- [x] **File viewer is illegible as a popup.** Fixed 2026-08-20: replaced
      the `<dialog>`-based viewer with a native `<details>`/`<summary>`
      inline collapsible, see
      [ADR 0020](adr/0020-file-viewer-inline-collapsible.md) (supersedes
      [ADR 0019](adr/0019-file-viewer-dialog.md)). Root cause diagnosed
      this time via Playwright: `.briefing code`'s `white-space: nowrap`
      was winning over the parent `<pre>`'s `pre-wrap` on CSS
      specificity, so the markup swap alone reproduced the identical bug
      until a `.file-viewer-body code` override was added. Same fix
      applied to the Slides companion.
- [x] **Remove the haddock3/robotics-lab sentence** from the "It states
      what can't be inferred from code" roster row. Done.
- [x] **Weave concrete new examples into the closing paragraph.** Done,
      deduped against s3's Include column per the original instruction
      (dropped "audience segments" specifically since that already
      appears there; kept tone-of-language, words-to-avoid, and
      commitment-to-certain-tools as the genuinely new material).

**`04-skills-best-practices.html`** — structural rewrite, not just copy.
**All items implemented 2026-08-20:**
- [x] **New section 2: a non-technical "when you'd know you need a
      skill" scenario.** Landed as "When You'd Know You Need One": a
      README-explaining-itself-four-times example, with the same signal
      shown in reverse (a repeated correction) and a closing line pointing
      at directing Claude to build the skill.
- [x] **Old s2 ("What Actually Makes This Work") folded into Build One
      (s3), not deleted outright.** Landed inside step 3 ("Review the
      description it wrote"), in if/then cause-and-effect style: the
      description-specificity point and the watched-not-imagined gotchas
      point both moved there; the baseline-testing point moved into step 4
      instead, since that step is literally about testing.
- [x] **Build One becomes s3**, but further reframed per a user note
      given while reviewing the draft: steps now center on directing
      Claude to build the skill and reviewing what it produces ("Direct
      Claude to build it," "Review the description it wrote"), not
      hand-authoring `SKILL.md` yourself.
- [x] **"Common Failure Patterns" (old s4) deleted, replaced with
      "Testing It For Real."** Practical and step-by-step, speaks back to
      the new s2 scenario (hands the same README skill a messy real case).
      "Installing skills from strangers" kept, landed in the new s4 as
      originally leaning toward (not moved into Build One).

---

## Collaborator feedback — Adiel, PR #8 (2026-08-17)

Adiel (co-instructor) opened
[PR #8](https://github.com/AndrewRCalderon/2026-ai-news-innovation-workshop/pull/8)
"Day 2 & 3 review notes for discussion" from her fork, adding
`project/review-notes/2026-08-17-adiel.md` — notes from reading Day 2 and
Day 3 on the main preview build (91ea88d), no site files touched.
**Not merged**; digested into requirement items below, same workflow as
PR #1 above. User left 9 inline GH review comments responding to specific
paragraphs (pulled via `gh api repos/.../pulls/8/comments`); those
comments, plus follow-up direction given directly in conversation, are
what actually resolved each item — logged here alongside Adiel's original
point so the reasoning traces back to the PR without reopening it.

- [x] **Glossary idea (her §1, "Things to maybe add")** — Adiel proposed
      a collective class-glossary exercise (students teach Claude to PR a
      shared glossary doc as they hit new terms). **Superseded**: user's
      GH reply proposed a different mechanism instead — give students a
      `Claude.md` on Day 2 with the exercise changed from "generate one
      from scratch via `/init`" to "ask Claude to update this starting
      file based on what it observed about how you worked on Day 1."
      That starting file carries pedagogical instructions ("explain X,"
      assume a nontechnical user needs things explained). This is the
      origin of the `STUDENT_CLAUDE_GUIDE.md` task below — the glossary
      idea itself goes unaddressed unless picked up separately later.
- [x] **Common-pitfalls lesson (her §2)** — Adiel: "Yes! 100%... I
      struggled with size/granularity, wasn't sure what to assume was
      'basic' vs. advanced," floated a dedicated slide/lesson or a
      standalone resource page. **Content and placement both decided**:
      lives in `STUDENT_CLAUDE_GUIDE.md` (see task below), not a separate
      slide or resource page.
- [x] **Product Design §02 citations** — Adiel suggested 3 more-recent
      sources for slides 2 & 4 (audience preferences around AI):
      - Reuters Institute, *Digital News Report 2026*, ["Emerging uses of
        AI chatbots for news and what it means for
        journalism"](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/emerging-uses-ai-chatbots-news-and-what-it-means-journalism),
        June 16 2026 — chatbot use for news rose 7%→10% globally in a
        year.
      - CNTI, ["Action, Ease & Personalization: AI Chatbot News
        Experiences"](https://cnti.org/reports/chatbots-for-news/),
        Jan 22 2026 — people use chatbots to *act* and *understand* far
        more than to know about or feel something about the news.
      - Florent Daudens, ["The half of journalism AI can't do
        yet"](https://fdaudens.substack.com/p/is-ai-better-at-our-jobs-than-us),
        June 23 2026 — 93% of an AI article's claims linked back to
        source, vs. 25% for the human-written comparison.
      **Confirmed** ("Love it. Yes.") — work these into
      `docs/day-3/02-product-design.html` /
      `slides/02-product-design-slides.html`, slides 2 and 4.
- [x] **AI-Human Design, "judgment doing two jobs" (her §2 under
      "Suggested page changes")** — Adiel: the word "judgment" does two
      different jobs in the same lecture (the thing never automated in
      the Full Fact section, vs. the thing people get worse at when they
      adjust an algorithm, in the Green & Chen study section just
      before). User's GH reply: "a lot of my intuitions are literally
      about 'how I code'... there might be a conversation here between
      judgment and the admonishments [pitfalls] you alluded to."
      **Resolved differently than first logged in this file** — not
      offloaded to `STUDENT_CLAUDE_GUIDE.md`; becomes its own new section
      within `docs/day-3/04-ai-human-design.html` itself, bridging the
      editorial-judgment examples to judgment as it shows up in students'
      own AI-assisted coding practice. See the §04 rewrite task below.
- [ ] **AI-Human Design, Adiel's 3-question framing** — her suggested
      reframe: at each point in a process, ask whether the criteria can
      be written down, whether the person has information the model
      doesn't, and whether either of them can check the result. User's
      GH reply: "I think I get what you mean but I'd love for you to
      explain on our call so I am sure I grasp your meaning." **Not
      adopted for the §04 rewrite** — user's own notes (below) are the
      confirmed direction instead. This stays a "discuss on the call"
      item, tracked here, not blocking the rewrite.
- [x] **Where Can You Take This — Capelouto** — Adiel suggested adding
      J.D. Capelouto (Semafor: breaking-news reporter with no programming
      background, built newsroom tools via GPT Builder, now helping
      oversee the Semafor intern) alongside Andy Sullivan (Reuters) and
      Joe Amditis (skills library) as examples of people who started from
      a repetitive task they disliked, no budget, nobody's permission.
      **Confirmed** ("Oh yes, great!") — added to §05 slide 1 alongside
      Sullivan and Amditis. **Still open**: no citable public source for
      the Capelouto claim yet, unlike the other two examples on that
      page. Flagged inline in `docs/day-3/05-where-you-can-take-this.html`
      with an HTML comment; find and add a source before this ships.
- [x] **Course wrap-up** — Adiel: the section currently ends on a
      developer-slowdown stat that feels like an odd note right before
      final builds; proposed a "where we started, where we are now"
      closing review, timing TBD (before final build vs. after
      presentations in the 15-min Closing & Celebration slot). User built
      on this in GH comments (a dynamic, energizing "map" reflection with
      peer share-out) and initially leaned toward doing it before the
      final build. **Resolved differently in conversation** — final
      shape is a schedule reorder (Final Coding Time moves right after
      lunch, Where Can You Take This moves after it, immediately before
      Final Show & Tell) plus a third slide added to §05 with reflection
      questions tied directly into the show-and-tell. See the §05 task
      below; no separate wrap-up page or Closing & Celebration change
      needed. **Implemented 2026-08-19.**

**Not yet decided**: whether to merge/close PR #8 now that its content is
digested here (no site files in the PR to merge, same situation as PR #1)
— flagged as a follow-up, not done as part of this logging pass.

### New task: `docs/day-3/04-ai-human-design.html` + slides rewrite

**Implemented 2026-08-19.** Replace the current judgment-framing thesis
with the user's own framework:

- Reframe the section's core question: AI is often used to automate
  processes/tasks; there was an emphasis on human-in-the-loop, but that
  shouldn't be the default any more than automation should. Give
  students questions to ask themselves at each stage of a process to
  decide which fits.
- Two concrete cases to build the framework around:
  - Deliberately slow a process down by adding a human checkpoint
    anyway, because the human benefits from sitting with the output at
    that stage — it deepens their own knowledge or adds context they'll
    need later.
  - Skip the human at a given point because their perspective, context,
    or verification isn't actually needed there — automate
    top-to-bottom, bring a human in only at the very end to verify the
    final output.
- Draw from human-AI design literature where it genuinely supports this
  framing; the intuition itself comes from practitioner experience, not
  the literature — don't force a citation that doesn't fit.
- Existing Full Fact / Zillow / Green & Chen study material can likely
  stay as supporting examples, re-slotted under this framework rather
  than rewritten from scratch — confirm fit when actually drafting.
- **New section, on the page itself**: bridges this framework to
  judgment as it shows up in students' own AI-assisted coding practice —
  connect the editorial-judgment examples (Full Fact deciding which
  claims to check, Zillow's removed pricing checkpoint) to the same
  human-in-the-loop-vs-automate questions applied to their own coding
  choices. Content not yet drafted.
- Adiel's 3-question framing stays a separate, non-blocking "discuss on
  the call" item (logged above), not folded into this rewrite.

### New task: condense §05 + schedule reorder

**Implemented 2026-08-19**, with one item still resolved differently
than first logged here: no file rename was needed. Investigation found
the index page and Overview prev/next links are both driven dynamically
from `schedule.json` order, not filenames; only 3 hardcoded "Next
section →" links in the Slides decks needed manual updates
(`04-ai-human-design-slides.html`, `05-...-slides.html`,
`06-...-slides.html`), all done. Filenames stay as-is, now
non-chronological (`05` runs after `06` in the actual schedule) —
cosmetic only, nothing reads the prefix.

**Schedule change** in `docs/data/schedule.json` (lines 46-49): swap the
order of `day-3/05-where-you-can-take-this` and
`day-3/06-final-coding-time`. Durations make this a clean swap with no
other time changes needed: Final Coding Time moves to 2:00-3:00 PM (was
2:45-3:45), Where Can You Take This moves to 3:00-3:45 PM (was 2:00-2:45),
Final Show & Tell stays 3:45-4:45 PM unchanged, immediately after.

Flag for implementation: the `NN-` filename prefixes
(`05-where-you-can-take-this.html`, `06-final-coding-time.html`, both
Overview and `slides/`) currently encode schedule order. Decide then
whether to rename the files to match the new order or leave them as-is;
either way, check both pages (and slides companions) for hard-coded
next/previous-session copy that assumes the old order.

**Content change**, `docs/day-3/05-where-you-can-take-this.html` +
`slides/05-where-you-can-take-this-slides.html`: condense from 4 sections
to 3 slides:

1. Industry-integration observation: AI is being folded into *existing*
   roles more than it's minting dedicated AI job titles — reporters
   using AI to augment investigations, data journalists using it to
   scrape/analyze/visualize.
2. High-level strategic AI-focused roles that do exist, backed by real
   examples: keep Sullivan and Amditis, add Capelouto (confirmed above).
   **Implemented 2026-08-19.** Background research turned up 4
   candidates; 3 were well-sourced and added to the roster (now 6 total
   with the original 3): Julia Hood, Newsroom AI Lead, Business Insider
   (Talking Biz News); Erica Osher, VP AI Labs, NPR (Editor & Publisher,
   corroborated by 3 other outlets); Zach Seward, Editorial Director of
   AI Initiatives, NYT (TheWrap, role dates to Dec 2023 but confirmed
   still current into 2026). **Excluded**: Arlyn Gajilan, Global Editor
   AI Development & Integration, Reuters — real role, but sourcing was
   one independent newsletter plus a company org-chart site, weaker than
   the bar the rest of this page holds to. A Nieman Lab piece likely
   covers her directly (blocked WebFetch during research); worth adding
   later if someone can pull that article.
3. **New** — reflection/discussion slide: questions framing a
   conversation about what students are taking away from the whole
   program, what will stick with them, explicitly asked so they can
   incorporate those takeaways into Final Show & Tell, which now
   immediately follows on the new schedule.

This replaces the separate "course wrap-up" item entirely — the
reflection lives inside §05 itself, timed right before presentations.

### Product Design §02 citation refresh

**Implemented 2026-08-19.** See the PR #8 item above — confirmed, no open
questions. Worked Adiel's 3 sources into
`docs/day-3/02-product-design.html` +
`slides/02-product-design-slides.html`, slides 2 and 4.

---

## Change log

- 2026-08-25 — **Day 3 morning restructured: Product Design cut, its
  disclosure section relocated into Safe & Auditable Design, Recap grows,
  and a new additional "Build Time" block added before lunch.** Product
  Design (formerly `02`, 10:30-11:15 AM) is removed from the schedule —
  archived (not deleted) to `project/removed-sessions/day-3/` (Overview,
  Slides, copy-draft), the same gitignored pattern used for the Day 2
  restructure above. Its "Design for Transparency" section (reader-facing
  AI-disclosure UI patterns: highlight-for-glancing, info button,
  outlet-level disclosure, proportional AI-ratio visualization, trust
  stamp, "no AI used" label) was the only part still needed, so it moved
  verbatim into Safe & Auditable Design as a new closing section (`04`
  block-eyebrow → `05`), with one new bridge sentence added since Safe &
  Auditable's existing s1-s4 are all inward-facing (audit trails,
  incidents, policy enforcement) and s5 pivots to reader-facing UI.
  Citation numbering needed no manual fix — confirmed `docs/js/citations.js`
  numbers `.cite` elements sequentially by DOM order at load time, not by
  a hardcoded index.

  This closes a long-standing gap first flagged 2026-08-13 (see the
  "VS Code/Claude Code/Git content has no scheduled home on any of the 3
  days" entries below): Recap grew (30→40 min) to add two new sections —
  a short "Platforms You'll See" awareness list (Vercel, Chainlit, Supabase,
  Turso, framed explicitly as awareness not tutorial) and "Getting to Know
  VS Code," which deep-links to `docs/setup.html#vscode` (a new anchor id
  added to that page's existing section 4) rather than duplicating its
  install steps. This gives VS Code its first real in-class touchpoint, on
  Day 3, not Day 2 as `STUDENT_CLAUDE_GUIDE.md` previously (inaccurately)
  claimed — see below.

  Time for Recap's growth, Build Time's new session, and everything else
  came from: the 45 min freed by cutting Product Design, plus 5 min
  trimmed from Safe & Auditable Design (45→40) and 10 min from Human-AI
  Design (45→35, content untouched, per explicit user direction to keep it
  as-is) — both denser per minute now, flagged during planning but not
  reversed, per the user's explicit numbers. Full math: Recap 40 + Break
  15 + Safe & Auditable 40 + Human-AI 35 + Build Time 50 = 180 min,
  10:00 AM–1:00 PM, matching the old AM block's total exactly. Both the
  1:00 PM lunch anchor and 5:00 PM day-end are unchanged, matching Day 1/2.

  Build Time (new `04`) is an *additional* hands-on block, not a
  replacement for the existing 2:00 PM Final Coding Time (renumbered
  `06`→`05`) — the explicit goal was more total build time, not the same
  amount moved earlier. Its content asks students to implement one
  concrete decision from Safe & Auditable Design or Human-AI Design (a
  kill switch, a human checkpoint, a disclosure pattern), framed to
  connect forward to Final Coding Time rather than duplicate it. Final
  Coding Time's own "flag from Product Design" prompt (in both its
  Overview and Slides deck) was rewritten to reference Safe & Auditable
  Design, Human-AI Design, and Build Time instead, since Product Design no
  longer exists to flag from.

  Renumbering also fixed a pre-existing mismatch: `06-final-coding-time`
  ran at 2:00 PM, clock-*before* `05-where-you-can-take-this` at 3:15 PM;
  swapping their numbers (`06`→`05`, `05`→`06`) resolves it while already
  touching both files. Updated in the same pass: `docs/data/schedule.json`
  (entries removed/renumbered/retimed, `note` field appended),
  `docs/partials/nav.html` (Day 3 flyout, was already in file-number not
  clock order — also fixed), `docs/resources.html` (two "from Product
  Design" entries deleted outright, confirmed neither citation appears in
  the surviving Design for Transparency section), `docs/day-3/index.html`
  (intro paragraph and learning outcome #1, which had no home once
  Product Design was cut), and every stale hardcoded "Next section →" link
  across the Day 3 Slides decks (`01-recap`→`02-safe-auditable-design`,
  `02-safe-auditable-design`→`03-ai-human-design`,
  `03-ai-human-design`→`04-build-time`, `04-build-time`→`05-final-coding-time`,
  `05-final-coding-time`→`06-where-you-can-take-this`, unchanged
  `06-where-you-can-take-this`→`07-final-show-and-tell`).

  Follow-up same day: Recap's two new sections were reordered (VS Code
  before Platforms, since VS Code is the more actionable one) and its
  Platforms bullet for Vercel was rewritten to point forward at Build
  Time rather than just naming it. Build Time itself picked up a genuine
  new first section, "Get Set Up: Deploy to Vercel" — real signup/import/
  deploy steps (sign up free at vercel.com with GitHub, import the
  project's repo, set a Root Directory if the code lives in a subfolder
  like a class-repo submission folder, deploy, save the live URL) — since
  the user wants each student's own live URL, not just a shared path on
  this course site, in anticipation of a later task to surface that URL
  on the auto-generated submission cards (`docs/students/index.html`, see
  [ADR 0023](adr/0023-auto-generated-submission-cards.md)). Build Time's
  other two sections renumbered `s1`→`s2`, `s2`→`s3` to make room; both
  its Overview and Slides deck updated in lockstep, copy-draft too.
  Re-verified after: no new slide-parity issues, valid JSON, all pages
  still 200.

  Separately, while reviewing this restructure the user confirmed GitHub
  Desktop is never actually used anywhere in the taught workshop (Day 1's
  Fork & Submit runs through Claude Desktop's own GitHub connector; Claude
  Code runs git commands directly from Day 2 on) and asked for it dropped.
  `docs/setup.html` section "5. GitHub Desktop" (4 of its 18 checklist
  items) was archived, not deleted, to
  `project/removed-sessions/setup-page/05-github-desktop.html`; the live
  page's progress counter updated 18→14, and its "Days 2 and 3" group
  heading/intro reworded to "Day 3" now that VS Code (section 4, which
  gained a new `id="vscode"` anchor) is the only item left under it and is
  genuinely a Day-3, not Day-2, touchpoint. `STUDENT_CLAUDE_GUIDE.md`'s
  "Where this file kicks in" section and its git-workflow bullet were
  corrected to match: VS Code starts Day 3 (not Day 2), and git happens
  through Claude Code directly (GitHub Desktop dropped as an offered
  option).

  Verified: `schedule.json` parses as valid JSON, a full session walk of
  Day 3 shows no gaps or overlaps end to end (10:00 AM–5:00 PM),
  `project/scripts/check-slide-parity.js` shows no new mismatches (the one
  pre-existing mismatch on `03-ai-human-design.html` predates this change,
  its content was never touched, only its filename/number), a local
  server spot-check confirmed every renamed/new Day 3 page and its Slides
  deck returns 200 and `02-product-design.html` now 404s, and a grep of
  `docs/` confirmed zero remaining references to any of the old
  file/session names or to "GitHub Desktop."

- 2026-08-25 — **Day 2 afternoon restructured: Your Goal & Plan Mode and
  Show & Tell + Critique both cut, Spec-Driven Development moved up,
  Revisit & Build extended to end of day.** Your Goal & Plan Mode
  (formerly `05`, 12:20-1:00 PM) and Show & Tell + Critique (formerly
  `08`, 3:30-5:00 PM) were pulled from the schedule at the user's
  direction and moved — not deleted — to `project/removed-sessions/`
  (Overview HTML, Slides, and copy-draft for each), a new directory added
  to `.gitignore` so it stays local and out of the deployed site but is
  recoverable if either session comes back. Spec-Driven Development moved
  into the vacated 12:20 PM slot and grew from 30 to 40 min to fill it
  exactly through to lunch (unchanged at 1:00 PM); renumbered `06`→`05`
  (file, slides, copy-draft, `data-session-id`, internal slides link, and
  its Slides deck's cover-meta time/duration). Revisit & Build absorbed
  all the freed afternoon time — its own original slot plus the old
  Spec-Driven Development slot plus the old Show & Tell slot — into one
  2:00-5:00 PM, 180-min block; renumbered `07`→`06` the same way. Day 2
  still ends at 5:00 PM, matching Day 1/3's shape. Plan mode content isn't
  actually gone from Day 2: Revisit & Build's existing §1 ("State Your
  Goal, Then Plan") already walks students through switching to Plan mode
  as part of the build exercise, so that instruction survives without a
  dedicated session — confirmed by reading `07-revisit-build.html` (now
  `06-`) before cutting `05-goal-plan-mode.html` rather than assuming.
  Updated every place that referenced the old session count/numbering:
  `docs/data/schedule.json` (entries removed/renumbered/retimed, `note`
  field appended), `docs/partials/nav.html` (Day 2 flyout menu, two items
  removed), `docs/resources.html` (two Plan Mode resource attributions
  changed from "from Your Goal & Plan Mode" to "from Revisit & Build"),
  and three stale hardcoded "Next section" links in the Slides decks
  (`04-skills-best-practices-slides.html` → `05-spec-driven-dev.html`,
  `05-spec-driven-dev-slides.html` → `06-revisit-build.html`,
  `06-revisit-build-slides.html`'s end-of-day link changed from the now-
  removed Show & Tell to `/day-3/`, since Day 2 no longer has a session
  after it). Did not touch Day 2's learning-outcomes copy on
  `docs/day-2/index.html` — the "Use plan mode..." outcome is still
  accurate per the point above, so left as-is pending user review.
- 2026-08-23 — **`docs/data/schedule.json`: Day 1 morning rebalanced
  (State of AI 15→20 min, Industry Conversation 30→40 min, Product
  Discussion 90→75 min), after several same-day dead ends that are worth
  recording so they aren't retried.** The starting ask was simple: take 30
  min from Product Discussion (90→60) and add two 15-min breaks in the
  afternoon. That led to three reworks in sequence, each backed out once
  its consequences became clear: (1) a `day-1/office-hours` slot (optional
  one-on-one instructor time, no linked page) inserted between Product
  Discussion and Lunch, which required a real code change to
  `docs/js/timeline.js` (it skipped rendering `summary` for anything
  without a `url`) — abandoned once the user found the resulting lunch
  shift didn't work for them, and `timeline.js` was reverted to its exact
  original committed state (confirmed via `git diff`, empty); (2) giving
  those 15 min to Problem Statement instead, and later Industry
  Conversation instead, while pinning Lunch to a fixed 1:00 PM — this
  kept producing either a dead gap before lunch, a day that ran past 5:00
  PM, or both, because a fixed-clock Lunch anchor combined with unequal
  pre/post-lunch adjustments can't reconcile without the numbers working
  out exactly; (3) the fix that actually worked: give the second
  afternoon break's 15 min back to Product Discussion instead of keeping
  it as a break, landing Product Discussion at 75 min (not 60), which
  makes it end at exactly 1:00 PM with no gap. Final shape, verified with
  a script that walks the full session list start-to-end: State of AI
  10:00-10:20 AM, Industry Conversation 10:20-11:00 AM, Use Cases
  11:00-11:30 AM, Break 11:30-11:45 AM, Product Discussion 11:45 AM-1:00
  PM, Lunch 1:00-2:00 PM (unmoved from its original 2026-08-11 confirmed
  time), then Problem Statement, AI Tools, Explore Claude Desktop, Fork &
  Submit, and Project Assignments all at their original 2026-08-11
  confirmed times, ending 5:00 PM. No office-hours slot and no second
  break survived; Day 1 has exactly one break, same as before this whole
  pass started. Verified: `schedule.json` parses as valid JSON, no gaps
  or overlaps anywhere in the session list, `git diff docs/js/timeline.js`
  is empty, and a grep of `docs/day-1/*.html` / `project/copy-drafts/
  day-1/*.md` for hardcoded times found none, every page reads its time
  from `schedule.json`.
- 2026-08-23 — **`docs/data/schedule.json`: Day 1 afternoon break added.**
  The morning rebalance above left the afternoon with no break at all
  (the two that had been tried there earlier in the day both got backed
  out). Fix: Explore Claude Desktop shrank from 55 to 45 min, funding a
  new 10-min `day-1/break-2` at 2:55-3:05 PM, immediately before it.
  Because Fork & Submit already started exactly when Explore Claude
  Desktop used to end (3:50 PM), pulling the 10 min directly out of
  Explore Claude Desktop needed no other reshuffling, Fork & Submit and
  Project Assignments are unchanged. Day 1 now has two breaks total
  (`day-1/break-1` at 11:30-11:45 AM, `day-1/break-2` at 2:55-3:05 PM).
  Verified: `schedule.json` parses as valid JSON, and a script walking
  the full Day 1 session list start-to-end confirmed no gaps or overlaps
  and an exact 5:00 PM end time.
- 2026-08-23 — **`docs/day-1/02-industry-conversation.html` fully
  regenerated from `project/copy-drafts/day-1/02-industry-conversation.md`
  after the user's own line-by-line hand-edit pass on the draft.** The
  hand-edit pass reordered sections (physical order became 1, 3, 5, 2)
  without renumbering the headings, renamed two sections ("Where News
  Workers Stand" → "Where News Workers & Students Stand", "What's Actually
  at Stake" → "What's at Stake", "The Scaling Debate" → "The Scaling Debate
  in Tech"), and deleted §4 "Where Newsrooms Actually Stand" entirely
  (the Reuters Institute UK survey, UMD/Pangram 186,507-article scan, CNTI
  policy synthesis, and Global South stat). Asked 2 questions before
  touching anything: confirmed the final section order/numbering should
  match physical placement (renumbered markdown headings to 1 Talking
  About, 2 News Workers & Students, 3 What's at Stake, 4 Scaling Debate),
  and confirmed the §4 deletion was intentional, not accidental. Also
  fixed one typo while porting ("convinving" → "convincing" in the "For
  the public" stakes line), consistent with past practice of silently
  fixing clear spelling errors during HTML implementation (see the
  "Agenctic" → "Agentic" fix in `01-state-of-ai.html`'s history entry).
  Converted all inline `[n]` citations to the site's `<sup class="cite"
  data-url="..." data-note="...">` pattern, matching `01-state-of-ai.html`'s
  established format; double quotes inside quoted material were converted
  to single quotes inside `data-note` attributes to keep valid HTML (the
  attribute itself is double-quoted). Verified: parsed the output HTML
  with Python's `html.parser` (no errors, 33 citation `<sup>` tags found,
  matching the 23+6+1+3 count across the four sections), grepped for
  leftover `[n]`-style brackets (none) and stray em-dashes outside the
  `<title>` tag (none), and confirmed every TOC anchor (`#s1`-`#s4`)
  matches a section `id`.
  **Not done**: `slides/02-industry-conversation-slides.html` was not
  updated to reflect the new section order/count, out of scope for this
  pass.
- 2026-08-23 — **`project/copy-drafts/day-1/02-industry-conversation.md`:
  new §3 "Where News Workers Stand" added, §4 converted to bullets, final
  section renumbered, per two more inline `{Claude note: ...}` flags the
  user left in the draft.** By the time this pass started, the user had
  already deleted the old §3 ("Where Journalism Splits") and §5
  ("Questions Without Settled Answers") sections by hand, leaving a
  numbering gap (1, 2, [gap], 4, [gap], 6). Asked 3 scoping questions
  before writing (per standing "ask directly when ambiguous" practice):
  confirmed the new section should be seeded by the orphaned
  "newsrooms cut more than 2,300 jobs" paragraph then sitting at the end
  of §2, confirmed it should include fresh research and not just
  synthesize existing page content, and confirmed the final section
  ("What's Actually at Stake") should renumber down to close the gap.
  Ran the `ground-content` skill: 2 parallel background research agents,
  one on newsworker displacement/freelancer-specific accounts, one on
  newsworker sentiment and skill-anxiety data, both with an explicit
  dedup list covering everything already cited on this page and sibling
  Day 1 pages. New §3 bullets, each with live, dated, named sources: job
  losses tangled with pre-AI trends (the moved MediaCopilot paragraph,
  citation carried over from §2), freelance commissions being quietly
  reassigned to AI (named freelancers Chris Sutcliffe, Sarah Scoles, Arif
  Ullah Sheikh via Reuters Institute), false AI-detector flags costing
  real freelancers their income (Kimberly Gasuras and a pseudonymous
  "Mark" via Gizmodo, a third via Authory), fabricated AI "freelancers"
  crowding out real ones (the Margaux Blanchard hoax and City AM editor
  Steve Dinneen's reaction, plus Ben Touati's byline hijacked by AI
  content after ClickOut Media fired him for declining to use it, both
  via Press Gazette), burnout and AI concern compounding in the same
  journalist population (a 436-journalist European survey via
  WAN-IFRA/Taktak), and a seniority/geography split in how personally
  threatened journalists feel (Poynter's named journalism students, CNTI's
  Global North/South sentiment split). The research agent flagged several
  leads it could not verify live and excluded rather than guessed:
  NewsGuild-CWA's Nov 2023 AI member survey (PDF wouldn't parse), a Nieman
  Lab piece that 403'd, a CJR piece that predates generative AI, and an
  EFJ/TWIIID report where only one stat (64.5% want AI training)
  corroborated across two fetches. §4 ("Where Newsrooms Actually Stand")
  converted from three flowing paragraphs into 6 bullets, same facts and
  citations, no new research needed, purely a compaction/readability
  pass. Final section ("What's Actually at Stake") renumbered from 6 to
  5. Verified: `grep "—"` clean (only inside citation lines), no
  first-person-plural outside a direct quote, dedup grep clean against
  sibling files for all newly-named individuals, and a live spot-check of
  8 new citation URLs (6×200, 2×403 on Poynter and CNTI, both normal
  bot-blocking).
  **Not done**: `docs/day-1/02-industry-conversation.html` still not
  regenerated from any of this week's markdown changes, markdown-only per
  this task's scope.
- 2026-08-23 — **`project/copy-drafts/day-1/02-industry-conversation.md` §1
  ("What Everyone's Talking About") rewritten from a generic tech-industry
  tension list into a journalism-specific one, per the user's inline
  `{Claude note: ...}` left in the draft.** Ran the `ground-content` skill:
  4 parallel background research agents plus 2 follow-up verification
  agents (the user asked to specifically re-vet the "Accuracy vs. Speed"
  and "Adoption vs. Readiness" bullets, both confirmed accurate, with one
  correction: the arXiv 2510.18774 paper's affiliation was wrong on the
  site, "University of Maryland/Pangram Labs" should be "University of
  Maryland, Simon Fraser University, and Pangram Labs" since co-author
  Karpinska is at Simon Fraser, not UMD, fixed in both §1 and §4 of this
  file). The old list (Progress vs. Caution/Grok 4, Accessibility vs.
  Concentration, Efficiency vs. Humanity/Klarna) was deleted outright, not
  archived, after a mid-session direction change: the user first asked for
  a collapsible "for the curious" module to preserve it, then reversed
  that and said to just remove it. New bullets, each grounded with live,
  dated, named sources not already used elsewhere on the site: License vs.
  Litigate (News Corp/Dotdash Meredith licensing deals vs. Alden
  Global/Ziff Davis lawsuits), Traffic vs. Answers (Pew's AI Overview
  click-through study, Condé Nast/Dotdash Meredith executives on "Google
  Zero," Perplexity/Cloudflare monetization workarounds), Labor
  Protections vs. Management Control (the G/O Media/WGAE 2023 dispute, The
  New Republic and Ziff Davis union AI clauses, the POLITICO arbitration
  ruling, NewsGuild-CWA's ~90-contract count), and Custom Tools vs.
  Off-the-Shelf (BloombergGPT, Reuters' internal AI platform and Fact
  Genie, the TUM "Automation Divide" framing). Deliberately excluded from
  all of the above: the NYT v. OpenAI suit, the Sports Illustrated/CNET/
  Gannett/Chicago Sun-Times/Tagesspiegel/BBC Eye incidents, and the Cody
  Enterprise/Ars Technica fabricated-quotes cases, since each is already
  used elsewhere on this page or on sibling Day 1 pages (checked via grep
  across `project/copy-drafts/day-1/*.md`, confirmed clean). Section 2
  ("The Scaling Debate") is untouched, mid-edit by the user for a
  different, separate future task (a planned new section on AI's effect
  on journalism specifically); left alone per instruction not to clobber
  concurrent edits. Verified: `grep "—"` clean (only inside `N. URL —
  description` citation lines), no first-person-plural outside a direct
  quote, dedup grep clean against sibling files, and a live spot-check of
  8 new citation URLs (7×200, 1×403 on newsguild.org, which is normal
  bot-blocking since the research agent live-fetched that page directly).
  **Follow-up same day**: the user asked whether "Accuracy vs. Speed" and
  "Adoption vs. Readiness" (the two carried-over bullets) were still the
  most representative choices, or thinner than the other four. Judged
  both still central to the actual conversation and worth keeping, so
  built each out to matching depth (one citation each before, four after)
  via 2 more background research agents: Accuracy vs. Speed gained AP's
  own "unvetted source material" standard (Amanda Barrett quote), the
  NewsBreak/Bridgeton, NJ fabricated-shooting-story incident (Dec 2023),
  and a Reuters Institute 2025 stat on how rarely people believe AI
  output gets checked before publishing; Adoption vs. Readiness gained
  the LA Times "Insights" tool's one-day KKK-sympathetic-content pullback
  (March 2025), a Trint survey on unsanctioned AI use (42.3%), and the
  Suncoast Searchlight editor secretly running reporter drafts through
  ChatGPT (Nov 2025). Same verification pass re-run clean on the
  additions (5 new URLs spot-checked, 2×403 on Poynter/Nieman Lab, both
  normal bot-blocking).
  **Not done**: this page's own live `docs/day-1/02-industry-conversation.html`
  was NOT regenerated from this draft, markdown-only per this task's scope.
- 2026-08-23 (later) — **`02-industry-conversation.md`/`.html` §1/§2 evidence
  format iterated down to plain single-source bullets; §3 stakes wording
  synced; a from-scratch verification pass then caught stale section titles
  on two other Day 1 pages and their Slides decks, plus a standing gap
  between Slides decks and their Overview pages.** Continuing the same
  day's line-by-line pass on `02`: §1 ("What Everyone's Talking About")
  and §2 ("Where News Workers & Students Stand") went through several
  format iterations in one sitting — collapsible-wrapped multi-sentence
  bullets → single-sentence bullets with combined citations → a two-column
  `.resource-table` (Observation/Evidence) → the Evidence column
  reformatted as bullets → landed on a plain `<ul class="field-notes">`
  with exactly one, preferentially report-over-news-story, citation per
  bullet, matching the density the rest of the page already uses. Caught
  and fixed a misattribution along the way: §2's last bullet credited a
  Global North/South sentiment stat to Poynter, that finding is actually
  CNTI's; the Poynter-only quotes were dropped and the bullet re-cited to
  CNTI alone. §3 ("What's at Stake") had three bullets (journalists, news
  organizations, for you) that the user had already hand-trimmed in the
  markdown but that hadn't been ported to the live HTML yet — synced.
  - **Full Day 1 reconciliation re-verification, all 9 Overview pages +
    `people-to-follow`**: re-ran the ad-hoc MD/HTML diff script used
    throughout this session's earlier reconciliation work and found it had
    a real bug — `**Sources**.*` with `re.S` matched past the *first*
    `**Sources**` heading to the end of the file, so any page with more
    than one Sources block (i.e., citations attached to more than one
    section) silently dropped everything after the first block from the
    comparison. Fixed the script, re-ran it against all 9 pages, and
    manually read full file pairs where the fix surfaced new diffs. Found
    stale section titles the earlier reconciliation pass had missed
    because of this bug: `03-use-cases.html` had 3 (`Not a Good Use Case
    (Yet)` → `Not a Refined Use Case (Yet)`, `The Pattern` → `The Emergent
    Patterns`, `The Practical Question` → `The Practical Questions`) plus
    two bullets carrying wording the markdown no longer had; `05-problem-
    statement-discussion.html` had 1 (`Get Specific` → `Get Curious with
    Hypothesis Testing`). All fixed in both files' Overview HTML. Also
    found two small punctuation typos in `09-project-assignments.md`
    itself (a dropped period, a dropped comma) where the live HTML already
    had the grammatically correct version — fixed the markdown to match
    rather than degrade the HTML, since these read as accidental drops,
    not deliberate edits.
  - **Slides decks found to be a standing, silent drift risk, not just a
    one-off staleness**: Slides pages are separate, hand-authored HTML,
    not generated from the Overview page or its markdown draft, so when an
    Overview page's sections get renamed/reordered/cut (as `03` and `05`
    just were, and as `02` has been over this whole session), nothing
    updates the matching Slides deck automatically. Per direct user
    instruction ("they should be the same," headings and order both),
    brought every Day 1 Slides deck in line with its Overview page's
    current section titles and order: `03-use-cases-slides.html` and
    `05-problem-statement-discussion-slides.html` got the same title fixes
    as their Overview pages (03's deck also had a whole stale intro slide,
    "What Does AI Actually Do?", already dropped from the Overview page
    earlier this session — removed, remaining slides renumbered, cover
    contents and slide counter updated). `01-state-of-ai-slides.html` had
    the same 5 topics as its Overview page but in the wrong order and
    partly mistitled — reordered (Moment → Timeline → State of the Art →
    Builders → Journalists) and retitled to match exactly, slide body
    content untouched. `02-industry-conversation-slides.html` needed a
    real rebuild, not just a reorder: its old deck had 6 sections, 3 with
    no Overview-page equivalent at all (a generic optimist/skeptic scaling
    framing, a newsroom-adoption-by-size breakdown, a named-tools section),
    running content from before this session's citation rework. Rebuilt to
    the Overview page's current 4 sections in order, each slide's body
    ported from the current Overview text with its citations intact.
    `07-explore-claude-desktop-slides.html` had 2 titles truncated
    (`Getting Oriented` / `The Code Environment`, missing their
    Overview-page subtitles) — restored in full. Verified via a script
    diffing each Slides deck's `block-title`s against its Overview page's,
    in order — every Day 1 page now matches (`09-project-assignments` has
    no Slides deck by design, confirmed via its Overview page's missing
    `slides-cta` block).
  - **`docs/instructors.html`**: the Andrew Calderón card's `<h3>` read
    "Andrew Calderón," shorter than the full name ("Andrew Rodríguez
    Calderón") already used in the card's own bio paragraph — updated the
    heading to match, per direct user request.
  - **Not done**: `04`-`09` and `people-to-follow`'s own line-by-line pass
    is still the user's own queued work, unaffected by this entry — see
    the 2026-08-22 entry below for that standing status.
- 2026-08-22 — **`docs/day-1/01-state-of-ai.html` and
  `02-industry-conversation.html` fully regenerated from the 2026-08-21
  research-first `project/copy-drafts/day-1/*.md` rewrite; `03-use-cases.html`
  §3/§4/§5/§6 updated for the same session's citation swaps and new
  incidents.** The user wants to do their line-by-line edit pass by
  looking at the live site rather than the raw markdown, so implementation
  came before the edit pass this time (reversing the usual
  draft-then-edit-then-implement order). `01` and `02`'s section order
  and structure changed substantially from what was live, not just the
  prose: `01`'s old §4/§5 (For Journalists / The Landscape) swapped
  content, with the `.stakes` block moving into §1; `02` dropped its old
  compare-grid optimist/skeptic framing entirely and gained a new §3
  ("Where Journalism Splits," newsroom incidents that weren't on the
  site before: Sports Illustrated, CNET, Gannett, Chicago Sun-Times,
  Tagesspiegel, BBC Eye) and a data-driven §4 replacing the old
  perception-based small/mid/large newsroom breakdown. `03-use-cases.html`
  §3 got its three swapped 2023+ citations (AAE moderation, healthcare
  transcription, Copilot vulnerability rate), §4 gained the Cody
  Enterprise/Ars Technica fabricated-quotes bullet (with em-dashes in
  that list's existing bullets converted to periods to match), §5 gained
  its benchmarked-pattern lede paragraph, and §6 got the
  "Questions to Ask Before Reaching for AI" `<h3>` the draft had already
  resolved. Verified by diffing tag counts (`<section>`, `<div>`, `<sup>`,
  `<ul>`, `<dl>`, `<ol>`) and checking for unescaped quotes inside
  `data-note` attributes, plus a local `http.server` smoke test (all
  three pages 200). **Not done**: no visual/browser check beyond that,
  since a browser automation tool wasn't invoked this session; the user
  should eyeball the rendered pages before treating this as final. The
  other 6 Day 1 pages are untouched and still queued for the user's own
  line-by-line pass per the 2026-08-21 entry below.
- 2026-08-22 — **`instructors.html` implemented for real (was a
  placeholder stub) and the home page updated to link to it.** Ported
  both bios from `project/copy-drafts/instructors.md` (finalized by the
  user since the 2026-08-21 draft: Andrew's title conflict resolved to
  "Network Weaver, Journalism + Design Lab · Adjunct Professor, CUNY
  Craig Newmark Graduate School of Journalism," a link to his personal
  site added). Each `.idea-card` got an `id` (`andrew-calderon`,
  `adiel-kaplan`) so other pages can link directly to a person's bio.
  Adiel's headshot (downloaded 2026-08-21) is now wired in via a new
  `.idea-card img` rule in `briefing.css` (96px circular thumbnail);
  Andrew's card has no photo yet, left as an HTML comment noting where
  one goes rather than a broken image reference. On `index.html`: the
  masthead's "3 Days · Hands-on · No ML background needed" meta line
  replaced with "Instructors: Andrew Calderón, Adiel Kaplan" (each name
  linking to their `instructors.html` anchor), and the "01"/"02"
  `.home-section-eyebrow` numbering removed from the "Workshop Days" and
  "Getting Started" section headers per user direction ("those headers
  don't need to be enumerated"); the now-unused `.home-section-eyebrow`
  CSS rule was deleted rather than left dead.
- 2026-08-21 — **Day 1's `01-state-of-ai.md` and `02-industry-conversation.md`
  rewritten from scratch, research-first**, on `review/full-site-audit-6`.
  These two were the first Day 1 pages ported to `project/copy-drafts/`
  (2026-08-04), before the site adopted its "plan → research via parallel
  background agents → write" discipline established for Day 2/3 (see the
  2026-08-13/08-19 entries below). Rereading them, the same shallowness
  Day 2 got flagged for showed up here too, plus real overlap the other
  days didn't have: both pages independently listed newsroom AI tools
  (NYT, WaPo, Sahan Journal, Outlier Media in `01` §5; WaPo, Reuters, NYT
  in `02` §5), answering the same question twice with different examples.
  User also asked explicitly that this pass not repeat content Day 3
  already owns (Day 3's Product Design/Safe & Auditable Design own named
  newsroom AI products like Chowbot/Ask FT/Adelaide/Rai and policy
  specifics like WBEZ/LAist/CBC), so Day 3's actual page content was read
  first to build a dedup list before writing anything.
  - **Confirmed with user first**: switch both pages to the declarative
    narrator voice used on Day 2/3 (drops `01`'s "The Moment We're In"
    heading and `02`'s scattered first-person-plural); scope this pass to
    the copy-drafts only, `docs/day-1/*.html` stays untouched until these
    drafts are reviewed.
  - **Division of labor** (fixes the page-to-page overlap): `01` now owns
    the technology-level story (what changed, pace/scale, history,
    capability limits for an individual journalist); `02` owns the
    industry debates and newsroom adoption/policy data, including the
    newsroom-tool material consolidated out of `01`.
  - **Research**: 5 parallel background agents (general-purpose, live-fetch
    only), each briefed to find multiple sources and concrete named
    examples/numbers rather than cite from memory: AI adoption pace
    (explicitly briefed to inflect toward news-industry data, not just
    general-population stats, per user direction mid-pass), AI history
    timeline verification, the scaling/AGI debate (real named voices:
    Sutskever, Amodei, LeCun, Marcus), newsroom AI adoption survey data,
    and named newsroom AI incidents. A 6th agent found 2023+ replacements
    for 4 stale (2017-2021) capability citations, after the user set a
    standing rule mid-pass: any citation describing *current* AI
    behavior/accuracy needs to be 2023 or later since older tools aren't
    representative, but the deliberate historical timeline in `01` §3 is
    exempt since dropping pre-2023 milestones (AlexNet, AlphaGo, GPT-3)
    would gut its purpose.
  - **Genuinely new findings worth flagging**: AP was automating earnings
    stories via Wordsmith back in 2014, a pre-ChatGPT newsroom-AI anchor
    now opening `01`'s history timeline. Newsroom AI adoption doesn't
    follow the assumed small/mid/large maturity ladder the old `02` §4
    asserted uncited — a measured (not self-reported) study found smaller
    papers (under 100K circulation) show *more* detectable AI use (9.3%)
    than larger ones (1.7%), and ownership predicts AI governance far
    better than size does. Journalists are adopting AI faster than the
    public (82%, Muck Rack) while trusting it less than almost anyone
    (62% of UK journalists call it a threat), a tension used directly in
    `02`'s disagreement list. Five dated, named newsroom AI-failure
    incidents (Sports Illustrated, CNET, Gannett, Chicago Sun-Times,
    Tagesspiegel) replaced `02`'s old unattributed skeptic/optimist
    bullets, paired against one clear counterexample (BBC Eye's
    multi-agent Ukraine investigation).
  - **`03-use-cases.md` also touched**, per user request mid-pass:
    §4 ("Not a Good Use Case Yet") and §5 ("The Pattern") were generic
    assertions with no citations, unlike §2-3's already-strong named
    examples. Grounded both with incidents not used elsewhere (Cody
    Enterprise and Ars Technica fabricated-quote firings for §4; AP,
    ICIJ's passport-detection tool, and METR's task-length benchmark for
    §5). Also swapped 3 stale citations in §3 (2019 AAE-moderation-bias
    study, 2020 speech-recognition-disparity study, 2021 Copilot-
    vulnerability study) for 2023+ equivalents under the new currency
    rule, and added a sub-heading to §6's previously-bare question list.
  - **Verification**: grepped all three files for em-dashes in prose
    (clean, except inside the site-wide "URL — description" citation-list
    convention, which is a structural format used on every page, not
    prose dash-itis) and for first-person-plural in headings (clean).
    Cross-checked every new named incident/stat against Day 3's actual
    page content and the rest of the site for collisions (none found).
    Spot-checked citation URLs live; the only failures were bot-blocking
    on Bloomberg/Oxford Academic/GlobeNewswire, not dead links, each
    already independently corroborated by the research agents that fetched
    them. Updated `project/copy-drafts/day-1/README.md`'s cross-page notes
    to mark voice/citation-density/bare-list/grounding as resolved for
    `01`-`03` specifically (still open for `04`-`08`).
  - **Not done**: `docs/day-1/*.html` implementation. These are drafts
    pending the user's review.
- 2026-08-21 (later) — **Follow-up: 3 sections the research pass missed,
  grounded.** User caught this by diffing: both files were "M" (modified,
  uncommitted) in git when this session started, meaning the user had
  hand-edited them before the rewrite; comparing the last commit against
  what got read confirmed most of those edits carried through (the
  relocated `.stakes` block, "You Should Be Wary," the trimmed history
  entries), but 3 sections stayed assertion-only because none of the 5
  research agents had been briefed on them: `01` §4 ("What This Means for
  Journalists," the You Can/You Should Be Wary lists), `01` §5 ("Who's
  Building It"), and `02` §1 (the 4-item disagreement list). 3 more
  background agents researched each. First attempt failed outright (all
  3 agents hit the account's monthly spend limit mid-run); user confirmed
  the limit had reset and they were retried successfully. Real findings:
  ChatGPT's app-market share fell below 50% for the first time in May
  2026 (46.4%, Sensor Tower/TechCrunch) while Anthropic passed OpenAI on
  U.S. business spend share the same year; open-weight models closed the
  gap to the leading proprietary model from ~13 points to ~6 in a year
  (Artificial Analysis); an AI fact-checker correctly caught false
  headlines 90% of the time but true ones only 15% (DeVerna et al., PNAS/
  arXiv 2024); people co-writing with an opinionated AI were twice as
  likely to adopt its stance, mostly without noticing (Jakesch et al.,
  CHI 2023); and AI-labeled news articles were 8.2x more likely to
  contain a hallucination than human-written ones, 41% vs. 5% (the same
  University of Maryland/Pangram study already cited elsewhere on `02`
  for a different finding, an accepted same-page reuse, not a new
  citation). One deliberate exclusion: the CJR/Tow Center 8-AI-search-
  tools study was found by the `01` §5 research agent but NOT used, since
  it's already Day 3 Product Design's centerpiece citation. Re-verified
  em-dash-in-prose and cross-page collision (against Day 3 and the rest
  of the site) on all new content; clean.
- 2026-08-21 — **Instructors page bios drafted**, `project/copy-drafts/
  instructors.md`. Adiel's bio pulled near-verbatim from
  journalismfutures.org/about (already well-written, concise); her
  headshot downloaded to `docs/assets/images/adiel-kaplan-headshot.jpg`
  (converted from WebP to JPEG) but not yet wired into `instructors.html`,
  which has no image slot in its `.idea-card` markup yet. Andrew's bio
  synthesized from his CUNY faculty page (more conventional bio voice)
  plus Pulitzer/Marshall Project/byline credits from his personal site;
  LinkedIn's About section is truncated behind login so it only
  contributed the headline. Flagged for the user to resolve: his own site
  and CUNY's page disagree on his Journalism + Design Lab title ("Network
  Weaver" vs. "Product Design + Tech Lead"). Both bios need the user's own
  edit pass per the established copy-drafts workflow.

- 2026-08-16 — **Day 2 round-3 audit, implemented**, on
  `review/full-site-audit-3`. Full arc: user reviewed all 8 Day 2 sessions
  page by page (Batches 1–6 logged in "Full-scale site review, round 3"
  above), asked for a grouped implementation plan before building
  anything (see `~/.claude/plans/ok-let-s-take-stock-shimmying-rose.md`),
  then approved it with three corrections: use this repo's own CLAUDE.md
  as the "real example" rather than hunting external cross-department
  examples, leave Plan Mode's position in the day unchanged (the
  resequence-before-CLAUDE.md idea from Batch 5 was reverted), and verify
  before writing whether VS Code's plan-review flow has an inline-comment
  feature (and whether Claude Desktop has an equivalent) rather than
  assuming.
  - **All 8 sessions touched** (Overview + Slides, except 08-show-tell
    which wasn't in scope): `01-debrief` (lede/exercise reframe),
    `02-prompting` (dek, history items, exercise), `03-claude-md` (new
    file-viewer component, cut technical examples, cross-department
    reframe), `04-skills-best-practices` (new "Build One" step-by-step
    replacing the case-study section, if/then rewrites, citation fixes),
    `05-goal-plan-mode` (jargon pass, restructure, exercise removed),
    `06-spec-driven-dev` (new "What a Spec Is" foundation, checklist
    rebuilt as steps-with-questions, new starter-prompt component),
    `07-revisit-build` (exercise rewritten to absorb the plan-mode
    practice moved out of `05`).
  - **Research**: 3 background agents (Sonnet, not a heavier model, per
    explicit user instruction to match model to task rather than default
    to the most capable one), run before writing per the established
    plan-then-research-then-write discipline: Prompting (found a real
    OpenAI comparable, its Oct 2024 Playground "Generate" feature, and
    pulled Anthropic's actual Nov 2025 best-practices specifics),
    CLAUDE.md (Anthropic's verbatim Include/Exclude table plus one
    genuine self-check question, explicitly didn't invent extras),
    Skills (real SKILL.md mechanics and a live-verified, accessible
    replacement for a paywalled Medium citation).
  - **New components, both new to the site**: a `<dialog>`-based
    click-to-open file viewer (`docs/js/file-viewer.js`, new CSS in
    `briefing.css`), first used to show this repo's actual `CLAUDE.md`
    in place, see [ADR 0019](adr/0019-file-viewer-dialog.md); and a
    styled `<pre><code>` starter-prompt block (`.code-block`), first
    used in Spec-Driven Dev's checklist. Spec-Driven Dev's checklist
    itself moved off `.process-wheel` (built for exactly 7 items per
    ADR 0016, force-fit here for 4) onto `.history` + nested
    `.field-notes.is-checklist`, the same steps-component now shared
    with the new Skills build-walkthrough.
  - **Judgment calls made during implementation, flagged rather than
    silently decided**: removed `05-goal-plan-mode`'s "State Your Goal"
    section entirely instead of leaving its framing text with no
    exercise attached; removed the Hagar/MuckRock case study from Skills
    rather than relocating it elsewhere, no obvious home found.
  - **Verification**: `check-slide-parity.js` clean except two accepted,
    reviewed mismatches (`03-claude-md` s3, `06-spec-driven-dev` s3) —
    both are real content present in Slides as condensed prose instead
    of matching `<li>` counts, not dropped items; consistent with the
    script's own stated allowance for condensed wording. Grepped all
    touched files for em-dashes (clean, except inside the verbatim
    CLAUDE.md quote in the new file-viewer, which has to stay
    byte-faithful to the real file) and for colon-joined clauses
    (several fixed in both Overview and Slides). `<sup class="cite">`
    open/close tags balanced across all touched files. All touched pages
    served 200 from a local static server; new CSS brace-balanced, new
    JS passes `node --check`; `<dialog>` open/close tags balanced.
    **Not done**: no Playwright/browser automation tool was available in
    this session, so the two new components were verified structurally
    (valid markup, live 200s) but not visually screenshot-tested, unlike
    this project's usual standard for layout-risk changes (see ADR
    0016's verification). Worth a real visual pass before this ships.
  - **Not done, still open**: `08-show-tell` wasn't reviewed in this
    audit round; Day 3 hasn't been reviewed at all yet (this was
    explicitly scoped to Day 2 only, per the user's original "start with
    Day 2, then move to Day 3" instruction).
- 2026-08-15 — **Day 2 content-depth revision**, on `review/full-site-audit-2`,
  addressing the "surface level... correct-but-generic" feedback logged in
  the 2026-08-13 Day 3 entry below. The user supplied a formal content
  standard for curriculum pages (three separate steps, plan structure then
  research then write, never collapsed; multiple live-verified sources for
  judgment topics; synthesis over data-dump; duration follows content
  richness, not time-math) and this pass applied it specifically to Day 2,
  the day it was written about.
  - **Scope**: 5 of 8 sessions revised, `02-prompting`, `03-claude-md`,
    `04-skills-best-practices`, `05-goal-plan-mode`, `06-spec-driven-dev`,
    all judgment/practice topics that were single-sourced or generic.
    `01-debrief`, `07-revisit-build`, `08-show-tell` left untouched,
    confirmed with the user first: discussion/build scaffolding with no
    factual claims to source, already at the right depth for their type.
  - **Schedule**: AM block (`02`–`05`) reallocated within its existing
    145-minute pool after sketching each session's actual content need,
    confirmed with the user before research started: `02` 40→35 min, `03`
    35→30 min, `04` unchanged at 40 min, `05` 30→40 min (was the thinnest
    session, ~15 min of real content behind its exercise). `06` stays fixed
    at 30 min, the PM block has no slack since `07`/`08` weren't in scope.
    Total day span unchanged, still 10:00 AM–1:00 PM / lunch / 2:00–5:00 PM.
  - **Research**: 5 dedicated background research passes, one per session,
    run after the schedule was locked and before any page content was
    rewritten, each fetching and verifying sources live. Replaced Day 2's
    original single-source-per-topic pattern (see the 2026-08-13 entry
    below) with genuinely convergent, independent evidence: `06`'s entire
    page had been sourced to one non-peer-reviewed arXiv paper
    (Piskala, arXiv:2602.00180) — now corroborated by GitHub's spec-kit,
    AWS Kiro, Anthropic's own Claude Code docs, a named practitioner case
    study (Joshua McDonald, ~2-3x throughput over a year), and two
    independent critiques (Wattenberger on spec staleness, Zaninotto on
    SDD-as-Waterfall for large codebases). `04` gained a real journalism
    case study (Nick Hagar replicating a MuckRock/WHRO Virginia
    police-decertification investigation with Claude Code, a documented
    80-vs-81 undercount without a data skill) plus independent builder
    accounts of Skills failing in practice, replacing a page that had been
    sourced entirely to Anthropic's own docs and one launch post. `03`
    gained a real cross-org convergence (Cloudflare, Block/goose, Next.js,
    Red Hat all using CLAUDE.md as a thin `@AGENTS.md` pointer) and a real
    51-line vs. 868-line before/after (`securego/gosec` vs.
    `RedHatInsights/insights-chrome`). `05` gained a 3-axis decision
    framework (uncertainty, blast radius, familiarity) that four
    independent practitioners converged on without citing each other or
    Anthropic, plus a documented reverse failure mode (over-planning as its
    own tax, giant unreviewable plans, plan drift). `02` gained a real
    before/after from the Claude Code team's own July 2026 system-prompt
    rewrite, plus a "verify your own work" finding convergent across
    official docs, the tool's creator, and independent practitioners.
  - **Verification**: `project/scripts/check-slide-parity.js` passes clean.
    All 37 citation URLs across the 5 rewritten pages spot-checked live;
    2 initially returned non-200s from bot-blocking (Medium, Time.com,
    generative-ai-newsroom.com) or GitHub rate-limiting, re-verified via a
    second fetch method rather than dropped, all confirmed real and saying
    what they're cited for. `<sup class="cite">` open/close tags balanced
    across all 5 files (the unclosed-tag bug class found on Day 3). No
    em-dashes, workshop name correct throughout.
- 2026-08-13 (later) — **Day 3 built from scratch**, on
  `review/full-site-audit-2`, same day as Day 2. Planned in plan mode from
  the user's 8-item draft agenda. This build has a different process than
  Day 2's: the user's explicit feedback on Day 2 was that it read as
  "surface level... correct-but-generic," not enough depth, and gave a
  standing instruction (saved to memory:
  `feedback_content-depth-over-surface-level`) to research multiple
  sources per judgment-based topic and extract genuinely actionable
  guidance, not just cite one canonical doc per topic. Two rounds of plan
  feedback also reshaped the schedule before any content was written:
  Recap cut from 60 to 30 minutes, the freed time moved to the three
  design lecture topics (35 → 45 min each); "Where Can You Take This?"
  reframed from a generic "keep learning" resource list into a session
  specifically about which newsroom roles/functions are adopting the
  *build* skills this workshop taught, explicitly required to not repeat
  Day 1's already-extensive Industry Conversation/Use Cases content (I
  read both pages first to confirm the new angle didn't overlap).
  - **Schedule**: 10:00 AM–5:00 PM, one 15-min break (11:15 AM, matching
    Day 1's break time exactly), lunch 1:00–2:00 PM. 7 sessions + a
    `url: null` closing marker: Recap & Open Questions (30m, discussion) →
    Product Design (45m, lecture) → break → Safe & Auditable Design (45m,
    lecture) → AI-Human Design (45m, lecture) → lunch → Where Can You Take
    This? (45m, lecture) → Final Coding Time (60m, hands-on) → Final Show
    & Tell (60m, discussion, includes the closing/celebration content
    inline rather than as a separate page) → Closing & Celebration (15m,
    schedule marker only, no page).
  - **Research**: 4 parallel background agents, each briefed to find
    multiple sources (not one canonical doc), fetch everything live, and
    extract checklists/named examples/concrete numbers rather than
    position statements. Genuinely deep results: Product Design found a
    consistent pattern across 5+ named newsroom AI products (Chowbot, Ask
    FT, Forbes' Adelaide, Rappler's Rai, a 4-bot UNC CISLM study) that all
    independently converged on "scope to what you own, say so when you
    can't." Safe & Auditable Design found real incidents (NYC's MyCity
    chatbot giving false legal guidance for over a year uncaught, Air
    Canada's tribunal loss, CNET's 53%-error self-audit) plus concrete
    newsroom mechanisms (WBEZ's per-instance approval, LAist's
    accountability language, CBC's one-question disclosure test) and NIST's
    actual AI Risk Management Framework simplified to a 4-question
    checklist. AI-Human Design surfaced a genuinely counterintuitive
    finding worth the session's centerpiece: a controlled study found
    giving people an algorithm's prediction to adjust produced a *worse*
    false-positive rate and introduced racial bias not present in the
    algorithm alone, directly complicating the naive "just add a human
    checkpoint" assumption; paired with Zillow's Project Ketchup (removing
    a working checkpoint under growth pressure, $421M quarterly loss) for
    the opposite failure mode. Where Can You Take This surfaced named,
    current (2026) roles (Politico's Newsroom Architect, ProPublica's
    Computational Journalist), a real repo-level statistic (37% of new
    newsroom repos show AI-coding signals by early 2026, up from a repo
    culture that had collapsed 80% since 2016), and solo-builder examples
    (a Reuters correspondent with no coding background who's built 14
    tools; a journalist's 50+ Skill open-source library), plus an honest
    counterweight (a controlled trial found experienced developers using
    AI tools were 19% slower while believing they were faster).
  - **Bug caught during build, not before**: repeatedly wrote `<sup
    class="cite">...*</dd>` in `.roster` rows across multiple pages,
    omitting the closing `</sup>` before `</dd>`. Not caught by
    `check-slide-parity.js` (which only checks item counts, not tag
    balance) — caught by explicitly grep-counting `<sup>`/`</sup>` opens
    vs. closes per file during verification. Fixed across all 3 affected
    files (`02-product-design.html`, `04-ai-human-design.html`,
    `05-where-you-can-take-this.html`). Worth remembering for future
    `.roster` sections with trailing citations.
  - **Not done**: no day of the workshop currently has a home for VS
    Code/Claude Code/Git content, see the "Downstream, not yet touched"
    section above for the full note.
- 2026-08-13 — **Day 2 built from scratch**, on `review/full-site-audit-2`.
  Planned in plan mode from the user's 14-item draft agenda, consolidated
  into 8 sessions after two rounds of user pushback (grouping confirmed via
  `AskUserQuestion`; time allocation reworked after the user challenged
  whether "Your Goal & Plan Mode" at 50 min had enough real substance while
  CLAUDE.md at 20 min was too thin for something "vital" — resolved by
  sketching actual content per session rather than just doing time-math,
  landing both at ~30-35 min; a second round added a prompting-history
  timeline and reframed Spec-Driven Development around a concrete
  checklist rather than a paper summary, per further user feedback). Full
  plan preserved at the top of `project/adr/` is not applicable here, this
  was tracked via the planning tool, not an ADR, since it's content
  structure, not a technical decision.
  - **Schedule** (`schedule.json`): 10:00 AM–5:00 PM, one 15-min break
    (11:35 AM), lunch 1:00–2:00 PM, matching Day 1's shape exactly. 8
    sessions: Yesterday's Debrief (20m, discussion) → Prompting (40m,
    hands-on) → CLAUDE.md (35m, hands-on) → break → Skills & Best
    Practices (40m, lecture) → Your Goal & Plan Mode (30m, hands-on) →
    lunch → Spec-Driven Development (30m, lecture) → Revisit & Build (60m,
    hands-on) → Show & Tell + Critique (90m, discussion).
  - **All 8 topics built**, Overview + Slides each, using the briefing
    template exactly as established on Day 1 (discussion sessions get
    light citation density and `.field-notes` as discussion prompts;
    lecture sessions are citation-backed; hands-on sessions get
    `.exercise-box`). `project/scripts/check-slide-parity.js` passes clean.
  - **Sourcing**: Day 2 leans on Anthropic's own documentation instead of
    Day 1's industry/journalism sourcing, gathered via 5 parallel
    background research agents (never inline, per standing preference),
    each one fetching and verifying sources live rather than citing from
    memory: `code.claude.com/docs/en/memory` and
    `code.claude.com/docs/en/best-practices` (CLAUDE.md, general best
    practices), `platform.claude.com/.../agent-skills/overview` and
    Anthropic's Oct 2025 Skills launch post (Skills),
    `code.claude.com/docs/en/permission-modes` (plan mode), and the user's
    linked paper (`arxiv.org/pdf/2602.00180`, "Spec-Driven Development:
    From Code to Contract," Piskala, Jan 2026) for the Spec-Driven
    Development checklist — the paper turned out to be genuinely
    prescriptive (a real four-phase Specify/Plan/Implement/Validate
    framework), not just conceptual, confirmed by extracting the full PDF
    text rather than trusting a summary. The prompting history timeline
    (2022 role-play era → 2023 "prompt engineer" job boom → 2024 Anthropic
    ships prompt generator/improver tools → 2025 Anthropic's own guidance
    that early scaffolding tricks matter less now) is built entirely from
    dated, fetched, live-verified sources, one Gartner claim was found and
    dropped because the primary source 403'd and couldn't be verified.
  - **Consequence**: this makes the site-wide divergence between `live`
    and `review` wider in one sense (Day 2 exists only on `review`) but
    narrower in the naming sense (Day 2's pages all use "AI News
    Innovation Workshop" and have zero em-dashes from the start, unlike
    the rest of `review`'s still-unswept pages).
  - **Not done**: `docs/day-3/` is still fully untouched. Whether Day 2
    should also carry VS Code/Claude Code/Git content (previously assumed
    in an earlier "downstream, not yet touched" note) turned out not to
    fit the day the user actually wanted, that note has been corrected
    above rather than fulfilled as originally written.
- 2026-08-12 (latest, round 2) — Three more small fixes on `live`,
  same "edit there directly, it's what's deployed" pattern as above:
  (1) removed the redundant "Setup" breadcrumb sitting right above the
  `<h1>` on `setup.html`. (2) Corrected the workshop's actual name
  site-wide on `live`: "AI Journalism Workshop" → "**AI News Innovation
  Workshop**", across `setup.html`, `setup-day-2.html`, `nav.html`, and
  `footer.html` (all 4 occurrences that branch has). **This name is
  still wrong everywhere on `review/full-site-audit-2`** — every page
  title, the nav logo, the footer — that's the correct name for the
  whole site, not just `live`'s pages, so this needs a full find/replace
  across `review` too, not yet done. (3) Added the Tow-Knight Center for
  Journalism Futures logo (`docs/assets/images/tow-knight-logo.png`,
  supplied by the user from `~/Downloads`) to the nav bar next to the
  workshop name, via a new `.site-nav-brand` flex wrapper in
  `nav.html`/`style.css` (28px tall, width auto). All three verified
  live via curl; the logo specifically confirmed as byte-identical to
  the source file (21,555 bytes) once served.
- 2026-08-12 (latest) — Two small requests on `live`'s setup pages: (1)
  added a real GitHub-connector walkthrough to `setup.html`'s GitHub
  section (find the `+` next to the message box → Connectors → GitHub →
  OAuth device-code sign-in → confirm connected), previously deferred to
  the live Explore Claude Desktop session, now self-serve since it's
  just an OAuth sign-in with no install step; checklist count 6 → 10.
  (2) Removed every em-dash from `setup.html` and `setup-day-2.html`
  (replaced with periods/colons/commas as fit each sentence). User set
  this as a **standing rule going forward, not a one-off edit** — saved
  to Claude's cross-session memory (`feedback_no-em-dashes`, outside
  this repo) so it applies to future copy work automatically. Both
  changes verified live via curl. Widens the divergence from `review`'s
  copies, already flagged above as a known follow-up.
- 2026-08-12 (later still) — Copy/design pass on `setup.html`, done
  directly on the `live` branch since that's what's actually deployed
  (not `review/full-site-audit-2`'s copy, which still has the original
  content and is now out of sync — see below). Found and fixed a real
  CSS bug in the process: `.field-notes.is-interactive-checklist label`
  has `display: flex`, and any inline element (`<strong>`, `<a>`) that's
  a *direct child* of a flex container becomes its own separate flex
  item instead of flowing as normal text — this is why "Chat," "Cowork,"
  "Code" and the `github.com` link were each rendering on their own
  line. Fixed by wrapping each label's text in a `<span>` (one flex
  item instead of many), applied to every checklist item in both
  `setup.html` and `setup-day-2.html` on `live`, not just the two the
  user flagged, since it's the same underlying bug everywhere the
  pattern appears. Content edits: dropped the Claude-account/paid-plan
  checklist item, split the "if something doesn't work" contact info
  into its own paragraph, "workshop account" → "email account" for the
  sign-in step, removed the Git/GitHub-Desktop blockquote. Checklist
  count 7 → 6. Verified live via curl.

  **Known follow-up, not yet done**: `review/full-site-audit-2`'s copies
  of `setup.html` and `setup-day-2.html` have the identical flex bug
  (same CSS, same HTML pattern) and none of today's content edits.
  Needs the same treatment whenever that branch's Day 1 rework actually
  ships — the two branches' setup pages are now genuinely divergent, not
  just differently-scoped.

  **Follow-up, same day**: added a real walkthrough for connecting
  Claude Desktop's GitHub connector to `live`'s `setup.html` (find the
  `+` next to the message box → Connectors → GitHub → OAuth device-code
  sign-in → confirm connected) — previously this was deliberately
  deferred to the live Explore Claude Desktop session; now self-serve,
  since it's just an OAuth sign-in with no install step. Steps sourced
  from the same research already used to write Explore Claude Desktop's
  "Connecting GitHub" section, not re-verified fresh. Checklist count
  6 → 10. This widens the divergence from `review`'s copy noted above.
- 2026-08-12 (later same day) — Even with production correctly tracking
  `live`, user found that clicking through the shared `nav.html`/
  `footer.html` from `setup.html` still reached the rest of the (old,
  pre-rework) site — every page, day, and the resources/students
  sections were all still one click away. Not acceptable. Stripped the
  `live` branch down to **only** `setup.html`, `setup-day-2.html`, and
  the assets they actually depend on (`style.css`, `briefing.css`,
  `partials.js`, `nav.js`, `checklist.js`, plus bare-logo versions of
  `nav.html`/`footer.html` with no links elsewhere) — every other page
  and unused script/stylesheet removed from the branch entirely (40
  files changed, ~3,400 lines removed). Fixed the dead links this left
  in both setup pages (breadcrumb, the old "resources page" and "Fork &
  Submit" mentions). Added a branch-local `.gitignore` blocking those
  removed paths from being reintroduced by a future merge/cherry-pick —
  note per the user's own question: `.gitignore` alone doesn't remove
  already-committed files or affect what Vercel builds; the actual fix
  was `git rm`, the gitignore is just a safety net against re-adding
  them later. Verified via curl against the live production URL:
  `/setup.html` and `/setup-day-2.html` load; `/`, `/resources.html`,
  `/students/`, every `/day-1/*`, `/day-2/`, `/day-3/`, and
  `/data/schedule.json` all 404. [ADR 0018](adr/0018-live-branch-for-partial-production-deploy.md)
  updated with this as a follow-on decision.
- 2026-08-12 — User merged PR #2 into `main` directly (deviating from the
  "don't merge yet" plan logged the day before). Vercel's production
  deploy off `main` then hit a **team-membership** block (git commit
  author wasn't recognized as a member of the connected Vercel team) —
  resolved by making the GitHub repo public, per the already-decided
  [ADR 0002](adr/0002-public-repo.md), which the repo had drifted from
  (it was still private). That fixed the deploy, but exposed Vercel's
  **Deployment Protection** login wall on top — and once that got sorted
  (via a Vercel "Share Deployment" bypass link, initially), a bigger
  problem surfaced: `main` now has the *entire* Day 1 restructure on it,
  not just the reviewed-and-ready `setup.html`. Resolved by creating a
  dedicated `live` branch instead — see
  [ADR 0018](adr/0018-live-branch-for-partial-production-deploy.md) for
  the full reasoning.

  **Resolved, same day.** Vercel's dashboard has moved this setting under
  "Environments" (not the classic "Settings → Git → Production Branch"
  path); user set the Production environment to track `live`. That alone
  didn't retroactively rebuild/promote anything — the stable production
  URLs kept serving the old `main`-based deployment (confirmed live via
  curl: today's new Product Discussion page was still reachable, and
  Deployment Protection was off project-wide, so this was a real public
  exposure of the in-review Day 1 content for a window, not just a
  theoretical one — user opted to leave it exposed rather than re-protect
  while sorting the setting out, judging it low-stakes). Pushed an empty
  commit to `live` to force a fresh build once Production was actually
  tracking it; that promoted correctly. **Verified via curl against both
  candidate stable domains**: `setup.html` loads (200, correct title,
  checklist present, checklist.js loads), today's `04-product-discussion`
  404s as expected, and the old `05-project-ideation` (pre-rework) is
  back, confirming production now serves the `live` branch, not `main`.
  Link to send students: `https://2026-ai-news-innovation-workshop.vercel.app/setup.html`.
- 2026-08-11 — Committed and pushed the full Day 1 restructure (Claude
  Desktop pivot, schedule retiming, Adiel's PR #1 feedback, State of AI
  tone pass) as one commit on `review/full-site-audit-2`, and opened
  [PR #2](https://github.com/AndrewRCalderon/2026-ai-news-innovation-workshop/pull/2)
  against `main` — not to merge yet, but to give Vercel (just connected
  to the repo) a PR-preview URL so `setup.html` can be shared with
  students without merging the whole diff into `main` first. **Superseded
  2026-08-12** — user merged anyway; see the entry above for what
  happened next.
- 2026-08-06 — Implemented most of Batches 1–4 from the full-scale site
  review (Topic 1 "State of AI" content edits, plus two template-level
  fixes applied across all 8 existing slide decks: removing the
  `cover-hint` and replacing the `-30-` end slide with a Restart/Back-to-
  schedule/Next-section nav block). Ran a background research agent to
  verify the ChatGPT "1M users in 5 days" stat, identify the 2012
  benchmark (AlexNet/ImageNet), and find real training-data-lawsuit and
  newsroom-AI examples — findings folded into the relevant copy as plain
  text (see research findings entry above). Explicitly **not** built:
  the interactive citation/footnote (superscript + popover) system the
  user has asked for three times now — still needs its own design pass,
  since it touches the shared briefing template. Also not yet done:
  home-page style harmonization, student-submission flow testing, Day 1
  index summary/learning-outcomes, and the "Caveat" column content-depth
  pass — all still open in the batches above.
- 2026-08-04 — Requirements log created from the approved build plan. Phase 1
  scaffold (structure, partials, base CSS, page skeletons, deploy config)
  completed in the same session.
- 2026-08-04 — Shifted focus to frontend/content per instruction; paused
  Phase 2 (backend proxy) and the remaining Vercel-connection item. Built
  `schedule.json`, the timeline system, and all 6 Day 1 topic pages plus
  stub Day 2/3 index pages. Verified locally with a static file server —
  all key routes return 200.
- 2026-08-04 — User supplied real content for Day 1/Topic 1 ("State of AI").
  Designed a distinct template for content-rich topic pages via Artifact
  prototypes (long-form scroll → paginated deck → combined with a mode
  toggle), approved by the user, then shipped it as `docs/css/briefing.css` +
  `docs/js/briefing.js` and wired into `day-1/01-state-of-ai.html` with the
  real content. See [ADR 0010](adr/0010-briefing-template.md) for the
  self-contained-nav tradeoff this required.
- 2026-08-04 — User asked to bring back the original scrolling design as the
  landing page and move the deck to a linked "Slides" subsection instead of
  a runtime toggle. Split into `day-1/01-state-of-ai.html` (Overview, shared
  nav restored, reuses `topic-metadata.js`) and
  `day-1/slides/01-state-of-ai-slides.html` (Slides, paginated deck only).
  Deleted `briefing.js`; added `docs/js/deck.js` and `docs/js/reveal.js`;
  simplified `briefing.css` accordingly. See
  [ADR 0011](adr/0011-split-overview-and-slides.md).
- 2026-08-04 — User supplied the real Day 1 schedule; it revealed the
  existing `schedule.json` was missing the project-ideation cluster (group
  conversation, problem statement/hypothesis/goal, a nudge/reminder) and had
  "AI Tools" undersized (45 min instead of the actual 2 hours). Corrected
  `schedule.json`: moved Project Ideation before lunch, added a new
  post-lunch "Problem Statement Discussion" and "Project Assignments"
  session (1hr, workshop-buddy pairs), added a non-linked "Nudge & Check-in"
  checkpoint (same pattern as Break/Lunch — `url: null`), and fixed AI Tools
  to 120 min. Renumbered `06-ai-tools.html` → `07-ai-tools.html` to keep
  filenames in chronological order; added placeholder pages
  `06-problem-statement-discussion.html` and `08-project-assignments.html`;
  updated `nav.html`'s Day 1 dropdown to match. Day 1 is now 8 linked topics
  (was 6) — total topic-page count across the site is 22 (was 20).
- 2026-08-04 — Retimed the Day 1 morning block per user direction: State of
  AI (15 min), Industry Conversation (30 min), Use Cases (30 min), People to
  Follow (15 min unchanged), two 15-min breaks, and Project Ideation
  expanding to fill the rest of the 9:00 AM–1:00 PM block (now 120 min,
  intentionally long for now per the user — "that's ok for now"). Lunch
  shifts to 1:00–2:00 PM, cascading the whole afternoon ~15 min later
  (Problem Statement Discussion 2:00 PM → Nudge & Check-in 5:30 PM). Worked
  out interactively with the user before writing to `schedule.json`.
- 2026-08-04 — User supplied real content for Day 1 Topics 2–4 (Industry
  Conversation, Use Cases, People to Follow) and built them on the same
  briefing-overview template as Topic 1 — no new CSS/JS needed, the existing
  component vocabulary (roster, compare-grid, field-notes, stakes,
  pull-question) covered all three. Also: Industry
  Conversation's type corrected `discussion` → `lecture`; "Problem Statement
  Discussion" renamed to "Problem Statement" (the type badge already says
  "discussion," redundant in the title); Day 1's headline changed to "Day 1:
  State of the Art & Experimentation" (`schedule.json` + `day-1/index.html`).
- 2026-08-04 — Added Slides companions for Topics 2–4
  (`day-1/slides/02-industry-conversation-slides.html`,
  `03-use-cases-slides.html`, `04-people-to-follow-slides.html`) plus the
  "Open the slides →" CTA on their Overview pages, matching Topic 1's
  pattern exactly — no new CSS/JS. Decided every content-complete topic gets
  a Slides page going forward, not a per-topic call. Caught and fixed a
  staleness bug this surfaced: Topic 1's slides page still showed the old
  "45 MIN" after the schedule retiming; see the new task above about
  `deck.js`'s static cover-meta.
- 2026-08-04 — User supplied real content for Day 1 Topics 5 (Project
  Ideation) and 7 (AI Tools) — the two densest topics so far. Both built as
  Overview + Slides pairs on the existing template with no new components:
  reused `.history` (originally built for chronological timelines) for two
  sequential-steps diagrams — the circular design process and the
  build/test/ship workflow — since a numbered step sequence is the same
  shape as a timeline. Reused `.exercise-box` (from the old generic
  template, defined in `style.css`) for the Project Ideation workshop
  activity, since briefing pages already load `style.css` first. AI Tools'
  tool-landscape section links tool names to their real URLs from the
  source doc. Day 1 is now 6/8 topics with real content; only Problem
  Statement and Project Assignments remain placeholders.
- 2026-08-06 — Added a new Day 1 session, "Explore Tech Stack," right after
  AI Tools, per user direction: AI Tools shrinks from 120 to 30 min, and the
  freed 90 min goes to the new session (30 + 90 = 120, so nothing downstream
  in the afternoon shifts). Renumbered `08-project-assignments.html` →
  `09-project-assignments.html` to make room; new
  `08-explore-tech-stack.html` scaffolded as a generic-template placeholder
  (content deferred — user is writing it separately). Updated
  `schedule.json` and `nav.html`. Flagged the likely content overlap this
  creates with AI Tools' existing workshop-stack section — see the task
  above.
- 2026-08-06 — Resolved that overlap: moved "Your Workshop Tech Stack" and
  "How They Work Together" out of `07-ai-tools.html`/its slides into
  `08-explore-tech-stack.html`, which now has real content instead of a
  placeholder. Added a facilitator roadmap the user asked for — a
  time-boxed plan for the 90-minute session (VS Code 20 min → Claude Code
  45 min → GitHub 25 min, confirmed with the user) rendered via the
  `.history` steps component, plus a "basics checklist" per tool (what to
  demo/have people do, not narrative prose) for VS Code, Claude Code, and
  GitHub. AI Tools renumbered down to 5 sections; both pages' slide/section
  counts and TOCs updated to match. No new CSS/JS — same component
  vocabulary throughout.
- 2026-08-06 — Split tool setup from tool walkthrough per user direction:
  `docs/setup.html` now has real, self-serve install instructions (VS Code,
  Claude Code, GitHub, opening them together inside VS Code, a
  verify-you're-ready step) instead of the original 5-bullet stub — this is
  the page sent to students before Day 1, so it's written assuming no
  instructor is present to help, plus a short reassurance line for anyone
  who gets stuck. `08-explore-tech-stack.html` (and its slides) had install
  steps removed accordingly and now link back to `/setup.html`; its Claude
  Code section was reframed from a basics checklist to best-practices/
  mindset content (be specific, use Plan Mode, read every diff, treat
  surprises as information) — the user's reasoning being that the real way
  to learn an agentic tool is to use it, so guardrails plus practice beats
  a checklist. `setup.html` now loads `briefing.css` alongside `style.css`
  to reuse its field-notes/roster styling, without adopting the full
  masthead/TOC/slides-cta template scaffolding (it isn't a schedule-tied
  topic page).
- 2026-08-06 — Reworked `setup.html`'s GitHub section for readers with no
  command-line experience: separated the Git-vs-GitHub concepts up front,
  added GitHub Desktop as the recommended no-terminal path (direct Git
  install stays as the alternative for anyone comfortable with one), linked
  GitHub's own setup docs for anyone who wants more depth, and noted that
  Claude Code can run git commands on a student's behalf once it's set up —
  so this step is about installing accounts/apps, not learning git syntax.
  Adjusted the "Verify You're Ready" step to branch by which path was
  taken, since GitHub Desktop's bundled Git isn't reliably on the system
  PATH (`git --version` isn't a valid check for that path).
- 2026-08-06 — Added a new Day 1 session, "Fork & Submit" (40 min,
  hands-on), between Explore Tech Stack and Project Assignments, funded by
  shrinking Project Ideation from 120 to 80 min. Because the new block sits
  in the afternoon while the time comes from late morning, Project
  Assignments and Nudge & Check-in land on the exact same clock times as
  before (4:30 PM / 5:30 PM) — everything between them shifted 40 min
  earlier, most visibly lunch (1:00 PM → 12:20 PM). New
  `09-fork-and-submit.html` + slides cover what a fork is, forking the real
  repo, cloning it, branching, and the commit/push/PR submission mechanics
  — content that used to be one unexplained bullet in Explore Tech Stack's
  GitHub Walkthrough, which is now trimmed to generic Git/GitHub mechanics
  only, with a forward-reference to the new session. Renumbered
  `09-project-assignments.html` → `10-project-assignments.html`.
  Confirmed and used the real repo URL
  (`github.com/AndrewRCalderon/2026-ai-news-innovation-workshop`)
  throughout, which also resolved the long-standing `setup.html` TODO about
  linking `STUDENT_CLAUDE_GUIDE.md` (see the note above — that file itself
  still needs to be written before setup.html actually goes out).
