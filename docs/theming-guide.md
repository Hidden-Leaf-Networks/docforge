# Theming Guide

Every visual aspect of DocForge documents is controlled through the `Theme` class. This guide covers all configurable properties and how they affect your output.

## Creating a Theme

```python
from docforge import Theme

theme = Theme(
    name="corporate",
    brand_name="Acme Corp",
    primary="#1E40AF",
    secondary="#F59E0B",
    text_dark="#1F2937",
    footer_text="Confidential — Acme Corp",
    footer_url="acme.com",
)
```

## Theme Properties

### Identity

| Property | Default | Description |
|----------|---------|-------------|
| `name` | `"default"` | Theme identifier |
| `brand_name` | `"DocForge"` | Organization name (appears in headers, footers, cover pages) |
| `footer_text` | `"Generated with DocForge"` | Left-side footer text on standard pages; centered on cover pages |
| `footer_url` | `""` | Appended to footer text with a pipe separator when set |

### Colors

All colors accept hex strings (e.g., `"#14B8A6"`).

| Property | Default | Used For |
|----------|---------|----------|
| `primary` | `"#14B8A6"` (teal) | Section headers, table headers, accent dividers, cover page accents |
| `secondary` | `"#F97316"` (orange) | Optional secondary dividers (`use_secondary=True`) |
| `text_dark` | `"#111827"` | Body text, H1/H3 headers |
| `text_gray` | `"#374151"` | Metadata text, cover page taglines, contact info |
| `grid_color` | `"#D1D5DB"` | Table borders, footer divider lines |
| `bg_light` | `"#F3F4F6"` | Alternating table row backgrounds |

### Page Layout

| Property | Default | Description |
|----------|---------|-------------|
| `page_size` | `LETTER` | Page dimensions (any ReportLab page size) |
| `margin_left` | `0.85` | Left margin in inches |
| `margin_right` | `0.85` | Right margin in inches |
| `margin_top` | `0.85` | Top margin in inches |
| `margin_bottom` | `0.85` | Bottom margin in inches |

### Fonts

| Property | Default | Description |
|----------|---------|-------------|
| `font_body` | `"Helvetica"` | Body text, metadata, table cells |
| `font_heading` | `"Helvetica-Bold"` | Headings, table headers, bold elements |
| `font_italic` | `"Helvetica-Oblique"` | Callouts, cover page taglines |
| `font_mono` | `"Courier"` | Inline code spans |

DocForge uses ReportLab's built-in fonts by default. These are available on all systems without installing additional font files.

## Color Properties

The `Theme` class exposes ReportLab-compatible `Color` objects as properties:

| Property | Source Field |
|----------|-------------|
| `primary_color` | `primary` |
| `secondary_color` | `secondary` |
| `text_dark_color` | `text_dark` |
| `text_gray_color` | `text_gray` |
| `grid` | `grid_color` |
| `bg` | `bg_light` |

These are used internally by components and table styles, but you can reference them when building custom layouts.

## Margin Properties

Margins are stored in inches but also available as point values for ReportLab:

| Property | Returns |
|----------|---------|
| `ml` | `margin_left * inch` |
| `mr` | `margin_right * inch` |
| `mt` | `margin_top * inch` |
| `mb` | `margin_bottom * inch` |

## Built-in Style Builders

### `build_styles(theme)`

Returns a dictionary of `ParagraphStyle` objects for standard documents:

| Key | Used For |
|-----|----------|
| `Body` | Body paragraphs (10.5pt, justified) |
| `H1` | Top-level heading (22pt, bold) |
| `H2` | Section headers (14pt, primary color) |
| `H3` | Subsection headers (12pt, bold) |
| `Meta` | Metadata lines (10pt, gray, centered) |
| `CoverTitle` | Cover page title (28pt, bold, centered) |
| `CoverTagline` | Cover page tagline (12pt, italic, centered) |
| `DocType` | Document type label (11pt, primary color, centered) |
| `Bullet` | Bullet list items (indented body style) |
| `Callout` | Callout/quote blocks (italic, indented, bordered) |

### `build_resume_styles(theme)`

Returns tighter styles optimized for one-page resumes:

| Key | Used For |
|-----|----------|
| `H1` | Name (24pt, centered) |
| `H2` | Section headers (10.5pt, primary color) |
| `H3` | Job titles (9.5pt, bold) |
| `Subtitle` | Role tagline (10pt, primary color, centered) |
| `Contact` | Contact info (9pt, gray, centered) |
| `Meta` | Employer/date lines (8.5pt, gray) |
| `Body` | Body text (9pt, justified) |
| `Bullet` | Tight bullet points (indented) |

## Table Styles

Two table style presets are available:

### `table_style(theme)`

Professional table with a themed header row and alternating row backgrounds.

### `simple_table_style(theme)`

Clean table with a themed header row but no alternating backgrounds.

Both are used internally by `add_table()` and the markdown parser, but can be applied directly when building custom table layouts.

## Example: Brand Preset

```python
# Nonprofit — purple and gold
nonprofit_theme = Theme(
    name="nonprofit",
    brand_name="Community Food Project",
    primary="#4A2070",
    secondary="#D4A745",
    text_dark="#1A1A1A",
    text_gray="#5C5C5C",
    footer_text="Community Food Project — Serving Since 2012",
    footer_url="communityfoodproject.org",
)
```

## What's Next

- [Quick Start Guide](quick-start.md) — Generate your first document
- [API Reference](api-reference.md) — Complete class and method documentation
- [Markdown Support](markdown-support.md) — Supported markdown syntax reference
