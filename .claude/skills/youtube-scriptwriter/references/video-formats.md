# Video Format Framework

## Format Selection

### 1. Experiment / Comparison (highest view ceiling)

**When to use:** New feature launches, tool comparisons, before/after scenarios.

**Why it works:** Creates narrative tension ("which one wins?"), appeals to casual viewers who don't need prior knowledge, and produces a clear visual payoff.

**Structure:**
1. **Hook (0:00-0:30):** State the experiment. "I'm going to build the same app twice — once with X, once with Y — and compare the results."
2. **Brief explainer (0:30-2:00):** Just enough context for a newcomer to follow. Use simple analogies, not technical primitives.
3. **Build A (2:00-5:00):** Show the first approach. Speed through setup, slow down on interesting moments.
4. **Build B (5:00-8:00):** Same task, different approach. Viewers are now watching for differences.
5. **Side-by-side comparison (8:00-10:00):** Click through both results. React genuinely. Give specific metrics (build time, features, quality).
6. **Verdict (10:00-11:00):** Clear winner + nuance. "X was faster but Y went deeper."

**Key rules:**
- Use the SAME prompt/task for both approaches — this is what makes the comparison fair and compelling
- Build something relatable (task manager, dashboard, landing page) not niche (terminal config, dev tooling)
- Show the finished product extensively — viewers want to see the output, not the process
- Give concrete metrics: build time, lines of code, number of features
- Don't hedge the verdict — pick a winner, then add nuance

**Example hook:** "I'm running an experiment: I'll build the exact same app with a single agent and with an agent team, then compare which one produces a better result."

---

### 2. Build-Along (high view ceiling)

**When to use:** Tutorials, workflow demonstrations, "how I use X" content.

**Why it works:** Tangible output viewers can replicate. Satisfying to watch something get built from zero.

**Structure:**
1. **Hook (0:00-0:30):** Show the finished product first (2-3 second flash), then "Here's how I built this in X minutes using Y."
2. **Setup (0:30-1:30):** What we're building and why. Keep it short.
3. **Build (1:30-8:00):** Step-by-step construction. Narrate decisions, not keystrokes.
4. **Result showcase (8:00-10:00):** Click through the finished product. Test edge cases live.
5. **Takeaway (10:00-10:30):** What this means for the viewer's workflow.

**Key rules:**
- Build something the viewer wishes they had (personal dashboard, automation, portfolio site)
- Show the final result early (flash preview) — this is what keeps people watching
- Keep config/setup under 90 seconds
- React to the output naturally — surprise and delight are retention gold

---

### 3. Deep Dive (medium view ceiling)

**When to use:** Explaining a single complex concept or feature in depth.

**Why it works:** Positions the creator as the authority. Longer watch time per viewer.

**Structure:**
1. **Hook (0:00-0:30):** Frame why this matters. "This one feature changed how I use Claude Code entirely."
2. **Concept (0:30-2:00):** Explain the idea simply. Use analogies from real life, not other technical concepts.
3. **Demo 1 — basic usage (2:00-4:00):** Show the simplest case.
4. **Demo 2 — advanced usage (4:00-7:00):** Show the power case that casual users miss.
5. **Behind the scenes (7:00-9:00):** How it works under the hood (optional, for technical audiences).
6. **Verdict/recommendation (9:00-10:00):** When to use this, when not to.

**Key rules:**
- ONE topic, not a feature roundup
- Lead with the "so what" — why should a viewer care about this feature?
- Use progressive complexity: simple example first, then build up
- Avoid going behind the scenes unless the audience is technical

---

### 4. Update Roundup (lowest view ceiling)

**When to use:** Multiple small features that individually don't justify a full video.

**Why it works:** Keeps the channel current and serves existing subscribers. But rarely goes viral.

**Structure:**
1. **Hook (0:00-0:20):** "X new features just dropped — here are the ones that matter."
2. **Features (0:20-8:00):** Cover each feature with a quick demo (30-90 seconds each). Order by impact, not chronology.
3. **Verdict (8:00-9:00):** "The biggest one is X because..."

**Key rules:**
- If one feature is significantly bigger than the rest, consider making it an Experiment or Deep Dive instead
- Lead with the most impactful feature, not the most recent
- Spend 60-80% of the video on the top 2-3 features, speed through the rest

---

## Universal Structural Rules

### Hook formula (first 30 seconds)

The hook must do ONE of these:
- **Create curiosity:** "I tested X vs Y and the results surprised me"
- **Promise a tangible outcome:** "By the end of this video you'll have a working X"
- **State a bold claim:** "This one feature makes every other tool obsolete"

**Never** open with:
- "Hey guys, welcome back" (dead air)
- "So there's this new feature..." (no tension)
- "Before we get started, let me explain..." (delays the value)
- Course/sponsor plugs before the hook

### One topic per video

Videos covering one thing deeply outperform videos covering many things broadly. If a release has 5 features, pick the biggest one and make an Experiment or Deep Dive. Save the rest for a separate roundup or ignore them.

**Exception:** Update roundups exist specifically for when no single feature is big enough alone.

### Show tangible, relatable output

Viewers connect with output they can imagine using:
- **High relatability:** Task manager, dashboard, portfolio, chatbot, landing page
- **Low relatability:** Terminal config, compiler, dev tooling, infrastructure setup

When demonstrating a feature, wrap it in a relatable build even if the feature itself is abstract.

### The "click-through" moment

After building/demoing something, spend 60-90 seconds clicking through the result like a user would. Test buttons, toggle modes, try edge cases. React naturally. This is the most rewatchable and shareable part of the video. Viewers want to see the output working, not hear about it.

### Explain for newcomers, deliver for experts

Use a 30-second "anyone can follow this" explainer before going deep. Simple analogies over technical jargon. "Sub-agents are like interns who do one task and report back. Agent teams are like a project team that talks to each other while working."

Don't assume viewers watched your previous videos.

### Clear verdict or takeaway

Every video must end with a concrete statement the viewer can repeat:
- "Agent teams are better for complex projects, sub-agents are better for simple tasks"
- "This build took 6 minutes with a single agent and 4 minutes with a team"
- "The experiment format gets 10x more views than feature overviews"

If you can't summarize the takeaway in one sentence, the video tried to cover too much.

### Pacing

- Setup/context: max 20% of video
- Core content/demos: 60-70% of video
- Result showcase + verdict: 15-20% of video
- Course/CTA: under 30 seconds total, ideally mid-roll not intro

---

## Competitor Analysis Checklist

When analyzing why a competitor video outperformed:

1. **Format:** What format did they use? (experiment, build-along, deep dive, roundup)
2. **Topic scope:** Single topic or multi-topic?
3. **Output:** What did they build/show? How relatable is it?
4. **Hook:** What's the first sentence? Does it create curiosity or tension?
5. **Click-through:** How long do they spend showing the finished result?
6. **Audience level:** Do they assume prior knowledge or explain from scratch?
7. **Verdict:** Do they give a clear comparison or takeaway at the end?
8. **Pacing:** How much time on setup vs demos vs results?
