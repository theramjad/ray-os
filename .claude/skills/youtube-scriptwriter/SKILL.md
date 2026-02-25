---
name: youtube-scriptwriter
description: Turn feature announcements, changelogs, or release notes into view-optimized YouTube video outlines. Use when the user pastes a changelog, feature announcement, release notes, or describes a new feature and wants help planning how to structure a video about it. Triggers on requests like "plan a video about this", "how should I cover this feature", "structure a video for this changelog", "scriptwrite this", or when the user pastes release notes and asks for a video angle. Also use when analyzing why a competitor video outperformed and extracting structural lessons.
---

# YouTube Scriptwriter

Turn raw feature info into a video outline structured for maximum views.

## Workflow

### 1. Digest the Feature Info

The user will paste one of:
- A changelog or release notes
- A tweet or announcement
- A docs page or blog post
- A verbal description of a new feature

Extract from it:
- **What's new** — list every distinct feature or change
- **What's big** — which feature has the most viewer appeal?
- **What's demoable** — which features produce visible, tangible output on screen?

### 2. Decide: One Video or Multiple?

If the input contains multiple features, decide whether to split:
- **One standout feature** that's demoable → make that the video, mention the rest briefly or save for a roundup
- **Multiple small features**, none dominant → update roundup format
- **Two comparable features** → potential comparison angle between them

Default: fewer videos with stronger angles beat more videos with weaker angles.

### 3. Pick the Format

Read `references/video-formats.md` for the full framework.

Choose based on the feature:

| Feature type | Best format | Example |
|---|---|---|
| New capability that changes workflow | Experiment/Comparison (old way vs new way) | "Agent teams" → build same app with and without |
| New tool or integration | Build-Along (build something cool with it) | "Browser control" → automate a real task live |
| Improvement to existing feature | Deep Dive (before/after + why it matters) | "Better planning" → show the difference in output quality |
| Multiple small updates | Update Roundup (cover the highlights) | "Weekly update" → rapid-fire demos |

**Always prefer Experiment or Build-Along over Deep Dive or Roundup** — they have higher view ceilings because they produce tangible output casual viewers can evaluate.

### 4. Choose a Relatable Demo

The demo subject matters as much as the feature itself. Wrap the feature in something viewers wish they had:

**High appeal:** task manager, personal dashboard, portfolio site, budget tracker, chatbot, landing page
**Low appeal:** compiler, terminal config, infrastructure setup, dev tooling

If the feature is abstract (e.g., "better sub-agent orchestration"), make it concrete by showing what it builds.

### 5. Write the Outline

Output a structured outline to the user. Format:

```
## Video Plan: [Working Title]

**Format:** [Experiment / Build-Along / Deep Dive / Roundup]
**Why this format:** [1 sentence]
**Target length:** [X-Y minutes]
**Demo subject:** [What we're building/showing]

### Hook (0:00-0:30)
[Write the actual opening line, not just a description]

### Setup (0:30-X:XX)
[Brief context — what is this feature, explained for someone
who's never used Claude Code]

### Core Content (X:XX-X:XX)
[Section-by-section breakdown with what to show on screen]

### Payoff (X:XX-X:XX)
[Click-through of results / side-by-side comparison / verdict]

### Takeaway (X:XX-X:XX)
[One sentence the viewer walks away with]

### Title/Thumbnail Angle
[2-3 title options cross-referenced with patterns from
socials/youtube/ab-tests/results.md]
```

### 6. Cross-Reference with Past Performance

Before finalizing, check:
- `socials/youtube/ab-tests/results.md` — which title formulas have won before?
- `socials/youtube/transcripts/` — has Ray already covered this topic? If so, the new video MUST use a different format/angle than the previous one
- `socials/youtube/ab-tests/competitive/` — any competitor data on this topic?
