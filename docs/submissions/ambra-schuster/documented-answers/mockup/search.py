"""
Search over Documented's article sections.

BM25, in memory, no dependencies. The corpus is 247 sections -- a database
would be theatre. The interface is what matters: swap the guts for SQLite
FTS5 or embeddings later and nothing above this file changes.

BM25 (keyword matching) rather than embeddings on purpose. This subject is
dense with names that have to match exactly -- Promise NYC, 3-K, COMPASS,
Head Start, FAFSA, IEP, Section 504, Dial-A-Teacher. Keyword search nails
those; embeddings blur them into "childcare-ish".
"""

import datetime
import json
import math
import os
import re
import unicodedata
from collections import Counter

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus.json")

K1, B = 1.5, 0.75  # standard BM25 knobs

# How old an article has to be before we say something about it.
#
# These are judgement calls, not science. Six months is roughly how long a
# benefit amount, a fee, or an eligibility rule can sit before it is worth
# double-checking; eighteen months is where "probably still true" stops being
# a safe assumption at all. Documented's own guide has articles on both sides
# of both lines, which is the whole reason this exists -- Project 2 in the
# plan is about fixing the stale ones, and this is about not hiding them in
# the meantime.
AGING_DAYS = 182
STALE_DAYS = 548


def describe_age(modified, today=None):
    """Turn a date string into (age_phrase, staleness) a person can act on.

    Returns e.g. ("2 years and 11 months ago", "stale"). The phrase is what
    goes in front of the reader; the staleness label is what the model is
    told to react to, so the warning does not depend on it doing date
    arithmetic in its head.
    """
    today = today or datetime.date.today()
    try:
        d = datetime.date(*(int(x) for x in modified.split("-")[:3]))
    except (ValueError, TypeError):
        return "date unknown", "unknown"

    days = (today - d).days
    if days < 0:
        return "just published", "fresh"
    if days < 45:
        phrase = "within the last few weeks"
    elif days < 365:
        phrase = f"about {max(1, round(days / 30.4))} months ago"
    else:
        years = days // 365
        months = round((days % 365) / 30.4)
        if months == 12:  # 2 years and 12 months is 3 years
            years, months = years + 1, 0
        phrase = f"about {years} year{'s' if years > 1 else ''}"
        if months:
            phrase += f" and {months} month{'s' if months > 1 else ''}"
        phrase += " ago"

    if days >= STALE_DAYS:
        return phrase, "stale"
    if days >= AGING_DAYS:
        return phrase, "aging"
    return phrase, "fresh"


def tokenize(s):
    """Lowercase, strip accents, split on non-word characters.

    Accent folding matters here: someone types "educacion", the article says
    "educación". Digits are kept -- 3-K and 504 are meaningful.
    """
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", s)


class Index:
    def __init__(self, path=CORPUS):
        with open(path, encoding="utf-8") as f:
            articles = json.load(f)

        self.chunks = []
        for a in articles:
            for i, sec in enumerate(a["sections"]):
                # The heading is weighted by repeating it: Documented writes
                # headings as the questions people ask, so a heading match is
                # a much stronger signal than a body match.
                blob = ((sec["heading"] or "") + " ") * 3 + a["title"] + " " + sec["text"]
                self.chunks.append({
                    "article_id": a["id"],
                    "title": a["title"],
                    "url": a["url"],
                    "lang": a["lang"],
                    "modified": a["modified"],
                    "heading": sec["heading"],
                    "text": sec["text"],
                    "links": sec["links"],
                    "section": i,
                    "_tokens": Counter(tokenize(blob)),
                    "_len": len(tokenize(blob)),
                })

        self.avg_len = sum(c["_len"] for c in self.chunks) / len(self.chunks)
        self.df = Counter()
        for c in self.chunks:
            self.df.update(c["_tokens"].keys())
        self.n = len(self.chunks)

    def _score(self, chunk, terms):
        score = 0.0
        for t in terms:
            tf = chunk["_tokens"].get(t, 0)
            if not tf:
                continue
            idf = math.log(1 + (self.n - self.df[t] + 0.5) / (self.df[t] + 0.5))
            norm = tf * (K1 + 1) / (tf + K1 * (1 - B + B * chunk["_len"] / self.avg_len))
            score += idf * norm
        return score

    def search(self, query, lang=None, k=6):
        """Best k sections. Prefers `lang`, falls back to English and says so.

        The fallback flag is not cosmetic -- the bot has to tell someone
        writing in Spanish when the only source is an English article, rather
        than translating it silently and hoping.
        """
        terms = tokenize(query)
        scored = []
        for c in self.chunks:
            s = self._score(c, terms)
            if s <= 0:
                continue
            fallback = bool(lang) and c["lang"] != lang
            if fallback:
                s *= 0.6  # real, but a worse answer than one in their language
            scored.append((s, fallback, c))

        scored.sort(key=lambda x: -x[0])
        out = []
        for s, fallback, c in scored[:k]:
            age, staleness = describe_age(c["modified"])
            out.append({
                "score": round(s, 2),
                "fallback_language": fallback,
                "title": c["title"],
                "url": c["url"],
                "lang": c["lang"],
                "last_updated": c["modified"],
                "age": age,
                "staleness": staleness,
                "heading": c["heading"],
                "text": c["text"],
                "links": c["links"],
            })
        return out

    def all_links(self):
        """Every URL the corpus contains -- used to verify the bot invented none."""
        urls = {c["url"] for c in self.chunks}
        for c in self.chunks:
            urls.update(c["links"])
        return urls


if __name__ == "__main__":
    import sys

    idx = Index()
    print(f"{idx.n} sections indexed\n")
    q = " ".join(sys.argv[1:]) or "enroll my child in school undocumented"
    # Crude, and only for this command-line view -- the bot itself is told the
    # language outright. Accents alone are not enough: "abogado inmigracion
    # gratis" is unmistakably Spanish and has none, and guessing English there
    # made every Spanish hit print as an "EN fallback", which is a lie.
    ES_WORDS = {
        "de", "que", "como", "donde", "para", "gratis", "el", "la", "los", "las",
        "mi", "mis", "hijo", "hija", "puedo", "necesito", "hay", "un", "una",
        "solicitar", "ayuda", "abogado", "escuela", "salud", "vivienda", "en",
    }
    lang = "es" if re.search(r"[¿ñáéíóú]", q) or (
        ES_WORDS & set(tokenize(q))) else "en"
    for r in idx.search(q, lang=lang):
        flag = "  [EN fallback]" if r["fallback_language"] else ""
        mark = {"stale": "  ** STALE", "aging": "  * aging"}.get(r["staleness"], "")
        print(f"{r['score']:6.2f}  [{r['lang']}] {r['heading'] or '(intro)'}{flag}")
        print(f"        {r['title'][:70]}  ({r['last_updated']}, {r['age']}){mark}")
