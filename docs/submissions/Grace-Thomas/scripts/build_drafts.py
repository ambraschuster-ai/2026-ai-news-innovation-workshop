#!/usr/bin/env python3
"""
Turn a drafts.json (written by Claude) into everything you need to review and send:

  outreach/<slug>/compose.html   one button per contact; opens a pre-filled Gmail draft
  outreach/<slug>/*.eml          same email as a file, for Apple Mail / Outlook
  outreach/<slug>/tracking.csv   who, when, deadline, status
  outreach/<slug>/REVIEW.md      all emails side by side for a fast read-through

Nothing here sends mail. It only writes files.

Usage:
  python3 scripts/build_drafts.py outreach/<slug>/drafts.json
"""

import csv
import html
import json
import os
import re
import sys
from email.message import EmailMessage
from urllib.parse import urlencode

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIG_PATH = os.path.join(ROOT, "config", "signature.txt")
PROFILE_PATH = os.path.join(ROOT, "config", "profile.md")

# Gmail truncates very long compose URLs. Emails past this get a copy-paste block
# in compose.html instead of a dead button.
URL_SAFE_LIMIT = 8000


def die(msg):
    sys.stderr.write("error: %s\n" % msg)
    sys.exit(1)


def read_signature():
    if not os.path.exists(SIG_PATH):
        die("missing %s — add your signature there first" % SIG_PATH)
    with open(SIG_PATH, "r", encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


def read_gmail_account_index():
    """Pull 'Gmail account index' out of profile.md; default 0."""
    if not os.path.exists(PROFILE_PATH):
        return 0
    with open(PROFILE_PATH, "r", encoding="utf-8") as fh:
        m = re.search(r"Gmail account index:\*{0,2}\s*(\d+)", fh.read())
    return int(m.group(1)) if m else 0


def gmail_compose_url(email, account_index):
    """
    Pre-filled Gmail compose window. Gmail inserts YOUR configured signature
    automatically, so the body deliberately omits it — otherwise you'd sign twice.
    """
    params = {
        "view": "cm",
        "fs": "1",
        "tf": "1",
        "to": email.get("to", ""),
        "su": email.get("subject", ""),
        "body": email.get("body", ""),
    }
    if email.get("cc"):
        params["cc"] = email["cc"]
    if email.get("bcc"):
        params["bcc"] = email["bcc"]
    return "https://mail.google.com/mail/u/%d/?%s" % (account_index, urlencode(params))


def write_eml(path, email, signature, from_addr):
    """Standalone .eml — signature IS embedded, since no client will add it here."""
    msg = EmailMessage()
    msg["To"] = email.get("to", "")
    if email.get("cc"):
        msg["Cc"] = email["cc"]
    if from_addr:
        msg["From"] = from_addr
    msg["Subject"] = email.get("subject", "")
    msg["X-Unsent"] = "1"  # tells Mail/Outlook to open it as an editable draft
    msg.set_content(email.get("body", "").rstrip("\n") + "\n\n" + signature + "\n")
    with open(path, "wb") as fh:
        fh.write(bytes(msg))


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s or "contact"


CONF_STYLE = {
    "HIGH": ("#0a7f3f", "#e6f5ec", "verified against a cited source"),
    "MEDIUM": ("#8a5a00", "#fdf3e0", "plausible, but confirm before sending"),
    "LOW": ("#a11", "#fdeaea", "guessed from a pattern — CONFIRM THIS ADDRESS"),
}


def build_html(data, emails, account_index, signature):
    slug = data.get("story_slug", "story")
    deadline = data.get("deadline", "")
    rows = []
    for i, em in enumerate(emails, 1):
        url = gmail_compose_url(em, account_index)
        conf = (em.get("confidence") or "MEDIUM").upper()
        color, bg, conf_note = CONF_STYLE.get(conf, CONF_STYLE["MEDIUM"])
        too_long = len(url) > URL_SAFE_LIMIT

        if too_long:
            action = (
                '<div class="warn">This email is long enough that a pre-filled link may get '
                'truncated by Gmail. Copy the body below instead.</div>'
                '<textarea readonly rows="10">%s</textarea>' % html.escape(em.get("body", ""))
            )
        else:
            action = '<a class="btn" href="%s" target="_blank" rel="noopener">Open Gmail draft &rarr; %s</a>' % (
                html.escape(url, quote=True),
                html.escape(em.get("company", "contact")),
            )

        src = em.get("source_url") or ""
        src_html = (
            '<a href="%s" target="_blank" rel="noopener">%s</a>' % (html.escape(src, quote=True), html.escape(src))
            if src.startswith("http")
            else html.escape(src or "—")
        )

        rows.append(
            """
    <section class="card">
      <div class="hd">
        <span class="num">%d</span>
        <h2>%s</h2>
        <span class="pill" style="color:%s;background:%s">%s &middot; %s</span>
      </div>
      <dl>
        <dt>To</dt><dd><code>%s</code></dd>
        <dt>Subject</dt><dd>%s</dd>
        <dt>Source</dt><dd class="src">%s <span class="dim">%s</span></dd>
      </dl>
      <pre>%s</pre>
      <p class="sigline">+ your Gmail signature, added automatically by Gmail</p>
      %s
    </section>"""
            % (
                i,
                html.escape(em.get("company", "")),
                color,
                bg,
                html.escape(conf),
                html.escape(conf_note),
                html.escape(em.get("to", "")),
                html.escape(em.get("subject", "")),
                src_html,
                html.escape(em.get("source_date", "") or ""),
                html.escape(em.get("body", "")),
                action,
            )
        )

    return """<!doctype html>
<meta charset="utf-8">
<title>RFC outreach — %s</title>
<style>
  :root { color-scheme: light dark; --fg:#111; --dim:#666; --bd:#e2e2e2; --bg:#fff; --card:#fff; }
  @media (prefers-color-scheme: dark) {
    :root { --fg:#e8e8e8; --dim:#9a9a9a; --bd:#333; --bg:#151515; --card:#1c1c1c; }
  }
  body { font: 15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         max-width: 820px; margin: 0 auto; padding: 32px 20px 80px;
         color: var(--fg); background: var(--bg); }
  h1 { font-size: 22px; margin: 0 0 4px; }
  .sub { color: var(--dim); margin: 0 0 28px; }
  .banner { border-left: 3px solid #c99700; background: rgba(201,151,0,.09);
            padding: 10px 14px; border-radius: 0 6px 6px 0; margin-bottom: 28px; }
  .card { border: 1px solid var(--bd); border-radius: 10px; padding: 18px 20px;
          margin-bottom: 18px; background: var(--card); }
  .hd { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 12px; }
  .hd h2 { font-size: 17px; margin: 0; flex: 1; }
  .num { width: 24px; height: 24px; border-radius: 50%%; background: var(--bd);
         display: grid; place-items: center; font-size: 12px; color: var(--dim); }
  .pill { font-size: 11px; font-weight: 600; padding: 3px 9px; border-radius: 20px;
          letter-spacing: .02em; }
  dl { display: grid; grid-template-columns: 76px 1fr; gap: 4px 12px; margin: 0 0 14px;
       font-size: 13px; }
  dt { color: var(--dim); }
  dd { margin: 0; word-break: break-word; }
  .src a { color: inherit; }
  .dim { color: var(--dim); }
  pre { white-space: pre-wrap; font: 13px/1.6 ui-monospace, SFMono-Regular, Menlo, monospace;
        background: rgba(127,127,127,.08); padding: 14px 16px; border-radius: 7px; margin: 0; }
  .sigline { font-size: 12px; color: var(--dim); margin: 6px 0 14px; font-style: italic; }
  .btn { display: inline-block; background: #1a73e8; color: #fff; text-decoration: none;
         padding: 9px 16px; border-radius: 6px; font-weight: 600; font-size: 14px; }
  .btn:hover { background: #1558b8; }
  .warn { color: #a11; font-size: 13px; margin-bottom: 8px; }
  textarea { width: 100%%; font: 12px/1.5 ui-monospace, Menlo, monospace;
             border: 1px solid var(--bd); border-radius: 6px; padding: 10px;
             background: var(--bg); color: var(--fg); }
  code { font-size: 13px; }
</style>
<h1>Request for comment — %s</h1>
<p class="sub">%d contact(s) &middot; deadline: <strong>%s</strong></p>
<div class="banner">
  Each button opens a Gmail compose window that is already filled in. <strong>Nothing sends
  until you press Send yourself.</strong> Read every email before sending, and confirm any
  address flagged MEDIUM or LOW.
</div>
%s
""" % (
        html.escape(slug),
        html.escape(slug),
        len(emails),
        html.escape(deadline),
        "\n".join(rows),
    )


def build_review_md(data, emails, signature):
    out = [
        "# RFC outreach — %s" % data.get("story_slug", ""),
        "",
        "- **Deadline:** %s" % data.get("deadline", ""),
        "- **Terms:** %s" % data.get("terms", ""),
        "- **Generated:** %s" % data.get("generated", ""),
        "",
        "## Contacts",
        "",
        "| # | Company | Email | Confidence | Source |",
        "|---|---|---|---|---|",
    ]
    for i, em in enumerate(emails, 1):
        out.append(
            "| %d | %s | `%s` | %s | %s |"
            % (
                i,
                em.get("company", ""),
                em.get("to", ""),
                (em.get("confidence") or "").upper(),
                (em.get("source_url") or "—"),
            )
        )
    out += ["", "---", ""]
    for i, em in enumerate(emails, 1):
        out += [
            "## %d. %s" % (i, em.get("company", "")),
            "",
            "**To:** %s  " % em.get("to", ""),
            "**Subject:** %s" % em.get("subject", ""),
            "",
            "```",
            em.get("body", "").rstrip("\n"),
            "",
            signature,
            "```",
            "",
        ]
    return "\n".join(out)


def write_tracking(path, data, emails):
    """Create the log, or add only genuinely new companies if it already exists."""
    cols = ["company", "email", "confidence", "drafted", "sent_at", "deadline", "status", "response_notes"]
    existing = set()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                existing.add((row.get("company", ""), row.get("email", "")))

    new_rows = []
    for em in emails:
        key = (em.get("company", ""), em.get("to", ""))
        if key in existing:
            continue
        new_rows.append(
            {
                "company": em.get("company", ""),
                "email": em.get("to", ""),
                "confidence": (em.get("confidence") or "").upper(),
                "drafted": data.get("generated", ""),
                "sent_at": "",
                "deadline": data.get("deadline", ""),
                "status": "not sent",
                "response_notes": "",
            }
        )

    write_header = not os.path.exists(path)
    if not new_rows and not write_header:
        return 0
    with open(path, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        if write_header:
            w.writeheader()
        w.writerows(new_rows)
    return len(new_rows)


def main():
    if len(sys.argv) != 2:
        die("usage: python3 scripts/build_drafts.py outreach/<slug>/drafts.json")
    src = sys.argv[1]
    if not os.path.exists(src):
        die("no such file: %s" % src)

    with open(src, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    emails = data.get("emails") or []
    if not emails:
        die("drafts.json has no emails")

    missing = [e.get("company", "?") for e in emails if not e.get("to")]
    if missing:
        die("these entries have no email address: %s" % ", ".join(missing))

    signature = read_signature()
    if "TODO" in signature:
        sys.stderr.write("WARNING: config/signature.txt still contains TODO placeholders.\n")

    account_index = read_gmail_account_index()
    from_addr = data.get("from_email", "")
    outdir = os.path.dirname(os.path.abspath(src))

    with open(os.path.join(outdir, "compose.html"), "w", encoding="utf-8") as fh:
        fh.write(build_html(data, emails, account_index, signature))

    for i, em in enumerate(emails, 1):
        name = "%02d-%s.eml" % (i, slugify(em.get("company", "")))
        write_eml(os.path.join(outdir, name), em, signature, from_addr)

    with open(os.path.join(outdir, "REVIEW.md"), "w", encoding="utf-8") as fh:
        fh.write(build_review_md(data, emails, signature))

    added = write_tracking(os.path.join(outdir, "tracking.csv"), data, emails)

    print("Wrote %d draft(s) to %s" % (len(emails), outdir))
    print("  compose.html   Gmail buttons (nothing sends on its own)")
    print("  *.eml          drafts for Apple Mail / Outlook")
    print("  REVIEW.md      read-through copy")
    print("  tracking.csv   %d new row(s)" % added)
    flagged = [e.get("company") for e in emails if (e.get("confidence") or "").upper() != "HIGH"]
    if flagged:
        print("\n  CONFIRM THESE ADDRESSES BEFORE SENDING: %s" % ", ".join(flagged))


if __name__ == "__main__":
    main()
