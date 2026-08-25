# CLAUDE.md

> One file, read at the start of every session. It's the difference between explaining your project to Claude once and explaining it every single time.

## 1. What It Is

CLAUDE.md is a plain-text file Claude reads automatically at the start of every session. [1] Every Claude Code session starts with an empty context window. Without this file, you're re-explaining your project's conventions, commands, and quirks from scratch, every time. [2]

A simple test for whether something belongs in yours: has Claude made the same mistake twice, or have you typed the same correction into chat more than once? That's the signal. [3]

CLAUDE.md is for what's true every time you open a new chat. It's foundational context. If something's only relevant sometimes, a specific kind of task you do occasionally, that's what Skills are for instead. [4]

**Sources**
1. https://code.claude.com/docs/en/memory — Claude Code Docs, "How Claude remembers your project": CLAUDE.md files are markdown files that give Claude persistent instructions for a project, your personal workflow, or your entire organization. Claude reads them at the start of every session.
2. https://claude.com/blog/using-claude-md-files — Anthropic blog, Nov 25 2025, "Using CLAUDE.md files": think of it as a configuration file that Claude automatically incorporates into every conversation, ensuring it always knows your project structure, coding standards, and preferred workflows.
3. https://code.claude.com/docs/en/memory — Claude Code Docs: add to CLAUDE.md when Claude makes the same mistake a second time, a code review catches something Claude should have known, or you type the same correction into chat that you typed last session.
4. https://code.claude.com/docs/en/best-practices — Claude Code Docs, Best Practices: "For domain knowledge or workflows that are only relevant sometimes, use skills instead" of CLAUDE.md.

## 2. A Real Example

This workshop's own repository has a CLAUDE.md file. It's not a hypothetical, it's the actual file governing how this website gets built. [See it on GitHub](https://github.com/AndrewRCalderon/2026-ai-news-innovation-workshop/blob/main/CLAUDE.md), or open the whole thing right here.

Three things worth noticing about it, and worth copying into your own:

**It points, it doesn't duplicate**: Instead of listing every task, it says: read `project/tasks.md` for what's open right now. The file stays short because it delegates to other files rather than repeating their contents.
**It states what can't be inferred from code**: A rule like "any non-trivial technical decision gets a new numbered file in `project/adr/`" isn't something Claude could guess by reading the codebase. That's exactly the kind of thing that belongs here.
**It's organized by when you'd need it**: Sections for "before starting work," "while working," and "repo layout" map to the actual moments in a session, not an abstract table of contents.

[Embedded file viewer, inline collapsible: shows this repo's actual `CLAUDE.md`, verbatim. Not something to edit here; edit the actual CLAUDE.md file if it needs to change.]

That's the shape worth copying, whatever your own project is about: point instead of duplicate, write down what Claude can't guess on its own, and organize around when you'll actually need each part. It's also the place to document decisions your team has already made about the product itself, the tone of the language across your site, words to avoid, or a commitment to only use certain kinds of tools. The decisions in your file might come from a design system, an audience persona, or a build process like this one, the habit is the same either way.

## 3. What Belongs In One

The most common mistake isn't leaving something out. It's putting too much in. [1]

A CLAUDE.md is a record of decisions your whole team has already made, so Claude doesn't have to guess at them or get them re-explained every session.

**Include**
- Decisions Claude can't guess on its own, a command, a required step, a deadline
- Your design system, fonts, colors, spacing, so pages built with Claude match on the first try
- What you know about your audience, personas, reading level, assumptions, so writing and design choices don't need re-explaining either
- Structural decisions specific to your project
- A gotcha you've already hit once, so it doesn't happen twice

**Leave out**
- Anything Claude can already figure out by looking at the project itself
- Long explanations of tools Claude already knows how to use
- Detailed documentation, link to it instead of copying it in [2]
- Information that changes often, an outdated CLAUDE.md is worse than a short one [3]
- Self-evident practices, like "write clean code"
- Credentials or anything sensitive, especially if this file is shared with others

### Before You Add a Line

- Would removing this line actually cause Claude to make a mistake? If not, cut it. [4]
- Could Claude figure this out just by looking at the project itself, without you writing it down? [5]

**Sources**
1. https://code.claude.com/docs/en/best-practices — Claude Code Docs, "Best practices for Claude Code": bloated CLAUDE.md files cause Claude to ignore your actual instructions. Target under 200 lines per file, longer files consume more context and reduce adherence.
2. https://code.claude.com/docs/en/best-practices — Claude Code Docs, "Write an effective CLAUDE.md" table, Exclude column: "Detailed API documentation (link to docs instead)".
3. https://code.claude.com/docs/en/best-practices — Claude Code Docs, same table, Exclude column: "Information that changes frequently."
4. https://code.claude.com/docs/en/best-practices — Claude Code Docs: for each line, ask "would removing this cause Claude to make mistakes?" If not, cut it.
5. https://code.claude.com/docs/en/memory — Claude Code Docs, on the /doctor command for oversized CLAUDE.md files: it "cuts content Claude can derive from the codebase, such as directory layouts, dependency lists, and architecture overviews, and keeps pitfalls, rationale, and conventions that differ from tool defaults."

## 4. Write Your Own

Claude Code can generate a starting CLAUDE.md by analyzing your project directly, with the `/init` command. [1] For this workshop, you didn't start blank: [STUDENT_CLAUDE_GUIDE.md](https://github.com/AndrewRCalderon/2026-ai-news-innovation-workshop/blob/main/STUDENT_CLAUDE_GUIDE.md) is already sitting in your `docs/submissions/your-name/` folder as `CLAUDE.md`, copied there yesterday during Fork & Submit. Today's task is reviewing it, not introducing it: ask Claude to update it based on what it actually observed about how you worked yesterday, instead of writing everything from scratch. Either way, it should keep growing from the actual friction points & insights in your workflow, not a theoretical checklist. [2]

> **Exercise: Update Your CLAUDE.md**
> - Time: ~15 minutes.
> - Description: Open the `CLAUDE.md` already in your `docs/submissions/your-name/` folder. Ask Claude to review your Day 1 session and update the file: what did it notice about technical decisions that you made, what you already understood without needing it explained, where you got stuck? Also ask whether every guardrail in the file still earns its place — a day of experience in, some of it (like the onboarding questions about explaining basic terms) might already be more scaffolding than you need. Don't write the changes yourself first.
> - Deliverable: Read what Claude changed. Pick two or three edits and, for each one, ask yourself whether it's something you actually told Claude directly, or something it inferred from a pattern in how you worked that you weren't even aware of. Share what stood out to you.

**Sources**
1. https://code.claude.com/docs/en/memory — Claude Code Docs: the /init command generates a starting CLAUDE.md by analyzing the codebase; re-run it to get improvement suggestions rather than overwrite.
2. https://claude.com/blog/using-claude-md-files — Anthropic blog: start simple with basic project structure, then expand based on actual friction points in your workflow. Your file should reflect how your team actually develops software, not theoretical best practices that sound good but don't match reality.
