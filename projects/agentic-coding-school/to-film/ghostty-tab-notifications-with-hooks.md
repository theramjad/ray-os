# Ghostty Tab Notifications with Claude Code Hooks

## The Problem
When Claude Code is running in a background Ghostty tab, you have no idea when it's finished or needs your attention. You're stuck constantly switching tabs to check.

## The Solution
Use Claude Code's `Stop` and `Notification` hooks to send a terminal bell character to Ghostty, which lights up the tab title when Claude finishes responding or needs permission.

## The Trick
Hook subprocesses don't have a controlling terminal — `printf '\a'` prints to nowhere. The fix is to walk up the process tree to find the ancestor shell's TTY device and write the bell directly to `/dev/ttysXXX`.

## Setup

### 1. Ghostty Config

In your Ghostty config (`~/Library/Application Support/com.mitchellh.ghostty/config` on macOS):

```
bell-features = title
```

This makes Ghostty highlight the tab title when a bell fires in a background tab.

### 2. Claude Code Hooks

In `~/.claude/settings.json`, add these hooks:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt|elicitation_dialog",
        "hooks": [
          {
            "type": "command",
            "command": "TTY=$(ps -o tty= -p $(ps -o ppid= -p $(ps -o ppid= -p $$)) 2>/dev/null | tr -d ' '); [ -n \"$TTY\" ] && printf '\\a' > /dev/$TTY"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "TTY=$(ps -o tty= -p $(ps -o ppid= -p $(ps -o ppid= -p $$)) 2>/dev/null | tr -d ' '); [ -n \"$TTY\" ] && printf '\\a' > /dev/$TTY"
          }
        ]
      }
    ]
  }
}
```

### What Each Hook Does
- **Notification** (with matcher `permission_prompt|elicitation_dialog`): Fires when Claude asks for permission or asks you a question
- **Stop**: Fires every time Claude finishes responding

### How the Command Works
1. `ps -o ppid=` walks up the process tree from the hook subprocess to find an ancestor with a real TTY
2. `ps -o tty=` gets the TTY device name (e.g. `ttys007`)
3. `printf '\a' > /dev/$TTY` writes the bell character directly to that device, bypassing the missing stdout
