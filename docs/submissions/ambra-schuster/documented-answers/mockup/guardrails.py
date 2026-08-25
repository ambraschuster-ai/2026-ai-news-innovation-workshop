"""
The two things the bot is never allowed to do, enforced in code.

These run before Claude sees the message. That placement is the whole point:
a system-prompt instruction is a request, and requests can be argued with.
This is a wall.

Deliberately narrow. A guardrail that fires on every mention of ICE would
swallow "Before ICE: A Guide for Parents at Risk of Deportation" -- an
article Documented wrote precisely so people could read it calmly, ahead of
time. The emergency rule looks for danger happening *now*.

On the phone numbers: this card lists only 911 and 311. Both are permanent
municipal numbers that will not change and cannot quietly go dead. A rapid
response hotline would be more useful and it is what this should eventually
carry -- but an unverified hotline number on a public page is worse than no
number at all, because someone in trouble spends their one phone call on it.
Nothing goes in here until a Documented editor has dialled it and signed off.
"""

import re

# Danger in progress -- present tense, happening to them, right now.
EMERGENCY = re.compile(
    r"""
    ( ice \s+ (is|are) \s+ (here|outside|at\s+my|at\s+the|in\s+my)
    | (they|ice|police) \s+ (are|is) \s+ (arresting|detaining|taking)
    | (being|getting) \s+ (arrested|detained|deported) \s* (right\s+now|now)?
    | raid \s+ (happening|now|in\s+progress)
    | just \s+ (got|been) \s+ (detained|arrested|picked\s+up)
    | just \s+ (detained|arrested|took|picked\s+up) \s+ my
    | (detained|arrested|took) \s+ my \s+ (husband|wife|son|daughter|mother|father|brother|sister|partner|dad|mom)
    | knocking \s+ (on|at) \s+ my \s+ door
    | ice \s+ (redada|esta\s+aqui|est[aá]\s+aqu[ií]|est[aá]n\s+aqu[ií])
    | (redada|migra) \s+ (ahora|aqu[ií]|en\s+mi)
    | (se\s+)?(lo|la|me)\s+ (llevaron|detuvieron) \s* (ahora|ahorita)?
    | acaban \s+ de \s+ (detener|arrestar)
    )
    """,
    re.I | re.X,
)

EMERGENCY_REPLY = """**If you are in immediate danger, call 911.**

I'm a bot that looks things up in Documented's articles, and this is not \
something to handle by reading an article. Please reach a person now:

- **911** — immediate emergency
- **311** — New York City's help line. Free, open 24 hours, and interpreters \
are available in over 175 languages. Ask them for immigration legal help.

I'm not going to search articles at you right now. Call one of those numbers, \
and come back later if you want help finding resources."""


# Asking the bot to predict or advise on their individual case.
# Note what is deliberately NOT here: "who qualifies for 3-K", "what are the
# requirements" -- those are answerable from the articles and should be.
LEGAL_ADVICE = re.compile(
    r"""
    ( will \s+ i \s+ (be \s+)? (get \s+)? (deported|denied|approved|removed)
    | (are|do) \s+ my \s+ chances
    | what \s+ are \s+ my \s+ chances
    | should \s+ i \s+ (apply|file|sign|appeal|accept|take \s+ the)
    | (is|will) \s+ (it|this) \s+ safe \s+ (for \s+ me \s+)? to \s+ (apply|file)
    | can \s+ they \s+ deport \s+ me
    | (me\s+)? (van\s+a|pueden) \s+ deportar
    | debo \s+ (aplicar|solicitar|firmar|apelar)
    | qu[eé] \s+ (posibilidades|probabilidad)
    )
    """,
    re.I | re.X,
)

LEGAL_ADVICE_REPLY = """I can't answer that one, and I want to be straight with \
you about why: that depends on the specifics of your case, and getting it wrong \
could hurt you. It needs a real immigration lawyer, not a bot.

For free, confidential immigration legal help in New York, call **311** and ask \
for **ActionNYC**. It's free, it's in your language, and they don't ask about \
your status.

What I *can* do is find what Documented has written about how a program works, \
who it's for, or what documents it asks for. Ask me that way and I'll look."""


def check(message):
    """Returns {'rule', 'reply'} to short-circuit, or None to let it through."""
    if EMERGENCY.search(message):
        return {"rule": "emergency", "reply": EMERGENCY_REPLY}
    if LEGAL_ADVICE.search(message):
        return {"rule": "legal-advice", "reply": LEGAL_ADVICE_REPLY}
    return None


if __name__ == "__main__":
    cases = [
        ("ICE is at my door", "emergency"),
        ("they just detained my husband", "emergency"),
        ("hay una redada ahora en mi edificio", "emergency"),
        ("Will I be deported if I apply?", "legal-advice"),
        ("¿me pueden deportar?", "legal-advice"),
        ("Should I apply for asylum?", "legal-advice"),
        # Must NOT fire -- these are answerable from the articles.
        ("What should I do to prepare in case ICE detains me?", None),
        ("Who qualifies for Promise NYC?", None),
        ("How do I enroll my daughter in pre-K?", None),
        ("¿Cómo inscribo a mi hijo en la escuela?", None),
    ]
    bad = 0
    for text, expected in cases:
        got = check(text)
        rule = got["rule"] if got else None
        ok = rule == expected
        bad += not ok
        print(f"{'ok ' if ok else 'FAIL'}  {rule or '(passes through)':<18} {text}")
    print(f"\n{len(cases) - bad}/{len(cases)} correct")
