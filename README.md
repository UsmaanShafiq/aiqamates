# AI QA Mates

A reusable AI QA team for Claude Code. Type **`/qa`** in any project: Claude asks a few setup questions as clickable forms, runs 10 specialist QA agents against your app, writes a QA report (Markdown + PDF), then asks which issues to fix.

Works best with:
- Next.js / React / Tailwind SaaS
- WordPress
- WooCommerce

## Install (once)

**Windows (PowerShell):**

    git clone https://github.com/UsmaanShafiq/aiqamates.git
    cd aiqamates
    powershell -ExecutionPolicy Bypass -File install.ps1

**macOS / Linux:**

    git clone https://github.com/UsmaanShafiq/aiqamates.git
    cd aiqamates
    bash install.sh

This copies the `/qa` skill to `~/.claude/skills/qa/` and the agents to `~/.claude/agents/`, and installs ReportLab for PDFs.

To update later: `git pull` and run the installer again.

## Use

1. Open your project in Claude Code (a **new** session after installing).
2. Type `/qa` (or `/qa http://localhost:3000` to skip the URL question).
3. Claude reads your project (README, docs, page copy, database schema, business logic, recent git changes) and shows you what it thinks the app is for. Confirm or correct it in the **Project context** form, and answer a few questions only you can answer (who can do what, pricing rules, what must never break, known bugs to skip).
4. Answer the setup forms:
   - **Target**: app URL, environment (local / staging / production), login, allowed actions
   - **Scope**: full pass, quick smoke test or custom areas; critical flows; devices; report format
5. If your app needs a login, Claude opens it in the browser and **you** sign in. Claude never types passwords.
6. Read the report in `qa/qa-report.md` / `qa/qa-report.pdf`.
7. Pick what to fix in the final form (all P0, all P1, specific IDs, or nothing).
8. Claude fixes, retests, runs regression checks and writes the final report.

Your answers are saved in the project:
- `qa/qa-context.md`: what the app is, users and roles, business rules, known issues. **Edit it anytime** to teach the QA team about your app; items you confirmed are never asked again.
- `qa/qa-config.json`: URL, environment and scope, so the next `/qa` run offers "Reuse last settings".

**Tip:** the better your project's README (or `CLAUDE.md`) explains what the app does and for whom, the fewer questions `/qa` needs to ask.

## What's inside

| Path | Purpose |
|---|---|
| `skills/qa/SKILL.md` | The `/qa` command: forms, workflow and QA Lead rules |
| `skills/qa/templates/qa-report-template.md` | Report structure |
| `skills/qa/scripts/generate_qa_report.py` | Markdown → PDF converter |
| `agents/qa-*.md` | Specialist subagents: functional, UX, technical, adversarial, API, security, data/auth, accessibility, responsive/visual, performance |

## Workflow

1. Discover the project (framework, dev server, auth, routes)
2. Setup forms
3. QA plan (`qa/qa-plan.md`) and login handoff
4. Specialist agents test the app
5. Findings deduplicated, reproduced, rated P0–P4 → report + PDF
6. **Stop and ask** which issues to fix
7. Fix approved issues, retest each one
8. Regression run and final report

## Safety

- No application code changes until you approve fixes in the form.
- Specialist agents can't edit files at all.
- Production defaults to read-only.
- Claude never enters passwords, API keys or payment details.
