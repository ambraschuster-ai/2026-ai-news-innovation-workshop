# Documented NY — Resource Guide → Multilingual Answer Engine

## Context

Documented has ~850 resource articles across four languages, but the information is hard to search, hard to digest, and goes stale. The ask: make the guide self-updating, put an AI chatbot on the site, connect it to WhatsApp/WeChat/Nextdoor, and use the incoming questions as a listening tool for reporters. Plus voice as a delivery option.

I researched Documented's actual stack before planning. **Four findings change the shape of this project.**

### 1. The corpus is bigger and better than the guide page suggests

The URL you sent (`/2020/06/11/immigrant-resources-new-york/`) has an almost-empty body — one paragraph. The actual categorized list lives in the site's **nav mega-menu**, not the post. Meanwhile the real content sits in WordPress:

| Category | Slug | Posts |
|---|---|---|
| Resources (EN) | `resources` (id 145) | 256 |
| Recursos (ES) | `recursos-espanol` | 224 |
| 资源 (ZH) | `chinese-language-resources` | 216 |
| Resous (HT) | `kreyol-resous` | 150 |
| Glossary | `glossary` | 134 |

**The WordPress REST API is fully open** — `https://documentedny.com/wp-json/wp/v2/posts` returns 4,606 posts with `content`, `modified`, `categories`, and Yoast metadata. No scraping needed, no credentials needed to start. `modified` timestamps make change detection trivial.

So this is **not a content problem and not a translation problem**. Documented already publishes in four languages. It's a *retrieval, freshness, and delivery* problem.

### 2. Documented already built the human-powered version of this — and it just died

