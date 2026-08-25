# Human-AI Design

> Neither human-in-the-loop nor full automation is the safe default. Both are design decisions.

## 1. Human in the Loop Isn't the Default

AI is often used to automate a process end-to-end when we want to standardize across domains, increase efficiency and productivity. But that isn't always the most reasonable choice from an AI-human interaction perspective. Human oversight matters, not just for safety but also for enhancing human experience while using AI. This means that when to automate and when to add human-in-the-loop is a serious design question at every stage in product design and development.

For example, you might slow a process down by adding human intervention, but you do it anyway because the person benefits from sitting with the output. It deepens their own understanding of the work, or allows them to add context you'll need at a later stage. Other times a human's perspective, context, or verification genuinely isn't needed at a given point or can be standardized as documentation, so you let the process run automated from top to bottom and bring a person in only at the very end, to check the final result.

Recent research provides guidance on how to make the decision between automation or human-in-the-loop, or both: 

- **Would a human actually make this better, or just slower?** A large 2024
  meta-analysis found human–AI teams often perform *worse* than whichever party
  is stronger alone. The pattern: pairing tends to hurt on decision/judgment
  tasks and help on drafting/creation. So lean human-led on judgment calls
  (what to publish, is this true); let AI carry more of the drafting. [1]

- **Is the human a real decision-maker, or a rubber stamp?** A checkpoint only
  adds value if the person has the context, authority, and time to genuinely
  override, not just click "approve." Nominal authority isn't enough: one
  study found this same "the human has final say" assumption unrealistic in
  practice, without real guidelines or training behind it. [2]

- **Will the reviewer stay sharp enough to catch mistakes?** "Physical skills
  deteriorate when they are not used," and a formerly experienced operator who
  has only been monitoring an automated process may no longer be one: their
  oversight decays right when it's needed most. [3]

- **Is this a domain where oversight isn't optional?** High-stakes or regulated
  uses (credit, employment, essential services) legally require a human. And ask
  who's accountable when it's wrong: Air Canada was held liable for its own
  chatbot's invented policy. [4]

- **Are there red lines you hold regardless of capability?** A newsroom might
  simply decide to bar AI from fact-checking or generating news images
  entirely, a decision made on values, not on how good the tool is.

For another perspective, Google's design guidance names four situations to keep a human checkpoint regardless of how good the AI is:

- The task has real physical, emotional, or financial stakes
- It's something the person enjoys doing
- There's a social obligation to be present for it
- It depends on idiosyncratic taste that's hard to actually standardize, like editing. [5]

**Sources**
1. https://www.nature.com/articles/s41562-024-02024-1 — Vaccaro, Almaatouq & Malone, "When combinations of humans and AI are useful: A systematic review and meta-analysis," Nature Human Behaviour, Oct. 28 2024: meta-analysis of 106 studies found human-AI combinations "performed significantly worse than the best of humans or AI alone" (Hedges' g = -0.23); the loss was concentrated in decision tasks (g = -0.27, significant), while creation/content-generation tasks showed synergy gains (g = 0.19).
2. https://www.benzevgreen.com/wp-content/uploads/2019/02/19-fat.pdf — Ben Green & Yiling Chen, "Disparate Interactions: An Algorithm-in-the-Loop Analysis of Fairness in Risk Assessments," FAT* '19 (ACM): "Many proponents defend the deployment of risk assessments on the grounds that judges have the final say and can discern when to rely on the predictions provided... But our results indicate that this is an unrealistic expectation," and separately, "the current approach of presenting predictions to judges without sufficient guidelines or training comes with the issues of poor interpretation and disparate interactions."
3. https://www.sciencedirect.com/science/article/abs/pii/0005109883900468 — Lisanne Bainbridge, "Ironies of Automation," Automatica 19(6), 1983, pp. 775-779: "physical skills deteriorate when they are not used... This means that a formerly experienced operator who has been monitoring an automated process may now be an inexperienced one. If he takes over he may set the process into oscillation."
4. https://www.forbes.com/sites/marisagarcia/2024/02/19/what-air-canada-lost-in-remarkable-lying-ai-chatbot-case/ — Forbes, Feb 19 2024, and Canada's Civil Resolution Tribunal ruling: Air Canada argued its chatbot was a separate legal entity responsible for its own actions. The tribunal rejected this, ordering a $650.88 refund and ruling Air Canada fully responsible for the chatbot's output.
5. https://pair.withgoogle.com/chapter/feedback-controls/ — Google PAIR Guidebook, Feedback + Control chapter: keep a human checkpoint for high physical/emotional/financial stakes, task enjoyment, personal/social obligation, or idiosyncratic creative vision hard to specify in a prompt.


