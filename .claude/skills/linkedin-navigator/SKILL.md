---
name: linkedin-navigator
description: Navigate LinkedIn and create posts via Chrome browser automation. Use when Claude needs to browse LinkedIn feed, view profiles, analyze posts, or compose and publish LinkedIn posts. Triggers on requests like "go to LinkedIn", "write a LinkedIn post", "post on LinkedIn", "check my LinkedIn", "browse LinkedIn feed", or any LinkedIn-related browser task. Also triggers when the user wants to review post performance or update engagement data. Requires Chrome browser automation tools (mcp__claude-in-chrome__*).
---

# LinkedIn Navigator

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
3. If they want Claude to post → follow the Posting workflow below
4. Either way, log the post with appropriate status

## Prerequisites

- Chrome browser automation tools (`mcp__claude-in-chrome__*`) must be available
- Get tab context first with `tabs_context_mcp`, then create or reuse a tab

## Navigation

### Feed

Navigate to `https://www.linkedin.com/feed/` to load the main feed.

LinkedIn uses heavily obfuscated CSS class names (CSS modules). Standard DOM selectors like `.feed-shared-update-v2` or `[data-urn]` return 0 results. Use these approaches instead:

- **Reading posts:** Use `get_page_text` for bulk text extraction, or `read_page` for accessibility tree
- **Expanding posts:** Click "...more" buttons via JavaScript:
  ```javascript
  document.querySelectorAll('button').forEach(btn => {
    const text = btn.textContent.trim().toLowerCase();
    if (text.includes('more') && (text.includes('…') || text.includes('...'))) btn.click();
  });
  ```
- **Scrolling:** Use incremental scrolling (`window.scrollBy(0, 1500)`) not `scrollTo(0, document.body.scrollHeight)` — LinkedIn virtualizes the feed and unloads off-screen posts
- **Extracting engagement data:** Use regex on page text: `/(\d[\d,]*)\s+others?\s+reacted/gi`

### Profiles

Navigate to `https://www.linkedin.com/in/{username}/` for profiles.

### Posting

Navigate to `https://www.linkedin.com/feed/` and use `find` to locate the post composer ("Start a post" button).

**Composing a post:**

1. Click "Start a post" to open the composer modal
2. Use `find` to locate the text input area
3. Use `form_input` or `computer` type action to enter text
4. For line breaks in posts, use Shift+Enter (plain Enter may submit or close)
5. To add media, click the image/document/video icons in the composer toolbar
6. Click "Post" when ready (requires explicit user permission per security rules)

## Writing Viral Posts

When composing posts, apply patterns from two sources:

1. **General patterns:** `references/viral-playbook.md` — hook formulas, formatting, 8 archetypes, media ranking
2. **Personal performance data:** `references/post-history.md` — what actually works for this user's audience

Prioritize patterns that have proven engagement in the user's own history over general best practices. If the user has 5+ posts with data, note which archetypes and hooks performed best for them specifically.
