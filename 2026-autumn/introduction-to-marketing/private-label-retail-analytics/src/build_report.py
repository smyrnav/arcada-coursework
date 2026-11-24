"""Build the report docx from report/report_draft.md.

Supports the restricted markdown subset used in the draft:
#, ##, ### headings; pipe tables; ![caption](path) images; - bullets;
*italic* source lines; paragraphs. Output goes to ~/Downloads.
"""
import re
import shutil
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "report" / "report_draft.md"
OUT = Path.home() / "Downloads" / "Group_Work_Introduction_to_Marketing_2026_Smyrna_Volzhevska.docx"

MD_LINE = re.compile(r"^(#{1,3})\s+(.*)$")
IMG = re.compile(r"^!\[(.*?)\]\((.*?)\)$")
TABLE_ROW = re.compile(r"^\|(.+)\|$")


def add_runs(par, text):
    """Minimal inline formatting: **bold** and *italic*."""
    for tok in re.split(r"(\*\*.+?\*\*|\*[^*]+?\*)", text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            par.add_run(tok[2:-2]).bold = True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            par.add_run(tok[1:-1]).italic = True
        else:
            par.add_run(tok)


def build():
    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(11)

    lines = SRC.read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
        m = MD_LINE.match(line)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            if level == 1 and text.startswith("Introduction to Marketing"):
                doc.add_heading(text, 0)
            else:
                doc.add_heading(text, level)
            i += 1
            continue
        m = IMG.match(line)
        if m:
            caption, rel = m.group(1), m.group(2)
            img = (BASE / "report" / rel).resolve()
            doc.add_picture(str(img), width=Inches(6.0))
            if caption:
                p = doc.add_paragraph()
                r = p.add_run(caption)
                r.italic = True
                r.font.size = Pt(9)
            i += 1
            continue
        if TABLE_ROW.match(line):
            rows = []
            while i < len(lines) and TABLE_ROW.match(lines[i].strip()):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):  # skip separator
                    rows.append(cells)
                i += 1
            table = doc.add_table(rows=len(rows), cols=len(rows[0]))
            table.style = "Light Grid Accent 1"
            for r, row in enumerate(rows):
                for c, cell in enumerate(row):
                    table.cell(r, c).text = cell
            continue
        if line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            add_runs(p, line[2:])
            i += 1
            continue
        # paragraph: merge continuation lines
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not (
            MD_LINE.match(lines[i]) or IMG.match(lines[i].strip())
            or TABLE_ROW.match(lines[i].strip()) or lines[i].startswith("- ")):
            para.append(lines[i].rstrip())
            i += 1
        p = doc.add_paragraph()
        add_runs(p, " ".join(para))

    doc.save(OUT)
    print(f"saved {OUT}")


if __name__ == "__main__":
    build()
