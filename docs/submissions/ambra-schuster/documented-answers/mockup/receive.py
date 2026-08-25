"""
One-shot receiver: the browser hands it articles, it writes ONE file.

Why this exists: documentedny.com sits behind Cloudflare, which refuses
requests from scripts -- verified Aug 25 2026, every article URL and the
whole /wp-json/ tree returns 403 to curl and urllib, browser user-agent or
not. A real browser gets through fine. So the browser does the fetching and
this catches what it sends.

It also serves the collector page itself, because Chrome won't let an https
page POST to a local address. Serving from 127.0.0.1 makes that POST
same-origin and the problem disappears.

    python3 mockup/receive.py      # then open http://127.0.0.1:8787/

Writes a single file, not one per article: this is a mockup on a hand-picked
sample, and nobody wants 900 files on their laptop.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST, PORT = "127.0.0.1", 8787
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "collect.html")
OUT = os.path.join(HERE, "corpus.json")


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, ctype):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        with open(PAGE, "rb") as f:
            self._send(f.read(), "text/html; charset=utf-8")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        articles = json.loads(self.rfile.read(n).decode("utf-8"))

        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=1)

        by_lang = {}
        for a in articles:
            by_lang[a["lang"]] = by_lang.get(a["lang"], 0) + 1
        sections = sum(len(a["sections"]) for a in articles)

        self._send(
            json.dumps({"articles": len(articles), "sections": sections, "by_lang": by_lang}).encode(),
            "application/json",
        )
        print(f"  saved {len(articles)} articles / {sections} sections {by_lang}", flush=True)
        print(f"  -> {OUT}", flush=True)
        self.server.done = True

    def log_message(self, *a):
        pass  # do_POST already prints what matters


if __name__ == "__main__":
    srv = HTTPServer((HOST, PORT), Handler)
    srv.done = False
    print(f"Open http://{HOST}:{PORT}/ in the browser to collect.", flush=True)
    while not srv.done:
        srv.handle_request()
    print("Done.")
