# Running Dedicated Refactoring Sessions

Basically the agent will *always* find problems, often shocking ones, e.g. where you discover you have two or even three completely redundant systems (databases, logging, telemetry, whatever) that need consolidating. And since agents tend to accrete code without automatic refactoring, your vibe-coded source files will tend to grow to thousands of lines, which makes them harder to agents (and humans) to reason about. So you should tell it regularly to break things up, and then run dedicated sessions to implement the refactoring!
