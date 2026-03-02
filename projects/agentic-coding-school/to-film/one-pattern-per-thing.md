---
duration: "1-4 min"
batch: 1
order: 22
batch_name: "Quick Wins"
---

# One Pattern Per Thing

Pairs with: [[delete-your-readme]]

## The problem

Agents are biased toward whatever code they see first. If your codebase has two ways to do the same thing — two error handling styles, two data-fetching patterns, two component structures — the agent picks whichever it encounters first, or invents a third. This is the "gravitational pull" effect: early code (often written by weaker models or under time pressure) becomes the template for everything that follows, even when better patterns exist elsewhere in the same repo.

This gets worse over time. Each generation of model leaves behind its own style — verbose boilerplate from early models, over-abstracted helpers from mid-era ones. The codebase accumulates "AI-shaped debt": not bugs, but inconsistent architecture that confuses every future agent run.

## The fix

**Step 1 — Audit with Explore subagents.** Before building anything new, spawn an Explore subagent with a specific "why": "Find every pattern used for error handling in this codebase, because we need to pick one canonical approach before adding new endpoints." The "why" filters results — instead of returning everything, the subagent focuses on the decision you actually need to make.

**Step 2 — Pick the winner and kill the rest.** Don't just document the canonical pattern — actually refactor the losers out. Two patterns "documented" in a CLAUDE.md still means two patterns in the code, and agents are biased toward code over instructions.

**Step 3 — Lock it in your CLAUDE.md.** Once there's one pattern per thing in the code, add a single line to your CLAUDE.md: "Error handling: use Result types, not try/catch." This isn't a style guide — it's a constraint. The agent can't go off-script when there's only one script.

## Why this matters for agents specifically

Models resist unconventional patterns (cognitive inertia) and degrade when instructions conflict with what they see in the code. When you have two patterns, the agent is fighting itself — the code says one thing, the CLAUDE.md says another, and instruction-following accuracy drops. One pattern per thing eliminates the conflict entirely.

The payoff compounds: run the agent 5 times on a consistent codebase and you get 5 similar results. Run it 5 times on an inconsistent one and you get 5 different approaches. Consistency is a form of constraint, and constraints make agents predictable.

## Demo idea

Take a real repo with duplicate patterns (e.g. some files use `fetch`, others use `axios`). Show the agent introducing a third HTTP client. Then: audit with an Explore subagent, consolidate to one pattern, add the CLAUDE.md line, run the same task again — agent nails it first try.
