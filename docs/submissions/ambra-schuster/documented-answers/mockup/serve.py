"""
The chat window, and the thing that gets deployed.

    python3 mockup/serve.py            # local, http://127.0.0.1:8080
    PORT=10000 python3 mockup/serve.py # what the host runs

Three things this has to get right that the local-only version did not:

1. **One conversation per visitor.** Sessions are keyed by a cookie. The
   earlier version had a single shared history, so two people using it at
   once would have read each other's messages.

2. **Spend guards.** A public link with an API key behind it is a bill
   waiting to happen. Two ceilings, both hard, both fail closed.

3. **Nothing is written down.** Conversations live in memory and die with
   the process. No database, no logs of what anyone asked. That is not
   laziness -- questions to an immigration bot are exactly the kind of
   record that should not exist (see Project 5).
"""

import hashlib
import hmac
import html
import json
import os
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from bot import Bot, LANGUAGES
from search import Index
import usage

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8080))
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "chat.html")

# --- spend guards -------------------------------------------------------
# Tuned so the worst realistic day costs about the price of a sandwich.
MAX_PER_SESSION = int(os.environ.get("MAX_PER_SESSION", 15))
MAX_PER_DAY = int(os.environ.get("MAX_PER_DAY", 150))
SESSION_TTL = 60 * 60  # an hour of inactivity and the conversation is dropped

# Language buttons get their own allowance rather than eating the message
# budget. Four buttons under every answer means a curious visitor could burn
# a fifteen-message session on translations without ever asking a second
# question -- which would be a bad demo and an unfair limit. They are cheaper
# than questions too: one call, no search, and a repeat click is served from
# memory for nothing.
MAX_RESTATE_PER_SESSION = int(os.environ.get("MAX_RESTATE_PER_SESSION", 24))

# Counting messages is not the same as capping spend. A message is charged by
# its length, so 150 messages a day is only a budget if a message has a size.
# Someone pasting a novel into the box -- or a script doing it 150 times --
# would otherwise run up a bill the daily counter would report as a quiet,
# well-behaved day. 4,000 characters is far more than anyone types and far
# less than anyone can do damage with.
MAX_MESSAGE_CHARS = int(os.environ.get("MAX_MESSAGE_CHARS", 4000))

# Nor is the body of a request the same as the message in it. Content-Length
# is a number the client picks, and rfile.read() will sit there waiting for
# as much of it as it is told to.
MAX_BODY_BYTES = 64 * 1024

# Sessions are keyed by a cookie the visitor supplies, so the number of them
# is also something the visitor controls. The daily ceiling still holds --
# a new cookie buys new messages but not new budget -- so this is about
# memory, not money.
MAX_SESSIONS = 500

# --- who is allowed in ---------------------------------------------------
#
# Set ACCESS_CODE and the whole thing is closed: no page, no API, nothing
# until a visitor proves they know the code. Leave it unset and it is open,
# which is right on a laptop and wrong on the public internet.
#
# This is a shared passphrase, not accounts. Everyone who has the link has
# the same code, anyone can pass it on, and it is only as private as the
# people you send it to. What it does buy is the thing that matters here:
# a stranger who finds the URL cannot spend the API key behind it.
#
# The cookie holds an HMAC of a fixed string keyed by the code itself.
# Knowing the code lets you compute it -- which is the point -- and not
# knowing it makes the cookie unforgeable. The code is never in the cookie.
ACCESS_CODE = os.environ.get("ACCESS_CODE", "").strip()
GATE_TTL = 60 * 60 * 24 * 30  # a month, so classmates type it once


def gate_token(code):
    return hmac.new(code.encode("utf-8"), b"documented-gate-v1", hashlib.sha256).hexdigest()


EXPECTED_TOKEN = gate_token(ACCESS_CODE) if ACCESS_CODE else ""

_lock = threading.Lock()
_sessions = {}       # sid -> {"bot": Bot, "count": int, "seen": float}

