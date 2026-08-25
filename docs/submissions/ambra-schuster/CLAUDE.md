# CLAUDE.md

> Starting instructions for the project you build during this workshop. Copy this into your own project as `CLAUDE.md`. Keep what's useful, edit what isn't, and let it grow as you learn what you and Claude keep having to repeat to each other.

## Where this file kicks in

This file gets copied into your project folder (`docs/submissions/your-name/`) during Day 1's Fork & Submit, so it may already be active from Day 1, in Claude Desktop's Code tab (same engine as Claude Code, just inside Desktop). Starting Day 2, you're working in VS Code with the Claude Code extension instead, and GitHub Desktop becomes your connection to GitHub — but it's the same file, in the same folder, the whole time.

## Where my work goes

- Everything I build on the `day-2` branch belongs inside `docs/submissions/ambra-schuster/`. That folder is the whole workspace — create, move, and edit files only in there.
- Don't add or change files elsewhere in the repo. The site's own directories (`docs/` outside my submission folder, `project/`, `api/`, root-level config) belong to the workshop maintainers, not to me.
- If something I ask for seems to require touching a file outside my folder, stop and tell me what and why before doing it, rather than reaching outside on your own.
- New sub-projects go in as subfolders of my submission folder — not at the repo root, and not with their own nested `.git` directory, which stops this repo from tracking them.

## The Documented NY project — read these first

The project I'm building lives in `documented-answers/`. It's split into
five projects. **Each one has its own three files**, and they are the source
of truth — not `PLAN.md`, which is the original research and background, and
not this file.

| Project | Status | Docs |
|---|---|---|
| 1 — Archive & audit | Paused (Stage 0.1 done) | [requirements](documented-answers/project-1-archive-audit/requirements.md) · [architecture](documented-answers/project-1-archive-audit/architecture.md) · [tasks](documented-answers/project-1-archive-audit/tasks.md) |
| 2 — Freshness engine | Not started | [requirements](documented-answers/project-2-freshness-engine/requirements.md) · [architecture](documented-answers/project-2-freshness-engine/architecture.md) · [tasks](documented-answers/project-2-freshness-engine/tasks.md) |
| **3 — Retrieval + answer engine** | **Active** — see `documented-answers/mockup/` | [requirements](documented-answers/project-3-answer-engine/requirements.md) · [architecture](documented-answers/project-3-answer-engine/architecture.md) · [tasks](documented-answers/project-3-answer-engine/tasks.md) |
| 4 — Channels + voice | Not started | [requirements](documented-answers/project-4-channels-voice/requirements.md) · [architecture](documented-answers/project-4-channels-voice/architecture.md) · [tasks](documented-answers/project-4-channels-voice/tasks.md) |
| 5 — Listening loop | Not started | [requirements](documented-answers/project-5-listening-loop/requirements.md) · [architecture](documented-answers/project-5-listening-loop/architecture.md) · [tasks](documented-answers/project-5-listening-loop/tasks.md) |

**Currently building Project 3.** The working mockup in
`documented-answers/mockup/` answers, cites, dates and refuses over 38 of
Documented's resource articles in English and Spanish. Its Stage 0 in
`project-3-answer-engine/tasks.md` records what it does and — just as
important — what it deliberately does not, so the mockup isn't mistaken for
progress on the real build. Project 1 is paused after its Stage 0.1 rescue.

Not yet decided, and both are mine to make: whether to host on Render (what
it's built for) or Vercel (what my instructor suggested), and whether the
page keeps Documented's name and styling.

Read the active project's three files at the start of every session, and
another project's docs only when I say we're moving to it. Projects 2, 4 and
5 are written at planning depth, so don't treat their details as settled —
they get rewritten before that project starts.

### How to work against these files

- **Before building anything**, propose a plan against the active project's
  `requirements.md` and `architecture.md`, and let me see it first. Don't
  start from your own read of what the project needs.
- **Don't decide on your own that something looks done.** Check it against
  the specific *Done when* line in `tasks.md`. If that line isn't literally
  true yet, the task isn't finished — say so instead of moving on.
- **Check tasks off in `tasks.md`** as they're actually completed, and add
  newly discovered work to the right stage rather than letting it float.
- **If the work wants to go outside what `requirements.md` says**, stop and
  tell me. That includes drifting into another project's scope — each
  `requirements.md` has an explicit "out of scope" section, and those
  boundaries are deliberate, not oversights.
- **If a decision in `architecture.md` turns out to be wrong**, say so and
  we'll change the file. Don't quietly build something different from what
  it describes.
- **When something in these files goes stale**, update it in the same
  commit as the code that made it stale.

## How to explain things to me

Before we dive into real work, ask me a few quick questions so you know how much to explain, and how much to just get moving, as we go:

- When you hear a term like "API," "environment variable," "commit," or "dependency," do I already know what it means, or should you explain it the first time it comes up?
- When we're starting something new, or something breaks, do you want to get moving and explain after (a rough first version, a fix, whatever's fastest), or talk me through the plan or what went wrong before you touch anything?
- Do I want the "why" behind every technical choice you make, or only when it's non-obvious?

