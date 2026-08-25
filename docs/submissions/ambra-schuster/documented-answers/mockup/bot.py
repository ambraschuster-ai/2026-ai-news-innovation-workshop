"""
The bot: Claude with Documented's articles as its only source of fact.

Shape of a turn:

    user message
      -> guardrails.check()          hard-coded, runs before Claude sees it
      -> Claude, with search as a tool it can reach for (0..N times)
      -> grounding check on the finished answer
      -> reply + the sources it used

Claude decides when and what to search. That is what makes it feel like a
conversation rather than a search box: it can look something up, realise the
answer splits by the child's age, ask, and search again once you answer.

What it can *say* is locked down three ways:
  1. the only article text in its context is what search returned;
  2. the system prompt makes every factual sentence carry its source link;
  3. check_grounding() rejects any link that search did not return.

Layer 3 is the one that cannot be talked around, and it is why the bot is
allowed to sound relaxed. Manner is free; facts are not.
"""

import json
import os
import re

import anthropic

from search import Index
import guardrails

MODEL = "claude-opus-5"
HERE = os.path.dirname(os.path.abspath(__file__))

# Longest article section sent to the model. Documented's college-funding
# article has one 6,000-character section; sending five of those is most of
# the cost of a turn for very little extra answer.
MAX_RESULT_CHARS = 2000

# Turns whose search results are kept in full. Older ones are stubbed out.
# Without this, every turn resends every previous search result and a long
# conversation costs several dollars. The model still has its own earlier
# answers -- which carry the substance and the links -- so it does not lose
# the thread, only the raw material it already used.
KEEP_FULL_RESULTS = 2

RESULTS_PER_SEARCH = 4


KEY_FILE = os.path.join(HERE, ".env")


def load_key():
    """Key from the environment (how the deployed app gets it), or from
    mockup/.env (how it runs on a laptop). Both are gitignored."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key.strip()

    if os.path.exists(KEY_FILE):
        for line in open(KEY_FILE, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Tolerate either a bare key or a NAME=value line, since both are
            # things a person might reasonably write in a file called this.
            if "=" in line and line.split("=", 1)[0].isupper():
                line = line.split("=", 1)[1].strip()
            line = line.strip("'\"")
            if line.startswith("sk-"):
                return line
            if line.startswith("PASTE_"):
                raise SystemExit(
                    f"{KEY_FILE} still has the placeholder in it.\n"
                    "Replace that line with your key and save."
                )

    raise SystemExit(
        "No API key found.\n\n"
        f"Put your key on the first line of:\n  {KEY_FILE}\n\n"
        "It should look like:  sk-ant-api03-...\n"
        "That file is gitignored -- it will not be committed."
    )


SYSTEM = """You are Documented's resource assistant. Documented is a newsroom \
that covers immigration in New York City. You help immigrants in New York find \
the resources Documented has written about.

## Where your facts come from

Everything factual you say must come from the search results in this \
conversation. You have no other knowledge about immigration, benefits, schools, \
or New York. You may know things from training -- do not use them here. If \
search does not turn it up, Documented has not covered it, and the honest \
answer is that you do not have it.

This is not a stylistic preference. People act on these answers, and a \
confident wrong answer about a benefit or a deadline does real harm.

## How to talk

Like a well-informed friend who happens to have read everything Documented \
published. Warm, direct, brief. Not a form, not a brochure, not a search engine.

Ask a follow-up question when -- and only when -- the answer genuinely changes \
depending on the answer. "I have two kids, what about schools?" depends \
enormously on whether they are 3 or 16, so ask. Ask **one** thing, the one that \
matters most, and say why it matters. Do not interrogate.

You may give a useful partial answer and then ask. That is often best: lead \
with what is true regardless ("your kids can enrol whatever your status -- \
that's settled law"), then ask what you need to narrow the rest.

## Rules for every factual answer

- Cite. Put the source link right there in markdown, as [article title](url).
- Prefer short bullets over paragraphs. People are usually on a phone.
- Pass along the specifics the articles give: program names, phone numbers, \
  which website, who qualifies. That is the useful part.
