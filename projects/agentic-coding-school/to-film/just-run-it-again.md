---
duration: "1-4 min"
---

# Just Run It Again

Basically the agent will *always* find problems, often shocking ones, e.g. where you discover you have two or even three completely redundant systems (databases, logging, telemetry, whatever) that need consolidating. And since agents tend to accrete code without automatic refactoring, your vibe-coded source files will tend to grow to thousands of lines, which makes them harder to agents (and humans) to reason about. So you should tell it regularly to break things up, and then run dedicated sessions to implement the refactoring!

Jeffrey described a long, complex series of prompts for this process; I'm sure we'd all be appreciative if he publishes them. But the way he described it to me, you first make them do a task, then you do a series of focused reviews. Each review should be slightly broader and more outlandish than the previous one, or you can do it the opposite order. But you need a mixture of in-the-small and in-the-large reviews. You're having it look for bad code (or designs), but also bad architecture.

To be slightly more concrete, Jeffrey first asks it to do a couple of regular code reviews, which find all the usual stuff. And you'll notice right away that even on the second review it will often find things it missed in the first review. But I think most of us stop there, if we even ask at all. It definitely feels weird to ask for the 3rd code review, which is the agent's 4th pass over the code, counting the generation step. But the 3rd review, especially during the Design phase, is where you start asking it existential questions about whether you're doing the Right Thing throughout the project.

I tried it, and sure enough, it does take 4–5 iterations, just as Jeffrey described, before the agent will say something like, "I think this is about as good as we can make it." At that point it has converged. And that, folks, is the first point at which you can begin to *moderately* trust the output the agent has produced. If you always take the first thing it generates, with no review at all, you're bound to be disappointed.
