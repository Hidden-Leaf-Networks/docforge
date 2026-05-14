"""Reusable flowable components for PDF document building."""

from __future__ import annotations

import re

from reportlab.lib.units import inch
from reportlab.platypus import (
    NextPageTemplate,
    PageBreak,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import HRFlowable

from docforge.theme import DEFAULT_THEME, Theme, table_style, simple_table_style


def accent_divider(
    theme: Theme | None = None,
    use_secondary: bool = False,
    thickness: int = 2,
    space_before: int = 6,
    space_after: int = 12,
) -> HRFlowable:
    """Themed horizontal divider line."""
    t = theme or DEFAULT_THEME
    color = t.secondary_color if use_secondary else t.primary_color
    return HRFlowable(
        width="100%",
        thickness=thickness,
        color=color,
        spaceBefore=space_before,
        spaceAfter=space_after,
        lineCap="round",
    )


def gray_divider(
    theme: Theme | None = None,
    thickness: int = 1,
    space_before: int = 6,
    space_after: int = 12,
) -> HRFlowable:
    """Subtle gray divider."""
    t = theme or DEFAULT_THEME
    return HRFlowable(
        width="100%",
        thickness=thickness,
        color=t.grid,
        spaceBefore=space_before,
        spaceAfter=space_after,
    )


def cover_page(
    story: list,
    styles: dict,
    title: str,
    doc_type: str,
    date_str: str,
    author: str,
    organization: str,
    location: str = "",
    tagline: str = "",
    theme: Theme | None = None,
    client: str = "",
) -> None:
    """Build a professional cover page.

    Args:
        story: List to append flowables to.
        styles: Style dictionary from build_styles().
        title: Document title.
        doc_type: Type label (e.g., "BUSINESS PLAN", "REPORT").
        date_str: Formatted date string.
        author: Author name.
        organization: Organization or business name.
        location: Optional location string.
        tagline: Optional tagline for bottom of cover.
        theme: Theme for accent divider.
        client: Client name for "Prepared for" line. Falls back to organization.
    """
    t = theme or DEFAULT_THEME

    story.append(Spacer(1, 1.8 * inch))
    story.append(Paragraph(doc_type.upper(), styles["DocType"]))
    story.append(Paragraph(title, styles["CoverTitle"]))
    story.append(accent_divider(t, thickness=3, space_before=8, space_after=20))

    prepared_for = client or organization
    story.append(Paragraph(f"<b>Prepared for:</b> {prepared_for}", styles["Meta"]))
    if location:
        story.append(Paragraph(f"<b>Location:</b> {location}", styles["Meta"]))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(f"<b>Date:</b> {date_str}", styles["Meta"]))
    story.append(Paragraph(f"<b>Prepared by:</b> {author}", styles["Meta"]))

    if tagline:
        story.append(Spacer(1, 0.8 * inch))
        story.append(Paragraph(tagline, styles["CoverTagline"]))

    story.append(NextPageTemplate("Standard"))
    story.append(PageBreak())


def section_header(
    story: list,
    styles: dict,
    title: str,
    new_page: bool = True,
    theme: Theme | None = None,
) -> None:
    """Add a section header with themed accent divider."""
    if new_page:
        story.append(PageBreak())
    story.append(Paragraph(title, styles["H2"]))
    story.append(accent_divider(theme, thickness=2, space_before=4, space_after=12))


def subsection_header(story: list, styles: dict, title: str) -> None:
    """Add a subsection header."""
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(title, styles["H3"]))
    story.append(Spacer(1, 0.08 * inch))


def add_paragraph(story: list, styles: dict, text: str) -> None:
    """Add a body paragraph."""
    story.append(Paragraph(text, styles["Body"]))


def add_bullet_list(story: list, styles: dict, items: list[str]) -> None:
    """Add a bulleted list."""
    for item in items:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {item}", styles["Bullet"]))


def add_numbered_list(story: list, styles: dict, items: list[str]) -> None:
    """Add a numbered list."""
    for i, item in enumerate(items, 1):
        story.append(Paragraph(f"<b>{i}.</b> {item}", styles["Bullet"]))


def add_table(
    story: list,
    data: list[list],
    col_widths: list | None = None,
    style: str = "standard",
    theme: Theme | None = None,
) -> None:
    """Add a professionally styled table.

    Args:
        story: List to append flowables to.
        data: 2D list of table data (first row is header).
        col_widths: Optional list of column widths.
        style: "standard" (alternating rows) or "simple".
        theme: Theme for table colors.
    """
    story.append(Spacer(1, 0.1 * inch))
    tbl = Table(data, colWidths=col_widths)
    ts = simple_table_style(theme) if style == "simple" else table_style(theme)
    tbl.setStyle(TableStyle(ts))
    story.append(tbl)
    story.append(Spacer(1, 0.15 * inch))


