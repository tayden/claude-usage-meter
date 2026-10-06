#!/usr/bin/env python3
"""Install or remove the usage-meter status line in ~/.claude/settings.json.

Plugins can't set the main status line themselves, so this copies the script
to a stable location (it survives plugin updates) and points `statusLine` at
it. Any previous `statusLine` is saved so `remove` can restore it.

Usage: configure.py install|remove [--data-dir DIR]
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

SETTINGS = Path.home() / ".claude" / "settings.json"
DEFAULT_DATA = Path.home() / ".claude" / "usage-meter"
HERE = Path(__file__).resolve().parent


def load_settings():
    if not SETTINGS.exists():
        return {}
    return json.loads(SETTINGS.read_text())


def save_settings(settings):
    SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    tmp = SETTINGS.with_suffix(".json.usage-meter.tmp")
    tmp.write_text(json.dumps(settings, indent=2) + "\n")
    tmp.replace(SETTINGS)


def install(data_dir: Path):
    data_dir.mkdir(parents=True, exist_ok=True)
    target = data_dir / "statusline.py"
    shutil.copy2(HERE / "statusline.py", target)
    target.chmod(0o755)

    settings = load_settings()
    backup = data_dir / "previous-statusline.json"
    current = settings.get("statusLine")
    ours = current and "usage-meter" in str(current.get("command", ""))
    if current and not ours:
        backup.write_text(json.dumps(current, indent=2) + "\n")
        print(f"Saved previous statusLine to {backup}")

    settings["statusLine"] = {
        "type": "command",
        "command": f'python3 "{target}"',
        "padding": 0,
    }
    save_settings(settings)
    print(f"Installed status line script at {target}")
    print(f"Updated statusLine in {SETTINGS}")


def remove(data_dir: Path):
    settings = load_settings()
    current = settings.get("statusLine") or {}
    if "usage-meter" not in str(current.get("command", "")):
        print("statusLine is not managed by usage-meter; nothing to do.")
        return
    backup = data_dir / "previous-statusline.json"
    if backup.exists():
        settings["statusLine"] = json.loads(backup.read_text())
        backup.unlink()
        print("Restored previous statusLine.")
    else:
        del settings["statusLine"]
        print("Removed statusLine.")
    save_settings(settings)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["install", "remove"])
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    args = parser.parse_args()
    data_dir = args.data_dir.expanduser()
    # Keep "usage-meter" in the path so install/remove can recognise our entry.
    if "usage-meter" not in str(data_dir):
        sys.exit("--data-dir must contain 'usage-meter' in its path")
    (install if args.action == "install" else remove)(data_dir)


if __name__ == "__main__":
    main()
