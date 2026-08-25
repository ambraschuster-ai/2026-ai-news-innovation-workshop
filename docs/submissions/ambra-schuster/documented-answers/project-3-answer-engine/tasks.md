# Project 3 — Retrieval + Answer Engine · tasks

> **Status: a working mockup exists** (`../mockup/`, Aug 25 2026). Stages 1–4
> below are still the real build and are still at planning depth. The mockup
> took a deliberately different, shorter route — see Stage 0 and the
> "What the mockup actually built" section in
> [architecture.md](architecture.md).
> Companion files: [requirements.md](requirements.md), [architecture.md](architecture.md).

## Stage 0 — Working mockup · done Aug 25 2026

Built in an afternoon to find out whether the idea holds up at all. It does.
Nothing here replaces Stages 1–4; it front-runs them on a small sample so the
expensive version gets built against something that has already been seen to
work.

- [x] **0.1 — Corpus by browser.** documentedny.com sits behind Cloudflare,
      which refuses scripts — every article URL and the whole `/wp-json/`
      tree returns 403 to curl and urllib, browser user-agent or not.
      Collection runs in a real browser (`mockup/collect.html`) handing
      articles to a local receiver. 38 articles, 23 EN / 15 ES, 247 sections,
      420 outbound links.
- [x] **0.2 — BM25 in memory** (`mockup/search.py`), accent-folding, heading
      weighted 3×, language preference with an honest fallback flag.
      *Verified:* IDNYC, SNAP, Promise NYC, 3-K all return the right article
      as top hit.
- [x] **0.3 — Search as a model-callable tool** (`mockup/bot.py`), so the bot
      can look something up, notice the answer forks, ask, and search again.
      This is what makes it feel like a conversation and not a search box.
- [x] **0.4 — Grounding check in code.** Every link in an answer must be one
      search returned; invented links are flagged in the UI. URL-normalised
      so stripped tracking params are not false positives.
- [x] **0.5 — Freshness, computed not prompted.** `describe_age()` turns a
      date into an age and a staleness label; the prompt requires the warning
      and the page renders a badge from the date regardless of what the model
      said. *Verified:* the 2023 Head Start article is flagged, and the bot
      spotted unprompted that a 2025 rule change had overtaken it.
- [x] **0.6 — Guardrails before the model sees the message**
      (`mockup/guardrails.py`) — emergency and legal-advice paths, 10/10 on
      the phrasings tested. **English only.** Emergency card ships 911 and
      311 only; no unverified hotline number.
- [x] **0.7 — Chat window** with streaming, sources, age badges, and four
      language buttons (Easy English / Español / Kreyòl / 中文).
- [x] **0.8 — Deploy hardening.** Per-visitor sessions, three fail-closed
      limits, message and body size caps, access code over every route,
      usage tracker at `/stats`. Measured: **$0.06 a question, $0.02 a
      language switch.**

### What Stage 0 deliberately did *not* do

Named here so it is not mistaken for progress on the stages below:

- No eval set. Eight test questions is not 100, and two languages is not four.
- No SQLite FTS5, no embeddings, no hybrid search. BM25 only.
- No Chinese or Haitian Creole corpus. Those buttons translate an English or
  Spanish answer, and the page says so. See the scope note in
  [requirements.md](requirements.md).
- Citation *presence* is still not enforced in code — only citation
  *validity*. See task 3.2.

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
      *Mockup got half of this:* it rejects a link search did not return, but
      an answer with **no** citation at all still goes out. The presence
      check is the missing half and it is the harder one — a refusal
      legitimately has no citation, so it cannot be a blanket rule.
- [ ] **3.3 — Hard-code emergency escalation** for ICE/detention/raid
      queries, short-circuiting retrieval.
      *Done when:* every emergency phrasing tested returns the hotline
      path, in every language.
- [ ] **3.4 — Adversarial pass.** Questions designed to pull the bot into
      legal advice, into stale information, and off-corpus.
      *Done when:* every refusal boundary has a passing test case.

## Stage 4 — Ship it

- [ ] **4.1 — Build the site chat widget.** The mockup's chat page is
      standalone, not embedded in documentedny.com.
- [ ] **4.2 — Publish the accuracy numbers**, per language.
- [ ] **4.3 — Take eval results to the newsroom** and let them set the
      autonomy dial.
      *Done when:* Documented has made that decision with evidence in hand.

## Discovered — from building the mockup

- [ ] **D.1 — Collect the Chinese and Haitian Creole corpora.** Documented
      publishes ~216 Chinese and ~151 Creole resource articles. Until they
      are read, those two language buttons translate English or Spanish
      rather than surfacing Documented's own reporting in that language,
      which may say something different. The collector already works; this
      is mostly picking articles.
- [ ] **D.2 — Guardrails in all four languages.** Currently English
      phrasings only, which means the emergency short-circuit does not fire
      for someone typing in Spanish. This is the most serious open gap —
      task 3.3 already names it, and the mockup made it concrete.
- [ ] **D.3 — Tell Documented about the stale Head Start article.**
      `/2023/08/31/immigrants-enroll-headstart-schools-nyc/` still tells
      undocumented parents Head Start is open to them; a July 2025 rule
      change reversed that, and Documented's own later article says so. Two
      live articles contradicting each other is a finding for the newsroom,
      not just an input to Project 2.
- [ ] **D.4 — Decide the host: Render or Vercel.** Built for Render (long-
      running process, streaming, in-memory sessions). Instructor suggested
      Vercel, which is serverless and would need conversation state moved to
      the browser and limits moved to Upstash Redis. Note a Vercel Python
      function must live in `/api/` at the repo root — outside this
      submission folder — so that route wants a separate repo.
- [ ] **D.5 — Decide whether the page keeps Documented's name and styling.**
      A Documented-branded page giving immigration guidance they have not
      reviewed becomes their problem if the link travels past the class.
      Either rebrand it or show it to the newsroom first.
