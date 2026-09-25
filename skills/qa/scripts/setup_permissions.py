#!/usr/bin/env python3
"""Allow the QA Office scripts to run without a permission prompt each time.

Adds narrow allow rules to ~/.claude/settings.json (existing settings are kept).
Only the two QA Office scripts are allowed: qa_event.py (logs progress) and
qa_office.py (serves the local view). Run by install.ps1 / install.sh.
"""
import json
from pathlib import Path

RULES = [
    "Bash(python *qa_event.py*)",
    "Bash(python3 *qa_event.py*)",
    "Bash(python *qa_office.py*)",
    "Bash(python3 *qa_office.py*)",
]

path = Path.home() / ".claude" / "settings.json"
settings = {}
if path.exists():
    text = path.read_text(encoding="utf-8").strip()
    if text:
        settings = json.loads(text)  # fail loudly rather than overwrite a settings file we can't parse

allow = settings.setdefault("permissions", {}).setdefault("allow", [])
added = [r for r in RULES if r not in allow]
if added:
    allow.extend(added)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
print(f"QA Office permissions: {len(added)} rule(s) added to {path}" if added else "QA Office permissions already set")
