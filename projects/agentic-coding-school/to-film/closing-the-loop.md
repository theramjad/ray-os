---
duration: "1-4 min"
batch: 2
order: 5
batch_name: "Bonus Techniques"
---

# Closing the Loop

See Obsidian for notes and make graphics here too

## Concept

Close the loop by connecting your agentic workflow end-to-end — input to output and back again.

**Example: TikTok Video Pipeline**
- Write code that generates TikTok videos automatically
- Instead of using the TikTok API (which gets nerfed), have it queue videos for a human to manually upload — avoids platform restrictions
- One day later, have an agent check back on the uploaded videos, pull any insights (views, comments, engagement), and update the content or related notes with what it learned

## MCP Servers as Loop Closers
Adding MCP servers is a great way to close the loop — give Claude Code the ability to diagnose what's happening in your system and act on it. Examples:
- A cost/billing MCP so Claude can monitor server spend and flag or adjust resources automatically
- A logging/observability MCP so it can detect errors in production and self-diagnose
- A database MCP so it can check outcomes and update records based on results

The idea: don't just have Claude *produce* something — give it the tools to *see what happened* and respond.

## Key Points
- "Closing the loop" = the agent doesn't just produce output, it also monitors and learns from the result
- Human-in-the-loop upload step sidesteps API risk while keeping the rest automated
- The delayed feedback step (check next day) is what makes it a *loop* vs a one-shot pipeline
- MCP servers extend the loop — they give the agent eyes and hands on your infrastructure
- Can apply to any content workflow: YouTube, blog posts, newsletters, etc.
