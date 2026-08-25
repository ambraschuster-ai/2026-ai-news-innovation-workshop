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

import json
import os
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from bot import Bot
from search import Index

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8080))
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "chat.html")

# --- spend guards -------------------------------------------------------
# Tuned so the worst realistic day costs about the price of a sandwich.
MAX_PER_SESSION = int(os.environ.get("MAX_PER_SESSION", 15))
MAX_PER_DAY = int(os.environ.get("MAX_PER_DAY", 150))
SESSION_TTL = 60 * 60  # an hour of inactivity and the conversation is dropped

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


def take_turn_budget(sid):
    """Claim one message. Returns (ok, reason). Fails closed."""
    with _lock:
        _reap()
        if _day["date"] != _today():
            _day.update(date=_today(), count=0)
        if _day["count"] >= MAX_PER_DAY:
            return False, "daily"

        s = _sessions.get(sid)
        if s is None:
            s = _sessions[sid] = {"bot": Bot(index=INDEX), "count": 0, "seen": time.time()}
        if s["count"] >= MAX_PER_SESSION:
            return False, "session"

        s["count"] += 1
        s["seen"] = time.time()
        _day["count"] += 1
        _save_day(_day)
        return True, None


SESSION_FULL = """You've reached this demo's limit of {n} messages — it's a \
student prototype running on a small budget, not a real service.

**Click "New conversation"** at the top to start fresh.

And a reminder: for anything that actually matters, call **311** and ask for \
**ActionNYC** — free immigration legal help, in your language."""

DAY_FULL = """This demo has hit its limit for today. It's a student prototype \
with a fixed daily budget, and enough people have used it that the budget is \
spent.

Try again tomorrow. For anything urgent, call **311** and ask for **ActionNYC** \
— free immigration legal help, in your language."""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # -- helpers --
    def _sid(self):
        cookie = self.headers.get("Cookie", "")
        for part in cookie.split(";"):
            k, _, v = part.strip().partition("=")
            if k == "sid" and v:
                return v, False
        return uuid.uuid4().hex, True

    def _event(self, kind, data):
        chunk = f"data: {json.dumps({'kind': kind, 'data': data})}\n\n".encode("utf-8")
        self.wfile.write(b"%x\r\n" % len(chunk) + chunk + b"\r\n")
        self.wfile.flush()

    # -- routes --
    def do_GET(self):
        if self.path == "/healthz":
            body = b'{"ok":true}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        with open(PAGE, "rb") as f:
            page = f.read()
        sid, fresh = self._sid()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        if fresh:
            self.send_header(
                "Set-Cookie", f"sid={sid}; Path=/; Max-Age=3600; SameSite=Lax; HttpOnly"
            )
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
        sid, _ = self._sid()

        if self.path == "/reset":
            with _lock:
                _sessions.pop(sid, None)
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

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
                for kind, data in bot.ask_stream(payload.get("message", "")):
                    self._event(kind, data)
            except Exception as e:  # noqa: BLE001 -- show it, don't 500 into a blank page
                self._event("error", type(e).__name__ + ": " + str(e)[:200])

        self.wfile.write(b"0\r\n\r\n")
        self.wfile.flush()

    def log_message(self, *a):
        pass  # deliberately no request log -- see the module docstring


if __name__ == "__main__":
    print(f"Documented resource assistant on port {PORT}")
    print(f"{INDEX.n} article sections loaded")
    print(f"limits: {MAX_PER_SESSION}/session, {MAX_PER_DAY}/day")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
