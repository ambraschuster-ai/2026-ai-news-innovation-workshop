# Project 1 — Archive & Audit · architecture

> How this gets built and what it has to work with or around.
> Companion files: [requirements.md](requirements.md), [tasks.md](tasks.md).

## The approach in one line

Pull everything down over public APIs into flat JSON, load that into a
single SQLite file, and run every audit as a query against that file — so
the slow network work happens once and the analysis can be rerun freely.

## Why it's shaped this way

Three constraints drove every choice below:

1. **documented.info could vanish.** Capture is urgent and irreversible if
   missed, so capture is separated from everything else and runs first,
   writing raw untouched JSON. Parsing decisions can be revisited later;
   a deleted website cannot.
2. **This has to still run in a year with nobody maintaining it.** The
   predecessor project died of upkeep. Fewer moving parts, fewer
   dependencies, no running services.
3. **Network calls are slow; analysis isn't.** Checking thousands of links
   takes real time. Doing it once and storing results means the audit can
   be re-cut a dozen different ways without hitting the network again.

## The pieces

```
  documentedny.com                documented.info
  WordPress REST API              Zendesk API + Directus
        │                                │
        ├──── ingest/wordpress.py        ├──── ingest/zendesk.py      [DONE]
        │                                └──── ingest/service_map.py  [TODO]
        │                                            │
        │                                            ↓
        │                              data/archives/  (raw JSON, never edited,
        │                                               committed to git)
        ↓
  ingest/normalize.py  ── strips ads/CTAs, extracts links, tags language
        │
        ↓
  data/corpus.db  (SQLite)
        │
        ├──── freshness/linkcheck.py  ── every external link, classified
        ├──── audit/staleness.py      ── age distribution by category
        └──── audit/translations.py   ── EN → ES/ZH/HT coverage matrix
                        │
                        ↓
              audit/report.py ──→ docs/audit-2026-09.md
                                  (the newsroom deliverable)
```

Each arrow is a separate command that can be run on its own. Nothing is a
long-lived service. Nothing runs on a schedule yet — that's Project 2.

## Decisions made, and what would change them

### SQLite, not Postgres

`data/corpus.db` is a single file in the project folder. Python has SQLite
built in, so there is nothing to install and nothing to keep running. At
~5,000 articles this is not close to a scale where it struggles, and its
built-in full-text search (FTS5) covers the keyword-search half of what
Project 3 will need.

*What would change this:* a hosted chat widget with many people writing at
once, or wanting to keep embeddings in the same database as the text.
Neither is true until Project 3 ships something public. Revisit then, not
before.

### Raw JSON archives get committed to git

Unusual for data files, deliberate here. These are small (~3 MB), they are
the only copy of a site that may be deleted, and git gives them versioning
and offsite backup for free. `data/corpus.db` is *derived* from them and
does **not** get committed — it can always be rebuilt.

### Standard library only, as far as it goes

`ingest/zendesk.py` already works with zero installed packages. Project 1
holds that line where it's free. Two places where it likely can't:

- **HTML parsing** for boilerplate stripping. Try stdlib `html.parser`
  first; reach for a real parser only if the ad and CTA blocks turn out to
  be irregular.
- **Concurrent link checking.** Thousands of HTTP requests one at a time is
  too slow to iterate on. Stdlib `concurrent.futures` handles this without
  a new dependency.

Any dependency that does get added is recorded in a `requirements.txt` with
a one-line note on why.

### Everything derived is rebuildable

No step edits its own input. `normalize.py` reads archives and writes the
database; it never modifies the archives. Deleting `data/corpus.db` and
rebuilding must produce the same result. This is what makes it safe to
change the parsing rules later after finding a class of article that
doesn't strip cleanly.

## What already exists and has to be worked with

### Already built here

- **`ingest/zendesk.py`** — done and run. Walks the Zendesk Guide API with
  backoff and pagination, dumps articles, categories, and sections per
  locale. **336 articles across `en-us`, `es`, `fr`, `fr-ht`** now sit in
  `data/archives/documented_info/`, with `_manifest.json` recording counts.
  Its retry/pagination/politeness logic is the pattern the WordPress
  ingester should copy rather than reinvent.
- **Scaffolded but empty:** `ingest/`, `freshness/`, `index/`, `answer/`,
  `eval/`, `channels/`, `listen/`, `docs/`, `data/`. Project 1 fills the
  first two plus a new `audit/`.

### External systems, and their quirks

| System | What it gives | What to work around |
|---|---|---|
| **documentedny.com WordPress REST API** | 4,606 posts with full content, `modified` timestamps, categories, Yoast metadata. Fully open, no auth. | Paginated, capped at 100/page. `content.rendered` includes `googletag` ad blocks and newsletter CTAs in every post. Total counts come from the `x-wp-total` response header — that's how completeness gets verified. |
| **documentedny.com categories** | `resources` (256), `recursos-espanol` (224), `chinese-language-resources` (216), `kreyol-resous` (150), `glossary` (134) | The four languages are **separate categories with no translation linkage**. Nothing in the data says "this is the Spanish version of that." The coverage matrix has to infer it. |
| **documented.info / Zendesk** | 129 EN articles + translations, categories, sections | Unmaintained since June 30, 2026. Could disappear without warning. Uses `fr-ht` for Haitian Creole, not `ht`. |
| **documented.info service map** | 358 providers, structured, filterable | **Not in Zendesk.** Rendered client-side from Directus (`directus-qa-support.azurewebsites.net`, IRC Signpost infrastructure). Needs its own extractor. Still uncaptured — the highest-risk open item in this project. |
| **The public guide page** | — | `/2020/06/11/immigrant-resources-new-york/` is nearly empty. The real categorized list is in the site's nav mega-menu, not the post body. Don't treat the post as the corpus. |

### Things that shape the audit, not the code

- Documented's articles are **prose explainers that point outward** — they
  link to `uscis.gov`, `nyc.gov`, and nonprofit sites rather than
  containing directories. So outbound links aren't incidental; they're the
  substance. A dead link is closer to a broken article than to a typo.
- Article H2/H3 headings are already written as questions ("What is Advance
  Parole?", "Who is eligible?"). Project 1 doesn't use this, but
  `normalize.py` should **preserve heading structure** in the stored text,
  because Project 3 will chunk on it. Cheap now, expensive to redo.
- **Rainmakers** is Documented's dev agency, and the site already has
  custom REST namespaces (`documented/v1`, `docu_article/v1`). There are
  existing conventions to respect if anything is ever written back — but
  Project 1 never writes back.
- The Signpost bundle references an existing IRC AI agent
  (`signpost-ia-app-qa.azurewebsites.net`). Worth asking about before
  Project 3 duplicates work that already exists.

## Known risks in this project

- **The service map extraction may be harder than the Zendesk pull.**
  Directus endpoints for a QA instance may be locked down or may change.
  Fallback: capture the rendered provider list from the page itself. Worse
  data, but better than none. Time-box it and take the fallback rather than
  losing the data to a takedown.
- **Boilerplate stripping is where silent corruption happens.** A rule that
  removes slightly too much loses real article text without any error. This
  is why hand-checking articles is a task, not an optional nicety.
- **Translation matching is a guess.** Matching by slug, by publication
  date, or by internal cross-links each fails differently. The matrix
  should carry a confidence level per match rather than pretending to be
  exact.
