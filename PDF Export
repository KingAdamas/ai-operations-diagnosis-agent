"""
PDF export for The Diagnosis Engine.

Generates a clean, plain-language printable report from a diagnosis result.
Written for small business owners and entrepreneurs — no operations jargon.
Uses reportlab Platypus for clean multi-page layout.
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER


# ----------------------------------------------------------------------------
# Color palette (matches app navy/slate)
# ----------------------------------------------------------------------------
NAVY        = colors.HexColor("#0F2044")
SLATE       = colors.HexColor("#475569")
LIGHT_SLATE = colors.HexColor("#94A3B8")
AMBER       = colors.HexColor("#D97706")
AMBER_BG    = colors.HexColor("#FFFBEB")
AMBER_BORDER= colors.HexColor("#F59E0B")
RED         = colors.HexColor("#DC2626")
PURPLE      = colors.HexColor("#7C3AED")
BLUE        = colors.HexColor("#1D4ED8")
BLUE_BG     = colors.HexColor("#EFF6FF")
GREEN       = colors.HexColor("#166534")
GREEN_BG    = colors.HexColor("#F0FDF4")
BORDER      = colors.HexColor("#E2E8F0")
PAGE_BG     = colors.HexColor("#F8FAFC")
WHITE       = colors.white
BLACK       = colors.HexColor("#0F172A")


# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
def build_styles():
    return {
        "report_title": ParagraphStyle(
            "report_title",
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=WHITE,
            leading=28,
            alignment=TA_LEFT,
        ),
        "report_sub": ParagraphStyle(
            "report_sub",
            fontName="Helvetica",
            fontSize=11,
            textColor=colors.HexColor("#94A3B8"),
            leading=16,
            alignment=TA_LEFT,
        ),
        "section_heading": ParagraphStyle(
            "section_heading",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=NAVY,
            leading=18,
            spaceBefore=18,
            spaceAfter=6,
        ),
        "sub_heading": ParagraphStyle(
            "sub_heading",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=SLATE,
            leading=14,
            spaceBefore=12,
            spaceAfter=4,
            textTransform="uppercase",
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=10,
            textColor=BLACK,
            leading=15,
            spaceAfter=4,
        ),
        "body_italic": ParagraphStyle(
            "body_italic",
            fontName="Helvetica-Oblique",
            fontSize=10,
            textColor=SLATE,
            leading=15,
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=10,
            textColor=BLACK,
            leading=15,
            leftIndent=14,
            spaceAfter=3,
        ),
        "label_pill": ParagraphStyle(
            "label_pill",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=SLATE,
            leading=10,
        ),
        "classification": ParagraphStyle(
            "classification",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=BLUE,
            leading=16,
            leftIndent=10,
        ),
        "callout": ParagraphStyle(
            "callout",
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#78350F"),
            leading=15,
            leftIndent=10,
        ),
        "exec_summary": ParagraphStyle(
            "exec_summary",
            fontName="Helvetica",
            fontSize=11,
            textColor=colors.HexColor("#1E3A8A"),
            leading=17,
            leftIndent=10,
        ),
        "verification_label": ParagraphStyle(
            "verification_label",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=WHITE,
            leading=12,
        ),
        "verification_value": ParagraphStyle(
            "verification_value",
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#E2E8F0"),
            leading=14,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Helvetica",
            fontSize=8,
            textColor=LIGHT_SLATE,
            leading=11,
            alignment=TA_CENTER,
        ),
    }


# ----------------------------------------------------------------------------
# Plain language label maps
# ----------------------------------------------------------------------------
DIRECTION_LABELS = {
    "increase": "Should go up",
    "decrease": "Should go down",
    "hold": "Should stay steady",
}

DIRECTION_ARROWS = {
    "increase": "UP",
    "decrease": "DOWN",
    "hold": "STEADY",
}

TYPE_LABELS = {
    "leading": "Early warning",
    "lagging": "End result",
}


# ----------------------------------------------------------------------------
# Header/footer canvas callback
# ----------------------------------------------------------------------------
def _on_page(canvas, doc, mode_label):
    canvas.saveState()
    w, h = letter

    # Navy header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 0.55 * inch, w, 0.55 * inch, fill=1, stroke=0)

    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(WHITE)
    canvas.drawString(0.6 * inch, h - 0.35 * inch, "The Diagnosis Engine")

    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#94A3B8"))
    canvas.drawRightString(w - 0.6 * inch, h - 0.35 * inch, mode_label)

    # Footer
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LIGHT_SLATE)
    canvas.drawCentredString(
        w / 2,
        0.35 * inch,
        f"Page {doc.page}   |   Layered Thinking Framework   |   {datetime.today().strftime('%B %d, %Y')}",
    )
    canvas.restoreState()


# ----------------------------------------------------------------------------
# Section block helpers
# ----------------------------------------------------------------------------
def _hr(story, color=BORDER, thickness=0.5):
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=4))


def _section(story, title, styles):
    story.append(Spacer(1, 6))
    story.append(Paragraph(title, styles["section_heading"]))
    _hr(story)


def _sub(story, title, styles):
    story.append(Paragraph(title, styles["sub_heading"]))


def _bullet(story, text, styles, color=NAVY):
    story.append(Paragraph(f"<bullet bulletIndent='0' bulletFontName='Helvetica-Bold' bulletColor='#{color.hexval()[2:]}'>&#x2022;</bullet>{text}", styles["bullet"]))


def _callout_box(story, label, text, styles, bg=AMBER_BG, border=AMBER_BORDER, text_style="callout"):
    data = [[
        Paragraph(label, ParagraphStyle(
            "cl", fontName="Helvetica-Bold", fontSize=8,
            textColor=border, leading=10,
        )),
        Paragraph(text, styles[text_style]),
    ]]
    t = Table(data, colWidths=[0.85 * inch, 5.65 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (0, 0), 8),
        ("RIGHTPADDING", (0, 0), (0, 0), 4),
        ("LEFTPADDING", (1, 0), (1, 0), 8),
        ("RIGHTPADDING", (1, 0), (1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEBEFORE", (0, 0), (0, -1), 3, border),
        ("ROUNDEDCORNERS", [4]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))


# ----------------------------------------------------------------------------
# Main export function
# ----------------------------------------------------------------------------
def generate_pdf(data: dict, mode: str) -> bytes:
    """
    Build a plain-language PDF report from a diagnosis result dict.
    Returns PDF bytes suitable for st.download_button.
    """
    is_project = mode == "project"
    mode_label = "Project Recovery" if is_project else "Operations Diagnosis"

    layer_1_key = "layer_1_visible_risks" if is_project else "layer_1_symptoms"
    layer_2_key = "layer_2_risk_drivers" if is_project else "layer_2_root_causes"
    layer_2_item_key = "driver" if is_project else "cause"
    layer_2_link_key = "explains_risks" if is_project else "explains_symptoms"

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.65 * inch,
        title="Diagnosis Report",
        author="The Diagnosis Engine",
    )

    styles = build_styles()
    story = []

    # ── Cover block ──────────────────────────────────────────────────────────
    cover_data = [[
        Paragraph("Business Diagnosis Report", styles["report_title"]),
        Paragraph(
            f"{mode_label}&nbsp;&nbsp;|&nbsp;&nbsp;{datetime.today().strftime('%B %d, %Y')}",
            styles["report_sub"],
        ),
    ]]
    cover = Table(cover_data, colWidths=[6.8 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (0, 0), 18),
        ("BOTTOMPADDING", (0, 0), (0, 0), 4),
        ("TOPPADDING", (0, 1), (0, 1), 4),
        ("BOTTOMPADDING", (0, 1), (0, 1), 18),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(cover)
    story.append(Spacer(1, 14))

    # ── What this report is ──────────────────────────────────────────────────
    story.append(Paragraph(
        "This report walks you through a layered diagnosis of your business issue. "
        "It starts with what you can see on the surface, works down to what is causing it, "
        "and finishes with a plain action plan you can start using this week. "
        "Each section builds on the one before it.",
        styles["body"],
    ))
    story.append(Spacer(1, 8))

    # ── Issue type ───────────────────────────────────────────────────────────
    _section(story, "What Kind of Problem Is This?", styles)
    class_data = [[Paragraph(data["classification"], styles["classification"])]]
    class_table = Table(class_data, colWidths=[6.8 * inch])
    class_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LINEBEFORE", (0, 0), (0, -1), 4, BLUE),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(class_table)
    story.append(Spacer(1, 6))

    # ── Layer 1 ──────────────────────────────────────────────────────────────
    _section(story, "What You Are Seeing Right Now", styles)
    story.append(Paragraph(
        "These are the signs that something is off. You may already be aware of some of these.",
        styles["body_italic"],
    ))
    story.append(Spacer(1, 4))
    for item in data[layer_1_key]:
        _bullet(story, item, styles)

    if data.get("layer_1_threshold_gate"):
        story.append(Spacer(1, 6))
        _callout_box(
            story,
            "PATTERN CHECK",
            data["layer_1_threshold_gate"],
            styles,
            bg=colors.HexColor("#F8FAFC"),
            border=SLATE,
            text_style="body_italic",
        )

    # ── Layer 2 ──────────────────────────────────────────────────────────────
    _section(story, "What Is Causing It", styles)
    story.append(Paragraph(
        "These are the real reasons the problems above keep happening. "
        "Fixing just the surface signs without addressing these will not stick.",
        styles["body_italic"],
    ))
    story.append(Spacer(1, 4))
    for item in data[layer_2_key]:
        cause_text = item[layer_2_item_key]
        linked = item[layer_2_link_key]
        linked_str = ", ".join(linked) if isinstance(linked, list) else linked
        block = KeepTogether([
            Paragraph(f"<b>{cause_text}</b>", styles["bullet"]),
            Paragraph(
                f"Connects to: {linked_str}",
                ParagraphStyle(
                    "link", fontName="Helvetica-Oblique", fontSize=9,
                    textColor=LIGHT_SLATE, leading=13, leftIndent=14, spaceAfter=6,
                ),
            ),
        ])
        story.append(block)

    if data.get("layer_2_threshold_gate"):
        story.append(Spacer(1, 6))
        _callout_box(
            story,
            "PATTERN CHECK",
            data["layer_2_threshold_gate"],
            styles,
            bg=colors.HexColor("#F8FAFC"),
            border=SLATE,
            text_style="body_italic",
        )

    # ── Layer 3 ──────────────────────────────────────────────────────────────
    _section(story, "The Deeper System Problem", styles)
    story.append(Paragraph(
        "These are the conditions in your business that are allowing the causes above to keep coming back. "
        "Until these change, the problem is likely to return even after you fix the surface issues.",
        styles["body_italic"],
    ))
    story.append(Spacer(1, 4))
    for item in data["layer_3_structural"]:
        _bullet(story, item, styles)

    if data.get("layer_3_bias_check"):
        story.append(Spacer(1, 6))
        _callout_box(
            story,
            "BLIND SPOT CHECK",
            data["layer_3_bias_check"],
            styles,
            bg=AMBER_BG,
            border=AMBER_BORDER,
            text_style="callout",
        )

    # ── What to do ───────────────────────────────────────────────────────────
    _section(story, "What to Do About It", styles)
    story.append(Paragraph(
        "Each action below targets a specific cause or system problem identified above.",
        styles["body_italic"],
    ))
    story.append(Spacer(1, 6))
    for i, action in enumerate(data["recommended_actions"], 1):
        block_data = [[
            Paragraph(str(i), ParagraphStyle(
                "num", fontName="Helvetica-Bold", fontSize=11,
                textColor=WHITE, leading=14, alignment=TA_CENTER,
            )),
            [
                Paragraph(action["action"], styles["body"]),
                Paragraph(
                    f"This addresses: {action['addresses']}",
                    ParagraphStyle(
                        "addr", fontName="Helvetica-Oblique", fontSize=9,
                        textColor=LIGHT_SLATE, leading=13,
                    ),
                ),
            ],
        ]]
        block_table = Table(block_data, colWidths=[0.35 * inch, 6.35 * inch])
        block_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), NAVY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (0, 0), 4),
            ("RIGHTPADDING", (0, 0), (0, 0), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (1, 0), (1, 0), 10),
            ("ROUNDEDCORNERS", [4]),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ]))
        story.append(block_table)
        story.append(Spacer(1, 6))

    # ── Action plan ──────────────────────────────────────────────────────────
    _section(story, "Your Step-by-Step Plan", styles)
    story.append(Paragraph(
        "Follow these three phases in order. Do not skip to Execution before you finish Discovery.",
        styles["body_italic"],
    ))
    story.append(Spacer(1, 6))

    phase_colors = {
        "Discovery": colors.HexColor("#EFF6FF"),
        "Structuring": colors.HexColor("#F0FDF4"),
        "Execution": colors.HexColor("#FFF7ED"),
    }
    phase_border_colors = {
        "Discovery": BLUE,
        "Structuring": GREEN,
        "Execution": AMBER,
    }
    phase_plain_names = {
        "Discovery": "Step 1: Find Out What Is Really Going On",
        "Structuring": "Step 2: Put the Right Things in Place",
        "Execution": "Step 3: Run It and Watch the Numbers",
    }

    for phase in data["action_plan"]:
        phase_name = phase["phase"]
        actions_paragraphs = [
            Paragraph(
                f"<bullet bulletIndent='0' bulletFontName='Helvetica-Bold'>&#x2022;</bullet>{a}",
                ParagraphStyle(
                    "pa", fontName="Helvetica", fontSize=10,
                    textColor=BLACK, leading=15, leftIndent=10, spaceAfter=3,
                ),
            )
            for a in phase["actions"]
        ]
        header = Paragraph(
            phase_plain_names.get(phase_name, phase_name),
            ParagraphStyle(
                "ph", fontName="Helvetica-Bold", fontSize=11,
                textColor=NAVY, leading=15,
            ),
        )
        focus = Paragraph(
            phase["focus"],
            ParagraphStyle(
                "pf", fontName="Helvetica-Oblique", fontSize=10,
                textColor=SLATE, leading=14, spaceAfter=6,
            ),
        )
        inner = [header, Spacer(1, 3), focus] + actions_paragraphs
        block_data = [[inner]]
        block_table = Table(block_data, colWidths=[6.8 * inch])
        block_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), phase_colors.get(phase_name, colors.HexColor("#F8FAFC"))),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LINEBEFORE", (0, 0), (0, -1), 4, phase_border_colors.get(phase_name, NAVY)),
            ("ROUNDEDCORNERS", [4]),
        ]))
        story.append(block_table)
        story.append(Spacer(1, 8))

    # ── Numbers to track ─────────────────────────────────────────────────────
    _section(story, "Numbers to Watch", styles)
    story.append(Paragraph(
        "These are the metrics that will tell you whether the changes are working. "
        "Check them on a regular schedule, not just when something goes wrong.",
        styles["body_italic"],
    ))
    story.append(Spacer(1, 6))

    kpi_header = [
        Paragraph("Metric", ParagraphStyle("kh", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12)),
        Paragraph("Direction", ParagraphStyle("kh", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12)),
        Paragraph("Type", ParagraphStyle("kh", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12)),
        Paragraph("What to aim for", ParagraphStyle("kh", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12)),
    ]
    kpi_rows = [kpi_header]
    for kpi in data["kpis"]:
        direction = kpi["direction"]
        kpi_type = kpi["type"]
        arrow = "UP" if direction == "increase" else "DOWN" if direction == "decrease" else "STEADY"
        kpi_rows.append([
            Paragraph(kpi["kpi"], ParagraphStyle("kb", fontName="Helvetica", fontSize=9, textColor=BLACK, leading=13)),
            Paragraph(f"{arrow}", ParagraphStyle("kd", fontName="Helvetica-Bold", fontSize=9, textColor=NAVY, leading=13)),
            Paragraph(TYPE_LABELS.get(kpi_type, kpi_type), ParagraphStyle("kt", fontName="Helvetica", fontSize=9, textColor=SLATE, leading=13)),
            Paragraph(kpi["target_or_threshold"], ParagraphStyle("ktar", fontName="Helvetica", fontSize=9, textColor=BLACK, leading=13)),
        ])

    kpi_table = Table(kpi_rows, colWidths=[1.8 * inch, 0.85 * inch, 0.95 * inch, 3.1 * inch])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F8FAFC")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 6))

    # ── Assumptions to check ─────────────────────────────────────────────────
    _section(story, "Check These Before You Start", styles)
    story.append(Paragraph(
        "This diagnosis makes some assumptions. Confirm these are true before you act on the recommendations.",
        styles["body_italic"],
    ))
    story.append(Spacer(1, 4))
    for item in data["assumptions_to_test"]:
        _callout_box(
            story,
            "CHECK",
            item,
            styles,
            bg=AMBER_BG,
            border=AMBER_BORDER,
            text_style="callout",
        )

    # ── Verification ─────────────────────────────────────────────────────────
    if data.get("verification"):
        v = data["verification"]
        _section(story, "How You Will Know It Worked", styles)
        story.append(Paragraph(
            "Before you make any changes, decide in advance what success looks like. "
            "This protects you from convincing yourself something worked when it did not.",
            styles["body_italic"],
        ))
        story.append(Spacer(1, 6))

        direction = v["direction"]
        arrow_word = DIRECTION_LABELS.get(direction, direction)

        ver_rows = [
            [
                Paragraph("The number to watch", ParagraphStyle("vl", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12)),
                Paragraph(v["metric"], ParagraphStyle("vv", fontName="Helvetica", fontSize=10, textColor=BLACK, leading=14)),
            ],
            [
                Paragraph("What it should do", ParagraphStyle("vl", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12)),
                Paragraph(f"{arrow_word} — {v['threshold']}", ParagraphStyle("vv", fontName="Helvetica", fontSize=10, textColor=BLACK, leading=14)),
            ],
            [
                Paragraph("If it does not move", ParagraphStyle("vl", fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#FCA5A5"), leading=12)),
                Paragraph(v["counter_signal"], ParagraphStyle("vv", fontName="Helvetica", fontSize=10, textColor=BLACK, leading=14)),
            ],
        ]
        ver_table = Table(ver_rows, colWidths=[1.6 * inch, 5.2 * inch])
        ver_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 1), NAVY),
            ("BACKGROUND", (0, 2), (0, 2), colors.HexColor("#7F1D1D")),
            ("BACKGROUND", (1, 0), (1, -1), WHITE),
            ("ROWBACKGROUNDS", (1, 0), (1, -1), [WHITE, colors.HexColor("#F8FAFC"), colors.HexColor("#FFF1F2")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROUNDEDCORNERS", [4]),
        ]))
        story.append(ver_table)
        story.append(Spacer(1, 6))

    # ── Executive summary ─────────────────────────────────────────────────────
    _section(story, "The Short Version", styles)
    exec_data = [[Paragraph(data["executive_summary"], styles["exec_summary"])]]
    exec_table = Table(exec_data, colWidths=[6.8 * inch])
    exec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LINEBEFORE", (0, 0), (0, -1), 4, BLUE),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 20))

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(
        story,
        onFirstPage=lambda c, d: _on_page(c, d, mode_label),
        onLaterPages=lambda c, d: _on_page(c, d, mode_label),
    )
    return buf.getvalue()