- When Documented points at an outside organisation, that IS the answer. \
  Give the link. Documented's articles are written to point outward.
- Never invent a URL, phone number, program name, dollar amount, or deadline. \
  If it is not in the search results, you do not have it.

## How old the information is -- say it, every time

Every search result carries `last_updated`, `how_old`, and `staleness`. Those \
are worked out for you. Do not do date arithmetic yourself and do not guess \
what today's date is; use the words you are given.

- **Say when it was written, next to the claim.** Not once at the bottom -- \
  next to the thing it supports, so someone skimming a bullet sees it. Give \
  the month and year from `last_updated`: "(Documented, updated Aug 2025)". \
  Use the actual month and year, never the `how_old` phrase in its place -- \
  "updated within the last few weeks" is not a date and a reader cannot check \
  it later. `how_old` is for the warning, not for the citation.
- `staleness: "aging"` -- add a light note that it is worth confirming, e.g. \
  "this is about a year old, so check the amount before you count on it".
- `staleness: "stale"` -- say so plainly and early, in the person's own \
  language: this is about X old, dollar figures, fees, deadlines and \
  eligibility rules in it may well have changed, confirm before acting. Do \
  not bury it after the useful part.
- **Never soften a stale date by leaving it out.** If the only thing \
  Documented has on a subject is three years old, the honest answer is the \
  old information *plus* a clear warning -- not the old information alone, \
  and not silence.
- If different bullets come from articles of different ages, date them \
  separately. One date at the end implies all of it is that fresh.

Programs, dollar amounts and deadlines are exactly what goes out of date. A \
reader acting on a stale benefit amount is the most likely way this bot \
causes real harm, so this rule is not decoration.

## Language

Reply in whatever language the person wrote in.

Search results are tagged with a language. If the only useful result is in a \
different language from the question, use it -- but say so plainly, in their \
language: something like "this is from an article Documented published in \
English". Never pretend a translated answer is a Spanish source.

## When you have nothing

Say so. Offer what is adjacent if there is anything adjacent, and suggest \
Documented's newsroom as the next step. Do not fill the gap from your own \
knowledge, and do not pad."""


SEARCH_TOOL = {
    "name": "search_documented",
    "description": (
        "Search Documented's published articles. Returns article sections with "
        "their text, source link, last-updated date, how old that is in plain "
        "words, a staleness label, and any outside organisations they link "
        "to.\n\n"
        "Search more than once when a question has several parts -- one search "
        "per idea beats one long search. Use the words the articles would use "
        "(program names like Promise NYC, 3-K, COMPASS, Head Start, FAFSA), not "
        "the words the person used, if they differ."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search terms. Keywords, not a sentence.",
            },
            "language": {
                "type": "string",
                "enum": ["en", "es"],
                "description": "Language the person is writing in. Prefers articles in that language.",
            },
        },
        "required": ["query", "language"],
        "additionalProperties": False,
    },
}


