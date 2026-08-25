# RFC Bot — request-for-comment outreach for breaking news

Fill in a brief, say "run the brief," and get one individually-written request for comment per
company: press contact researched and source-cited, subject line, deadline, your signature, and
a tracking log. **It never sends anything.** You review every email and press Send yourself.

## One-time setup

1. Open `config/profile.md` and replace every `TODO` — your byline name, outlet, and a phone
   number you'll actually answer on deadline.
2. Open `config/signature.txt` and paste in your real signature. This is what gets embedded in
   the `.eml` files. (Gmail supplies its own signature — see below.)

That's it. No API keys, no install.

## Running a story

1. Open `BRIEF.md` and fill it in: the story, who you're contacting, your question(s), your
   deadline. It's pre-filled with the pink cleats story as a worked example — overwrite it.
2. Tell Claude: **"run the brief"**
3. Claude researches each company's press contact, shows you a table with sources and
   confidence levels, writes each email, and builds the output.
4. Open `outreach/<slug>/compose.html` in your browser:

```bash
open "outreach/pink-cleats-world-cup/compose.html"
```

5. Each button opens a Gmail compose window already filled with To, Subject, and body. Gmail
   inserts your real signature automatically. Read it, fix anything, hit Send.

## What you get per story

| File | What it's for |
|---|---|
| `compose.html` | One button per contact → opens a pre-filled Gmail draft. Your main workflow. |
| `01-nike.eml`, … | Same emails as files. Double-click to open in Apple Mail or Outlook. |
| `REVIEW.md` | Every email in one document, for a fast read-through before you send. |
| `tracking.csv` | Who, when, deadline, status. Update `status` as replies come in. |
| `drafts.json` | The structured source. Edit it and re-run the build to regenerate everything. |

If you edit `drafts.json` by hand, rebuild with:

```bash
python3 scripts/build_drafts.py outreach/pink-cleats-world-cup/drafts.json
```

## About the signature

The two outputs handle it differently on purpose:

- **Gmail links** deliberately leave the signature out of the body, because Gmail appends your
  configured signature to every compose window. You get the real thing — logo, links, whatever
  you have set — instead of a copy.
- **`.eml` files** embed `config/signature.txt`, because nothing else will add one.

Send your first email from `compose.html` and glance at the bottom to confirm your Gmail
signature is landing. If it isn't, turn it on in Gmail Settings → General → Signature and set
it to apply to new messages.

## Confidence levels — read these before you send

Every address is labeled:

- **HIGH** — printed on the company's own newsroom page, which was fetched and read.
- **MEDIUM** — from a credible secondary source, or from the company's site but not
  directly verified this run. **Confirm before sending.**
- **LOW** — guessed from a naming pattern like `press@`. **Do not send without confirming.**

`compose.html` color-codes these and the build script prints a warning listing anything below
HIGH. A wrong address on deadline is a missed statement, so the bot never pretends to be more
certain than it is.

## The contact cache

`contacts/press-contacts.csv` grows as you confirm contacts. Next time you email Nike, it's
instant — no research step. Each row keeps its source URL and date; anything older than about
six months gets re-verified. Only HIGH and MEDIUM contacts are cached, so a guess never
hardens into a permanent record.

## Following up

Once you've sent, mark statuses in `tracking.csv` (`awaiting`, `responded`, `declined`). Then
tell Claude **"draft follow-ups for the non-responders"** and it writes short chasers into
`outreach/<slug>-followup/`.

When you write "did not respond to a request for comment by press time" in your story, the
tracking log is your record of exactly when you asked and what deadline you gave.

## Optional: real Gmail drafts

`scripts/gmail_drafts.py` writes drafts straight into your Gmail Drafts folder via the Gmail
API. It requires about 15 minutes of Google Cloud setup — the steps are in a comment at the top
of the file. It requests the `gmail.compose` scope, which cannot send mail, so it can only ever
create drafts.

## Layout

```
BRIEF.md                          fill this in per story
config/profile.md                 your name, outlet, phone
config/signature.txt              your signature (used in .eml files)
contacts/press-contacts.csv       verified contacts, grows over time
outreach/<slug>/                  one folder per story
scripts/build_drafts.py           drafts.json → Gmail links, .eml, tracking, review
scripts/gmail_drafts.py           optional: real Gmail drafts via API
.claude/skills/rfc-outreach/      the instructions Claude follows
```
