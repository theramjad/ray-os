---
name: linkedin-post-writer
description: Navigate LinkedIn and create posts via Chrome browser automation. Use when Claude needs to browse LinkedIn feed, view profiles, analyze posts, or compose and publish LinkedIn posts. Triggers on requests like "go to LinkedIn", "write a LinkedIn post", "post on LinkedIn", "check my LinkedIn", "browse LinkedIn feed", or any LinkedIn-related browser task. Also triggers when the user wants to review post performance or update engagement data. Requires Chrome browser automation tools (mcp__claude-in-chrome__*).
---

# LinkedIn Post Writer

## Feedback Loop (Run Every Session)

On every skill trigger, before doing anything else:

1. Read `references/post-history.md`
2. Check for posts with status `posted` but no engagement data
3. If any exist, ask the user: "Last time you posted [title/hook]. How did it do? (reactions, comments, reposts)"
4. Update the post entry with the reported metrics
5. Check for posts with status `draft` — ask "Did you end up posting [hook]?"
   - If yes → update status to `posted`, ask for metrics next session
   - If no → update status to `skipped`
6. After collecting data, briefly note any pattern emerging (e.g., "Your personal story posts average 2x the reactions of your how-to posts")

Then proceed with whatever the user asked for.

## Post History

All generated posts are logged in `references/post-history.md`. Each entry includes:

- Date generated
- Hook (first line)
- Full text
- Archetype used (from the 8 viral archetypes)
- Media type suggested
- Status: `draft` | `posted` | `skipped`
- Engagement: reactions, comments, reposts (filled in later)
- Notes: what worked, what didn't (filled in later)

After generating a post, always:
1. Append it to `references/post-history.md`
2. Ask the user: "Want me to post this, or are you going to post it yourself?"
3. If they want Claude to post → see `references/browser-navigation.md` for how
4. Either way, log the post with appropriate status

## Writing Viral Posts

When composing posts, apply patterns from two sources:

1. **General patterns:** `references/viral-playbook.md` — hook formulas, formatting, 8 archetypes, media ranking
2. **Personal performance data:** `references/post-history.md` — what actually works for this user's audience

Prioritize patterns that have proven engagement in the user's own history over general best practices. If the user has 5+ posts with data, note which archetypes and hooks performed best for them specifically.

## References

- `references/viral-playbook.md` — Hook formulas, formatting rules, 8 viral archetypes, media ranking, CTAs
- `references/post-history.md` — Log of all generated posts + engagement tracking
- `references/browser-navigation.md` — How to navigate LinkedIn via Chrome automation (feed, profiles, posting)
