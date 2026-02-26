# ray-os

Ray's centralised personal operating system — content, courses, research, projects, and social media in one place.

## Structure

```
ray-os/
├── courses/                 — Course content (Advanced Context Engineering, Techniques, VSL)
├── research/                — Research notes and deep dives
├── projects/                — Active projects (agentic-coding-school, codex-cli)
├── socials/                 — YouTube & LinkedIn content, analysis, and performance data
├── tasks/                   — Todos and task tracking
├── .claude/skills/          — Claude Code skills (video editing, content writing, image gen, etc.)
├── .obsidian/               — Obsidian vault config
└── schedules.yaml           — Scheduled automations
```

## Obsidian Vault

This repo doubles as an Obsidian vault. When working with markdown files:

- **No H1 titles** — Obsidian uses filename as title
- **Linking** — Use `[[Note Name]]` for internal links, `[[Note Name|Display Text]]` for aliases
- **Tags** — `#tag` inline or in YAML frontmatter
- **Never delete files without explicit user permission**

### Frontmatter

```yaml
---
tags: [tag1, tag2]
aliases: [alternate-name]
date: YYYY-MM-DD
---
```

## Conventions

- Date-prefix files as `YYYY-MM-` for chronological sorting
- `analysis/` folders contain research about *other* creators/posts
- `self-audit/` or `posts/` folders contain Ray's own content and performance data
- Images tracked via Git LFS (`*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.webp`, `*.svg`)

## Timeouts

For image generation tasks (excalidraw-gen skill), use extended timeouts:
```bash
timeout: 180000  # 3 minutes per operation
```
When generating 5+ images, plan for 2-3 minutes total.
