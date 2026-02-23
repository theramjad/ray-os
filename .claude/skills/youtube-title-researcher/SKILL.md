---
name: youtube-title-researcher
description: Research competing YouTube video titles in a niche to find high-performing title patterns and generate new A/B test hypotheses. Use when the user wants to analyze competitor titles, find what's getting views, research title ideas, or generate new title hypotheses for their YouTube channel. Triggers on requests like "research youtube titles", "what titles are working", "find competing videos", "title ideas for my next video", or "competitive title analysis".
---

# YouTube Title Researcher

Research competing YouTube videos via browser automation, extract title/view/channel data, analyze patterns, and generate new title hypotheses for A/B testing.

## Workflow

### 1. Search YouTube

Use browser automation (mcp__claude-in-chrome tools) to search YouTube. Open the Filters modal and select **"This month"** + **"Videos"** before browsing results.

Run multiple search queries to cover the niche. For Claude Code content, use:
- `"claude code" tips workflow`
- `"claude code" new update features`
- `"claude code" tutorial beginner`
- `claude code agent teams`

### 2. Collect Video Data

Scroll through results and record for each relevant video:
- **Title** (exact)
- **Channel name**
- **View count**
- **Age** (e.g., "3 weeks ago")
- **Subscriber count** (from vidIQ overlay or channel badge)

Calculate **Views/Sub ratio** = views / subscribers. This is the key metric — it normalizes for channel size so a 20k-view video on a 16K-sub channel (1.3x) ranks higher than a 200k-view video on a 900K-sub channel (0.22x).

### 3. Analyze Patterns

Read `references/analysis-framework.md` for the full framework of title patterns to look for, scoring benchmarks, and output format.

Cross-reference findings with existing A/B test results at `youtube/ab-tests/results.md` to identify:
- Which patterns align with proven winners
- Which patterns are new and worth testing
- Which patterns are underperforming despite popularity

### 4. Generate Hypotheses

Produce ranked title hypotheses (High / Medium / Lower priority) based on:
- **High**: Strong views/sub ratio evidence from multiple videos
- **Medium**: Works for 1-2 creators, plausible for the user's style
- **Lower**: Interesting but limited evidence

### 5. Save Output

Write findings to `youtube/ab-tests/competitive/YYYY-MM.md` using the template in `references/analysis-framework.md`.
