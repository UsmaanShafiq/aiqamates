# AI QA Mates

A reusable AI QA team for Claude Code. Type **`/qa`** in any project: Claude asks a few setup questions as clickable forms, runs a team of 10 specialist QA agents against your app, writes a QA report (Markdown + PDF), then asks which issues to fix.

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

This copies the `/qa` skill to `~/.claude/skills/qa/` and the agents to `~/.claude/agents/`, installs ReportLab for PDFs, and adds a narrow permission rule to `~/.claude/settings.json` so the QA Office progress scripts (`qa_event.py`, `qa_office.py`) run without a prompt each time.

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
| `skills/qa/office/index.html` | The QA Office page (pixel-art team view) |
| `skills/qa/scripts/qa_office.py`, `qa_event.py` | QA Office server and progress logger |
| `agents/*.md` | The 10 specialist subagents (see The team) |

## QA Office: watch the team work

When `/qa` starts, a live **QA Office** opens in the browser pane: a pixel-art office where every agent sits at their own desk. You can see:

- who is **working** (typing, green code on their screen, a speech bubble saying what they're checking)
- who just **found a bug** (red flashing screen, a "!" and the severity)
- when the QA Lead is **waiting for you** to answer a form ("?")
- who is **done** (a little jump and a ✓), plus bug counts per severity, the current phase and an activity feed

Open it yourself anytime from a project folder:

    python ~/.claude/skills/qa/scripts/qa_office.py

Then visit `http://localhost:4477`. Use **Replay** to watch a finished run again, pick older runs from the dropdown, or press **Demo** (or add `?demo=1`) to see a simulated run. Progress is stored in `qa/live/` in your project.

## The team

| Role | Agent | What they check |
|---|---|---|
| QA Lead | `/qa` skill | Plans the run, coordinates the team, validates findings, owns the report |
| Functional Test Engineer | `functional-test-engineer` | Features, forms, CRUD, navigation, search, uploads |
| Exploratory UX Tester | `exploratory-ux-tester` | Confusing flows, dead ends, empty/loading/error states |
| Technical QA Engineer | `technical-qa-engineer` | Console errors, network failures, hydration, build/lint/types |
| Edge-Case Test Engineer | `edge-case-test-engineer` | Double submits, odd inputs, multiple tabs, interrupted flows |
| API Test Engineer | `api-test-engineer` | Endpoints, validation, status codes, error handling |
| Application Security Tester | `application-security-tester` | Access control, data exposure, sessions, injection (non-destructive) |
| Data Integrity & Access Control Analyst | `data-integrity-analyst` | Persistence, ownership, roles, login/logout |
| Accessibility Specialist | `accessibility-specialist` | Keyboard, focus, labels, contrast (WCAG 2.2 AA) |
| Visual & Responsive QA Engineer | `visual-qa-engineer` | Layouts on mobile, tablet and desktop |
| Performance Test Engineer | `performance-test-engineer` | Load speed, heavy assets, request counts, layout shift |

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
