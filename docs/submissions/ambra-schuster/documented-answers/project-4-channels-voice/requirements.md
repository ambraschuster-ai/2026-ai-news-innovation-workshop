# Project 4 — Channels + Voice · requirements

> **Status: not started.** Planning depth. One leg (WeChat) may be
> infeasible — that gets settled in Project 1's task A.4, not here.
> Companion files: [architecture.md](architecture.md), [tasks.md](tasks.md).

## The problem

A chat widget on a website only reaches people who visit the website.
Documented's audience already talks to them on WhatsApp and Messenger —
documented.info proved that. And a large share of that audience
communicates by voice note, which every text-only tool silently excludes.

## What this has to do

1. **Answer on WhatsApp**, in all four languages, using the same retrieval
   and the same answer contract as the site widget. Not a second bot with
   its own rules.
2. **Answer on Messenger**, which is nearly free once WhatsApp works —
   same Meta stack, existing page.
3. **Accept voice notes in**, transcribe them, and run them through the
   same pipeline. This is an equity feature, not a nice-to-have: it works
   for people with low literacy in *any* written language.
4. **Offer a voice reply out**, as a toggle rather than a default — and
   **always send the text answer alongside the audio**, so a bad
   transcription is visible and correctable.
5. **Disclose that it's a bot** in every channel, in the user's language,
   including what it can't do and how to reach a human.
6. **Be honest about metadata.** WhatsApp metadata belongs to Meta, not to
   Documented. The disclosure says so plainly rather than making promises
   that can't be kept.
7. **For channels without a bot API, make the humans faster.** Nextdoor has
   no public messaging API; WeChat likely can't have one. Auto-draft posts;
   a human publishes.

## What "finished" looks like

- [ ] End-to-end from a real phone, in all four languages, text and voice —
      including a deliberately garbled voice note.
- [ ] Answers on WhatsApp are identical in substance to the site widget's.
- [ ] The bot disclosure appears in the user's language on first contact in
      every channel.
- [ ] WeChat feasibility has a definite answer, documented, either way.

## Explicitly out of scope

- **Video.** Short vertical explainers auto-drafted from top articles is a
  phase-2 idea. Noted, not built.
- Four separate chatbots. The honest promise is one excellent WhatsApp bot,
  a nearly-free Messenger twin, and a drafting tool for the surfaces where
  humans post.
- Storing contacts, locations, or any cross-session identity. → see
  Project 5's privacy rules, which apply here too.

## Depends on

Project 3 working and measured. Meta Business account access for the
existing WhatsApp/Messenger presence (Project 1, task A.4 covers the
WeChat question).
