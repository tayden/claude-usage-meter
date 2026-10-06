# usage-meter

Claude Code plugin that shows your current usage in the status line under the prompt:

```
Opus │ 5h ██░░░░░░ 24% ↻2h13m │ 7d ███████░ 84% ↻Fri 22:03 │ ctx 55% │ $1.23
```

- **5h / 7d**: Claude subscription rate-limit usage, with time until reset (`↻`).
  Shown after the first API response of a session; Pro/Max subscriptions only.
- **ctx**: context window used. **$**: session cost estimate.
- Green < 50%, yellow < 80%, red ≥ 80%. Set `NO_COLOR=1` to disable colors.

## Install

```
claude plugin marketplace add ~/PycharmProjects/claude-usage-meter
claude plugin install usage-meter@taylor-plugins
```

Then run `/usage-meter:setup` in Claude Code. Plugins can't set the main status line
directly, so setup copies the script to `~/.claude/usage-meter/` and adds `statusLine` to
`~/.claude/settings.json`. Any existing status line is backed up.
`/usage-meter:remove` restores it.