# The daily counter is written to disk so it survives the process restarting.
# It has to: on a free host the app sleeps when idle, and an in-memory counter
# would reset to zero every time it woke up -- which is not a daily ceiling at
# all, it is a ceiling per nap.
#
# Still not bulletproof: a host that wipes its disk on restart resets this too.
# The spend cap in the Anthropic Console is the only limit that cannot be
# reset by anything happening on this server. Set it. See DEPLOY.md.
COUNTER = os.environ.get("COUNTER_FILE", os.path.join(HERE, ".daily-count"))

INDEX = Index()      # loaded once, shared -- read-only, so sharing is fine


def _today():
    return time.strftime("%Y-%m-%d", time.gmtime())


def _load_day():
    try:
        with open(COUNTER, encoding="utf-8") as f:
            d = json.load(f)
        if d.get("date") == _today():
            return d
    except (OSError, ValueError):
        pass
    return {"date": _today(), "count": 0}


def _save_day(day):
    try:
        with open(COUNTER, "w", encoding="utf-8") as f:
            json.dump(day, f)
    except OSError:
        pass  # a read-only disk is not a reason to take the app down


_day = _load_day()


def _reap():
    """Drop idle conversations. Keeps memory flat and shortens what exists."""
    cutoff = time.time() - SESSION_TTL
    for sid in [s for s, v in _sessions.items() if v["seen"] < cutoff]:
        del _sessions[sid]

    # If something is minting cookies faster than they expire, drop the
    # oldest rather than growing without limit. The evicted visitor loses
    # their conversation, which is a worse experience than the alternative
    # of the whole thing falling over.
    if len(_sessions) > MAX_SESSIONS:
        oldest = sorted(_sessions, key=lambda s: _sessions[s]["seen"])
        for sid in oldest[: len(_sessions) - MAX_SESSIONS]:
            del _sessions[sid]


def _session(sid):
    """The visitor's conversation, created on first sight. Caller holds _lock."""
    s = _sessions.get(sid)
    if s is None:
        s = _sessions[sid] = {
            "bot": Bot(index=INDEX), "count": 0, "restated": 0, "seen": time.time(),
        }
    return s


def take_turn_budget(sid):
    """Claim one message. Returns (ok, reason). Fails closed."""
    with _lock:
        _reap()
        if _day["date"] != _today():
            _day.update(date=_today(), count=0)
        if _day["count"] >= MAX_PER_DAY:
            return False, "daily"

        s = _session(sid)
        if s["count"] >= MAX_PER_SESSION:
            return False, "session"

        s["count"] += 1
        s["seen"] = time.time()
        _day["count"] += 1
        _save_day(_day)
    # Outside the lock: this writes a file, and the rate limiter should not
    # wait on the bookkeeping. usage has its own lock, and nothing it holds
    # ever waits on ours, so the two cannot deadlock.
    usage.count("question")
    return True, None


def take_restate_budget(sid, answer_id, target):
    """Claim one language-button press. Returns (ok, reason). Fails closed.

    A press that will be served from the session's cache costs nothing and is
    not charged -- otherwise switching back and forth between two languages
    to compare them, which is the natural thing to do, would be punished.
    """
    with _lock:
        _reap()
        s = _session(sid)
        s["seen"] = time.time()

        try:
            if s["bot"].answers[answer_id]["versions"].get(target):
                return True, None
        except (IndexError, TypeError):
            # An answer id this conversation never issued. Nothing to bill --
            # no API call is coming. restate_stream says so to the visitor.
            return True, None

        if _day["date"] != _today():
            _day.update(date=_today(), count=0)
        if _day["count"] >= MAX_PER_DAY:
            return False, "daily"
        if s["restated"] >= MAX_RESTATE_PER_SESSION:
            return False, "restate"

        s["restated"] += 1
        _day["count"] += 1
        _save_day(_day)
    usage.count("restatement")
    return True, None


SESSION_FULL = """You've reached this demo's limit of {n} messages — it's a \
student prototype running on a small budget, not a real service.

**Click "New conversation"** at the top to start fresh.

And a reminder: for anything that actually matters, call **311** and ask for \
**ActionNYC** — free immigration legal help, in your language."""

