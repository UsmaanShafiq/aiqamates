#!/usr/bin/env bash
# Installs the /qa skill and qa-* agents into ~/.claude so /qa works in every project.
# Usage (from the repo folder):  bash install.sh
set -euo pipefail

repo="$(cd "$(dirname "$0")" && pwd)"
claude="$HOME/.claude"

mkdir -p "$claude/skills/qa" "$claude/agents"
cp -R "$repo/skills/qa/." "$claude/skills/qa/"
cp "$repo"/agents/qa-*.md "$claude/agents/"

echo "Installed /qa skill   -> $claude/skills/qa"
echo "Installed QA agents   -> $claude/agents"

PY="$(command -v python3 || command -v python || true)"
if [ -n "$PY" ]; then
  "$PY" -c "import reportlab" 2>/dev/null || { echo "Installing ReportLab for PDF reports..."; "$PY" -m pip install --quiet reportlab; }
else
  echo "Python not found: PDF reports need Python + 'pip install reportlab'. Markdown reports still work."
fi

echo
echo "Done. Open any project in a NEW Claude Code session and type:  /qa"
