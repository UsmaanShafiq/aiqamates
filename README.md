# AI QA Team

Reusable QA system for Claude Code Desktop.

## Supported project types
- Next.js / React / Tailwind SaaS
- WordPress
- WooCommerce

## Main workflow

1. Claude discovers the project.
2. Claude creates the QA plan.
3. Specialized QA agents test the application.
4. Findings are reproduced and validated.
5. Claude generates `qa/qa-report.md` and `qa/qa-report.pdf`.
6. Claude stops and asks for explicit permission to fix.
7. After approval, Claude fixes approved issues.
8. Claude retests every fix.
9. Claude runs regression tests.
10. Claude regenerates the final PDF showing found, fixed, retested and remaining issues.

## Safety principle

The initial QA run must not modify application code.

## Recommended next setup

If browser access already works in Claude Code Desktop, start by asking Claude to use its available browser tooling. If you want deterministic browser automation, add Playwright to the project later.

For PDF generation, install ReportLab in the QA environment:

    pip install reportlab

Then the included script can convert the Markdown report to PDF.
