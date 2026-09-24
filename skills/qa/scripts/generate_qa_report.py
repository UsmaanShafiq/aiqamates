#!/usr/bin/env python3
"""Convert qa/qa-report.md to a readable PDF.

Requires reportlab:
    pip install reportlab

Usage:
    python generate_qa_report.py qa/qa-report.md qa/qa-report.pdf
"""
import re
import sys
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle
except ImportError:
    print("ReportLab is not installed. Install it with: pip install reportlab")
    sys.exit(2)

src = Path(sys.argv[1] if len(sys.argv) > 1 else "qa/qa-report.md")
dst = Path(sys.argv[2] if len(sys.argv) > 2 else "qa/qa-report.pdf")
lines = src.read_text(encoding="utf-8").splitlines()

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="QA_Title", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle(name="QA_H1", parent=styles["Heading1"], spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle(name="QA_H2", parent=styles["Heading2"], spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="QA_H3", parent=styles["Heading3"], spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name="QA_Body", parent=styles["BodyText"], leading=14, spaceAfter=4))
styles.add(ParagraphStyle(name="QA_Bullet", parent=styles["QA_Body"], leftIndent=14, bulletIndent=4))
styles.add(ParagraphStyle(name="QA_Cell", parent=styles["BodyText"], fontSize=8.5, leading=11))
styles.add(ParagraphStyle(name="QA_Code", parent=styles["Code"], fontSize=8, leading=10,
                          backColor=colors.whitesmoke, borderPadding=4))


def inline(text):
    """Escape XML and convert **bold**, *italic* and `code` to ReportLab markup."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", text)
    return text


def split_row(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def build_table(rows):
    rows = [r for r in rows if not re.fullmatch(r"\|?[\s:\-|]+\|?", r.strip())]
    data = [[Paragraph(inline(c), styles["QA_Cell"]) for c in split_row(r)] for r in rows]
    width = max(len(r) for r in data)
    data = [r + [""] * (width - len(r)) for r in data]
    avail = A4[0] - 84
    t = Table(data, colWidths=[avail / width] * width, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8ECF3")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C0CC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


story = []
i = 0
while i < len(lines):
    raw = lines[i]
    line = raw.strip()
    if line.startswith("```"):
        block = []
        i += 1
        while i < len(lines) and not lines[i].strip().startswith("```"):
            block.append(lines[i])
            i += 1
        story.append(Preformatted("\n".join(block), styles["QA_Code"]))
        story.append(Spacer(1, 6))
    elif line.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append(lines[i])
            i += 1
        story.append(build_table(rows))
        story.append(Spacer(1, 8))
        continue
    elif not line:
        story.append(Spacer(1, 4))
    elif line.startswith("# "):
        story.append(Paragraph(inline(line[2:]), styles["QA_Title"]))
    elif line.startswith("## "):
        story.append(Paragraph(inline(line[3:]), styles["QA_H1"]))
    elif line.startswith("### "):
        story.append(Paragraph(inline(line[4:]), styles["QA_H2"]))
    elif line.startswith("#### "):
        story.append(Paragraph(inline(line[5:]), styles["QA_H3"]))
    elif re.match(r"[-*] ", line):
        indent = (len(raw) - len(raw.lstrip())) // 2
        style = ParagraphStyle(name=f"b{indent}", parent=styles["QA_Bullet"], leftIndent=14 + indent * 12,
                               bulletIndent=4 + indent * 12)
        story.append(Paragraph(inline(line[2:]), style, bulletText="•"))
    elif re.match(r"\d+\. ", line):
        num, rest = line.split(" ", 1)
        story.append(Paragraph(inline(rest), styles["QA_Bullet"], bulletText=num))
    else:
        story.append(Paragraph(inline(line), styles["QA_Body"]))
    i += 1

dst.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(dst), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42,
                        title="QA Report")
doc.build(story)
print(f"Created {dst}")
