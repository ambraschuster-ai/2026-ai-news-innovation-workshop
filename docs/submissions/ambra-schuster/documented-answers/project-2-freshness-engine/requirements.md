# Project 2 — The Freshness Engine · requirements

> **Status: not started.** Written at planning depth. Expect this to be
> revised once Project 1's audit shows what's actually broken.
> Companion files: [architecture.md](architecture.md), [tasks.md](tasks.md).

## The problem

Project 1 measures the corpus's decay once. That's a snapshot, and
snapshots go stale. The guide needs something that notices decay on its own
and puts it in front of an editor — because the predecessor project,
documented.info, died of exactly this: manual upkeep nobody had time for.

## What this has to do

1. **Score staleness by risk, not by age.** A TPS or DACA article decays in
   weeks; "How to join a PTA" decays in years. Articles carry a volatility
   class, and the staleness score combines age with volatility.
2. **Watch the sources articles depend on.** For the most-depended-on
   external pages (USCIS forms, nyc.gov benefits, HRA), notice when the
   source page changes *after* the Documented article was last updated —
   and flag that pairing. This is the actual "the guide updates itself"
   mechanism.
3. **Sort every finding into one of three tiers** and never let a finding
   cross tiers on its own:
   - **Fully automatic:** dead-link flagging, clean-redirect rewriting,
     guide-page regeneration, staleness scoring.
   - **AI-drafted, human-approved:** "USCIS changed this fee page; the
     article still says $410" → a drafted correction an editor accepts or
     rejects.
   - **Never automatic:** legal eligibility, deadlines, policy
     interpretation. A human writes those. No exceptions.
4. **Produce one weekly digest, ranked by staleness × readership.** One
   message a week to Slack or a shared sheet. Not an alert per finding.
5. **Regenerate the public guide page from the database**, so
   `/immigrant-resources-new-york/` stops being a hand-maintained artifact.
6. **Keep running without anyone remembering it exists.** If it needs a
   person to kick it off each week, it has already failed.

## What "finished" looks like

- [ ] The weekly digest has gone out on its own for four consecutive weeks
      with no manual intervention.
- [ ] A named editor at Documented has acted on at least one finding.
- [ ] A deliberate test — pointing a test article at a URL I control, then
      changing that URL's content — makes the watcher fire.
- [ ] The regenerated guide page matches the database and is reviewed by an
      editor before anything is published.
- [ ] Median corpus staleness has measurably fallen since Project 1's
      baseline.

## Explicitly out of scope

- Publishing anything to documentedny.com without human approval. Detection
  is automated; publication is not.
- Rewriting article *content* automatically — only clean redirect URLs get
  touched without a human.
- Retrieval, search, or answering questions. → Project 3
- Any change to legal or eligibility claims, ever, by any automation.

## Depends on

Project 1 complete: the corpus database, the link table, and the baseline
staleness numbers. Traffic data (task A.3) is what makes the ranking real
rather than arbitrary.
