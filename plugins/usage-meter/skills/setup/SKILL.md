---
name: setup
description: Install the usage-meter status line, which shows Claude subscription usage (5-hour and weekly limits), context window % and session cost under the prompt. Use when the user asks to show or enable usage in the UI or status line.
disable-model-invocation: true
allowed-tools: Bash(python3 *)
---

Run this command and report its output to the user:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/configure.py" install
```

Then tell the user:
- The status line appears under the prompt and updates after each response.
  The 5h/7d usage bars show up after the first API response of a session.
  They are only shown for Claude Pro/Max subscriptions, not API-key billing.
- Colors: green < 50%, yellow < 80%, red ≥ 80%. `↻` is time until reset.
- Re-run `/usage-meter:setup` after updating the plugin to pick up script changes.
- `/usage-meter:remove` restores their previous status line.
