# Project 3 — Retrieval + Answer Engine · architecture

> **Status: not started.** Planning-depth sketch.
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
