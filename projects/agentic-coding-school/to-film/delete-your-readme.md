---
duration: "1-4 min"
batch: 1
order: 20
batch_name: "Quick Wins"
---

# Delete Your README.md

README.md files go stale. The moment you commit one, it starts drifting from reality — wrong setup steps, outdated architecture descriptions, deprecated commands. When an agent reads it, it takes that stale info as ground truth and makes decisions based on it.

The fix: delete it, and generate documentation on demand instead. Spawn an Explore subagent pointed at the actual codebase and ask it to summarise whatever you need — the architecture, the setup steps, the data flow. You get accurate docs every time because the subagent reads the real code, not a 6-month-old description of it.

This is the same principle as "just-in-time" context: don't pre-load stale information, generate fresh context at the moment you need it.
