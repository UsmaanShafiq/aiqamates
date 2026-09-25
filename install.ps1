# Installs the /qa skill and the QA team agents into your user-level Claude Code folder (~/.claude)
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
# Remove agents installed under the old v1 names
foreach ($old in "qa-functional","qa-ux-exploratory","qa-technical","qa-adversarial","qa-api","qa-security","qa-data-auth","qa-accessibility","qa-responsive-visual","qa-performance") {
    $f = Join-Path $agentDst "$old.md"
    if (Test-Path $f) { Remove-Item -Force $f }
}
Copy-Item -Force (Join-Path $repo "agents\*.md") $agentDst

Write-Host "Installed /qa skill   -> $skillDst"
Write-Host "Installed QA agents   -> $agentDst"

$py = Get-Command python -ErrorAction SilentlyContinue
if ($py) {
    & python (Join-Path $skillDst "scripts\setup_permissions.py")
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
