#!/usr/bin/env python3
"""Convert qa/qa-report.md to a simple readable PDF.

Requires reportlab:
    pip install reportlab

Usage:
    python scripts/generate_qa_report.py qa/qa-report.md qa/qa-report.pdf
"""
import sys
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
    from reportlab.lib import colors
except ImportError:
    print("ReportLab is not installed. Install it with: pip install reportlab")
    sys.exit(2)

src = Path(sys.argv[1] if len(sys.argv) > 1 else "qa/qa-report.md")
dst = Path(sys.argv[2] if len(sys.argv) > 2 else "qa/qa-report.pdf")
text = src.read_text(encoding="utf-8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="QA_Title", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle(name="QA_H1", parent=styles["Heading1"], spaceBefore=12, spaceAfter=8))
styles.add(ParagraphStyle(name="QA_H2", parent=styles["Heading2"], spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="QA_Body", parent=styles["BodyText"], leading=14, spaceAfter=6))
styles.add(ParagraphStyle(name="QA_Code", parent=styles["Code"], fontSize=8, leading=10))

story = []
for line in text.splitlines():
    line = line.strip()
    if not line:
        story.append(Spacer(1, 5))
    elif line.startswith("# "):
        story.append(Paragraph(line[2:], styles["QA_Title"]))
    elif line.startswith("## "):
        story.append(Paragraph(line[3:], styles["QA_H1"]))
    elif line.startswith("### "):
        story.append(Paragraph(line[4:], styles["QA_H2"]))
    elif line.startswith("- "):
        story.append(Paragraph("• " + line[2:], styles["QA_Body"]))
    elif line.startswith("|"):
        # Keep tables readable by rendering rows as simple text blocks.
        story.append(Paragraph(line.replace("|", "  •  "), styles["QA_Body"]))
    else:
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        story.append(Paragraph(safe, styles["QA_Body"]))

dst.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(dst), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
doc.build(story)
print(f"Created {dst}")
