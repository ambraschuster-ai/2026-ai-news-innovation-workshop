# Build Time

> An extra build block before lunch. Take one thing from this morning and actually ship it.

## 1. Get Set Up: Deploy to Vercel

Before you build, get a live URL for your project. This is the same platform this workshop site itself deploys on.

- Go to [vercel.com/signup](https://vercel.com/signup) and sign up with your GitHub account, the same one from Day 1 setup. It's free.
- Click **Add New** > **Project**, then find and import the repo your project actually lives in.
- If your project's code is in a subfolder rather than the root of that repo, for example your submission folder inside the class repo, expand **Root Directory** in the import settings and point it at that subfolder before deploying.
- Leave the framework and build settings on their auto-detected defaults unless you know they're wrong, then click **Deploy**.
- Once it finishes, Vercel gives you a live `.vercel.app` URL. Save it, you'll want it for your submission card later.

If the deploy fails, that's normal and part of the exercise. Paste the error into Claude Code and ask it to help you fix it.

## 2. Apply What You Just Covered

50 minutes is enough to actually build something, not just talk about it. Use it that way.

Safe & Auditable Design and Human-AI Design both gave you a framework, not just a lecture. Now's the time to turn one piece of either into real, working code, not a plan for later.

- From Safe & Auditable Design's checklist: do you actually have a kill switch, or a place a user can flag a wrong answer?
- From Human-AI Design: is there a step in your product that's currently fully automated but should have a human checkpoint, or the reverse, a checkpoint that's slowing things down for no real safety reason?
- From the disclosure patterns you just saw: could you add even the simplest version, an info button or a one-line label, right now?

Pick one. Something small enough to actually finish in this window, not something that spawns three more decisions before you can start.

## 3. Build

> **🛠️ Build Time**
> - Time: The rest of this session.
> - Description: Implement one specific decision from this morning, a kill switch, a human checkpoint, a disclosure pattern, actually working in your project, not just planned.
> - Deliverable: Something concrete to point at. Ideally something Final Coding Time this afternoon can build on rather than repeat.
