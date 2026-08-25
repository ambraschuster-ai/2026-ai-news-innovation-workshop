# Project 1 — Archive & Audit · tasks

> Build order, top to bottom. Each task names its own done-test, so
> "is this finished?" has an answer that isn't an opinion.
> Companion files: [requirements.md](requirements.md), [architecture.md](architecture.md).
>
> **Rule:** a task is checked off only when its *Done when* line is
> literally true. Not "looks right" — verified.

---

## Stage 0 — Finish the rescue (urgent, do first)

Everything else here can wait a week. This can't; the source may be
deleted.

- [x] **0.1 — Archive documented.info article content**
      All four locales off the Zendesk Guide API, raw JSON, with a manifest.
      *Done when:* `data/archives/documented_info/` holds articles,
      categories, and sections per locale with counts recorded.
      ✅ **Done Aug 25, 2026** — 336 articles (`en-us` 129, `es` 72,
      `fr` 77, `fr-ht` 58), ~3.3 MB, via `ingest/zendesk.py`.

- [ ] **0.2 — Find the service map's real endpoint**
      Open documented.info's service map, watch the network requests, and
      write down the exact URL that returns provider data. Don't build
      anything yet — just confirm it's reachable and see the shape of one
      provider record.
      *Done when:* a working URL is pasted into a scratch note along with
      one full provider record, and it's clear whether it needs auth.

- [ ] **0.3 — Write `ingest/service_map.py`**
      Pull all 358 providers. Copy the retry/backoff/pagination pattern
      from `ingest/zendesk.py`. Raw JSON, untouched, to
      `data/archives/service_map/`.
      *Done when:* the file count matches the 358 the site advertises — or
      the difference is explained in a comment — and re-running it
      overwrites cleanly without error.

- [ ] **0.4 — Fallback if 0.2/0.3 is blocked**
      If the endpoint is locked down, capture the rendered provider list
      from the page instead. Note in the file that it's the degraded path
      and what's missing versus the API version.
      *Done when:* provider data exists in `data/archives/` by *some*
      route. Time-box: stop and take the fallback rather than lose the data.

- [ ] **0.5 — Write the archive README**
      One page in `data/archives/README.md`: what's here, where it came
      from, when it was captured, what each file contains, and what's
      missing.
      *Done when:* someone who has never seen this project can read it and
      know what the archive contains without opening a JSON file.

---

## Stage 1 — Pull Documented's own corpus

- [ ] **1.1 — Confirm the category IDs and counts**
      Hit the WordPress API for each of the five categories and record the
      `x-wp-total` header. This is the number everything gets checked
      against later.
      *Done when:* the five expected counts (256 / 224 / 216 / 150 / 134)
      are confirmed or corrected, written down with the date checked.

- [ ] **1.2 — Write `ingest/wordpress.py`**
      Paginate all five categories, dump raw JSON per category to
      `data/archives/documentedny/`. Raw only — no parsing in this file.
      *Done when:* article counts per category match 1.1 exactly, and the
      script runs start to finish without hand-holding.

- [ ] **1.3 — Design the database schema**
      Tables for articles, links, and categories. Article rows need: id,
      url, title, language, body text, `modified` date, source file.
      *Done when:* the schema is written as a `.sql` file, and it's clear
      by reading it how each audit in Stage 2 would be queried.

- [ ] **1.4 — Write `ingest/normalize.py` — text extraction**
      Read raw JSON, produce clean article text. Strip `googletag` ad
      blocks and newsletter CTAs. **Preserve H2/H3 heading structure** —
      Project 3 depends on it.
      *Done when:* 10 articles chosen at random (at least 2 per language)
      have been read start to finish by eye with no ad code, no CTA text,
      and no missing paragraphs.

- [ ] **1.5 — Extract outbound links during normalization**
      Every external `href` in every article, stored with the article it
      came from and the anchor text.
      *Done when:* three articles have been hand-compared against the live
      page and every external link on them appears in the table.

- [ ] **1.6 — Make the load idempotent**
      Running the loader twice must not duplicate rows.
      *Done when:* running it twice in a row leaves the row counts
      identical, verified by actually doing it.

