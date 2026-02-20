---
duration: "5-9 min"
batch: 7
order: 4
batch_name: "Context Engineering"
---

# Language Server Protocol

Use LSP-powered tools (like Serena/JetBrains MCP) instead of text-based search for code navigation. Semantic understanding beats grep.

## Example: Serena in AGENTS.md for Sub-Agents

Show how you can add LSP instructions to your `AGENTS.md` so sub-agents use semantic tools first:

**The anti-pattern:** Sub-agents defaulting to Grep/Glob/Read on Java/Kotlin files — wasteful and misses context.

**The fix:** Instruct sub-agents to start with semantic tools:
- `jet_brains_get_symbols_overview` — get file/class structure
- `jet_brains_find_symbol` — locate specific symbols by name path
- `jet_brains_find_referencing_symbols` — find where symbols are used
- `search_for_pattern` — search when exact names unknown

Only fall back to Grep/Read for non-code files or when Serena returns nothing.

**Wrong (wasteful):**
```
Grep pattern="class Composition"
Read file_path="src/main/java/songscribe/music/Composition.java"
```

**Right (efficient):**
```
jet_brains_get_symbols_overview(relative_path="src/.../Composition.java", depth=2)
jet_brains_find_symbol(name_path_pattern="Composition/isEmpty", include_body=true)
```

## Key Points
- LSP gives semantic understanding that text search can't match
- Add these instructions to your AGENTS.md so sub-agents inherit them
- Link out to detailed rules files (e.g. `./rules/serena.md`, `./rules/development.md`)
- Saves tokens and gives more complete results
