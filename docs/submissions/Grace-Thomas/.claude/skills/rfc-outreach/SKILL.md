---
name: rfc-outreach
description: Generate request-for-comment emails for a breaking news story from BRIEF.md — research and verify each company's press contact, write an individual email per recipient with subject line and deadline, and output Gmail draft links, .eml files, and a tracking log. Never sends. Use when the user says "run the brief", "generate the outreach emails", "RFC these companies", or asks to draft requests for comment for a story.
---

# RFC outreach

Turn a filled-in `BRIEF.md` into per-recipient request-for-comment emails, ready to send but
never sent.

## Hard rules

1. **Never send anything.** No mail tools, no SMTP, no `mailto:` execution, no browser
   automation that clicks Send. This skill writes files. The reporter sends.
2. **Never invent an email address and present it as verified.** Every address carries a
   source URL and a confidence level. A guessed address is labeled `LOW` and says so.
3. **Never invent facts about a company** to make a paragraph land better. If the brief
   doesn't establish that a company did the thing, don't assert they did — ask.
4. **Never fabricate the reporter's identity.** If `config/profile.md` still has `TODO` in a
   field an email needs, stop and ask for it.

## Steps

### 1. Read the inputs

- `BRIEF.md` — the story
- `config/profile.md` — reporter name, outlet, phone, Gmail account index
- `config/signature.txt` — used in `.eml` files (Gmail adds its own)
- `contacts/press-contacts.csv` — previously confirmed contacts

If the brief is missing a **story summary**, **recipient list**, **the question**, or a
**deadline**, ask for just those. Everything else has a reasonable default. If `profile.md`
still contains `TODO`, ask for those values before writing any email.

### 2. Resolve the press contact for each company

For each company, in order:

1. **Cache hit.** If `contacts/press-contacts.csv` has a row for the company, use it. Note
   the `source_date` — if it's more than ~6 months old, re-verify.
