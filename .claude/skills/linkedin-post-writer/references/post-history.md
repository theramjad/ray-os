# LinkedIn Post History

Track all generated posts and their performance to learn what works.

## Posts

<!-- New posts are appended below. Format:

### YYYY-MM-DD — [Hook first line]
- **Archetype:** [one of the 8 archetypes]
- **Media:** [text/carousel/image/video/none]
- **Status:** draft | posted | skipped
- **Engagement:** reactions: — | comments: — | reposts: —
- **Notes:** —

**Full text:**
> [complete post text]

-->

### 2026-02-24 — "i woke up to IBM down 10% and spent the morning reading about COBOL."
- **Archetype:** The News + Insight
- **Media:** text only
- **Status:** posted
- **Engagement:** reactions: — | comments: — | reposts: —
- **Notes:** —
- **URL:** https://www.linkedin.com/feed/update/urn:li:activity:7431926133006426112/

**Full text:**
> i woke up to IBM down 10% and spent the morning reading about COBOL.
>
> turns out 90% of all money in circulation runs on it. $50+ trillion sitting on mainframes programmed by people who retired before i was born.
>
> nobody modernized these systems because nobody could afford to understand them first. the knowledge walked out the door with the original developers and never came back.
>
> Anthropic just announced Claude can read COBOL codebases, map the dependencies, and document the business logic.
>
> twitter is split between "this is the biggest thing ever" and "lmao good luck touching a system that processes $3 trillion a day." honestly both reactions make sense to me.
>
> the part that sticks with me: this is the third time in 2026 that Anthropic shipped a feature and an entire industry lost billions in market cap within hours. IBM, CrowdStrike, Adobe. it's February.
>
> i don't know what that means exactly. but i know i've never seen anything move markets like this before. not a company, not a product. a capability.

### 2026-02-25 — "anthropic just turned your phone into a remote for your computer."
- **Archetype:** The News + Insight
- **Media:** text only
- **Status:** posted
- **Engagement:** reactions: — | comments: — | reposts: —
- **Notes:** Based on remote control video (y3xzYwxQuHc). Covers claude rc, phone control, security/sandbox angle, Hetzner server tip.
- **URL:** https://www.linkedin.com/feed/update/urn:li:activity:7432426590422343680/

**Full text:**
> anthropic just turned your phone into a remote for your computer.
>
> claude code shipped remote control. you run `claude rc` in a folder on your machine, open the Claude app on your phone, and you're coding from anywhere.
>
> i tested it by having it edit a video for me while i started a second session on another project. from my phone. sitting on my couch.
>
> here's what makes it actually useful:
>
> → all your skills, MCP servers, and config carry over. whatever you've set up locally just works remotely.
>
> → you can approve permissions from your phone. no more SSH + tmux hacks.
>
> → plan mode works too. so you can kick off research tasks on the go and answer follow-up questions from lunch.
>
> the security angle is the interesting part though.
>
> if you don't want to run bypass permissions on your main machine, spin up a $3.50/month Hetzner server. install claude code there. run it with dangerously skip permissions in a sandbox. set up a proxy that only allows specific URLs.
>
> now you have a remote research agent that can't touch your local files. even if it gets prompt injected, the blast radius is one throwaway server.
>
> the one thing it's missing vs OpenClaw: it's passive, not proactive. you tell it what to do. it doesn't ping you on a schedule.
>
> but given how fast anthropic is shipping, i'd bet that's coming.
