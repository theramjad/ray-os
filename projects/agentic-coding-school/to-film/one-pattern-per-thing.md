---
duration: "1-4 min"
batch: 1
order: 22
batch_name: "Quick Wins"
---

# One Pattern Per Thing

Agents don't have taste. If your codebase has two ways to do the same thing — two error handling styles, two ways to fetch data, two component patterns — the agent will pick one at random, or worse, invent a third.

The fix has two parts:

1. **Before building:** run an Explore subagent to audit the codebase and surface any duplicate patterns. Resolve them before the agent touches anything new.
2. **In your CLAUDE.md:** document the canonical pattern for common decisions (e.g. "use X for API calls, not Y"). This gives the agent a single source of truth to follow.

The payoff isn't just cleaner code — it's that agents get more predictable. When there's one pattern per thing, the agent can't go off-script. Consistency is a form of constraint, and constraints make agents better.
