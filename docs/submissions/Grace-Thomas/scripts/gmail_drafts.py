#!/usr/bin/env python3
"""
UPGRADE PATH — writes real drafts into your Gmail Drafts folder via the Gmail API.

This creates drafts. It does NOT send. The scope requested (gmail.compose) does not
grant send permission at all, so a bug here cannot mail anyone.

One-time setup (~15 min):

  1. pip3 install --user google-auth-oauthlib google-api-python-client
  2. Go to https://console.cloud.google.com → create a project (any name).
  3. APIs & Services → Library → search "Gmail API" → Enable.
  4. APIs & Services → OAuth consent screen → External → fill in the required fields →
     under "Test users" add tkc.intern2@journalism.cuny.edu.
  5. APIs & Services → Credentials → Create Credentials → OAuth client ID →
     Application type: Desktop app → Create → Download JSON.
  6. Save that file as config/gcp_credentials.json in this project.

Then:
  python3 scripts/gmail_drafts.py outreach/<slug>/drafts.json

First run opens a browser to authorize; the token is cached in config/gmail_token.json.
Both config/gcp_credentials.json and config/gmail_token.json are secrets — they are
gitignored, and you should not share them.
"""

import base64
import json
import os
import sys
from email.message import EmailMessage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED = os.path.join(ROOT, "config", "gcp_credentials.json")
TOKEN = os.path.join(ROOT, "config", "gmail_token.json")
SIG = os.path.join(ROOT, "config", "signature.txt")

# Compose-only. This scope cannot send mail.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def die(msg):
    sys.stderr.write("error: %s\n" % msg)
    sys.exit(1)


def get_service():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        die(
            "missing libraries. Run:\n"
            "  pip3 install --user google-auth-oauthlib google-api-python-client"
        )

    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CRED):
                die("missing %s — see the setup steps at the top of this file" % CRED)
            creds = InstalledAppFlow.from_client_secrets_file(CRED, SCOPES).run_local_server(port=0)
        with open(TOKEN, "w", encoding="utf-8") as fh:
            fh.write(creds.to_json())
        os.chmod(TOKEN, 0o600)
    return build("gmail", "v1", credentials=creds)


def main():
    if len(sys.argv) != 2:
        die("usage: python3 scripts/gmail_drafts.py outreach/<slug>/drafts.json")
    with open(sys.argv[1], "r", encoding="utf-8") as fh:
        data = json.load(fh)

    emails = data.get("emails") or []
    if not emails:
        die("drafts.json has no emails")

    with open(SIG, "r", encoding="utf-8") as fh:
        signature = fh.read().rstrip("\n")

    service = get_service()
    created = 0
    for em in emails:
        if not em.get("to"):
            print("SKIP %s — no address" % em.get("company", "?"))
            continue
        msg = EmailMessage()
        msg["To"] = em["to"]
        if em.get("cc"):
            msg["Cc"] = em["cc"]
        msg["Subject"] = em.get("subject", "")
        msg.set_content(em.get("body", "").rstrip("\n") + "\n\n" + signature + "\n")
        raw = base64.urlsafe_b64encode(bytes(msg)).decode()
        service.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
        created += 1
        print("draft created: %s <%s>" % (em.get("company", ""), em["to"]))

    print("\n%d draft(s) in your Gmail Drafts folder. Nothing was sent." % created)


if __name__ == "__main__":
    main()
