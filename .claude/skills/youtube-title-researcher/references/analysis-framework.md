# Title Analysis Framework

## Metrics to Collect Per Video

| Field | How to Get It |
|-------|---------------|
| Title | From search results |
| Channel | From search results |
| Views | From search results metadata |
| Age | From search results ("X days/weeks ago") |
| Subscriber count | From search results (vidIQ overlay or channel page) |
| Views/Sub ratio | Calculate: views / subscribers — the key normalization metric |
| VPH (views per hour) | From vidIQ overlay if available |

**Views/Sub ratio benchmarks:**
- **> 1.0x** = Viral outlier (title/topic is doing massive work)
- **0.3x - 1.0x** = Strong performer
- **0.1x - 0.3x** = Average for niche
- **< 0.1x** = Underperforming (channel size carried it)

## Title Pattern Categories

When analyzing titles, classify each into one or more of these patterns:

### Authority Patterns
- **Credential authority**: "How I Use X (Job Title/Company)" — e.g., "(Meta Staff Engineer Tips)"
- **Brand authority**: "Anthropic Just [verb]..." — company name as source
- **Expert framing**: "Pro Tips", "Advanced", "Master"

### Emotional Hook Patterns
- **Negative hook**: "You're Using X Wrong", "Stop Doing X"
- **Superlative claims**: "Insane", "Crazy", "Mind-Blowing"
- **Outcome promises**: "10x Your Productivity", "Unfair Advantage"
- **Third-person reaction**: "His/Their Workflow Is Insane"
- **Regret hook**: "I Wish I Knew From the Start"

### Structural Patterns
- **Number lists**: "10 Tips", "8 Use Cases", "5 Features"
- **Time-constrained**: "in 7 Minutes", "in 13 Mins"
- **Definitive**: "The Only Tutorial You Need"
- **News/update**: "Just Added", "Just Dropped", "New"
- **How-to**: "How to Use X", "How I Use X"

### Underperforming Patterns (avoid)
- **ALL CAPS hype**: "Just Changed EVERYTHING" — feels overdone
- **Curiosity gap**: "Nobody's Talking About" — too vague in this niche
- **Explained/educational**: "X Explained" — consistently underperforms
- **Trailing ellipsis**: "The BEST FEATURE is..." — cliffhanger fatigue
- **Pipe format**: "Title | Subtitle" — underperforms clean titles

## Search Queries to Use

Run these YouTube searches filtered to **"This month"** + **"Videos"**:

1. `"claude code" tips workflow` — catches tutorial/workflow content
2. `"claude code" new update features` — catches update/news content
3. `"claude code" tutorial beginner` — catches intro content
4. `claude code agent teams` — catches specific feature content

Sort by relevance (default) rather than view count — YouTube's relevance sort surfaces the niche-relevant results better than pure view count which gets polluted by large general channels.

## Output Format

Save findings to `youtube/ab-tests/competitive/YYYY-MM.md` using this structure:

```markdown
# Competitive Title Research: [Month Year]

**Date:** YYYY-MM-DD
**Search method:** YouTube search filtered to this month, multiple query variations
**Niche:** Claude Code CLI tutorials, updates, workflows

---

## Top Performing Videos (adjusted for channel size)

| Title | Channel | Views | Subs | Views/Sub Ratio |
|-------|---------|-------|------|-----------------|
| ... | ... | ... | ... | ... |

---

## Pattern Analysis

### What's working
[List patterns with evidence]

### What's NOT working
[List patterns with evidence]

---

## New Title Hypotheses to A/B Test

### High Priority (strong evidence)
1. ...

### Medium Priority
2. ...
```
