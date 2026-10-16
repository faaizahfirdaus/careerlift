"""ATS-friendly single-column resume PDF generator (reportlab)."""
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

NAVY = colors.HexColor("#0F2B46")

def _esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build_resume(p: dict, target_role: str = "") -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=16*mm, bottomMargin=16*mm, title=f"Resume - {p.get('name','')}")
    name = ParagraphStyle("n", fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=NAVY)
    contact = ParagraphStyle("c", fontName="Helvetica", fontSize=10, leading=13, textColor=colors.HexColor("#444444"))
    head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=10, spaceAfter=2)
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=10.5, leading=14.5)
    bullet = ParagraphStyle("bl", parent=body, leftIndent=12, bulletIndent=2)

    s = [Paragraph(_esc(p.get("name") or "Your Name"), name)]
    bits = [x for x in [p.get("city"), p.get("email"), p.get("phone")] if x]
    if bits:
        s.append(Paragraph(_esc("  |  ".join(bits)), contact))
    s.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceBefore=6, spaceAfter=2))

    skills = p.get("skills", [])
    role = target_role or "an entry-level role"
    summary = "Motivated candidate"
    if p.get("city"):
        summary += f" based in {p['city']}"
    summary += f" seeking {role}."
    if skills:
        summary += f" Skilled in {', '.join(skills[:5])}."
    if p.get("interests"):
        summary += f" Interested in {p['interests']}."
    s += [Paragraph("PROFESSIONAL SUMMARY", head), Paragraph(_esc(summary), body)]

    if skills:
        s += [Paragraph("SKILLS", head), Paragraph(_esc(", ".join(x.title() if len(x) > 3 else x.upper() for x in skills)), body)]
    if p.get("education"):
        s.append(Paragraph("EDUCATION", head))
        for line in p["education"].splitlines():
            if line.strip():
                s.append(Paragraph(_esc(line.strip()), bullet, bulletText="\u2022"))
    if p.get("experience"):
        s.append(Paragraph("EXPERIENCE / PROJECTS", head))
        for line in p["experience"].splitlines():
            if line.strip():
                s.append(Paragraph(_esc(line.strip()), bullet, bulletText="\u2022"))
    doc.build(s)
    return buf.getvalue()
