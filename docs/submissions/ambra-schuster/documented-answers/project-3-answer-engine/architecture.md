# Project 3 — Retrieval + Answer Engine · architecture

> **Status: planning-depth sketch for the real build, plus a working mockup
> that took a different route.** Everything from "Approach" down is the
> planned architecture and still stands. What was actually built in the
> mockup, and where it deliberately departs, is recorded at the bottom under
> [What the mockup actually built](#what-the-mockup-actually-built).
> Companion files: [requirements.md](requirements.md), [tasks.md](tasks.md).

## Approach

Build the eval set *before* the bot. This is the step that separates a demo
from something a newsroom will trust, and doing it second means tuning
toward whatever the bot already happens to do well.

## The pieces

```
  data/corpus.db
        │
  index/chunk.py    ── split on H2/H3 boundaries
        │
  index/embed.py    ── vectors
        │
  index/search.py   ── HYBRID: BM25 (SQLite FTS5) + vector, combined
        │
  answer/generate.py ← answer/prompt.py + answer/guardrails.py
        │
        ├── channels/widget/   (site chat)
        └── eval/run_eval.py   ← eval/goldset.yaml
```

## Key decisions

### Hybrid retrieval, not embeddings alone

This domain is saturated with acronyms and program names — SNAP, TPS, DACA,
NYCHA, IDNYC, ActionNYC, Section 8, EBT, WIC — where exact keyword match
beats semantic similarity and pure vector search reliably fumbles. Keyword
search catches "IDNYC"; vector search catches "the city ID card thing."
Both are needed.

SQLite's FTS5 covers the keyword half, which is part of why Project 1 chose
SQLite.

### Chunk on H2/H3 boundaries

Documented's explainers are already written as question-headings, and each
section is a self-contained answer. This is why Project 1's
`normalize.py` preserves heading structure — cheap there, expensive to
retrofit here.

Ad blocks and newsletter CTAs must be stripped before indexing or they
pollute every chunk. Project 1 handles that.

### Embeddings

Anthropic doesn't make an embedding model. Evaluate `cohere
embed-multilingual-v3.0` against `voyage-3-large` on a Chinese and Spanish
test set.

**Flag honestly:** Haitian Creole is poorly supported by every commercial
embedding model. For Kreyòl, lean harder on BM25 and on the
translation-coverage matrix from Project 1, and be prepared to tell the
newsroom that Kreyòl retrieval quality is measurably worse rather than
papering over it.

### Generation

`claude-opus-5`. Cost controls that matter at volume:

- **Prompt caching** on the system prompt and guardrails — large discount
  on the cached prefix. Keep the volatile user question *after* the last
  cache breakpoint.
- **Batch API** for all offline work: eval runs, bulk translation-gap
  analysis, org extraction.
- Whether routine queries drop to a smaller, cheaper model is the
  newsroom's call — measure quality first, then let them choose.

Rough live cost: a cited answer over ~4 retrieved chunks runs roughly
3–6k input / 300–600 output tokens ≈ $0.02–0.05 per answer before caching.
At 1,000 questions/month that's $20–50/month. This is not the expensive
part; staff time is.

### The answer contract is enforced twice

In the system prompt **and** in code. A prompt is a request, not a
guarantee. Citation presence, freshness stamping, and refusal routing get
checked programmatically before an answer is returned.

## What it works with or around

- **Project 1's corpus and normalization.** Directly downstream.
- **Possible prior art:** the Signpost bundle references an existing IRC AI
  agent (`signpost-ia-app-qa.azurewebsites.net/agent`, `.../signpostbot`).
  Ask before duplicating (Project 1, task A.2).
- **The site itself** — the widget has to live on documentedny.com, which
  means Rainmakers and their conventions.
- **The audience is in genuine legal jeopardy.** This is not a domain where
  a confident wrong answer is a minor bug.

---

## What the mockup actually built

Built 25 Aug 2026 in `../mockup/`. It is a prototype on a hand-picked sample,
not a smaller version of the above — it departs from the plan in three ways
that matter, each for a stated reason. Recording them here so the real build
starts from what was learned rather than from the sketch alone.

```
  mockup/collect.html  ── browser-side collection (Cloudflare blocks scripts)
        │                 splits on H2/H3, sub-splits sections over 2,200 chars
  mockup/corpus.json   ── 38 articles, 247 sections, 420 links (gitignored)
        │
  mockup/search.py     ── BM25 in memory + describe_age() staleness labels
        │
  mockup/bot.py        ── search as a model-callable tool, grounding check,
        │                 restate_stream() for the language buttons
  mockup/guardrails.py ── emergency + legal-advice, before the model sees it
        │
  mockup/serve.py      ── sessions, limits, access code, /stats
  mockup/chat.html     ── streaming chat, source ages, language buttons
  mockup/usage.py      ── token and cost accounting
```

### Departure 1: corpus by browser, not from Project 1

Project 1 is paused, so there is no clean SQLite corpus to sit downstream of.
More importantly, **documentedny.com is behind Cloudflare and refuses
scripted access** — every article URL and the whole `/wp-json/` tree returns
403 to curl and urllib regardless of user-agent, and the Wayback Machine was
unreachable from this network. A real browser gets through fine.

This is a genuine finding for the newsroom, and it constrains Project 1 too:
any collection strategy that assumes a script can fetch these pages is wrong.

### Departure 2: BM25 only — no embeddings, no hybrid

The plan above argues for hybrid because this domain is saturated with exact-
match names. That argument turned out to be *stronger* than expected, not
weaker: Promise NYC, 3-K, COMPASS, Head Start, FAFSA, IEP, Section 504,
IDNYC, Dial-A-Teacher. On a 247-section corpus, keyword search alone returns
the right article as top hit for every acronym tested.

Not a claim that hybrid is unnecessary at 850 articles — only that the
vector half earns its complexity later, and BM25 is the half to build first.
`Index` keeps a narrow interface precisely so the guts can be swapped.

### Departure 3: two languages, and translation for the other two

The plan is four languages, each retrieving from Documented's own articles in
that language. The mockup reads English and Spanish only. Chinese and Creole
are handled by **restating a finished answer** — a separate call with no
search tool, no corpus and no history, so it cannot add facts, and both the
invented-link check and a new dropped-link check run on the output.

This sits close to a line requirements.md draws, and the resolution is
written down there rather than left implicit. The page states plainly, under
every such answer, that it is a translation and that Documented's own Creole
or Chinese reporting has not been read. Collecting those corpora is D.1.

### Things the plan did not anticipate

- **Cost is dominated by context, not by answers.** The first working version
  resent every previous search result on every turn — about $4 a
  conversation. Pruning older tool results, capping section length, and cache
  breakpoints brought it to **$0.06 a question**, close to the $0.02–0.05
  estimated above. A language switch is **$0.02**.
- **Freshness has to be computed, not prompted.** Asking the model whether
  2023-08-30 is over a year ago is asking it to be wrong occasionally, and a
  warning that only fires sometimes is not a warning. `describe_age()` does
  the arithmetic and the UI renders a badge from the date whatever the model
  wrote.
- **Sections without subheadings.** Three articles had none and arrived as
  4,000–8,000 character blobs. Since only the first 2,000 characters of a
  section are sent to the model, the bot would have confidently named the
  first two clinics on a list of twelve. The collector now regroups oversized
  sections at paragraph boundaries.
- **Public deployment is its own design problem.** Counting messages is not
  capping spend — a message needs a maximum size, `Content-Length` cannot be
  trusted, and the session cookie is attacker-controlled. An access code
  gates every route including the API, because gating only the page protects
  nothing when the key is spent at the API.

### Still open

Host is undecided — built for Render (long-running process, streaming,
in-memory sessions); Vercel is serverless and would need conversation state
in the browser and limits in Upstash Redis. See D.4 in
[tasks.md](tasks.md).
