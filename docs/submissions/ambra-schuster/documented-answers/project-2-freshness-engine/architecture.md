# Project 2 — The Freshness Engine · architecture

> **Status: not started.** Planning-depth sketch. Revisit before building.
> Companion files: [requirements.md](requirements.md), [tasks.md](tasks.md).

## Approach

Project 1 built a database and ran the audit once, by hand. Project 2 is
the same measurements on a schedule, plus one genuinely new capability:
watching external pages for change.

Nothing here is a new system. It's the audit, automated, with an editor
attached to the output.

## The pieces

```
  (scheduled weekly)
        │
        ├── freshness/linkcheck.py     ← reused from Project 1
        ├── freshness/staleness.py     ← age × volatility class
        └── freshness/source_watch.py  ← NEW: snapshot + diff external pages
                    │
                    ↓
            findings table (in data/corpus.db)
                    │
        ┌───────────┴───────────┐
        ↓                       ↓
  freshness/report.py     drafted corrections
  weekly digest →         → editor approval queue
  Slack / sheet                    │
                                   ↓
                        (human approves) → publish
```

## Decisions to make when this starts

- **What runs the schedule.** GitHub Actions is the cheapest option that
  requires no server and no upkeep, which matters more here than anywhere
  else in the project. Alternative is a cron job somewhere, which means
  something to maintain.
- **Where source snapshots live.** Storing full HTML for ~50 pages weekly
  adds up. Storing a content hash plus extracted text is probably enough to
  detect meaningful change while ignoring rotating ad slots and CSRF
  tokens — which is the hard part of diffing a live page.
- **How volatility classes get assigned.** Hand-labeling by category is the
  honest starting point. Inferring it from how often an article has
  historically been revised is more elegant and may not have enough data.
- **Where the approval queue lives.** A shared sheet an editor already
  opens beats a custom interface nobody logs into. Optimize for the
  editor's existing habits.

## What it works with or around

- **Everything from Project 1** — the corpus database, the link table, the
  normalization pipeline, and the baseline numbers to measure against.
- **Documented's WordPress** — writing back needs admin access and should
  respect the existing custom REST namespaces (`documented/v1`,
  `docu_article/v1`). Loop in Rainmakers, their dev agency, before writing
  anything.
- **External source pages fight back.** Government sites change markup
  constantly for reasons unrelated to content. The diff has to be tuned to
  ignore noise, or the digest becomes a firehose and gets muted — which is
  the same as not existing.
- **The named editor is a hard dependency, not a nicety.** Tier-2 findings
  need a specific person who has agreed to review them. Without one, this
  tier should not ship at all.
