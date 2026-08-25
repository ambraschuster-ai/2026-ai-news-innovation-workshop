---
name: ground-content
description: Research-first grounding pass for this workshop site's copy-drafts. Replaces generic, unsourced, repetitive, or stale claims with live-fetched, dated, named evidence via parallel background research agents, with a dedup check against sibling pages so no incident or stat repeats across the site. Use when the user says a copy-drafts page or section reads "shallow," "generic," "repetitive," "surface level," or "unsourced," or asks to "ground," "research," or "deepen" specific content.
---

# Ground content

This codifies the research discipline built up across Day 2, Day 3, and Day
1's 2026-08-21 rewrite (see `project/CHANGELOG.md`'s Change log for the
full history). The pattern: plan the scope, dedup-check against what the
rest of the site already owns, run parallel background research agents with
a fixed set of standing rules, write from what they find, then verify.

Don't skip the scoping questions below even when the request seems obvious.
Every past run of this by hand has hit at least one surprise once the actual
target content and its neighbors got read closely (duplicate incidents
across pages, a citation Day 3 already owns, a claim too old to represent
current tools). The questions exist because guessing on any of them has
already cost a redo once.

## Step 0 — Scope it

Ask, unless the user's request already answers these unambiguously:

1. **Which page(s)/section(s), specifically?** A whole page from scratch
   (like `01-state-of-ai.md`) and one weak section inside an otherwise-fine
   page (like Use Cases' §4-§5) call for different amounts of work. Don't
   assume "the page" means every section in it.
2. **Anything this must NOT repeat?** Name the sibling pages/days most
   likely to collide (usually the other 2 days, since Day 1/2/3 have each
   stepped on each other's material before) and any specific incident or
   stat the user already knows is spoken for elsewhere.
3. **How far should this go right now?** Copy-drafts only (the default,
   and the safer one, since `docs/*.html` is the live-editable surface and
   these rewrites are large), or copy-drafts plus implementation into the
   matching `docs/day-N/*.html`.

Skip re-asking about voice or citation format. Those are already-decided,
site-wide standing rules, see Step 2.

## Step 1 — Read before writing

- Read the target file(s) in full, including any inline `{Claude note:
  ...}` or `<!-- Content-architecture note: ... -->` comments. Both are
  real signal: the bracketed ones are usually the user's own notes left
  directly in the draft; the HTML-comment ones are prior structural flags.
  Resolve each one explicitly rather than dropping it silently.
- Check `git status` on the target file(s) before touching them. A file
  showing as modified/uncommitted means the user has pending hand-edits
  in the working tree, read those (they're already in the file you'll
  read) and preserve their substance through the rewrite, don't silently
  overwrite them just because a full rewrite is happening.
- Read the actual page content (not a changelog summary) of every
  sibling page named in Step 0's dedup answer. Build a short list of
  named incidents, stats, and sources already in use there, this is what
  the research agents in Step 2 get briefed to avoid.
- Grep the rest of `project/copy-drafts/` and `docs/` for any specific
  named example already under consideration, before assuming it's fresh.

## Step 2 — Research: parallel background agents, standing rules baked in

Never research inline, always background agents (per standing user
preference). Split the work into one agent per distinct sub-topic or
claim-cluster, not one giant agent for the whole page, narrow briefs get
better results. Every agent brief includes these fixed rules:

- **Live-fetch only.** No citing from memory. If a claim can't be
  verified live, the agent reports that explicitly rather than guessing
  or softening a citation to fit.
- **Multiple sources, not one canonical doc.** Extract concrete named
  examples, dated incidents, and real numbers, not restated position
  statements.
- **Currency rule**: any claim about *current* AI behavior, accuracy, or
  capability needs a 2023-or-later source, older tools aren't
  representative. Claims about historical *events* (a launch date, a
  filing) are exempt, don't apply this rule to a deliberate historical
  timeline.
- **The dedup list from Step 1**, spelled out by name, so the agent
  doesn't independently rediscover and re-suggest something already used
  elsewhere on the site (this happens more than you'd expect, the same
  incidents and studies keep surfacing since they're genuinely the
  best-known ones in this space).
- Model: match to the task, general-purpose/Sonnet-tier is normally
  right for this; don't default to a heavier model without a reason.

## Step 3 — Write from the research

- Match the site's existing citation convention: numbered `**Sources**`
  list per section, each entry `N. https://... — org, date: one-line
  plain-language finding with the actual number.`
- Declarative narrator voice, no first-person-plural in headings or body
  prose (this was a deliberate, confirmed site-wide choice, not an
  open question to re-litigate per page).
- No em-dashes in prose. The `N. URL — description` citation-list format
  is a structural, site-wide convention and is exempt, that's not the
  "AI voice" em-dash problem this rule targets.
- Stay inside the page's existing component vocabulary (`.chip-strip`,
  `.stat-pull`, `.stakes`, `.roster`, `.compare-grid`, `.field-notes`,
  etc., see the relevant day's `README.md` Format section) unless the
  scoping conversation explicitly opened up restructuring.
- Resolve every `{Claude note: ...}` and structural `<!-- -->` flag from
  Step 1 as part of the rewrite, don't carry them forward unaddressed.

## Step 4 — Verify

- `grep -n "—"` the touched files; every hit should be inside a
  `N. URL — description` citation line, nothing else.
- Grep for first-person-plural in headings and prose.
- Cross-check every new named incident/stat against the Step 1 dedup
  list and against a fresh grep of `project/copy-drafts/` and `docs/`,
  confirm nothing repeats.
- Spot-check a handful of citation URLs with `curl -s -o /dev/null -w
  "%{http_code}"`. A 403 on a known publisher (Bloomberg, Oxford
  Academic, GlobeNewswire, etc.) is normal bot-blocking, not a dead
  link, trust a live agent fetch over a blocked curl. A `000` or 404 is
  worth a second look.

## Step 5 — Log it

Add a dated entry to `project/CHANGELOG.md`'s `## Change log` (newest
entries go directly under the header, it's reverse-chronological), at the
same level of detail as the existing Day 2/Day 3 build entries: why this
pass happened, what was found worth flagging, what got deliberately
excluded and why, and what verification ran clean. Update `project/tasks.md`
too if this changes what's currently open. Don't skip this even for a small
follow-up pass, half of this skill's own origin was another session losing
track of exactly this kind of detail.
