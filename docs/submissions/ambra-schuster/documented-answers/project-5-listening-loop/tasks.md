# Project 5 — The Listening Loop · tasks

> **Status: not started.** Planning depth — rewrite before building.
> Companion files: [requirements.md](requirements.md), [architecture.md](architecture.md).

## Stage 0 — Before any real question is handled

- [ ] **0.1 — Threat model reviewed and signed off** (Project 1, task A.5).
      *Done when:* a supervisor has read it and agreed. This gates
      everything below.

## Stage 1 — The scrubber

- [ ] **1.1 — Write `listen/scrub.py`.** Names, phone numbers, addresses,
      A-numbers, case numbers.
- [ ] **1.2 — Put it inline in the answer path**, before any write.
      *Done when:* there is no code path where unscrubbed text reaches
      storage. Verified by reading the code, not by testing outputs.
- [ ] **1.3 — The adversarial privacy test.** Submit a question containing
      a fake name, phone number, and A-number; inspect the stored record.
      *Done when:* all three are gone. Repeat in all four languages —
      scrub rules tuned on English fail on other scripts.
- [ ] **1.4 — Rotating salted session hash**, discarded on a short cycle.

## Stage 2 — Storage and retention

- [ ] **2.1 — Define the minimal record** and store nothing beyond it.
- [ ] **2.2 — Automatic retention.** Raw text deletes itself; aggregates
      survive.
      *Done when:* it has actually deleted something on schedule, observed.

## Stage 3 — Analysis

- [ ] **3.1 — Write `listen/cluster.py`.** Weekly clustering.
- [ ] **3.2 — Rising topics.** Week-over-week movement.
- [ ] **3.3 — Information gaps.** Frequent questions where retrieval found
      nothing.
      *Done when:* the top gaps read like plausible story assignments to a
      reporter.

## Stage 4 — Delivery

- [ ] **4.1 — Weekly digest to the newsroom.** Two sections only.
- [ ] **4.2 — Confirm it's being read.**
      *Done when:* a reporter has turned a surfaced gap into a story. That,
      not the digest existing, is the finish line.
