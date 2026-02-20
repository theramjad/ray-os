---
duration: "1-4 min"
batch: 1
order: 7
batch_name: "Quick Wins"
---

# Boxing the Model In

Boris Cherny explains the "boxing the model in" anti-pattern — the instinct to force the model to behave in a very particular way.

## What it looks like
- **Layering strict workflows** — dictating a precise sequence: "you must do step one, then step two, then step three," using a sophisticated orchestrator
- **Over-curating context upfront** — providing all the context from the beginning instead of letting the model figure things out

## Why it backfires
This approach is often counterproductive. You generally get better results by simply giving the model tools and a goal, then letting it figure things out on its own.

This scaffolding might have been necessary a year ago — it's not really needed with current models.

## What to do instead
Give the model tools so it can get the context it needs itself. Trust it to reason through the steps rather than pre-scripting the path.

> Source: Boris Cherny (1:03:44)
