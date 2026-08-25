# Project 1 — Archive & Audit · requirements

> **Status: active.** This is the project being worked on now.
> Source of truth for *what this has to do*. Written as behavior, not code.
> Companion files: [architecture.md](architecture.md), [tasks.md](tasks.md).

## The problem, in one paragraph

Documented publishes roughly 850 immigrant-resource articles across four
languages, plus a glossary. Nobody has a complete picture of that corpus:
how much of it is stale, how many of its outbound links are dead, or which
English articles have no Spanish, Chinese, or Haitian Creole equivalent.
Separately, a partner site (documented.info) that held the only structured
provider dataset in Documented's orbit has been mothballed and could be
taken offline at any time.

## What this project has to do

### A. Preserve what's about to disappear

1. Capture every article documented.info published, in every language it
   published in, as raw data — before the site goes away.
2. Capture the 358-provider service map that documented.info rendered but
   documentedny.com never had.
3. Store all of it in a form that is still readable years from now with no
   special software: plain files, plain JSON, no proprietary format.
4. Record what was captured, when, and from where, so anyone can tell later
   whether the archive is complete.

### B. Get Documented's own corpus into one queryable place

5. Pull every post from the four language resource categories and the
   glossary off documentedny.com.
6. For each article, keep: title, full text, the URL it lives at, its
   language, its categories, the date it was last modified, and every
   external link it points to.
7. Strip the boilerplate that appears in every article — ad slots,
   newsletter sign-up prompts — so it doesn't pollute anything built on top
   of this later. An article's stored text should read like the article.
8. Re-running the pull must not create duplicates. It updates what changed
   and leaves the rest alone.
9. The whole pull must be repeatable by one person running one command,
   with no credentials required.

### C. Say something true about the corpus's condition

10. **Link health:** check every external link and sort each one into
    alive / redirected / dead / unreachable. For redirects, record where it
    now goes.
11. **Staleness:** report how old the corpus is — not just an average, but a
    distribution, so "half of it is fine and a quarter of it is three years
    old" is visible rather than hidden behind a mean.
12. **Translation coverage:** for each English article, say whether a
    Spanish, Chinese, and Haitian Creole equivalent exists. The four
    language versions are separate WordPress categories with no linkage
    between them, so this has to be inferred, and the report must be honest
    about how confident each match is.
13. Every number in the audit must be traceable back to the rows that
    produced it. A claim like "312 dead links" needs a list attached.

### D. Be useful to a newsroom, not just to me

14. Produce a written audit a Documented editor can read without knowing
    anything about how it was made: what's broken, how badly, and what to
    fix first.
15. Rank findings by what matters, not by what's easy to count. A dead link
    in a heavily-read Know Your Rights article outranks a dead link in a
    2019 event listing.
16. Flag anything discovered along the way that changes the plan — for
    example, an existing tool that already does part of this.

## What "finished" looks like

Project 1 is done when **all** of the following are true:

- [ ] The documented.info archive is complete — articles in all four
      locales *and* the provider dataset — and I can say what's in it
      without re-running anything.
- [ ] A single command rebuilds the entire local corpus from scratch, and a
      second run of it changes nothing.
- [ ] Article counts in the local corpus match what documentedny.com's own
      API reports for each category. Any gap is explained, not ignored.
- [ ] Ten articles spot-checked by hand read cleanly — no ad code, no
      newsletter prompts, no truncation.
- [ ] Every external link in the corpus has been checked and classified,
      and twenty of the dead ones have been hand-verified as genuinely dead.
- [ ] The translation-coverage matrix exists and its matches have been
      hand-checked on a sample.
- [ ] The written audit exists, has been read by someone other than me, and
      that person could act on it.

## Explicitly out of scope for Project 1

These are real parts of the wider plan, but they are **not** this project,
and work here should not quietly start doing them:

- Any automatic *fixing* of what the audit finds. Project 1 reports; it
  does not rewrite articles or repair links. → Project 2
- Monitoring external source pages for changes over time. → Project 2
- Search, embeddings, chunking, or any retrieval index. → Project 3
- Anything that generates text or answers a question. → Project 3
- Any chat interface, on the site or on a messaging app. → Projects 3–4
- Logging or analyzing user questions. → Project 5
- Writing anything back to documentedny.com. Project 1 is read-only against
  Documented's systems, without exception.
- Machine-translating articles to fill translation gaps. The matrix reports
  the gaps; deciding what to do about them is an editorial call.

## Constraints that hold regardless

- **Read-only and polite.** Public APIs only, rate-limited, identified by a
  real user agent. Nothing here should be noticeable to whoever runs those
  servers.
- **No credentials in the repo.** Nothing in Project 1 needs a key. If that
  changes, the key goes in an ignored `.env` file and never in a commit.
- **No personal data.** The corpus is published articles. If anything
  containing a real person's contact details turns up in the archived
  provider data, that's flagged before it's committed.
- **Honest reporting.** Where a measurement is uncertain — a fuzzy
  translation match, a link that might be a soft 404 — the report says so
  rather than rounding to a confident number.
