# Submission Info

<!-- Fill this in as your project takes shape, and keep it current.
     This becomes your public profile card on the workshop showcase page,
     pulled live from this file — worth a real sentence per field, not a
     placeholder. -->

- **Student Name:** Grace Thomas

- **Fork URL:** `https://github.com/graceathomas5/2026-ai-news-innovation-workshop`

- **Hypothesis or problem statement:** On a breaking story, the request for comment is the step that gets rushed or skipped. A reporter working a deadline has to find each company's press contact, verify it's current, write an individually tailored email, and keep a record of who was asked and when — repeated once per company, in the same hour the story is being written. My hypothesis is that the research and drafting can be automated without automating the judgment, and that keeping a human on the Send button is what makes that safe.

- **What you're building:** RFC Bot — a Claude skill that turns a filled-in story brief into one individually written request for comment per company. It researches each press contact and cites the source, labels how confident it is in that address, writes an email tailored to each recipient with the reporter's question, deadline, and signature, and produces a tracking log for the "did not respond by press time" line. It never sends anything; the reporter reviews every draft and presses Send.

- **Solution:** Working end to end on the pink-cleats World Cup story (Nike, Adidas, New Balance, Puma). You fill in `BRIEF.md`, say "run the brief," and get a `compose.html` of one-click pre-filled Gmail drafts, matching `.eml` files, a `REVIEW.md` for a fast read-through, and a `tracking.csv`. Every contact is labeled HIGH / MEDIUM / LOW confidence, and the build script warns on anything below HIGH, because a wrong address on deadline is a missed statement. Confirmed contacts cache to `contacts/press-contacts.csv` so repeat outlets are instant. Not yet generalized beyond Gmail-based workflows, and the contact research still needs a human to confirm anything below HIGH before sending.
