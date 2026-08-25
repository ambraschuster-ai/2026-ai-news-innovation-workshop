# RFC Bot — working plan

> **How this file came about:** written 2026-08-24 at the end of Day 1, reconstructed from the
> actual state of the project rather than from an earlier written plan (there wasn't one). If
> we agreed on something before this that isn't captured here, add it — this file is meant to
> be edited, not preserved.

## The idea, in one paragraph

On a breaking story, the request for comment is the step that gets rushed. Finding each
company's press contact, confirming it's current, writing a real email per recipient, and
keeping a record of who was asked and when — that's 30–45 minutes of work in the same hour the
story is being written, so it gets compressed into a generic blast or skipped. RFC Bot
automates the research and the drafting but deliberately **not** the sending or the judgment.
The reporter reads every draft and presses Send.

## Where things stand

**Built and working end to end.** The `rfc-outreach` skill takes a filled-in `BRIEF.md` and
produces, per story:

| Output | Purpose |
|---|---|
| `compose.html` | One button per contact → pre-filled Gmail compose window. Main workflow. |
| `NN-company.eml` | Same emails as files, for Apple Mail / Outlook. |
| `REVIEW.md` | All emails in one document for a fast read-through. |
| `tracking.csv` | Who, when, deadline, status — the record behind "did not respond by press time." |
| `drafts.json` | Structured source; edit and re-run `scripts/build_drafts.py` to regenerate. |

**Test story:** pink cleats at the 2026 World Cup — Nike, Adidas, New Balance, Puma. All four
drafted 2026-08-24, rewritten the same day to the four-sentence format. Contacts resolved: New Balance and Puma at HIGH confidence (fetched from
their own press pages), Nike and Adidas at MEDIUM (Adidas' media-contact page timed out on
direct fetch; Nike's address is cited in their own releases but the newsroom page wasn't read
directly). Nothing sent.

**Design decisions worth not re-litigating:**

- *Never sends.* No SMTP, no browser automation that clicks Send. The skill writes files.
- *Confidence labels are load-bearing.* HIGH / MEDIUM / LOW on every address, with a source
  URL and date. `build_drafts.py` warns on anything below HIGH. A wrong address on deadline is
  a missed statement, so the bot never sounds more certain than it is.
- *Gmail links omit the signature on purpose*, because Gmail appends the real one. `.eml` files
  embed `config/signature.txt`, because nothing else will.
- *Only HIGH and MEDIUM contacts get cached*, so a guess never hardens into a permanent record.
- *Four sentences, maximum.* Added 2026-08-24 after reading the first real drafts. A breaking-news
  PR inbox gets triaged in seconds and a 250-word email buries the ask. The body is: who you are,
  the story thesis, the specific claim about this company, the numbered questions, and
  `My deadline is 4 ET today.` Nothing after that line. No sign-off — the Gmail signature is the
  close. The skill carries an explicit do-not-add-back list so a future run doesn't reinstate the
  press-time warning, the accuracy-check offer, or the on-the-record paragraph.
- *Terms are deliberately not stated in the email.* Reporter's call: establish on-the-record in
  the reply thread rather than spend a sentence on it. Recorded in `drafts.json` for reference.

## Next up

1. **Fill in `config/profile.md` and `config/signature.txt`.** *(Mostly done 2026-08-24.)*
   Byline name (Grace Thomas) and outlet (NYCity News Service) are set. **Deadline phone is
   still `TODO`.** It now only affects the signature line — the four-sentence body no longer
   offers a phone number — so it doesn't block a send, and the Gmail path uses your real
   signature regardless. The `.eml` files carry the placeholder until it's filled.
2. **Send the pink-cleats round, or retire it as a test.** Four drafts are sitting at "not
   sent" against a 4 p.m. ET deadline dated 2026-08-24. Decide whether this is a live story or
   a fixture — and if it's a fixture, say so in the brief so it isn't mistaken for real
   pending outreach later.
3. **Confirm the two MEDIUM addresses** (Nike, Adidas) before any real send.
4. **Exercise the follow-up path.** `"draft follow-ups for the non-responders"` reads statuses
   from `tracking.csv` and writes chasers to `outreach/<slug>-followup/`. Untested so far.
5. **Run a second, unrelated story** — the real test of whether this generalizes or is
   quietly shaped around the cleats example.

## Open questions

- **Does it generalize past Gmail?** Everything routes through Gmail compose URLs. A reporter
  on Outlook gets the `.eml` files, which is a worse experience. Is that acceptable?
- **Is contact research reliable enough to trust?** Two of four came back MEDIUM on the first
  real attempt. That's honest, but it means a human still confirms half the list. Does that
  leave enough time saved to matter?
- **Optional Gmail API drafts** (`scripts/gmail_drafts.py`) needs ~15 min of Google Cloud
  setup and requests the `gmail.compose` scope, which cannot send. Worth doing, or does
  `compose.html` already cover it?

## Edit log

**2026-08-24 — cut every email to four sentences.**

Reviewed the first real drafts and found them too long for breaking news. Applied across all
four pink-cleats emails and baked into `.claude/skills/rfc-outreach/SKILL.md` as the default,
so the next story generates the short form without re-cutting.

Cut: the redundant "I'm on deadline today with a story about..." sentence; the "I'm seeking a
response on the record" paragraph; the "did not respond by press time" sentence; the offer to
share the passage for an accuracy check; the "Thank you," sign-off.

Compressed: the three-sentence thesis paragraph into one sentence, to fit the four-sentence cap
after the other cuts. The market-research point survives.

Result, per email:

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

Verified after rebuild: four sentences plus three questions in all four emails; last line
correct in all four; zero hits for `Thank you`, `[YOUR NAME]`, `[YOUR PHONE]`, `press time`,
`on the record` or `happy to share`; signature reads Grace Thomas; Gmail compose URLs down from
~1,900 to ~1,050 characters; re-running adds no duplicate tracking rows.

## Housekeeping

- Project now lives at `docs/submissions/Grace-Thomas/` in the workshop repo, branch `day-1`.
- It was **copied**, not moved, from `~/082626_AI Workshop`, which is not a git repo. Both
  copies exist and can drift. The clone is the one under version control. They *did* drift on
  2026-08-24 — the four-sentence rewrite happened in the working copy only, and ten files were
  re-synced into the repo after the fact. Worth doing the edits in the clone from here on.
- Day 2 moves from Claude Desktop's Code tab to VS Code + the Claude Code extension.
