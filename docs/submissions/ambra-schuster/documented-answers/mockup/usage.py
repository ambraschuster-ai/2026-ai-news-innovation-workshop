"""
What this has actually cost, in tokens and dollars.

Separate from the rate limiting in serve.py on purpose, because the two jobs
are different. The daily counter exists to *stop* spending and has to be
cheap and fail-closed. This exists to *report* spending and is allowed to be
approximate -- if a write fails, the app keeps answering.

What is recorded: counts, tokens, cost, per day. What is not recorded: who
asked, what they asked, or anything that could identify a person. The same
rule as everywhere else in this project -- questions typed into an
immigration bot are not a record that should exist.

Two honest limits on the numbers here:

  1. The prices below are hard-coded. If Anthropic changes them, this keeps
     reporting the old ones and nothing will complain. Check them against
     the Console occasionally.
  2. On a free host the disk is wiped when the service redeploys, so history
     starts over. The Console's billing page is the real record; this is a
     dashboard for the afternoon, not an accounting system.
"""

import json
import os
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FILE = os.environ.get("USAGE_FILE", os.path.join(HERE, ".usage.json"))

# Opus 5, dollars per million tokens. Checked against the Console pricing
# page 25 Aug 2026. Cached reads are the reason a long conversation costs
# far less than its length suggests -- roughly a tenth of the input rate.
PRICES = {
    "claude-opus-5": {"input": 5.0, "output": 25.0, "cache_write": 6.25, "cache_read": 0.50},
}
DEFAULT_PRICE = PRICES["claude-opus-5"]

KEEP_DAYS = 30

_lock = threading.Lock()


def _today():
    return time.strftime("%Y-%m-%d", time.gmtime())


def _blank(date):
    return {
        "date": date, "questions": 0, "restatements": 0, "api_calls": 0,
        "input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "cost": 0.0,
    }


def _load():
    try:
        with open(FILE, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except (OSError, ValueError):
        pass
    return {}


def _save(data):
    try:
        # Keep the file from growing without bound, and from carrying a
        # longer history than anyone needs.
        for date in sorted(data)[:-KEEP_DAYS]:
            del data[date]
        tmp = FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f)
        os.replace(tmp, FILE)
    except OSError:
        pass  # reporting must never be the thing that takes the app down


def price_of(model, u):
    """Dollars for one API response's usage object."""
    p = PRICES.get(model, DEFAULT_PRICE)
    return (
        getattr(u, "input_tokens", 0) * p["input"]
        + getattr(u, "output_tokens", 0) * p["output"]
        + (getattr(u, "cache_creation_input_tokens", 0) or 0) * p["cache_write"]
        + (getattr(u, "cache_read_input_tokens", 0) or 0) * p["cache_read"]
    ) / 1e6


def record(model, u, kind):
    """Add one API response. `kind` is 'question' or 'restatement'.

    Called once per API call, which is more than once per question when the
    model searches -- api_calls is deliberately tracked separately from
    questions so the difference is visible.
    """
    if u is None:
        return
    with _lock:
        data = _load()
        day = data.setdefault(_today(), _blank(_today()))
        day["api_calls"] += 1
        day["input"] += getattr(u, "input_tokens", 0)
        day["output"] += getattr(u, "output_tokens", 0)
        day["cache_write"] += getattr(u, "cache_creation_input_tokens", 0) or 0
        day["cache_read"] += getattr(u, "cache_read_input_tokens", 0) or 0
        day["cost"] = round(day["cost"] + price_of(model, u), 6)
        _save(data)


def count(kind):
    """Note that a question or a restatement began, whatever it went on to cost."""
    with _lock:
        data = _load()
        day = data.setdefault(_today(), _blank(_today()))
        key = "questions" if kind == "question" else "restatements"
        day[key] += 1
        _save(data)


def report(days=14):
    """Recent days, newest first, plus a total."""
    data = _load()
    rows = [data[d] for d in sorted(data, reverse=True)[:days]]
    total = _blank("total")
    for r in rows:
        for k in ("questions", "restatements", "api_calls",
                  "input", "output", "cache_write", "cache_read"):
            total[k] += r.get(k, 0)
        total["cost"] += r.get("cost", 0.0)
    total["cost"] = round(total["cost"], 4)
    return rows, total
