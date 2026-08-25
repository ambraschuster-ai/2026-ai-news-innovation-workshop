# Project 5 — The Listening Loop · architecture

> **Status: not started.** Planning-depth sketch.
> Companion files: [requirements.md](requirements.md), [tasks.md](tasks.md).

## Approach

The scrubber sits **inline in the answer path**, before anything is
written — not as a cleanup job afterward. That ordering is the entire
security model. A cleanup job means the raw text existed on disk, and
"existed on disk" is what a subpoena reaches.

```
  question arrives (any channel)
        │
        ↓
  listen/scrub.py  ← INLINE, before any write
        │            names, phones, addresses, A-numbers, case numbers
        ↓
  minimal record: scrubbed text, language, time bucket,
                  retrieval result, answered y/n
        │
        ├── listen/cluster.py  ── weekly: rising topics + gaps
        │         │
        │         ↓
        │   weekly digest → newsroom
        │
        └── retention job ── raw text deletes on a short cycle,
                             aggregates survive
```

## Key decisions

- **Scrubbing is lossy and irreversible on purpose.** If a scrub rule is
  too aggressive and eats a real word, that's an acceptable cost. The
  reverse is not.
- **Coarse time buckets, not timestamps.** "Tuesday afternoon" supports
  trend analysis; an exact second helps correlate a person with an event.
- **Two things get surfaced, not twenty.** Rising topics and information
  gaps. A digest that reports everything gets read by nobody.
- **Gaps are the product.** A frequent question retrieval can't answer is
  the single most valuable output of this whole project — it's a story
  Documented hasn't written.
- **Deletion is automatic, not procedural.** A retention policy that
  depends on someone running a script is not a retention policy.

## What it works with or around

- **Every channel from Projects 3 and 4** feeds this, so the scrubber has
  to sit at the shared choke point rather than being reimplemented per
  channel.
- **WhatsApp metadata is Meta's.** Nothing built here changes that. It's a
  disclosure obligation, and it's why the bot's disclosure says so plainly.
- **The threat model document** (Project 1, task A.5) governs this project.
  If the implementation and the document disagree, the document wins or the
  document gets rewritten deliberately — not silently.
- **The audience is in genuine legal jeopardy.** This is the project where
  a convenient shortcut has consequences for someone other than me.

## Why this project matters institutionally

This is the piece most likely to secure long-term buy-in, because it
produces something the newsroom wants for its own sake: story leads. The
freshness engine keeps the guide alive; the listening loop is what makes
someone at Documented care whether it stays alive.
