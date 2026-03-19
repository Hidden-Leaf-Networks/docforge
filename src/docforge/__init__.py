"""
DocForge — Professional document generation with configurable theming.

Supports PDF, Word (.docx), and multi-format chat/conversation export.
Built by Hidden Leaf Networks.
"""

__version__ = "0.1.0"

from docforge.theme import Theme, build_styles, DEFAULT_THEME
from docforge.pdf.document import ForgeDocument, SimpleForgeDocument
from docforge.pdf.components import (
    cover_page,
    section_header,
    subsection_header,
    add_paragraph,
    add_bullet_list,
    add_numbered_list,
    add_table,
    add_metadata_table,
    add_callout,
    accent_divider,
    parse_markdown_content,
)
from docforge.generator import DocumentGenerator

__all__ = [
    # Theme
    "Theme",
    "build_styles",
    "DEFAULT_THEME",
    # PDF
    "ForgeDocument",
    "SimpleForgeDocument",
    "DocumentGenerator",
    # Components
    "cover_page",
    "section_header",
    "subsection_header",
    "add_paragraph",
    "add_bullet_list",
    "add_numbered_list",
    "add_table",
    "add_metadata_table",
    "add_callout",
    "accent_divider",
    "parse_markdown_content",
]
