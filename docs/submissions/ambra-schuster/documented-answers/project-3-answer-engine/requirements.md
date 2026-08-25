# Project 3 — Retrieval + Answer Engine · requirements

> **Status: not started.** Planning depth. The gold-set source is
> unresolved (task A.1 in Project 1), and this project's shape depends
> on the answer.
> Companion files: [architecture.md](architecture.md), [tasks.md](tasks.md).

## The problem

Documented's resource guide is a list. Finding the answer to an actual
question — "can I renew my work permit if my TPS lapsed?" — means reading
several articles in a language that may not be yours. The corpus already
holds the answer; retrieving it is the hard part.

## What this has to do

1. **Answer questions from Documented's own corpus only.** No outside
   knowledge about immigration law, ever. If the corpus doesn't cover it,
   the answer is "I don't have that," not a guess.
2. **Always cite.** Every answer links the source article it came from.
3. **Always stamp freshness.** "Based on an article last updated March 2026
   — policies change, verify before relying on this."
4. **Refuse individualized legal advice.** "Will I be deported?" routes to
   legal-help resources. It never gets an opinion.
5. **Short-circuit emergencies.** ICE, detention, and raid queries bypass
   retrieval entirely and return hard-coded escalation paths — rapid
   response hotlines, ActionNYC.
6. **Answer in the language asked**, and say so when the underlying source
   is in a different language.
7. **Treat "here is the authoritative external directory" as a valid
   answer.** Documented's articles point outward by design; pointing
   outward is not a failure to answer.
8. **Be measurable.** Accuracy is a number the newsroom can see, broken out
   per language — an aggregate score can hide Haitian Creole being broken.

## What "finished" looks like

- [ ] An eval set of ~100 real questions across four languages exists,
      tagged answerable / stale / out-of-scope / must-refuse.
- [ ] Retrieval hit rate, citation accuracy, and refusal correctness are
      reported **per language**, not just in aggregate.
- [ ] Every refusal boundary has a test case, and an adversarial pass has
      tried to pull the bot into legal advice and off-corpus.
- [ ] A chat widget works on the site.
- [ ] Documented has seen the eval results and set the autonomy dial
      themselves, with evidence in hand.

## Explicitly out of scope

- Messaging channels and voice. → Project 4
- Logging or analyzing questions. → Project 5
- Machine-translating articles to fill retrieval gaps. Report the gap.
- Any answer generated from the model's own knowledge rather than from
  retrieved Documented content. This is the line the whole project rests on.

## Depends on

Project 1's clean corpus with heading structure preserved. Ideally the
documented.info Zendesk ticket archive (Project 1, task A.1) — two years of
real questions with journalists' answers is a ready-made gold set. Fallback
if it can't be obtained: article headings plus interviews with Documented's
engagement reporters.
