"""
Configurable document theme system.

Themes define colors, fonts, page layout, and branding. Create custom themes
or use DEFAULT_THEME as a starting point.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth


@dataclass
class Theme:
    """Document theme configuration.

    All colors accept hex strings (e.g., "#14B8A6") or reportlab Color objects.
    """

    # Identity
    name: str = "default"
    brand_name: str = "DocForge"
    footer_text: str = "Generated with DocForge"
    footer_url: str = ""

    # Colors (hex strings)
    primary: str = "#14B8A6"       # Teal accent
    secondary: str = "#F97316"     # Orange accent
    text_dark: str = "#111827"     # Near-black body text
    text_gray: str = "#374151"     # Dark gray
    grid_color: str = "#D1D5DB"    # Grid/border lines
    bg_light: str = "#F3F4F6"     # Light background

    # Page layout
    page_size: tuple = LETTER
    margin_left: float = 0.85
    margin_right: float = 0.85
    margin_top: float = 0.85
    margin_bottom: float = 0.85

    # Fonts
    font_body: str = "Helvetica"
    font_heading: str = "Helvetica-Bold"
    font_italic: str = "Helvetica-Oblique"
    font_mono: str = "Courier"

    @property
    def primary_color(self) -> colors.Color:
        return HexColor(self.primary)

    @property
    def secondary_color(self) -> colors.Color:
        return HexColor(self.secondary)

    @property
    def text_dark_color(self) -> colors.Color:
        return HexColor(self.text_dark)

    @property
    def text_gray_color(self) -> colors.Color:
        return HexColor(self.text_gray)

    @property
    def grid(self) -> colors.Color:
        return HexColor(self.grid_color)

    @property
    def bg(self) -> colors.Color:
        return HexColor(self.bg_light)

    @property
    def ml(self) -> float:
        return self.margin_left * inch

    @property
    def mr(self) -> float:
        return self.margin_right * inch

    @property
    def mt(self) -> float:
        return self.margin_top * inch

    @property
    def mb(self) -> float:
        return self.margin_bottom * inch

    def full_footer(self) -> str:
        if self.footer_url:
            return f"{self.footer_text} | {self.footer_url}"
        return self.footer_text


DEFAULT_THEME = Theme()


def build_styles(theme: Theme | None = None) -> dict[str, ParagraphStyle]:
    """Build paragraph styles from a theme."""
    t = theme or DEFAULT_THEME
    base = getSampleStyleSheet()
    styles: dict[str, ParagraphStyle] = {}

    styles["Body"] = ParagraphStyle(
        "ForgeBody",
        parent=base["BodyText"],
        fontName=t.font_body,
        fontSize=10.5,
        leading=15,
        textColor=t.text_dark_color,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
    )

    styles["H1"] = ParagraphStyle(
        "ForgeH1",
        parent=base["Heading1"],
        fontName=t.font_heading,
        fontSize=22,
        leading=26,
        textColor=t.text_dark_color,
        spaceAfter=12,
    )

    styles["H2"] = ParagraphStyle(
        "ForgeH2",
        parent=base["Heading2"],
        fontName=t.font_heading,
        fontSize=14,
        leading=18,
        textColor=t.primary_color,
        spaceBefore=16,
        spaceAfter=8,
    )

    styles["H3"] = ParagraphStyle(
        "ForgeH3",
        parent=base["Heading3"],
        fontName=t.font_heading,
        fontSize=12,
        leading=15,
        textColor=t.text_dark_color,
        spaceBefore=12,
        spaceAfter=6,
    )

    styles["Meta"] = ParagraphStyle(
        "ForgeMeta",
        parent=base["BodyText"],
        fontName=t.font_body,
        fontSize=10,
        leading=13,
        textColor=t.text_gray_color,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    styles["CoverTitle"] = ParagraphStyle(
        "ForgeCoverTitle",
        parent=base["Title"],
        fontName=t.font_heading,
        fontSize=28,
        leading=34,
        textColor=t.text_dark_color,
        alignment=TA_CENTER,
        spaceAfter=14,
    )

    styles["CoverTagline"] = ParagraphStyle(
        "ForgeCoverTagline",
        parent=base["BodyText"],
        fontName=t.font_italic,
        fontSize=12,
        leading=15,
        textColor=t.text_gray_color,
        alignment=TA_CENTER,
    )

    styles["DocType"] = ParagraphStyle(
        "ForgeDocType",
        parent=base["BodyText"],
        fontName=t.font_heading,
        fontSize=11,
        leading=14,
        textColor=t.primary_color,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=4,
    )

    styles["Bullet"] = ParagraphStyle(
        "ForgeBullet",
        parent=styles["Body"],
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=6,
    )

    styles["Callout"] = ParagraphStyle(
        "ForgeCallout",
        parent=base["BodyText"],
        fontName=t.font_italic,
        fontSize=10.5,
        leading=14,
        textColor=t.text_gray_color,
        leftIndent=20,
        rightIndent=20,
        spaceBefore=10,
        spaceAfter=10,
        borderColor=t.primary_color,
        borderWidth=2,
        borderPadding=10,
    )

    return styles


def table_style(theme: Theme | None = None) -> list:
    """Professional table style with themed header."""
    t = theme or DEFAULT_THEME
    return [
        ("BACKGROUND", (0, 0), (-1, 0), t.primary_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), t.font_heading),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.75, t.grid),
        ("FONTSIZE", (0, 1), (-1, -1), 9.5),
        ("FONTNAME", (0, 1), (-1, -1), t.font_body),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("TEXTCOLOR", (0, 1), (-1, -1), t.text_dark_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, t.bg]),
    ]


def simple_table_style(theme: Theme | None = None) -> list:
    """Simpler table style without alternating rows."""
    t = theme or DEFAULT_THEME
    return [
        ("BACKGROUND", (0, 0), (-1, 0), t.primary_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), t.font_heading),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, t.grid),
        ("FONTSIZE", (0, 1), (-1, -1), 9.5),
        ("FONTNAME", (0, 1), (-1, -1), t.font_body),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]


def draw_footer(canvas, doc, theme: Theme | None = None):
    """Draw footer with page number on standard pages."""
    t = theme or DEFAULT_THEME
    canvas.saveState()

    y = t.mb - 0.18 * inch
    canvas.setStrokeColor(t.grid)
    canvas.setLineWidth(0.5)
    canvas.line(t.ml, y, doc.pagesize[0] - t.mr, y)

    canvas.setFillColor(HexColor("#6B7280"))
    canvas.setFont(t.font_body, 8.5)
    canvas.drawString(t.ml, t.mb - 0.35 * inch, t.footer_text)

    page_str = f"Page {doc.page}"
    w = stringWidth(page_str, t.font_body, 8.5)
    canvas.drawString(doc.pagesize[0] - t.mr - w, t.mb - 0.35 * inch, page_str)

    canvas.restoreState()


def draw_cover_footer(canvas, doc, theme: Theme | None = None):
    """Footer for cover page (no page number, centered branding)."""
    t = theme or DEFAULT_THEME
    canvas.saveState()

    y = t.mb - 0.18 * inch
    canvas.setStrokeColor(t.primary_color)
    canvas.setLineWidth(1)
    canvas.line(t.ml, y, doc.pagesize[0] - t.mr, y)

    canvas.setFillColor(t.text_gray_color)
    canvas.setFont(t.font_body, 9)

    footer = t.full_footer()
    w = stringWidth(footer, t.font_body, 9)
    x = (doc.pagesize[0] - w) / 2
    canvas.drawString(x, t.mb - 0.35 * inch, footer)

    canvas.restoreState()
