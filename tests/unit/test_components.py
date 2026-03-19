"""Tests for PDF components."""

from docforge.pdf.components import (
    accent_divider,
    add_bullet_list,
    add_callout,
    add_metadata_table,
    add_numbered_list,
    add_paragraph,
    add_table,
    convert_markdown_inline,
    cover_page,
    gray_divider,
    parse_markdown_content,
    section_header,
    subsection_header,
)
from docforge.theme import Theme, build_styles


class TestDividers:
    def test_accent_divider_uses_primary(self):
        d = accent_divider()
        assert d.color is not None

    def test_accent_divider_secondary(self):
        t = Theme(secondary="#FF0000")
        d = accent_divider(t, use_secondary=True)
        assert d.color is not None

    def test_gray_divider(self):
        d = gray_divider()
        assert d.color is not None


class TestCoverPage:
    def test_cover_page_adds_flowables(self):
        styles = build_styles()
        story = []
        cover_page(
            story=story,
            styles=styles,
            title="Test Document",
            doc_type="REPORT",
            date_str="March 19, 2026",
            author="Test Author",
            organization="Test Org",
        )
        assert len(story) > 0
        # Should end with PageBreak
        from reportlab.platypus import PageBreak
        assert isinstance(story[-1], PageBreak)

    def test_cover_page_with_location(self):
        styles = build_styles()
        story = []
        cover_page(
            story=story, styles=styles,
            title="T", doc_type="R", date_str="D",
            author="A", organization="O", location="Detroit, MI",
        )
        assert len(story) > 5  # More flowables with location


class TestSections:
    def test_section_header_with_page_break(self):
        styles = build_styles()
        story = []
        section_header(story, styles, "My Section", new_page=True)
        from reportlab.platypus import PageBreak
        assert any(isinstance(f, PageBreak) for f in story)

    def test_section_header_without_page_break(self):
        styles = build_styles()
        story = []
        section_header(story, styles, "My Section", new_page=False)
        from reportlab.platypus import PageBreak
        assert not any(isinstance(f, PageBreak) for f in story)

    def test_subsection_header(self):
        styles = build_styles()
        story = []
        subsection_header(story, styles, "Sub Section")
        assert len(story) == 3  # spacer + paragraph + spacer


class TestListComponents:
    def test_bullet_list(self):
        styles = build_styles()
        story = []
        add_bullet_list(story, styles, ["Item 1", "Item 2", "Item 3"])
        assert len(story) == 3

    def test_numbered_list(self):
        styles = build_styles()
        story = []
        add_numbered_list(story, styles, ["First", "Second"])
        assert len(story) == 2

    def test_paragraph(self):
        styles = build_styles()
        story = []
        add_paragraph(story, styles, "Hello world")
        assert len(story) == 1


class TestTable:
    def test_add_table(self):
        story = []
        data = [["Name", "Value"], ["A", "1"], ["B", "2"]]
        add_table(story, data)
        assert len(story) == 3  # spacer + table + spacer

    def test_add_table_simple_style(self):
        story = []
        data = [["Name", "Value"], ["A", "1"]]
        add_table(story, data, style="simple")
        assert len(story) == 3

    def test_metadata_table(self):
        story = []
        add_metadata_table(story, [["Key", "Value"], ["Author", "Test"]])
        assert len(story) == 2  # table + spacer


class TestCallout:
    def test_add_callout(self):
        styles = build_styles()
        story = []
        add_callout(story, styles, "Important note here")
        assert len(story) == 3  # spacer + paragraph + spacer


class TestMarkdownConversion:
    def test_bold(self):
        assert "<b>bold</b>" in convert_markdown_inline("**bold**")

    def test_italic(self):
        assert "<i>italic</i>" in convert_markdown_inline("*italic*")

    def test_code(self):
        result = convert_markdown_inline("`code`")
        assert "Courier" in result

    def test_horizontal_rule_stripped(self):
        assert "---" not in convert_markdown_inline("---")


class TestParseMarkdown:
    def test_headings(self):
        styles = build_styles()
        story = []
        parse_markdown_content("## Section Title\n\nSome text.", story, styles)
        assert len(story) > 0

    def test_bullet_list(self):
        styles = build_styles()
        story = []
        parse_markdown_content("- Item 1\n- Item 2\n- Item 3", story, styles)
        assert len(story) == 3

    def test_numbered_list(self):
        styles = build_styles()
        story = []
        parse_markdown_content("1. First\n2. Second", story, styles)
        assert len(story) == 2

    def test_horizontal_rule(self):
        styles = build_styles()
        story = []
        parse_markdown_content("Above\n\n---\n\nBelow", story, styles)
        # Should have: paragraph, divider, paragraph
        assert len(story) == 3

    def test_bold_header_pattern(self):
        styles = build_styles()
        story = []
        parse_markdown_content("**Executive Summary**\n\nContent here.", story, styles)
        assert len(story) > 1  # subsection header + content

    def test_empty_content(self):
        styles = build_styles()
        story = []
        parse_markdown_content("", story, styles)
        assert len(story) == 0
