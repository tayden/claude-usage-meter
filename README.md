# usage-meter

A [Claude Code](https://code.claude.com) plugin that shows your current usage in the status line under the prompt:

```
Opus │ 5h ██░░░░░░ 24% ↻2h13m │ 7d ███████░ 84% ↻Fri 22:03 │ ctx 55% │ $1.23
```

## Quick install

Paste this into Claude Code and it will install the plugin for you:

> **Install the usage-meter status line plugin: run `claude plugin marketplace add tayden/claude-usage-meter`, then `claude plugin install usage-meter@taylor-plugins`, then `python3 ~/.claude/plugins/cache/taylor-plugins/usage-meter/*/scripts/configure.py install`, and show me the output.**

The status line appears in your next Claude Code session.

## What it shows

| Segment | Meaning |
|---|---|
| `5h` | Usage of your 5-hour session limit, with time until reset (`↻`) |
| `7d` | Usage of your weekly limit, with reset time |
| `spend` | Spend-limit usage, when your organization has one |
| `ctx` | How full the context window is |
| `$` | Estimated cost of the current session |

Colors: green under 50%, yellow under 80%, red at 80% or more. Set `NO_COLOR=1` to turn colors off.
Set `USAGE_METER_BAR_WIDTH` to change the bar length (default 8).

The `5h` / `7d` bars are only available on Claude Pro and Max subscriptions. They appear after
the first response of a session; until then the status line says `usage: waiting for first response`.

## Manual install

```bash
claude plugin marketplace add tayden/claude-usage-meter
claude plugin install usage-meter@taylor-plugins
```

Then run `/usage-meter:setup` inside Claude Code.

Or do it all from inside Claude Code:

```
/plugin marketplace add tayden/claude-usage-meter
/plugin install usage-meter@taylor-plugins
/usage-meter:setup
```

### Why the setup step?

Plugins can't set Claude Code's main status line. Only `settings.json` can. Setup copies the
script to `~/.claude/usage-meter/statusline.py` and adds a `statusLine` entry to
`~/.claude/settings.json`. If you already had a status line, it is backed up first.

## Updating

```bash
claude plugin marketplace update taylor-plugins
claude plugin update usage-meter@taylor-plugins
```

Then run `/usage-meter:setup` again to copy the new script into place.

## Uninstall

Run `/usage-meter:remove` in Claude Code. It removes the status line, or restores the one you
had before. Then:

```bash
claude plugin uninstall usage-meter@taylor-plugins
```

## Requirements

- Claude Code
- Python 3 (standard library only)