class Bot:
    def __init__(self, index=None):
        self.client = anthropic.Anthropic(api_key=load_key())
        # The index is read-only, so one copy is shared across visitors.
        # The history is not, which is why each visitor gets their own Bot.
        self.index = index if index is not None else Index()
        self.corpus_links = self.index.all_links()
        self._corpus_norm = {Bot._norm(u) for u in self.corpus_links}
        self.history = []

    # ---- context and cost ----------------------------------------------

    def _tool_result(self, block_id, hits):
        """Search results as the model sees them -- trimmed, not raw."""
        payload = []
        for h in hits:
            text = h["text"]
            if len(text) > MAX_RESULT_CHARS:
                text = text[:MAX_RESULT_CHARS].rsplit(" ", 1)[0] + " […section continues]"
            payload.append({
                "title": h["title"],
                "url": h["url"],
                "language": h["lang"],
                "last_updated": h["last_updated"],
                # Age is computed here rather than left to the model. Asking a
                # language model to work out "is 2023-08-30 more than a year
                # ago" is asking it to be wrong occasionally, and the whole
                # point of the warning is that it fires every time.
                "how_old": h["age"],
                "staleness": h["staleness"],
                "fallback_language": h["fallback_language"],
                "heading": h["heading"],
                "text": text,
                "links": h["links"],
            })
        return {
            "type": "tool_result",
            "tool_use_id": block_id,
            "content": json.dumps(payload, ensure_ascii=False),
        }

    def _prune(self):
        """Stub out search results from older turns.

        Cost driver: every request resends the whole conversation. Search
        results are ~90% of its weight and the model has already used them.
        Keeping the last few turns intact preserves follow-up questions like
        "what about the older one" while dropping the dead weight.
        """
        turns_seen = 0
        for msg in reversed(self.history):
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            blocks = [b for b in content if isinstance(b, dict) and b.get("type") == "tool_result"]
            if not blocks:
                continue
            turns_seen += 1
            if turns_seen <= KEEP_FULL_RESULTS:
                continue
            for b in blocks:
                if b["content"] != "[earlier search results omitted to save context]":
                    b["content"] = "[earlier search results omitted to save context]"

    def _messages(self):
        """History with a cache breakpoint on the last message.

        Everything before that point is billed at the cached rate on the next
        turn, which is roughly a tenth of the price.
        """
        self._prune()
        msgs = list(self.history)
        last = msgs[-1]
        content = last["content"]
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        else:
            content = [dict(b) if isinstance(b, dict) else b for b in content]
        if content and isinstance(content[-1], dict):
            content[-1] = {**content[-1], "cache_control": {"type": "ephemeral"}}
            msgs[-1] = {**last, "content": content}
        return msgs

    # ---- grounding -----------------------------------------------------

    @staticmethod
    def _norm(url):
        """Compare links by host+path, ignoring tracking junk.

        Documented's articles carry links with long advertising query strings
        (`?s_kwcid=...&gclid=...`). The model sensibly strips those when it
        cites them. Comparing raw strings flags that as an invented link,
        which is a false alarm -- same page, tidier URL.
        """
        u = url.split("#")[0].split("?")[0].rstrip("/").lower()
        return u.replace("https://", "").replace("http://", "").replace("www.", "")

    # Documented's own homepage. The system prompt tells the bot to point
    # people at the newsroom when the articles come up short, so it needs a
    # link to point with. Deliberately just the root -- an invented
    # documentedny.com/some/article path still gets flagged.
    ALWAYS_ALLOWED = {"documentedny.com"}

    def check_grounding(self, text, retrieved):
        """Every link in the answer must be one search actually returned.

        Catches the failure that matters most: a plausible-looking URL the
        model produced from memory rather than from Documented's article.
        """
        allowed = set(self.ALWAYS_ALLOWED)
        for r in retrieved:
            allowed.add(self._norm(r["url"]))
            allowed.update(self._norm(l) for l in r["links"])

        invented = []
        for url in re.findall(r"\]\((https?://[^\s)]+)\)", text):
            n = self._norm(url)
            if n in allowed:
                continue
            # A link that exists in the corpus but wasn't in *these* results is
            # not an invention -- it's real Documented material.
            if n in self._corpus_norm:
                continue
            invented.append(url)
        return invented

    # ---- one turn ------------------------------------------------------

    def ask(self, message, on_search=None):
        """Run one user turn. Returns (reply_text, sources, notes)."""
        notes = []

        blocked = guardrails.check(message)
        if blocked:
            self.history.append({"role": "user", "content": message})
            self.history.append({"role": "assistant", "content": blocked["reply"]})
            return blocked["reply"], [], [f"guardrail: {blocked['rule']}"]

        self.history.append({"role": "user", "content": message})
        retrieved = []

        while True:
            resp = self.client.messages.create(
                model=MODEL,
                max_tokens=4000,
                system=[{
                    "type": "text",
                    "text": SYSTEM,
                    # Frozen prefix -- cached across every turn and every user.
                    "cache_control": {"type": "ephemeral"},
                }],
                tools=[SEARCH_TOOL],
                messages=self._messages(),
            )
            self.history.append({"role": "assistant", "content": resp.content})

            if resp.stop_reason != "tool_use":
                break

            results = []
            for block in resp.content:
                if block.type != "tool_use":
                    continue
                q = block.input.get("query", "")
                lang = block.input.get("language", "en")
                hits = self.index.search(q, lang=lang, k=RESULTS_PER_SEARCH)
                retrieved.extend(hits)
                if on_search:
                    on_search(q, len(hits))
                results.append(self._tool_result(block.id, hits))
            self.history.append({"role": "user", "content": results})

        reply = "".join(b.text for b in resp.content if b.type == "text")

        invented = self.check_grounding(reply, retrieved)
        if invented:
            notes.append("links not found in Documented's articles: " + ", ".join(invented))

        # Sources actually cited, in the order they appear in the reply.
        cited = []
        seen = set()
        for url in re.findall(r"\]\((https?://[^\s)]+)\)", reply):
            for r in retrieved:
                if r["url"] == url and url not in seen:
                    seen.add(url)
                    cited.append({
                        "title": r["title"],
                        "url": url,
                        "last_updated": r["last_updated"],
                        "age": r["age"],
                        "staleness": r["staleness"],
                        "lang": r["lang"],
                    })
        return reply, cited, notes


    # ---- one turn, streamed --------------------------------------------

    def ask_stream(self, message):
        """Same turn as ask(), yielding events as they happen.

        Events: ('guardrail', rule) ('search', query) ('text', delta)
                ('done', {sources, notes})
        """
        blocked = guardrails.check(message)
        if blocked:
            self.history.append({"role": "user", "content": message})
            self.history.append({"role": "assistant", "content": blocked["reply"]})
            yield ("guardrail", blocked["rule"])
            yield ("text", blocked["reply"])
            yield ("done", {"sources": [], "notes": [f"guardrail: {blocked['rule']}"]})
            return

        self.history.append({"role": "user", "content": message})
        retrieved = []
        reply = ""

        while True:
            with self.client.messages.stream(
                model=MODEL,
                max_tokens=4000,
                system=[{
                    "type": "text",
                    "text": SYSTEM,
                    "cache_control": {"type": "ephemeral"},
                }],
                tools=[SEARCH_TOOL],
                messages=self._messages(),
            ) as stream:
                for event in stream.text_stream:
                    reply += event
                    yield ("text", event)
                resp = stream.get_final_message()

            self.history.append({"role": "assistant", "content": resp.content})
            if resp.stop_reason != "tool_use":
                break

            results = []
            for block in resp.content:
                if block.type != "tool_use":
                    continue
                q = block.input.get("query", "")
                hits = self.index.search(
                    q, lang=block.input.get("language", "en"), k=RESULTS_PER_SEARCH
                )
                retrieved.extend(hits)
                yield ("search", q)
                results.append(self._tool_result(block.id, hits))
            self.history.append({"role": "user", "content": results})

        notes = []
        invented = self.check_grounding(reply, retrieved)
        if invented:
            notes.append("links not found in Documented's articles: " + ", ".join(invented))

        cited, seen = [], set()
        for url in re.findall(r"\]\((https?://[^\s)]+)\)", reply):
            for r in retrieved:
                if r["url"] == url and url not in seen:
                    seen.add(url)
                    cited.append({
                        "title": r["title"],
                        "url": url,
                        "last_updated": r["last_updated"],
                        "age": r["age"],
                        "staleness": r["staleness"],
                        "lang": r["lang"],
                    })
        yield ("done", {"sources": cited, "notes": notes})


if __name__ == "__main__":
    import sys

    bot = Bot()
    print("Documented resource assistant. Ctrl-C to quit.\n")
    for line in sys.stdin if not sys.stdin.isatty() else iter(lambda: input("you> "), ""):
        line = line.strip()
        if not line:
            continue
        print()
        reply, sources, notes = bot.ask(
            line, on_search=lambda q, n: print(f"   [searched: {q!r} -> {n} results]")
        )
        print("\nbot>", reply)
        if sources:
            print("\n  sources:")
            for s in sources:
                print(f"    - {s['title']} ({s['lang']}, updated {s['last_updated']})")
        for n in notes:
            print(f"  ! {n}")
        print()