def add_metadata_table(
    story: list,
    metadata_pairs: list[list[str]],
    theme: Theme | None = None,
) -> None:
    """Add a metadata/info table (key-value pairs)."""
    t = theme or DEFAULT_THEME
    tbl = Table(metadata_pairs, colWidths=[1.8 * inch, 4.5 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), t.grid),
        ("FONTNAME", (0, 0), (0, -1), t.font_heading),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, t.grid),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.15 * inch))


def add_callout(story: list, styles: dict, text: str) -> None:
    """Add a callout/quote block."""
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(text, styles["Callout"]))
    story.append(Spacer(1, 0.1 * inch))


# ---------------------------------------------------------------------------
# Markdown → ReportLab conversion
# ---------------------------------------------------------------------------


def convert_markdown_inline(text: str) -> str:
    """Convert inline markdown to ReportLab XML tags.

    Handles **bold**, *italic*, and `code` spans.
    """
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = text.replace("---", "")
    return text


def parse_markdown_content(
    content: str,
    story: list,
    styles: dict,
    theme: Theme | None = None,
) -> None:
    """Parse markdown-style content and add to story.

    Handles headings (#/##/###), bold/italic inline formatting,
    bullet points (- or *), numbered lists, horizontal rules, and
    regular paragraphs.
    """
    lines = content.split("\n")
    current_paragraph: list[str] = []
    list_items: list[str] = []
    list_type: str | None = None

    def flush_paragraph():
        nonlocal current_paragraph
        if current_paragraph:
            text = " ".join(current_paragraph).strip()
            if text:
                text = convert_markdown_inline(text)
                story.append(Paragraph(text, styles["Body"]))
            current_paragraph = []

    def flush_list():
        nonlocal list_items, list_type
        if list_items:
            formatted = [convert_markdown_inline(item) for item in list_items]
            if list_type == "numbered":
                add_numbered_list(story, styles, formatted)
            else:
                add_bullet_list(story, styles, formatted)
            list_items = []
        list_type = None

    table_rows: list[list[str]] = []

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        # Filter out separator rows (e.g., |---|---|)
        data_rows = [
            r for r in table_rows
            if not all(re.match(r"^[-:]+$", cell.strip()) for cell in r)
        ]
        if len(data_rows) < 1:
            table_rows = []
            return

        t = theme or DEFAULT_THEME
        cell_style = styles["Body"].clone("MDTableCell")
        cell_style.fontSize = 9.5
        cell_style.spaceAfter = 0
        cell_style.alignment = 0  # TA_LEFT

        num_cols = max(len(row) for row in data_rows)
        # Pad rows to equal column count
        padded = [row + [""] * (num_cols - len(row)) for row in data_rows]
        # Wrap cells in Paragraphs for text wrapping and inline formatting
        wrapped = []
        for row in padded:
            wrapped.append([
                Paragraph(convert_markdown_inline(cell.strip()), cell_style)
                for cell in row
            ])

        avail_width = 6.3 * inch
        col_width = avail_width / num_cols
        col_widths = [col_width] * num_cols

        md_table = Table(wrapped, colWidths=col_widths)
        md_table.setStyle(TableStyle(simple_table_style(t)))
        story.append(md_table)
        story.append(Spacer(1, 0.15 * inch))
        table_rows = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            if table_rows:
                flush_table()
            continue

        # Markdown table row (starts and ends with |, or contains | separators)
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_list()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            table_rows.append(cells)
            continue

        # If we were accumulating table rows but hit a non-table line, flush
        if table_rows:
            flush_table()

        # Horizontal rule
        if stripped in ("---", "***", "___"):
            flush_paragraph()
            flush_list()
            story.append(accent_divider(theme, thickness=1, space_before=8, space_after=8))
            continue

        header_text = stripped.lstrip("#").strip().replace("**", "")

        if stripped.startswith("### "):
            flush_paragraph()
            flush_list()
            subsection_header(story, styles, header_text)
        elif stripped.startswith("## "):
            flush_paragraph()
            flush_list()
            section_header(story, styles, header_text, new_page=False, theme=theme)
        elif stripped.startswith("# "):
            flush_paragraph()
            flush_list()
            section_header(story, styles, header_text, new_page=True, theme=theme)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            flush_paragraph()
            if list_type == "numbered":
                flush_list()
            list_type = "bullet"
            list_items.append(stripped[2:])
        elif re.match(r"^\d+[.)]\s", stripped):
            flush_paragraph()
            if list_type == "bullet":
                flush_list()
            list_type = "numbered"
            list_items.append(re.sub(r"^\d+[.)]\s*", "", stripped))
        else:
            flush_list()
            bold_header_match = re.match(r"^\*\*(\d+\.\s*)?([^*]+)\*\*:?\s*$", stripped)
            if bold_header_match:
                flush_paragraph()
                subsection_header(story, styles, bold_header_match.group(2).strip())
            elif stripped.isupper() and len(stripped) < 60 and ":" not in stripped:
                flush_paragraph()
                section_header(story, styles, stripped.title(), new_page=False, theme=theme)
            else:
                current_paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    flush_table()
