"""PDF document templates with configurable theming."""

from __future__ import annotations

from functools import partial

from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

from docforge.theme import DEFAULT_THEME, Theme, draw_cover_footer, draw_footer


class ForgeDocument(BaseDocTemplate):
    """Professional document template with cover page and standard pages.

    Uses the provided theme for page layout, colors, and footer branding.
    """

    def __init__(self, filename: str, theme: Theme | None = None, **kwargs):
        self.theme = theme or DEFAULT_THEME
        t = self.theme

        super().__init__(
            filename,
            pagesize=t.page_size,
            leftMargin=t.ml,
            rightMargin=t.mr,
            topMargin=t.mt,
            bottomMargin=t.mb,
            **kwargs,
        )

        content_frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="content",
            showBoundary=0,
        )

        cover_template = PageTemplate(
            id="Cover",
            frames=[content_frame],
            onPage=partial(draw_cover_footer, theme=t),
        )

        standard_template = PageTemplate(
            id="Standard",
            frames=[content_frame],
            onPage=partial(draw_footer, theme=t),
        )

        self.addPageTemplates([cover_template, standard_template])


class SimpleForgeDocument(BaseDocTemplate):
    """Simplified document without cover page distinction.

    All pages use the standard footer with page numbers.
    """

    def __init__(self, filename: str, theme: Theme | None = None, **kwargs):
        self.theme = theme or DEFAULT_THEME
        t = self.theme

        super().__init__(
            filename,
            pagesize=t.page_size,
            leftMargin=t.ml,
            rightMargin=t.mr,
            topMargin=t.mt,
            bottomMargin=t.mb,
            **kwargs,
        )

        content_frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="content",
            showBoundary=0,
        )

        self.addPageTemplates([
            PageTemplate(
                id="Standard",
                frames=[content_frame],
                onPage=partial(draw_footer, theme=t),
            )
        ])