**My answers (Aug 25, 2026):**

- **Jargon:** explain a technical term the first time it comes up, briefly. After that, use it normally.
- **Working style:** depends on size. Small things, just do them. Anything substantial or hard to undo, check with me first. (This is also the default for how much to build before checking in.)
- **Reasoning:** only when I ask. Don't narrate the "why" behind routine choices.
- **Answer shape:** lead with the direct answer — usually one short sentence, yes or no where that fits — then the detail underneath. Plain words over technical ones. Use a short list or a small table when there are a few things to compare, not paragraphs. Keep the whole thing brief, and close with the question I actually need to decide, if there is one.

If I start asking for more or less than this, update these answers rather than guessing.

My answer to the second question is also your default for how much to build before checking in with me generally, not just for explanations, since it's really the same preference. Use my answers to calibrate, but don't treat them as fixed. Check back in occasionally, especially if I start using a term correctly that I didn't know before, or start asking for more or less than my first answers suggested.

After explaining something non-obvious, ask a short question that checks whether it actually landed, don't just move on to the next step. If I say I don't follow, give me the simplest version first, and only add detail if I ask for more.

## Things to watch for

- Never write an API key, token, or password directly into a file that isn't already covered by `.gitignore`. If you're about to, stop and tell me instead.
- Check that `.gitignore` actually covers `.env` and any credentials file before the first commit of a new project, not after.
- Keep the project folder organized as it grows. Don't let one-off scripts and test files pile up alongside real project code without flagging it so we can sort it out.
- Before a change that's expensive or awkward to undo, use Plan Mode and let me review the plan first, regardless of how I answered above — that's about risk, not about how much I want explained. A first rough scaffold of starter files for something brand new isn't what this is about, even if it's more than a file or two; match that instead to how I answered the "starting something new" question above.
- If I paste a real credential into chat by mistake, tell me immediately instead of quietly using it.

## Choosing the right model for the task

- Before starting a subtask, especially one you could hand off to a background agent, tell me the model options and the actual tradeoff between them for this specific task, in plain language, then let me choose. Don't just pick silently and move on.
- Keep it short. "I'd default to a smaller/faster model here because this is a quick lookup, want me to use something else?" is enough, it doesn't need to be a lecture every time.
- If I ask why you'd choose a given model, or what my options are, answer with the actual tradeoff (speed/cost vs. capability) for the task in front of us, not a generic explanation.

## Using git and GitHub

- Commit regularly, in small changes that each do one clear thing, with a real message that says why the change was made, not just what changed.
- For anything bigger than a quick fix, work in a branch and open a Pull Request rather than committing straight to `main`, even if I'm the only one who'll ever review it. It gives us a place to see the diff before it's permanent.
- Do this through GitHub Desktop, or ask Claude Code to run the git commands directly. Either is fine, use whichever feels more natural.
- Keep these habits even on a solo project. They're what make it possible to look back later and understand what got built and why, and they're the same habits a team project would need.

## Keeping submission info current

- `SUBMISSION.md` lives alongside this file in your `docs/submissions/your-name/` folder (copied there during Day 1's Fork & Submit). Fill it in as soon as there's a real direction, don't wait until the end.
- Keep it accurate as things change. If the pitch or what you're building shifts, update `SUBMISSION.md` in the same commit, don't let it go stale.
- If you restructure the project, keep `SUBMISSION.md` in that same folder and keep it filled in, rather than losing track of it in the shuffle.

---

Update this file as the project grows. If Claude makes the same mistake twice, or you find yourself typing the same correction more than once, that's the signal to add a line here.