## 2. Human-in-the-loop in Practice

Full Fact, a 15-journalist fact-checking newsroom, draws an explicit line around automating the high-volume filtering, never automate the judgment call.

**Fully automated**: Topic classification, claim extraction, ranking which claims are worth checking, matching against past fact-checks. [1]
**Never automated**: Deciding if a claim is actually true, and writing the published fact-check. "We never ask it 'Is this claim true?' because no model can reliably answer that." [2]

AP's own newsroom rule states the same idea plainly: any AI output is "unvetted source material," staff still apply normal sourcing standards before it goes anywhere near publication. [3]


**Sources**
1. https://fullfact.org/blog/2025/feb/how-ai-can-help-fact-checkers/ — Full Fact, Feb 11 2025: fully automated tasks include topic classification, claim extraction and labeling, checkworthiness scoring, media monitoring, and claim-matching against a database of prior fact-checks.
2. https://fullfact.org/blog/2025/feb/how-ai-can-help-fact-checkers/ — Full Fact: "We never ask it Is this claim true? because no model...can reliably answer that as it depends on real-world knowledge and reasoning." The actual writing is done by fact checkers, reviewed and edited by colleagues.
3. https://www.poynter.org/ethics-trust/2023/new-ap-stylebook-guidelines-artificial-intelligence-chatgpt/ — Poynter, Aug 16 2023, on AP's guidelines: "Any output from a generative AI tool should be treated as unvetted source material. AP staff must apply their editorial judgment and AP's sourcing standards when considering any information for publication."

## 3. Humans can make things better or worse

**Zillow Offers** originally had pricing experts vet every algorithm-generated home value estimate. Under growth pressure in 2021, "Project Ketchup" explicitly barred those experts from adjusting the algorithm's numbers. Purchase volume doubled the next quarter. Then the algorithm's blind spots, no longer caught by anyone, caught up: a $421 million loss in a single quarter, the business shut down, about 25% of the company laid off.[1]

This doesn't mean that automation beats humans. It means that whether you keep the human or remove them, it's a specific, testable design choice for each task, not a value you apply uniformly everywhere.

**Sources**
1. https://jise.org/Volume35/n1/JISE2024v35n1pp67-72.pdf — Gudigantala & Mehrotra, "When Strength Turns Into Weakness," Journal of Information Systems Education 35(1), Winter 2024. Zillow's "Project Ketchup" barred pricing experts from adjusting the algorithm's home value estimates in early 2021. Purchase volume more than doubled the next quarter, followed by a $421M Q3 2021 loss, the business unit shut down, about 25% of workforce laid off.

## 4. Same Judgment, When You're the One Coding

Full Fact deciding which claims are worth checking, and Zillow's removed pricing checkpoint, are versions of the same decision you make constantly while you build. Does this particular step need a human, or can it run on its own?

A formatting fix Claude proposes is cheap to undo and easy to verify at a glance. Let it commit. A change to how your app handles user data or credentials is expensive to undo and hard to verify just by reading a summary. That one is worth reviewing line by line before it ships, even if it slows you down. 

Plan Mode, from Day 2, is built around this same choice. It's a checkpoint you add on purpose before a costly action, not because you don't trust the tool, but because reviewing the plan is where you catch a wrong assumption while it's still cheap to fix. And it deepens your expertise and understanding, which means you can explain it, like we discussed in Safe & Auditable Design.

Sometimes the right call is to read every line anyway, even on a low-stakes change, because doing so is how you actually learn what your own codebase does. That's the same tradeoff from Section 01. Not every checkpoint exists to catch an error. Some exist because you're the one who benefits from being in the loop.

> **Exercise: Apply This**
> - Time: While coding
> - Description: As we move into coding time, ask yourself what parts of your project are currently automated, checkpointed, or fully manual? Using the questions from Section 01, ask yourself whether that's actually the right call for this stage, or did you default without deciding?
> - Deliverable: Deliberateness in your human-ai design choices
