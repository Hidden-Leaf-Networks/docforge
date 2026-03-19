"""Tests for theme configuration and style building."""

from reportlab.lib import colors

from docforge.theme import (
    DEFAULT_THEME,
    Theme,
    build_styles,
    draw_cover_footer,
    draw_footer,
    simple_table_style,
    table_style,
)


class TestTheme:
    def test_default_theme_exists(self):
        assert DEFAULT_THEME.name == "default"
        assert DEFAULT_THEME.brand_name == "DocForge"

    def test_custom_theme(self):
        t = Theme(name="acme", brand_name="Acme Corp", primary="#FF0000")
        assert t.name == "acme"
        assert t.brand_name == "Acme Corp"
        assert t.primary_color == colors.HexColor("#FF0000")

    def test_color_properties(self):
        t = Theme(primary="#123456", secondary="#654321")
        assert t.primary_color == colors.HexColor("#123456")
        assert t.secondary_color == colors.HexColor("#654321")

    def test_margin_properties(self):
        t = Theme(margin_left=1.0, margin_right=1.0)
        from reportlab.lib.units import inch
        assert t.ml == 1.0 * inch
        assert t.mr == 1.0 * inch

    def test_full_footer_with_url(self):
        t = Theme(footer_text="Made by Acme", footer_url="acme.com")
        assert t.full_footer() == "Made by Acme | acme.com"

    def test_full_footer_without_url(self):
        t = Theme(footer_text="Made by Acme", footer_url="")
        assert t.full_footer() == "Made by Acme"


class TestBuildStyles:
    def test_returns_all_required_styles(self):
        styles = build_styles()
        required = ["Body", "H1", "H2", "H3", "Meta", "CoverTitle",
                     "CoverTagline", "DocType", "Bullet", "Callout"]
        for name in required:
            assert name in styles, f"Missing style: {name}"

    def test_custom_theme_colors_applied(self):
        t = Theme(primary="#FF0000")
        styles = build_styles(t)
        assert styles["H2"].textColor == colors.HexColor("#FF0000")
        assert styles["DocType"].textColor == colors.HexColor("#FF0000")

    def test_custom_fonts_applied(self):
        t = Theme(font_body="Times-Roman", font_heading="Times-Bold")
        styles = build_styles(t)
        assert styles["Body"].fontName == "Times-Roman"
        assert styles["H1"].fontName == "Times-Bold"


class TestTableStyles:
    def test_table_style_returns_list(self):
        ts = table_style()
        assert isinstance(ts, list)
        assert len(ts) > 0

    def test_simple_table_style_returns_list(self):
        ts = simple_table_style()
        assert isinstance(ts, list)

    def test_custom_theme_table(self):
        t = Theme(primary="#FF0000")
        ts = table_style(t)
        # First entry is header background
        assert ts[0][3] == colors.HexColor("#FF0000")
