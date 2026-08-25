# Submission Info

<!-- Fill this in as your project takes shape, and keep it current.
     This becomes your public profile card on the workshop showcase page,
     pulled live from this file — worth a real sentence per field, not a
     placeholder. -->

- **Student Name:** Ambra Schuster

- **Fork URL:** `https://github.com/ambraschuster-ai/2026-ai-news-innovation-workshop`

- **Hypothesis or problem statement:** Documented NY has spent years building a
  resource guide of roughly 250 articles in four languages, but it is a list —
  an immigrant with an actual question ("I have two kids, what do I need to know
  about schools?") has to read several articles, possibly in a language that
  isn't theirs, to find the answer. If I use AI to answer questions using only
  Documented's own published articles, then immigrant New Yorkers will get a
  direct, sourced, dated answer in their own language instead of a reading list.

- **What you're building:** A chatbot that only knows what Documented has
  published. It searches their articles, cites every claim with a link, stamps
  how old the source is, asks the one follow-up question that changes the answer
  (usually the child's age or the borough), and refuses anything it can't source
  — routing legal questions and emergencies to ActionNYC instead of guessing.

- **Solution:** A working prototype over 38 of Documented's resource articles
  (23 English, 15 Spanish; 247 searchable sections). It reaches the corpus
  through a browser, because Documented's own site blocks scripted access — a
  finding worth knowing on its own. Answers are held to their sources three
  ways: the model only ever sees what search returned, the prompt requires a
  link per claim, and code rejects any link search didn't return. Article age is
  calculated rather than left to the model, so a three-year-old article is
  flagged red whether or not the bot mentions it — which surfaced a real
  problem: a 2023 Documented article still tells undocumented parents Head Start
  is open to them, and a 2025 rule change reversed that. Every answer can be
  re-read in Easy English, Spanish, Haitian Creole or Chinese; the last two are
  labelled as translations, since Documented's own Creole and Chinese articles
  haven't been read yet. Costs $0.06 a question, measured. Not affiliated with
  Documented and not reviewed by them.