RESTATE_FULL = """You've switched languages as many times as this demo \
allows in one conversation.

**Click "New conversation"** at the top to start fresh — the answers you \
already have stay readable in whichever language you last picked."""

DAY_FULL = """This demo has hit its limit for today. It's a student prototype \
with a fixed daily budget, and enough people have used it that the budget is \
spent.

Try again tomorrow. For anything urgent, call **311** and ask for **ActionNYC** \
— free immigration legal help, in your language."""


SHELL = """<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
 :root {{ --bg:#fbfaf8; --panel:#fff; --ink:#1a1a1a; --muted:#6b6b6b;
          --line:#e5e2dc; --accent:#b03a2e; --chip:#f3f1ec; }}
 @media (prefers-color-scheme:dark) {{ :root {{ --bg:#16161a; --panel:#1e1e23;
   --ink:#ececec; --muted:#9a9a9a; --line:#33333a; --accent:#e8735f; --chip:#26262c; }} }}
 *{{box-sizing:border-box}}
 body {{ margin:0; background:var(--bg); color:var(--ink); padding:2rem 1.25rem;
   font:16px/1.6 ui-sans-serif,system-ui,-apple-system,sans-serif; }}
 .wrap {{ max-width:44rem; margin:0 auto; }}
 h1 {{ font-size:1.15rem; margin:0 0 .3rem; }}
 p {{ color:var(--muted); font-size:.9rem; }}
 input {{ font:inherit; padding:.6rem .8rem; border-radius:10px; width:100%;
   border:1px solid var(--line); background:var(--panel); color:var(--ink); }}
 button {{ background:var(--accent); color:#fff; border:0; border-radius:10px;
   padding:.6rem 1.4rem; font:inherit; cursor:pointer; margin-top:.7rem; }}
 table {{ border-collapse:collapse; width:100%; font-size:.85rem; margin-top:1rem; }}
 th,td {{ text-align:right; padding:.4rem .5rem; border-bottom:1px solid var(--line); }}
 th:first-child,td:first-child {{ text-align:left; }}
 th {{ color:var(--muted); font-weight:600; font-size:.75rem;
   text-transform:uppercase; letter-spacing:.05em; }}
 tr.total td {{ font-weight:700; border-top:2px solid var(--line); border-bottom:0; }}
 .note {{ background:var(--chip); border:1px solid var(--line); border-radius:10px;
   padding:.8rem 1rem; font-size:.8rem; color:var(--muted); margin-top:1.5rem; }}
 .big {{ font-size:2rem; font-weight:700; color:var(--ink); }}
 .err {{ color:var(--accent); font-size:.85rem; }}
</style>
<div class="wrap">{body}</div>"""

GATE_PAGE = SHELL.format(title="Documented — enter code", body="""
 <h1>This is a private prototype.</h1>
 <p>Enter the code you were given.</p>
 <form onsubmit="go(event)">
   <input id="c" type="password" autofocus placeholder="Code" autocomplete="off">
   <button>Enter</button>
   <div class="err" id="e"></div>
 </form>
 <script>
 async function go(e) {
   e.preventDefault();
   const r = await fetch('/unlock', { method:'POST',
     headers:{'content-type':'application/json'},
     body: JSON.stringify({ code: document.getElementById('c').value }) });
   if ((await r.json()).ok) location.href = '/';
   else document.getElementById('e').textContent = 'That code is not right.';
 }
 </script>""")


