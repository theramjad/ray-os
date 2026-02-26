
Include
Mention Aparajita's plan manager: https://github.com/aparaji

1. You should always be doing something whilst using Claude Code. For example, for me, I'm just matching
2. You should basically always update your model of where the models are, and remember that they're capable of more than you actually think. You don't want to be like, okay, the model can't do this. Chances are the model will be able to do it for you if you put in the time and effort to train it. And then here's an example of actually having fun equals. 
**Run Claude Code as a persistent background agent** — keep a task running all the time for things you can't be bothered doing manually. Example: a dating app message reply bot that monitors and responds so you never have to open the app.
3. **Use `--dangerously-skip-permissions` with hooks that block internet access** — get the speed of fully autonomous operation while scoping Claude's reach to only what's safe for that workload. The hooks act as the guardrail that makes the permission skip safe.
4. **Use hooks to prevent prompt injection** — hooks can intercept and block dangerous actions (like sending emails) entirely, so even if Claude gets injected via malicious file or web content, it can't do damage.
5. **Use Ghostty as your terminal** — GPU-accelerated, native splits, tab renaming, command palette (`Cmd+Shift+P`), and bell features that integrate perfectly with Claude Code hooks.
6. **Ring the terminal bell when Claude needs your input** — add a global Notification hook in `~/.claude/settings.json` with matcher `permission_prompt|idle_prompt` that runs `tput bel`. Pair with Ghostty's `bell-features = title,attention` so background tabs get a 🔔 indicator that clears when you focus them.
7. **Split panes to run multiple Claude sessions side-by-side** — in Ghostty: `Cmd+D` splits right, `Cmd+Shift+D` splits down, `Cmd+Option+Arrows` moves focus. Run one Claude per pane for parallel workstreams.
8. **Rename Ghostty tabs to track what each Claude is doing** — add `keybind = cmd+shift+r=prompt_surface_title` to your Ghostty config for a quick rename shortcut. Label tabs by task ("refactor auth", "write tests") so you always know which session is which.
9. **Use Obsidian as your notes/docs tool** — your vault is just markdown files on disk, so Claude can read, write, and link them directly. Backlinks and graph view let you spot patterns across notes that Claude creates or edits for you.
10. **Use a voice-to-text tool for prompting** — talk instead of type. It's faster for explaining what you want, especially for longer or more nuanced prompts. Tools like Whisper, macOS Dictation, or SuperWhisper work well.