[Documented.info](https://documented.info) (with the International Rescue Committee, launched Oct 2024) is exactly this idea, staffed by humans: immigrants message via WhatsApp (`wa.me/16469395145`) and Messenger (`m.me/170561090311008`), and journalists answer in English, Spanish, French, and Haitian Creole.

The site now says: *"Documented.Info is no longer being updated, and our chat is no longer monitored. All content was last reviewed on June 30, 2026."*

**It died of maintenance burden, not lack of demand.** This is the single most important fact for your pitch and your design. Every choice should be judged by: *will this still be alive in 12 months without someone babysitting it?* It also means the channels, the audience, and the editorial workflow are already proven — you are not starting from zero, you are building the sustainable successor.

### 3. There is a structured 358-provider dataset sitting on a mothballed site

Documented.info has a **Service Map with 358 providers**, filterable by service category, location, provider, and populations served — the structured org data that documentedny.com completely lacks. It runs on Zendesk Guide (IRC's Signpost project), and its API is open:

- `https://signpost-nyc.zendesk.com/api/v2/help_center/en-us/articles.json` → 129 articles
- Locales: `en-us`, `es`, `fr`, `fr-ht`

**This is urgent.** The site is unmaintained and could be taken down at any time. Archiving it is a week-1 task regardless of everything else.

### 4. Documented's articles point outward, they don't contain directories

"Food Pantries Open Today in New York" is 263 words and defers to City Harvest's map and 311. Articles are prose explainers with Q&A-style headings ("What is Advance Parole?", "Who is eligible?") that link to `uscis.gov`, `nyc.gov`, and nonprofit sites.

Two consequences: the H2/H3 headings are **already the questions people ask** (excellent retrieval chunks), and **"here is the authoritative external directory" is a legitimate answer type**, not a failure.

Evidence of the staleness problem: that food pantry article was last modified **2024-11-20** — 21 months ago.

---

## Guiding principles

1. **Build for the day after the internship ends.** The predecessor project died of manual upkeep. Prefer boring, cheap, automated things over impressive fragile ones.
2. **Ship standalone value early.** The link-rot audit (week 3) is useful to the newsroom even if nothing else ever ships. That's how you earn access and trust.
3. **Grounded or silent.** The bot answers only from Documented's corpus, always cites the source article, always stamps how old the information is, and refuses rather than guesses. You chose "answer directly, tightly scoped" — the tight scoping is what makes direct answering defensible.
4. **Collect as little as possible.** A queryable log of undocumented people asking about ICE is a subpoena target. Design so there's nothing worth seizing.
5. **Automate detection, not publication.** Facts about immigration law get human approval. Always.

---

## Architecture

```
INGEST                    ENRICH                    SERVE
─────────                 ────────                  ─────────
WP REST API ─┐                                   ┌─ Site chat widget
             ├─→ corpus DB ─→ chunk + embed ─→ ──┼─ WhatsApp (+ voice)
Zendesk API ─┘   (Postgres)     hybrid index      ├─ Messenger
                     │                            └─ Regenerated guide page
                     ↓
              freshness engine ──→ weekly editorial triage report
              (link rot, staleness, source-change detection)
                     │
                     ↓
              question log (privacy-scrubbed) ──→ listening dashboard
```

**Repo layout** (new, in the current working directory):

```
documented-answers/
  ingest/       wordpress.py, zendesk.py, normalize.py
  freshness/    linkcheck.py, staleness.py, source_watch.py, report.py
  index/        chunk.py, embed.py, search.py        # hybrid BM25 + vector
  answer/       prompt.py, generate.py, guardrails.py
  eval/         goldset.yaml, run_eval.py
  channels/     whatsapp.py, messenger.py, widget/
  listen/       scrub.py, cluster.py, dashboard/
  data/         corpus.db, archives/
```

### Retrieval: hybrid, not pure vector

Use **BM25 + vector search combined**, not embeddings alone. This domain is saturated with acronyms and program names — SNAP, TPS, DACA, NYCHA, IDNYC, ActionNYC, Section 8, EBT, WIC — where lexical match beats semantic similarity and pure vector search reliably fumbles. Keyword search catches "IDNYC"; vector search catches "the city ID card thing."

**Chunk on H2/H3 boundaries.** Documented's explainers are already written as question-headings; each section is a self-contained answer. Strip the `googletag` ad blocks and newsletter-signup CTAs during ingestion — they're in every article's `content.rendered` and will pollute your index.

**Embeddings:** Anthropic doesn't make an embedding model. Evaluate `cohere embed-multilingual-v3.0` against `voyage-3-large` on a Chinese and Spanish test set. **Flag honestly:** Haitian Creole is poorly supported by every commercial embedding model. For Kreyòl, lean harder on BM25 and on the translation-coverage matrix, and be prepared to tell the newsroom that Kreyòl retrieval quality is measurably worse rather than pretending it isn't.

### Generation

`claude-opus-5` (1M context, $5/$25 per MTok). Cost controls that matter at volume:
- **Prompt caching** on the system prompt + guardrails (~90% discount on cached prefix; keep the volatile user question *after* the last cache breakpoint).
- **Batch API** (50% off) for all offline work — eval runs, bulk translation-gap analysis, org extraction.
- The newsroom can decide later whether routine queries drop to `claude-sonnet-5` or `claude-haiku-4-5`. Measure quality first, then let them choose.

Rough live cost: a cited answer over ~4 retrieved chunks runs roughly 3–6k input / 300–600 output tokens ≈ **$0.02–0.05 per answer** before caching. At 1,000 questions/month that's $20–50/month. This is not the expensive part; staff time is.

---

## The work, in five projects

You have ~15 weeks and want more than one shippable thing. Each project below stands alone and is useful even if you stop there.

### Project 1 — Archive & audit (weeks 1–3) · *ships a report*

**Build:** `ingest/`, `freshness/linkcheck.py`

- Pull all four language resource categories + glossary from the WP REST API into a local DB. Strip ad/CTA boilerplate. Store `modified`, categories, outbound links.
- **Archive documented.info before it disappears** — all 129 Zendesk articles in all four locales, plus the 358-provider service map. Save raw JSON to `data/archives/`.
- HTTP-check every external link in the corpus. Classify: dead (404/410), redirected (301 → where?), soft-dead (200 but content changed materially), alive.
- Build a **translation-coverage matrix**: which EN articles have no ES/ZH/HT equivalent? The four language versions are separate WordPress categories with *no translation linkage* — nobody at Documented currently has this map.

**Deliverable:** A written audit — link rot count, staleness distribution, translation gaps, and the archived provider dataset. This is a real newsroom asset and it's your credibility with the editors.

### Project 2 — The freshness engine (weeks 3–6) · *ships a weekly workflow*

**Build:** `freshness/staleness.py`, `source_watch.py`, `report.py`

Be honest about what "auto-update" can safely mean. Three tiers:

| Tier | Examples | Automation |
|---|---|---|
| **Fully automatic** | Dead-link flagging, clean-redirect rewriting, guide-page regeneration, staleness scores | Ship it, no human |
| **AI-drafted, human-approved** | "USCIS changed this fee page; the article says $410" → drafted correction | Editor approves in a queue |
| **Never automatic** | Legal eligibility, deadlines, policy interpretation | Human writes it |

- **Volatility classes**: a TPS or DACA article decays in weeks; "How to join a PTA" decays in years. Score staleness as `age × volatility`, not age alone.
- **Source watching**: for the ~50 most-depended-on external pages (USCIS forms, nyc.gov benefits, HRA), snapshot and diff them. When a source page changes *after* the Documented article's `modified` date, flag it. This is the core "the guide updates itself" mechanism — the ruling in the Advance Parole article (BIA decision, Aug 13 2026) is exactly the pattern.
- **Output**: one weekly triage digest to Slack or a shared sheet, ranked by `staleness × traffic`. Not an inbox firehose.

**Deliverable:** A recurring editorial workflow that keeps the guide alive without anyone remembering to check. Also: regenerate the actual guide page from the database, so `/immigrant-resources-new-york/` stops being a hand-maintained artifact.

### Project 3 — Retrieval + answer engine (weeks 5–10) · *ships the chatbot core*

**Build:** `index/`, `answer/`, `eval/`

**Build the eval set before the bot.** This is the step that separates a demo from something a newsroom will trust.

- Source real questions: **ask for the documented.info Zendesk ticket archive** — two years of actual questions immigrants sent via WhatsApp and Messenger, with the answers journalists gave. That is a ready-made gold set and the single most valuable thing you could be granted. Fall back to article headings + interviews with Documented's engagement reporters.
- Assemble ~100 questions across all four languages, tagged: answerable-from-corpus / answerable-but-stale / out-of-scope / must-refuse.
- Score: retrieval hit rate, citation accuracy, refusal correctness, and **cross-lingual recall** (does a Chinese question find the English article when no Chinese version exists?).

**The answer contract** — enforce in the system prompt *and* in code:
- Answer only from retrieved Documented content. No outside knowledge about immigration law.
- Always cite, always link the source article.
- Always stamp freshness: *"Based on an article last updated March 2026 — policies change, verify before relying on this."*
- Refuse individualized legal advice. "Will I be deported?" → route to legal-help resources, never an opinion.
- Answer in the language asked, and say so when the underlying source is in a different language.
- Hard-code escalation paths (rapid-response hotlines, ActionNYC) for ICE/detention/emergency queries — these should short-circuit retrieval entirely.

**Deliverable:** A site chat widget with a measured accuracy number. Bring the newsroom the eval results and let them set the autonomy dial with evidence — you flagged that this is partly their call, and this is what makes their decision informed rather than nervous.

### Project 4 — Channels + voice (weeks 9–13) · *ships WhatsApp*

Honest assessment of the three channels you named — they are not equivalent:

| Channel | Reality | Plan |
|---|---|---|
| **WhatsApp** | Real API (Meta Cloud API / Twilio). Documented has an existing community + number. Voice notes supported. | **Primary. Build this.** |
| **Messenger** | Same Meta stack, existing page. Near-free once WhatsApp works. | Second, cheap |
| **WeChat** | Official Account API effectively requires a verified Chinese entity; overseas accounts get heavily restricted API access plus content moderation. | **Verify feasibility in week 1 with whoever runs their WeChat.** Likely human-assisted posting, not a bot |
| **Nextdoor** | No public bot or messaging API. It's a human posting surface. | Repurpose: auto-draft posts, human publishes |

Don't promise four chatbots. Promise one excellent WhatsApp bot, a nearly-free Messenger twin, and a drafting tool that makes WeChat/Nextdoor posting fast for the humans who already do it.

**Voice — your instinct here is right, and it's an equity feature, not a nice-to-have.** Voice notes are how a large share of this audience actually communicates, and they work for users with low literacy in *any* written language, which text-only tools silently exclude.

- **In:** WhatsApp voice note → Whisper transcription → same retrieval pipeline. Cheap, high impact, build it.
- **Out:** TTS reply as a voice note (ElevenLabs or OpenAI TTS, both multilingual). Offer it as a toggle, not a default.
- **Caveat to test early:** ASR quality for Haitian Creole and for Spanish regional accents is uneven. Always send the text answer alongside the audio so a bad transcription is visible and correctable.
- Video is out of scope this semester. Note it as a phase-2 idea (short vertical explainers auto-drafted from top articles) and move on.

### Project 5 — The listening loop (weeks 12–15) · *ships a reporter dashboard*

**Build:** `listen/`

This is the piece most likely to secure long-term buy-in, because it produces something the newsroom wants for its own sake: story leads.

- Scrub PII **at write time**, never after: no names, no phone numbers, no addresses, no A-numbers, no case numbers. Rotating salted hash for session continuity, discarded on a short cycle.
- Store: question text (scrubbed), language, timestamp bucket, retrieval result, whether the bot could answer.
- Cluster weekly. Surface two things: **rising topics** (what's spiking) and **information gaps** (frequent questions where retrieval found nothing — these are literally assignment ideas).
- Deliver as a simple weekly digest to the newsroom. Resist building an elaborate dashboard nobody opens.

---

## Safety, privacy, and ethics

Not a footnote — this is high-stakes information for people in genuine legal jeopardy, and it should be written into the project from week 1.

- **Threat model first.** Write a one-page document: what data exists, who could compel it, what happens if it leaks. Get it reviewed by your supervisor before the bot handles a single real question. The right answer to "could this log be subpoenaed?" is "there's nothing useful in it."
- **Retention:** shortest window that supports the listening tool. Aggregate, then delete raw text.
- **No location capture. No contact storage. No cross-session identity.**
- **WhatsApp metadata is Meta's, not yours** — you cannot make promises about it. Say so plainly in the bot's disclosure.
- **Disclosure in every channel, in the user's language:** it's a bot, here's what it can't do, here's how to reach a human.
- **Translation dignity:** never present machine-translated text as reviewed. If Kreyòl retrieval is weaker, say so in the interface.
- **Publish the refusal boundaries.** A newsroom shipping an AI tool to a vulnerable audience should be able to show its work — that's also a good story about your own project.

---

## Success metrics

Your stated bar is "communities use it and prefer it to browsing the list." Make that measurable:

| Question | Metric |
|---|---|
| Do people use it? | Sessions/week per channel; % returning |
| Do they prefer it? | Chat sessions vs. guide-page pageviews; task completion (did they tap through to a resource?) |
| Is it right? | Eval-set accuracy; citation validity rate; % refused correctly |
| Does it stay alive? | Median corpus staleness over time; dead-link count trend — **both should fall and stay down** |
| Does it help reporters? | Information gaps surfaced → stories commissioned |

The staleness trend is the one that proves you solved the problem that killed documented.info.

---

## Week 1: what to ask Documented for

You assume full access; confirm it, because several items have long lead times and the plan branches on them.

1. **The documented.info Zendesk archive** — tickets *and* content. Highest value, likely hardest to get (IRC partnership, data-sharing agreement). Ask immediately.
2. **WordPress admin + staging** — needed to write back structured fields and regenerate the guide page. Loop in Rainmakers, their dev agency; the site already has custom REST namespaces (`documented/v1`, `docu_article/v1`) so there's an established codebase and conventions to respect.
3. **Meta Business account access** for the existing WhatsApp/Messenger presence.
4. **WeChat account owner** — a 15-minute conversation that will tell you whether Project 4's WeChat leg is possible at all.
5. **Analytics** (they run Parse.ly) — you need traffic data to rank staleness by impact.
6. **An editor as a standing reviewer** for the freshness queue. The tool fails without a named human.

**Everything in Projects 1 and 2 can start today against public APIs** while these conversations happen. Don't block.

---

## Verification

- **Ingest:** row counts match the API's `x-wp-total` headers per category; spot-check 10 articles for clean boilerplate stripping; confirm all four Zendesk locales archived.
- **Freshness:** hand-verify 20 flagged links; deliberately point a test article at a URL you control, change it, confirm the watcher fires.
- **Retrieval:** run `eval/run_eval.py` against the gold set; report hit rate per language separately — a good aggregate number can hide Kreyòl being broken.
- **Answers:** adversarial pass — questions designed to pull the bot into legal advice, into outdated information, and off-corpus. Every refusal boundary gets a test case.
- **WhatsApp:** end-to-end from a real phone in all four languages, text and voice, including a deliberately garbled voice note.
- **Privacy:** submit a question containing a fake name, phone number, and A-number; inspect the stored record and confirm all three are gone.

---

## Honest risks

- **Scope.** Five projects in one semester is aggressive. Projects 1 and 2 are the ones that must land — they're achievable and they solve the problem that actually killed the predecessor. Treat 3–5 as ordered stretch, and cut from the bottom.
- **The Zendesk archive may not be obtainable.** IRC partnership data, possibly with agreements attached. Have the fallback (headings + reporter interviews) ready rather than stalling.
- **WeChat may be flatly infeasible.** Find out in week 1, not week 12.
- **Kreyòl quality will lag.** Measure it, report it, don't paper over it.
- **The real risk isn't technical, it's institutional.** documented.info had a national NGO partner and staff, and still stopped. Ask early who owns this in month 13 — and build so the answer can be "nobody has to do much."

---

## Progress

**Aug 25, 2026 — Project 1 started.**

- `documented-answers/` scaffolded (ingest / freshness / index / answer / eval / channels / listen).
- **documented.info archived.** `ingest/zendesk.py` (stdlib only, no dependencies) pulled all four
  locales off the mothballed Signpost/Zendesk instance before it can be taken down:

  | Locale | Articles | Categories | Sections |
  |---|---|---|---|
  | `en-us` | 129 | 11 | 32 |
  | `es` | 72 | 11 | 19 |
  | `fr` | 77 | 11 | 19 |
  | `fr-ht` | 58 | 11 | 19 |

  336 articles, ~3.3 MB of raw JSON in `data/archives/documented_info/`.

- **Service map data source identified:** the 358 providers are served from **Directus**
  (IRC Signpost infrastructure, `directus-qa-support.azurewebsites.net`), not Zendesk —
  so it needs its own extractor. Not yet captured. *This is the next task and it is still urgent.*

- Incidental finding worth following up: the Signpost bundle references an existing AI agent
  (`signpost-ia-app-qa.azurewebsites.net/agent`, `.../signpostbot`). IRC may already have built
  something adjacent to Project 3. Worth asking about before duplicating effort.