- [ ] **1.7 — Make the whole rebuild one command**
      Archives → database in a single documented step.
      *Done when:* deleting `data/corpus.db`, running the command, and
      comparing counts gives the same result as before deletion.

---

## Stage 2 — Measure the corpus

- [ ] **2.1 — Write `freshness/linkcheck.py`**
      Check every external link. Classify: alive (2xx), redirected (3xx —
      record the destination), dead (404/410), unreachable (timeout, DNS,
      connection refused — a *different* category from dead). Concurrent,
      rate-limited, results written to the database with a checked-at
      timestamp.
      *Done when:* every link in the table has a status, and re-running
      updates rather than duplicates.

- [ ] **2.2 — Hand-verify 20 dead links**
      Open them. Confirm they're actually dead and not blocking the
      checker's user agent, rate-limiting it, or sitting behind a
      redirect loop.
      *Done when:* 20 have been opened by hand and the false-positive count
      is written down. If it's above ~10%, fix the checker before moving on.

- [ ] **2.3 — Write `audit/staleness.py`**
      Age distribution from `modified`, broken out by category and
      language. Distribution, not just an average.
      *Done when:* it outputs a table showing how many articles fall in
      each age band per category, and the food-pantry article known to be
      from 2024-11-20 lands in the right band.

- [ ] **2.4 — Write `audit/translations.py`**
      For each English article, look for ES / ZH / HT equivalents. Carry a
      confidence level per match — this is inference, not lookup.
      *Done when:* the matrix covers every English article, and 15 matches
      plus 5 "no equivalent" calls have been hand-checked for correctness.

- [ ] **2.5 — Make every number traceable**
      Each headline figure in the audit gets a companion CSV listing the
      rows behind it.
      *Done when:* for any claim in the report, the supporting rows can be
      produced in one step without rerunning analysis.

---

## Stage 3 — Ship the deliverable

- [ ] **3.1 — Get traffic data, or note its absence**
      Ask for Parse.ly access so findings can be ranked by readership
      rather than by count. If it isn't available, rank by category
      importance instead and say so in the report.
      *Done when:* either traffic data is joined to the article table, or
      the report states plainly that ranking is by proxy and why.

- [ ] **3.2 — Write `audit/report.py`**
      Generate the audit as markdown from the database, so it can be
      regenerated rather than hand-edited when numbers change.
      *Done when:* running it produces `docs/audit-2026-09.md` end to end
      with no manual editing.

- [ ] **3.3 — Write the narrative sections**
      The parts a script can't generate: what this means, what to fix
      first, what surprised me. Written for an editor, not an engineer —
      no jargon, no method detail in the body.
      *Done when:* it can be read cover to cover without needing to know
      what an API is.

- [ ] **3.4 — Get it read by a human**
      Send it to a Documented editor or the workshop supervisor.
      *Done when:* someone else has read it and their questions are either
      answered in a revision or written down as follow-ups.

- [ ] **3.5 — Update `PLAN.md` progress and `SUBMISSION.md`**
      *Done when:* both reflect what actually shipped, in the same commit
      as the finished report.

---

## Parallel track — access requests (start immediately, don't block on them)

These have long lead times and other projects branch on the answers.
Nothing in Stages 0–3 waits for any of them.

- [ ] **A.1 — Ask for the documented.info Zendesk ticket archive.**
      Two years of real questions with journalists' answers. Highest-value
      ask, likely hardest to get (IRC partnership). Blocks Project 3's
      gold set — have the fallback ready rather than stalling.
- [ ] **A.2 — Ask about the existing IRC Signpost AI agent** before
      Project 3 rebuilds something that exists.
- [ ] **A.3 — Ask for Parse.ly analytics access** (feeds 3.1).
- [ ] **A.4 — Ask who runs Documented's WeChat account.** A 15-minute
      conversation that determines whether part of Project 4 is possible
      at all. Find out now, not in week 12.
- [ ] **A.5 — Write the one-page threat model** — what data exists, who
      could compel it, what happens if it leaks — and get it reviewed
      before any project handles a real user's question.
