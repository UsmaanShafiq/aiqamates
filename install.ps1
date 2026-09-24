# Installs the /qa skill and qa-* agents into your user-level Claude Code folder (~/.claude)
# so /qa works in every project.
# Usage (from the repo folder):  powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"
$repo = $PSScriptRoot
$claude = Join-Path $env:USERPROFILE ".claude"
$skillDst = Join-Path $claude "skills\qa"
$agentDst = Join-Path $claude "agents"

New-Item -ItemType Directory -Force $skillDst | Out-Null
New-Item -ItemType Directory -Force $agentDst | Out-Null

Copy-Item -Recurse -Force (Join-Path $repo "skills\qa\*") $skillDst
Copy-Item -Force (Join-Path $repo "agents\qa-*.md") $agentDst

Write-Host "Installed /qa skill   -> $skillDst"
Write-Host "Installed QA agents   -> $agentDst"

$py = Get-Command python -ErrorAction SilentlyContinue
if ($py) {
    & python -c "import reportlab" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing ReportLab for PDF reports..."
        & python -m pip install --quiet reportlab
    }
} else {
    Write-Host "Python not found: PDF reports need Python + 'pip install reportlab'. Markdown reports still work."
}

Write-Host ""
Write-Host "Done. Open any project in a NEW Claude Code session and type:  /qa"
