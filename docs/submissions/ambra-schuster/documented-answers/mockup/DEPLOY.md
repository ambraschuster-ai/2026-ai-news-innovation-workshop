# Deploying the mockup

Goal: a link you can send to classmates, with your API key server-side and a
hard ceiling on what it can spend.

**Host: Render.** Free tier, deploys straight from GitHub, holds secrets
properly, runs a plain Python process (which this needs — the answers stream,
and serverless hosts fight that). You need one thing you don't already have: a
Render account, which you make with your GitHub login. No card required on the
free plan.

The free plan sleeps after 15 minutes of no traffic and takes 30–60 seconds to
wake. For classmates clicking a link, that's a slow first load and then it's
fine.

---

## Before you push

Two files must never reach GitHub. Both are already in `.gitignore`:

| file | why it stays out |
|---|---|
| `mockup/.env` | your API key |
| `mockup/corpus.json` | Documented's article text — theirs, not ours to republish |

Verify it yourself rather than trusting this file:

```bash
git check-ignore -v docs/submissions/ambra-schuster/documented-answers/mockup/.env docs/submissions/ambra-schuster/documented-answers/mockup/corpus.json
```

Both must print a matching rule. If either prints nothing, stop.

---

## Deploy

1. Push the branch to GitHub.

2. Render → **New** → **Blueprint** → pick this repo. It reads
   [`render.yaml`](render.yaml) and fills in the build and start commands.

3. **Environment → Environment Variables**, add:

   - `ANTHROPIC_API_KEY` — your key. Paste it here and nowhere else.

4. **Environment → Secret Files**, add one file:

   - Filename: `corpus.json`
   - Contents: paste all of your local `mockup/corpus.json`

   This is how the articles get to the server without going through git.
   It is about 283 KB — a long paste, but well inside Render's limit. Check
   the saved file's size afterwards; a truncated paste produces a bot that
   silently knows less than the banner says it does.

5. Deploy. When it's live, open the URL and check `/healthz` returns
   `{"ok":true}`.

---

## Set your own spend ceiling

The app's limits are the first line; this is the backstop that doesn't depend
on my code being right.

In the [Anthropic Console](https://console.anthropic.com): **Settings →
Limits** to cap monthly spend for the workspace, and **Settings → Billing** to
check what's actually been used. Set the cap at whatever number you'd be
annoyed but not hurt to lose — $5 is plenty for this.

Do this before you send anyone the link. It's the only limit that still holds
if the app has a bug.

Also worth doing: make this key a **separate key** used only for this app, so
you can revoke it without breaking anything else. Console → API Keys → Create
Key.

---

## The limits in the app

Set as environment variables, changeable in the Render dashboard without a
code change:

| variable | default | what it does |
|---|---|---|
| `MAX_PER_SESSION` | 15 | messages per visitor before it stops and tells them |
| `MAX_PER_DAY` | 150 | total messages across everyone, resets at UTC midnight |

Both fail closed — when the budget is gone, no API call is made at all.

---

## What is and isn't stored

Nothing is written to disk. Conversations live in the server's memory, keyed by
a cookie, and are dropped after an hour of silence or when the process
restarts — which on the free plan is every time it sleeps. There is no request
log; that's turned off deliberately in `serve.py`.

So there's no record of who asked what. For a bot that immigrants might type
real questions into, that is the correct default, and it's the same principle
Project 5 in the main plan is built around.

---

## Taking it down

Render dashboard → the service → **Settings** → **Suspend** (stops it, keeps
the config) or **Delete**. Then revoke the key in the Anthropic Console.