def stats_page():
    """What this has cost. Reachable only behind the access code."""
    rows, total = usage.report(days=14)
    today = rows[0] if rows and rows[0]["date"] == time.strftime("%Y-%m-%d", time.gmtime()) \
        else usage._blank("today")

    def tr(r, cls=""):
        return (
            f'<tr class="{cls}"><td>{html.escape(str(r["date"]))}</td>'
            f'<td>{r["questions"]}</td><td>{r["restatements"]}</td>'
            f'<td>{r["api_calls"]}</td>'
            f'<td>{r["input"] + r["cache_write"] + r["cache_read"]:,}</td>'
            f'<td>{r["output"]:,}</td>'
            f'<td>${r["cost"]:.2f}</td></tr>'
        )

    with _lock:
        live = len(_sessions)
        used_today = _day["count"]

    body = f"""
 <h1>Usage</h1>
 <p>Today, {html.escape(_today())} UTC</p>
 <div class="big">${today['cost']:.2f}</div>
 <p>{today['questions']} questions · {today['restatements']} language switches ·
    {used_today} of {MAX_PER_DAY} against today's limit · {live} live conversations</p>
 <table>
  <tr><th>Day</th><th>Questions</th><th>Switches</th><th>API calls</th>
      <th>In</th><th>Out</th><th>Cost</th></tr>
  {''.join(tr(r) for r in rows) or '<tr><td colspan="7">Nothing yet.</td></tr>'}
  {tr(total, "total")}
 </table>
 <div class="note">
  <p><b>These are estimates, and they are not the bill.</b> Prices are written
  into <code>usage.py</code> by hand, so if Anthropic changes them this page
  keeps quoting the old ones. The Anthropic Console's billing page is the
  real number — and your spend cap there is the real limit.</p>
  <p>History resets when the service redeploys or restarts, because a free
  host has no permanent disk. Nothing here records who asked what; only
  counts and tokens are kept.</p>
 </div>"""
    return SHELL.format(title="Usage", body=body)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # -- helpers --
    def _sid(self):
        """The visitor's session id, from their cookie or newly minted.

        The cookie is whatever the client sends, so it is checked against the
        shape we issue rather than trusted. Anything else gets a fresh id --
        which costs the sender nothing and costs us nothing either.
        """
        cookie = self.headers.get("Cookie", "")
        for part in cookie.split(";"):
            k, _, v = part.strip().partition("=")
            if k == "sid" and len(v) == 32 and all(c in "0123456789abcdef" for c in v):
                return v, False
        return uuid.uuid4().hex, True

    def _body(self):
        """The request body, or None if it is malformed or oversized."""
        try:
            n = int(self.headers.get("Content-Length", 0))
        except ValueError:
            return None
        if n <= 0 or n > MAX_BODY_BYTES:
            return None if n > MAX_BODY_BYTES else {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None

    def _cookie(self, name):
        for part in self.headers.get("Cookie", "").split(";"):
            k, _, v = part.strip().partition("=")
            if k == name:
                return v
        return ""

    def unlocked(self):
        """Has this visitor proved they know the code? Open if none is set."""
        if not ACCESS_CODE:
            return True
        return hmac.compare_digest(self._cookie("gate"), EXPECTED_TOKEN)

    def _set_gate_cookie(self):
        self.send_header(
            "Set-Cookie",
            f"gate={EXPECTED_TOKEN}; Path=/; Max-Age={GATE_TTL}; SameSite=Lax; HttpOnly",
        )

    def _plain(self, code, body=b""):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _event(self, kind, data):
        chunk = f"data: {json.dumps({'kind': kind, 'data': data})}\n\n".encode("utf-8")
        self.wfile.write(b"%x\r\n" % len(chunk) + chunk + b"\r\n")
        self.wfile.flush()

    def _html(self, body, extra_cookie=None):
        body = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        # A gated page must not be cached by anything in between.
        self.send_header("Cache-Control", "no-store")
        if extra_cookie:
            extra_cookie()
        self.end_headers()
        self.wfile.write(body)

    # -- routes --
    def do_GET(self):
        path, _, query = self.path.partition("?")

        # Health checks stay open: the host polls this to decide whether the
        # service is alive, and it says nothing except that it is.
        if path == "/healthz":
            body = b'{"ok":true}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # A code in the link, so one URL can be all a classmate needs.
        if ACCESS_CODE and not self.unlocked():
            for pair in query.split("&"):
                k, _, v = pair.partition("=")
                if k == "k" and hmac.compare_digest(gate_token(v), EXPECTED_TOKEN):
                    self.send_response(303)
                    self.send_header("Location", path)
                    self._set_gate_cookie()
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
            self._html(GATE_PAGE)
            return

        if path == "/stats":
            self._html(stats_page())
            return

        with open(PAGE, "rb") as f:
            page = f.read()
        sid, fresh = self._sid()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.send_header("Cache-Control", "no-store")
        if fresh:
            self.send_header(
                "Set-Cookie", f"sid={sid}; Path=/; Max-Age=3600; SameSite=Lax; HttpOnly"
            )
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        payload = self._body()
        if payload is None or not isinstance(payload, dict):
            self._plain(400, b"bad request")
            return

        if self.path == "/unlock":
            given = payload.get("code", "")
            ok = isinstance(given, str) and ACCESS_CODE and hmac.compare_digest(
                gate_token(given.strip()), EXPECTED_TOKEN
            )
            body = b'{"ok":true}' if ok else b'{"ok":false}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            if ok:
                self._set_gate_cookie()
            self.end_headers()
            self.wfile.write(body)
            return

        # Every other POST is the API. Gating the page and leaving this open
        # would protect nothing -- the key is spent here, not there.
        if not self.unlocked():
            self._plain(403, b"forbidden")
            return

        sid, _ = self._sid()

        if self.path == "/reset":
            with _lock:
                _sessions.pop(sid, None)
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        if self.path == "/restate":
            self._restate(sid, payload)
            return

        message = payload.get("message", "")
        if not isinstance(message, str):
            self._plain(400, b"bad request")
            return
        message = message.strip()[:MAX_MESSAGE_CHARS]

        ok, reason = take_turn_budget(sid)

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Transfer-Encoding", "chunked")
        self.end_headers()

        if not ok:
            msg = SESSION_FULL.format(n=MAX_PER_SESSION) if reason == "session" else DAY_FULL
            self._event("limit", reason)
            self._event("text", msg)
            self._event("done", {"sources": [], "notes": []})
        else:
            try:
                bot = _sessions[sid]["bot"]
                for kind, data in bot.ask_stream(message):
                    self._event(kind, data)
            except Exception as e:  # noqa: BLE001 -- show it, don't 500 into a blank page
                self._event("error", type(e).__name__ + ": " + str(e)[:200])

        self._end_stream()

    def _end_stream(self):
        """Close a chunked response, tolerating a reader who has walked away.

        Someone closing the tab mid-answer is normal, not an error, and it
        should not leave a traceback in the log of a server that deliberately
        keeps no log.
        """
        try:
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True

    def _restate(self, sid, payload):
        """A language button. Rewrites an answer already given -- never a new
        one, and never a new search."""
        answer_id = payload.get("id")
        target = payload.get("lang")

        # Check the request is even coherent before charging for it. Taking
        # the budget first meant a request naming a language that does not
        # exist spent a message and then failed -- a free way to drain the
        # daily ceiling without ever getting an answer.
        if target not in LANGUAGES or not isinstance(answer_id, int) or isinstance(answer_id, bool) or answer_id < 0:
            self._plain(400, b"bad request")
            return

        ok, reason = take_restate_budget(sid, answer_id, target)

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Transfer-Encoding", "chunked")
        self.end_headers()

        if not ok:
            self._event("limit", reason)
            self._event("text", RESTATE_FULL if reason == "restate" else DAY_FULL)
            self._event("done", {"sources": [], "notes": []})
        else:
            try:
                bot = _sessions[sid]["bot"]
                for kind, data in bot.restate_stream(answer_id, target):
                    self._event(kind, data)
            except Exception as e:  # noqa: BLE001
                self._event("error", type(e).__name__ + ": " + str(e)[:200])

        self._end_stream()

    def log_message(self, *a):
        pass  # deliberately no request log -- see the module docstring


if __name__ == "__main__":
    print(f"Documented resource assistant on port {PORT}")
    print(f"{INDEX.n} article sections loaded")
    print(f"limits: {MAX_PER_SESSION}/session, {MAX_PER_DAY}/day")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