2. **Research.** Otherwise use WebSearch/WebFetch. Look for the company's actual newsroom or
   media-relations page: `<company>.com/newsroom`, `/press`, `/media`, `/news`, or their
   corporate site (Nike's is `about.nike.com`, not `nike.com`). Prefer a media-relations
   inbox over a named individual — individuals change jobs, inboxes get routed on deadline.
   Prefer the regional desk that matches the story (a global sports story usually wants
   global or North America comms, not the local retail PR contact).
3. **Assign confidence honestly:**
   - `HIGH` — the address is printed on the company's own site or its official press kit,
     and you fetched that page.
   - `MEDIUM` — from a credible secondary source (a press release wire, a recent news story,
     a trade publication's masthead), or from the company's own site but not recently dated.
   - `LOW` — inferred from a naming pattern (`press@`, `media@`) without seeing it published.
4. **If you can't find one at all**, still write the email, set `to` to `""`, and tell the
   reporter which companies need a manual lookup. Don't quietly drop a recipient.

Report contacts to the reporter as a table (company, address, source, confidence) **before**
moving on, so they can catch a wrong desk early.

### 3. Write one email per recipient

Every email is individually written. Same core question, but the context paragraph names the
specific company and what the reporting shows about *them*. Substitute `{COMPANY}` throughout.

**Subject line.** It has to survive a PR inbox on deadline. Pattern:

> `<Outlet> query — <specific topic> — response requested by <deadline>`

e.g. `NYCity News Service query — Nike's pink World Cup cleats — response by 4 p.m. ET today`

Not "Media inquiry" or "Quick question." Name the outlet, the subject, and the clock.

Keep the subject line **plain ASCII** — use a hyphen, not an em dash. Non-ASCII characters
get MIME-encoded into `=?utf-8?b?...?=` gibberish in the raw `.eml`, and they bloat the
Gmail compose URL. Em dashes in the body are fine.

**Body.** Plain text. **Four sentences maximum**, not counting the numbered questions.
Breaking-news PR inboxes get triaged in seconds — a long email buries the ask. Exactly this
structure, in this order:

1. **Who you are** — one sentence. Name and outlet. Nothing else.
2. **The story** — one sentence. The actual thesis, compressed. If it takes three sentences to
   explain, compress it; do not spend a second sentence here.
3. **What it says about them** — one sentence, ending in the handoff to the questions. Drawn
   from the brief's "What I already have" field. This is what makes it a real request for
   comment rather than a survey.
4. **The numbered questions**, company name substituted in. These don't count toward the four.
5. **The deadline** — one sentence, last line, nothing after it. Format: `My deadline is 4 ET
   today.`

Example (Nike, pink cleats):

```
Hello,

I'm Grace Thomas, a reporter with NYCity News Service.

The story examines a pattern: every major athletic brand released pink cleats timed to
the 2026 World Cup, and my reporting indicates they were working from similar market
research concluding that pink offers the highest visibility against the green of the pitch.

Nike released at least one pink cleat colorway timed to the tournament, which is why I'm
bringing these questions to you:

1. Why did Nike choose pink for the boots worn by players at the World Cup?
2. Why did Nike release pink cleats for consumers to purchase during this period?
3. Did Nike rely on market research indicating pink would have the highest on-pitch
   visibility, and if so, was that research conducted internally or by an outside firm?

My deadline is 4 ET today.
```

**Do not include any of the following.** Each was deliberately cut. Do not add them back
because they seem helpful or standard:

- Any sign-off — no "Thank you," "Best," or "Sincerely." The Gmail signature is the close.
- The signature itself. The pipeline handles it: Gmail appends the reporter's real signature,
  and the `.eml` files embed `config/signature.txt`. Writing it into the body signs twice.
- "If I don't hear back, the story will note that X did not respond by press time."
- An offer to share the passage before publication for an accuracy check.
- A statement of terms ("on the record, attributed to a named spokesperson"). The reporter
  chose to leave terms out of the email and establish them in the reply thread.
- An offer to take a call, or a phone number.
- Any sentence after the deadline line.

The `terms` field in the brief still gets recorded in `drafts.json` for the reporter's own
reference — it just doesn't appear in the email body.

**Tone.** Neutral, specific, plain. No flattery, no "I hope this finds you well," no implied
accusation. Respect the reader's time: they are also on deadline.

### 4. Write `drafts.json`

Create `outreach/<story-slug>/drafts.json`:

```json
{
  "story_slug": "pink-cleats-world-cup",
  "deadline": "today, Aug. 24, at 4:00 p.m. ET",
  "terms": "on the record, attributed to a named spokesperson",
  "generated": "2026-08-24",
  "from_email": "tkc.intern2@journalism.cuny.edu",
  "emails": [
    {
      "company": "Nike",
      "contact_name": "Nike Media Relations",
      "to": "nikemedia@nike.com",
      "cc": "",
      "source_url": "https://about.nike.com/en/newsroom",
      "source_date": "2026-08-24",
      "confidence": "HIGH",
      "subject": "...",
      "body": "..."
    }
  ]
}
```

Get today's date from the system rather than assuming it.

### 5. Build the outputs

```bash
python3 scripts/build_drafts.py outreach/<story-slug>/drafts.json
```

That writes `compose.html` (Gmail buttons), one `.eml` per contact, `REVIEW.md`, and
`tracking.csv`.

### 6. Update the contact cache

Append any **HIGH or MEDIUM** contact that isn't already in `contacts/press-contacts.csv`,
with its source URL and date. Never cache a `LOW` address — that's how a guess becomes
permanent.

### 7. Report back

Tell the reporter:

- the contact table with confidence levels
- which addresses they must confirm before sending
- the path to `compose.html` and how to open it
- anyone who needs a manual lookup

Then stop. Do not open the browser and start clicking.

## Follow-ups

If asked to chase non-responders, read `tracking.csv`, take the rows still marked
`awaiting`, and write short follow-ups referencing the original send time and restating the
deadline. Same pipeline, into `outreach/<slug>-followup/`.
