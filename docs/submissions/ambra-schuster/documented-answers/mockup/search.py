"""
Search over Documented's article sections.

BM25, in memory, no dependencies. The corpus is 43 sections -- a database
would be theatre. The interface is what matters: swap the guts for SQLite
FTS5 or embeddings later and nothing above this file changes.

BM25 (keyword matching) rather than embeddings on purpose. This subject is
dense with names that have to match exactly -- Promise NYC, 3-K, COMPASS,
Head Start, FAFSA, IEP, Section 504, Dial-A-Teacher. Keyword search nails
those; embeddings blur them into "childcare-ish".
"""

import json
import math
import os
import re
import unicodedata
from collections import Counter

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus.json")

K1, B = 1.5, 0.75  # standard BM25 knobs


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
            out.append({
                "score": round(s, 2),
                "fallback_language": fallback,
                "title": c["title"],
                "url": c["url"],
                "lang": c["lang"],
                "last_updated": c["modified"],
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
    lang = "es" if re.search(r"[¿ñáéíóú]", q) else "en"
    for r in idx.search(q, lang=lang):
        flag = "  [EN fallback]" if r["fallback_language"] else ""
        print(f"{r['score']:6.2f}  [{r['lang']}] {r['heading'] or '(intro)'}{flag}")
        print(f"        {r['title'][:70]}  ({r['last_updated']})")
