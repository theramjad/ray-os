# Improving Skills Trigger

[Shell + Skills + Compaction: Tips for long-running agents that do real work](https://developers.openai.com/blog/skills-shell-tips)

Your skill's description is effectively the model's decision boundary. It should answer:
- When should I use this?
- When should I not use this?
- What are the outputs and success criteria?

A practical pattern is to include a short "Use when vs. don't use when" block directly in the description.

A surprising failure mode is that making skills available can initially reduce correct triggering. One fix: negative examples plus edge case coverage.

Write a few explicit "Don't call this skill when…" cases (and what to do instead). Glean saw this directly: skill-based routing initially dropped triggering by about 20% in targeted evals, then recovered after they added negative examples and edge case coverage in descriptions.
