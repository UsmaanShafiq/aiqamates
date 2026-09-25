#!/usr/bin/env bash
# Installs the /qa skill and the QA team agents into ~/.claude so /qa works in every project.
# Usage (from the repo folder):  bash install.sh
set -euo pipefail

repo="$(cd "$(dirname "$0")" && pwd)"
claude="$HOME/.claude"

mkdir -p "$claude/skills/qa" "$claude/skills/qa-office" "$claude/agents"
cp -R "$repo/skills/qa/." "$claude/skills/qa/"
cp -R "$repo/skills/qa-office/." "$claude/skills/qa-office/"
# Remove agents installed under the old v1 names
for old in qa-functional qa-ux-exploratory qa-technical qa-adversarial qa-api qa-security qa-data-auth qa-accessibility qa-responsive-visual qa-performance; do rm -f "$claude/agents/$old.md"; done
cp "$repo"/agents/*.md "$claude/agents/"

echo "Installed /qa skill   -> $claude/skills/qa"
echo "Installed /qa-office -> $claude/skills/qa-office"
echo "Installed QA agents   -> $claude/agents"

PY="$(command -v python3 || command -v python || true)"
if [ -n "$PY" ]; then
  "$PY" "$claude/skills/qa/scripts/setup_permissions.py"
  "$PY" -c "import reportlab" 2>/dev/null || { echo "Installing ReportLab for PDF reports..."; "$PY" -m pip install --quiet reportlab; }
else
  echo "Python not found: PDF reports need Python + 'pip install reportlab'. Markdown reports still work."
fi

echo
echo "Done. Open any project in a NEW Claude Code session and type:  /qa"
echo "To just watch the team: /qa-office   (or /qa-office demo)"
