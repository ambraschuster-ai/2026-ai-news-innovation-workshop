# Project 2 — The Freshness Engine · tasks

> **Status: not started.** Task list is at planning depth — expect to
> rewrite it against Project 1's actual findings before building.
> Companion files: [requirements.md](requirements.md), [architecture.md](architecture.md).

## Stage 1 — Scoring

- [ ] **1.1 — Assign volatility classes.** Every article category gets a
      decay rate. Start by hand-labeling.
      *Done when:* every article in the corpus has a class, and the
      assignments have been sanity-checked by someone at Documented.
- [ ] **1.2 — Write `freshness/staleness.py`.** Score = age × volatility.
      *Done when:* the top 20 stalest articles are ones a human agrees are
      genuinely the most urgent.
- [ ] **1.3 — Join traffic data.** Rank by staleness × readership.
      *Done when:* the ranking changes meaningfully versus staleness alone,
      or it's confirmed that it doesn't.

## Stage 2 — Source watching

- [ ] **2.1 — Pick the ~50 most-depended-on external pages.** Query the
      link table for most-linked destinations.
      *Done when:* the list exists and covers the obvious ones (USCIS,
      nyc.gov benefits, HRA).
- [ ] **2.2 — Write `freshness/source_watch.py` — snapshot.** Fetch and
      store extracted text plus a content hash.
      *Done when:* all 50 have a baseline snapshot stored.
- [ ] **2.3 — Tune the diff to ignore noise.** Ad slots, timestamps,
      session tokens must not register as changes.
      *Done when:* a week of snapshots produces near-zero false positives.
- [ ] **2.4 — Flag source-changed-after-article-modified.**
      *Done when:* the deliberate test fires — point a test article at a
      URL I control, change it, confirm the flag appears.

## Stage 3 — Getting it in front of a human

- [ ] **3.1 — Write `freshness/report.py`.** One ranked weekly digest.
      *Done when:* the digest fits on one screen and leads with the most
      urgent item.
- [ ] **3.2 — Pick the delivery channel** based on what the editor already
      opens daily, not what's nicest to build.
- [ ] **3.3 — Build the tier-2 approval queue.**
      *Done when:* an editor has approved one drafted correction end to end.
- [ ] **3.4 — Automate the schedule.**
      *Done when:* it has run unattended four weeks in a row.

## Stage 4 — Guide page regeneration

- [ ] **4.1 — Generate the guide page from the database.**
      *Done when:* generated output is compared against the live mega-menu
      list and differences are explained.
- [ ] **4.2 — Get WordPress write access** and confirm conventions with
      Rainmakers before writing anything.
- [ ] **4.3 — Publish behind human approval.**
      *Done when:* an editor has reviewed and approved a regenerated page
      before it went live.
