"""PDF document generation."""

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

__all__ = [
    "ForgeDocument",
    "SimpleForgeDocument",
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
