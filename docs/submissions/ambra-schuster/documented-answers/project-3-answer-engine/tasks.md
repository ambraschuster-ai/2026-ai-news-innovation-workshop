# Project 3 — Retrieval + Answer Engine · tasks

> **Status: not started.** Planning depth — rewrite before building.
> Companion files: [requirements.md](requirements.md), [architecture.md](architecture.md).

## Stage 1 — The eval set, first

- [ ] **1.1 — Resolve the gold-set source.** Chase the documented.info
      Zendesk ticket archive (Project 1, task A.1). If it's a no, switch to
      the fallback rather than stalling.
- [ ] **1.2 — Assemble ~100 questions** across all four languages, tagged
      answerable-from-corpus / answerable-but-stale / out-of-scope /
      must-refuse.
      *Done when:* every tag has real coverage in every language.
- [ ] **1.3 — Write `eval/run_eval.py`** scoring retrieval hit rate,
      citation accuracy, refusal correctness, and cross-lingual recall.
      *Done when:* it reports per-language, not just aggregate.

## Stage 2 — Retrieval

- [ ] **2.1 — Write `index/chunk.py`** splitting on H2/H3.
      *Done when:* 10 chunks read as self-contained answers.
- [ ] **2.2 — Stand up BM25** over the corpus using SQLite FTS5.
      *Done when:* acronym queries (IDNYC, TPS, SNAP) return the right
      article as the top hit.
- [ ] **2.3 — Compare embedding models** on Chinese and Spanish test sets.
      *Done when:* there's a number behind the choice, and Kreyòl's
      measured deficit is written down.
- [ ] **2.4 — Combine into hybrid search** in `index/search.py`.
      *Done when:* hybrid beats both BM25 alone and vector alone on the
      eval set.

## Stage 3 — Answering

- [ ] **3.1 — Write the system prompt** encoding the answer contract.
- [ ] **3.2 — Enforce the contract in code** in `answer/guardrails.py` —
      citation present, freshness stamped, refusals routed.
      *Done when:* an answer missing a citation cannot be returned.
- [ ] **3.3 — Hard-code emergency escalation** for ICE/detention/raid
      queries, short-circuiting retrieval.
      *Done when:* every emergency phrasing tested returns the hotline
      path, in every language.
- [ ] **3.4 — Adversarial pass.** Questions designed to pull the bot into
      legal advice, into stale information, and off-corpus.
      *Done when:* every refusal boundary has a passing test case.

## Stage 4 — Ship it

- [ ] **4.1 — Build the site chat widget.**
- [ ] **4.2 — Publish the accuracy numbers**, per language.
- [ ] **4.3 — Take eval results to the newsroom** and let them set the
      autonomy dial.
      *Done when:* Documented has made that decision with evidence in hand.
