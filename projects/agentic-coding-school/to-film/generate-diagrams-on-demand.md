---
duration: "1-4 min"
batch: 1
order: 21
batch_name: "Quick Wins"
---

# Generate Diagrams On Demand

Pairs with: [[delete-your-readme]]

Same idea as deleting your README — don't maintain a static architecture diagram that drifts from reality. Instead, use the mermaid-diagram-generator skill to generate fresh diagrams on demand from the actual codebase.

Ask an Explore subagent to map out the code, then pipe that into the mermaid skill to get an interactive HTML diagram — data flow, component hierarchy, sequence diagrams, whatever you need. It takes seconds and reflects the real state of the code, not what it looked like when someone last bothered to update the Confluence page.

Live demo: clone a repo you've never seen, generate an architecture diagram in one command, actually understand the codebase in 30 seconds.
