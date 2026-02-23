---
name: good-morning-todos
description: >
  Check and execute Claude's own pending tasks from todos.yaml. Use at the start of a session
  or when the user says "good morning", "check your todos", "what do you need to do",
  "any tasks due", or "run your todos". This skill handles tasks that Claude should do
  autonomously (e.g., check post performance, follow up on experiments) — not the user's
  personal Todoist tasks.
---

# Good Morning Todos

## How It Works

Claude maintains its own task list at:

```
/Users/ray/.claude/projects/-Users-ray-Desktop-ray-os/memory/todos.yaml
```

These are tasks Claude should handle — distinct from Ray's personal tasks in Todoist.

## On Trigger

1. Read `todos.yaml` from the memory directory
2. Check today's date against each task's `due` field
3. Categorize tasks:
   - **Overdue**: `due` is before today and `status: pending`
   - **Due today**: `due` matches today and `status: pending`
   - **Upcoming**: `due` is within the next 3 days and `status: pending`
4. Present a summary to the user:
   ```
   I have [N] task(s) to handle:

   OVERDUE
   - [task] (was due [date])

   DUE TODAY
   - [task]

   UPCOMING
   - [task] (due [date])
   ```
5. Ask the user: "Want me to get started on these? Any you want to skip or reprioritize?"
6. Wait for the user's response before executing anything
7. Work through approved tasks one by one, asking for clarification if needed
8. After completing a task, update its `status` to `completed` and add a `completed_date` field in `todos.yaml`

## Task Format

Each task in `todos.yaml` follows this structure:

```yaml
- task: Short task title
  description: >
    Detailed description with any URLs, context, or instructions
    needed to complete the task.
  due: YYYY-MM-DD
  status: pending | completed
  completed_date: YYYY-MM-DD  # added on completion
```

## Adding New Tasks

When Claude identifies follow-up work during a session (e.g., "check back on this in a week"),
append a new entry to `todos.yaml` with an appropriate `due` date.

## Guidelines

- Always read the full task description before starting — it may contain URLs or specific instructions
- Use the appropriate skills/tools for each task (e.g., linkedin-navigator for checking post performance)
- If a task can't be completed (missing tool, needs user input), mark it with `status: blocked` and explain why
- Keep the yaml file clean — don't delete completed tasks, just mark them as completed for history
