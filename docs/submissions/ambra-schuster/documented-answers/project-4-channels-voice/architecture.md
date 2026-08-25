# Project 4 — Channels + Voice · architecture

> **Status: not started.** Planning-depth sketch.
> Companion files: [requirements.md](requirements.md), [tasks.md](tasks.md).

## Approach

One brain, several mouths. Every channel is a thin adapter over Project 3's
answer engine — never its own logic. The moment a channel gets its own
rules for what it will say, the answer contract stops being enforceable.

```
  WhatsApp ─┐
  Messenger ─┼→ channels/*.py (adapters) → Project 3's answer engine
  Site widget ─┘                                    ↑
                                          voice in: Whisper transcription
                                          voice out: TTS (optional toggle)

  WeChat ────┐
  Nextdoor ──┴→ draft generator → human posts
```

## The channels are not equivalent

| Channel | Reality | Plan |
|---|---|---|
| **WhatsApp** | Real API (Meta Cloud API / Twilio). Documented has an existing community and number (`wa.me/16469395145`). Voice notes supported. | **Primary. Build this.** |
| **Messenger** | Same Meta stack, existing page (`m.me/170561090311008`). | Second, cheap. |
| **WeChat** | Official Account API effectively requires a verified Chinese entity; overseas accounts get heavily restricted API access plus content moderation. | Verify feasibility early. Likely human-assisted posting, not a bot. |
| **Nextdoor** | No public bot or messaging API. It's a human posting surface. | Repurpose: auto-draft posts, human publishes. |

## Voice

- **In:** WhatsApp voice note → Whisper transcription → same retrieval
  pipeline. Cheap, high impact, build it.
- **Out:** TTS reply as a voice note (ElevenLabs or OpenAI TTS, both
  multilingual). A toggle, not a default.
- **Test early:** ASR quality for Haitian Creole and for Spanish regional
  accents is uneven. Always send the text answer alongside the audio so a
  bad transcription is visible and correctable — this is a design
  requirement, not a fallback.

## What it works with or around

- **Documented's existing Meta presence** — an existing number and page
  with an existing community. This is an asset, and also means the account
  isn't a sandbox to experiment in freely.
- **documented.info proved the channels work.** The audience and the
  editorial workflow are already validated. What killed it was upkeep, not
  demand — so every choice here gets judged by whether it survives without
  someone babysitting it.
- **Meta's platform rules** on business messaging, template messages, and
  the 24-hour customer-service window shape what the bot can send and when.
- **Meta holds the metadata regardless of anything built here.** That's a
  disclosure problem, not an engineering one.
