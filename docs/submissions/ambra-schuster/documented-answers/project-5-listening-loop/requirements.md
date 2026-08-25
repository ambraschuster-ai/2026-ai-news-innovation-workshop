# Project 5 — The Listening Loop · requirements

> **Status: not started.** Planning depth.
> Companion files: [architecture.md](architecture.md), [tasks.md](tasks.md).

## The problem

Every question the bot receives is information the newsroom doesn't
currently have: what immigrants in New York are actually worried about this
week, and what Documented hasn't written about yet. That's story leads.

It's also, handled carelessly, a queryable log of undocumented people asking
about ICE — which is a subpoena target. Both facts are true at once, and
the design has to hold both.

## What this has to do

1. **Scrub personal information at write time, never after.** No names, no
   phone numbers, no addresses, no A-numbers, no case numbers. Scrubbing
   after storage means it was stored.
2. **Store as little as possible:** scrubbed question text, language, a
   coarse timestamp bucket, what retrieval returned, and whether the bot
   could answer. Nothing else.
3. **No cross-session identity.** A rotating salted hash for continuity
   within a conversation, discarded on a short cycle. No contact storage.
   No location capture.
4. **Surface rising topics** — what's spiking week over week.
5. **Surface information gaps** — frequent questions where retrieval found
   nothing. These are literally assignment ideas.
6. **Deliver as a simple weekly digest** to the newsroom. Resist building
   an elaborate dashboard nobody opens.
7. **Aggregate, then delete.** Raw text has the shortest retention window
   that still supports the analysis.

## The design bar

The right answer to "could this log be subpoenaed?" is **"there's nothing
useful in it."** Not "we'd fight it." Design so there is nothing worth
seizing.

## What "finished" looks like

- [ ] Submitting a question containing a fake name, phone number, and
      A-number, then inspecting the stored record, shows all three are gone.
- [ ] The weekly digest has surfaced at least one information gap that a
      reporter turned into a story.
- [ ] Retention is enforced automatically — old raw text deletes itself
      rather than needing someone to remember.
- [ ] The threat model document has been reviewed and the implementation
      matches it.

## Explicitly out of scope

- Any per-user analytics, profiles, or history.
- Location data, in any form, for any reason.
- An interactive dashboard, unless a weekly digest has been running and a
  reporter has specifically asked for more.
- Sharing question data outside Documented.

## Depends on

Projects 3 and 4 receiving real questions. The threat model (Project 1,
task A.5) reviewed and signed off **before** this handles a single real
user's question — not after.
