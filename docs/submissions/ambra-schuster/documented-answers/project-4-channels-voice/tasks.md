# Project 4 — Channels + Voice · tasks

> **Status: not started.** Planning depth — rewrite before building.
> Companion files: [requirements.md](requirements.md), [architecture.md](architecture.md).

## Stage 0 — Settle feasibility (do this in week 1, not week 12)

- [ ] **0.1 — Talk to whoever runs Documented's WeChat account.** A
      15-minute conversation determines whether the WeChat leg exists.
      *Done when:* the answer is written down either way.
- [ ] **0.2 — Get Meta Business account access** for the existing
      WhatsApp number and Messenger page.
- [ ] **0.3 — Confirm Nextdoor has no usable API** and commit to the
      draft-and-human-post approach.

## Stage 1 — WhatsApp, text

- [ ] **1.1 — Stand up the webhook** and echo a message end to end from a
      real phone.
- [ ] **1.2 — Wire it to Project 3's answer engine.** Adapter only, no new
      answer logic.
      *Done when:* the same question gives the same substantive answer on
      WhatsApp and on the site widget.
- [ ] **1.3 — Bot disclosure on first contact**, in the user's language,
      including the metadata caveat and how to reach a human.
- [ ] **1.4 — Test all four languages from a real phone.**

## Stage 2 — Voice

- [ ] **2.1 — Voice note in → Whisper → pipeline.**
- [ ] **2.2 — Test ASR quality per language**, especially Haitian Creole
      and Spanish regional accents.
      *Done when:* the per-language error rate is written down, including
      the bad news.
- [ ] **2.3 — Always return the text answer alongside audio.**
      *Done when:* a deliberately garbled voice note produces a visible,
      correctable transcription.
- [ ] **2.4 — TTS reply as an opt-in toggle.**

## Stage 3 — Messenger

- [ ] **3.1 — Reuse the WhatsApp adapter** on the existing page.
      *Done when:* it works end to end with substantially less new code.

## Stage 4 — The human-posting surfaces

- [ ] **4.1 — Draft generator for Nextdoor and (if needed) WeChat.**
      *Done when:* a human at Documented has published a drafted post and
      says it saved them time.
