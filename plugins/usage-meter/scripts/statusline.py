#!/usr/bin/env python3
"""Claude Code status line showing subscription usage, context and cost.

Reads the status line JSON from stdin and prints one line, e.g.

    Opus │ 5h ██░░░░░░ 23% ↻2h14m │ 7d ███░░░░░ 41% ↻Thu 09:00 │ ctx 8% │ $0.01

Rate-limit fields only appear for Claude subscription users, after the first
API response of the session; until then a placeholder is shown.
"""

import json
import os
import sys
import time

NO_COLOR = bool(os.environ.get("NO_COLOR"))
BAR_WIDTH = int(os.environ.get("USAGE_METER_BAR_WIDTH", "8"))
SEP = " \033[2m│\033[0m " if not NO_COLOR else " | "


def color(text, pct):
    if NO_COLOR or pct is None:
        return text
    code = "32" if pct < 50 else "33" if pct < 80 else "31"
    return f"\033[{code}m{text}\033[0m"


def dim(text):
    return text if NO_COLOR else f"\033[2m{text}\033[0m"


def bar(pct):
    filled = round(max(0.0, min(100.0, pct)) / 100 * BAR_WIDTH)
    return "█" * filled + "░" * (BAR_WIDTH - filled)


def until(resets_at):
    if not resets_at:
        return ""
    secs = int(resets_at - time.time())
    if secs <= 0:
        return "↻now"
    if secs < 24 * 3600:
        h, m = divmod(secs // 60, 60)
        return f"↻{h}h{m:02d}m" if h else f"↻{m}m"
    return "↻" + time.strftime("%a %H:%M", time.localtime(resets_at))


def limit_segment(label, info):
    pct = info.get("used_percentage")
    if pct is None:
        return None
    text = f"{label} {bar(pct)} {pct:.0f}%"
    reset = until(info.get("resets_at"))
    return color(text, pct) + (" " + dim(reset) if reset else "")


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print("usage-meter: no data")
        return

    parts = []

    model = (data.get("model") or {}).get("display_name")
    if model:
        parts.append(model)

    limits = data.get("rate_limits") or {}
    limit_parts = [
        seg
        for seg in (
            limit_segment("5h", limits.get("five_hour") or {}),
            limit_segment("7d", limits.get("seven_day") or {}),
        )
        if seg
    ]
    spend = limits.get("spend_limit") or {}
    if spend.get("used_percentage") is not None:
        pct = spend["used_percentage"]
        if spend.get("used_usd") is not None and spend.get("limit_usd"):
            text = f"spend ${spend['used_usd']:.0f}/${spend['limit_usd']:.0f}"
        else:
            text = f"spend {pct:.0f}%"
        limit_parts.append(color(text, pct))
    parts.extend(limit_parts or [dim("usage: waiting for first response")])

    ctx = data.get("context_window") or {}
    if ctx.get("used_percentage") is not None:
        pct = ctx["used_percentage"]
        parts.append(color(f"ctx {pct:.0f}%", pct))

    cost = (data.get("cost") or {}).get("total_cost_usd")
    if cost:
        parts.append(dim(f"${cost:.2f}"))

    print(SEP.join(parts))


if __name__ == "__main__":
    main()
