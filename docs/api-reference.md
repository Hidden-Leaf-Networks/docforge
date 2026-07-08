# API Reference

Complete reference for all public classes, functions, and components in DocForge.

---

## DocumentGenerator

**Module:** `docforge.generator`

The high-level API for creating documents. Wraps PDF and Word generation with theme support.

### Constructor

```python
DocumentGenerator(theme: Theme | None = None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `theme` | `Theme \| None` | `DEFAULT_THEME` | Theme for all generated documents |

### Methods

#### `create_pdf(filepath, title, content, metadata=None) -> str`

Create a professional PDF with a cover page.

| Parameter | Type | Description |
|-----------|------|-------------|
| `filepath` | `str` | Output file path |
| `title` | `str` | Document title (cover page and header) |
| `content` | `dict \| str` | Markdown string, or dict with `"sections"` or `"generated_content"` key |
| `metadata` | `dict \| None` | Keys: `author`, `organization`, `document_type`, `location`, `client` |

Returns the filepath written to.

**Supported `document_type` values:** `business_plan`, `grant_application`, `marketing_plan`, `financial_projection`, `executive_summary`, `pitch_deck`, `report`, `proposal`, `whitepaper`

#### `create_simple_pdf(filepath, title, content, metadata=None) -> str`

Create a PDF without a separate cover page. Title, metadata table, and content appear on the first page.

Same parameters as `create_pdf`.

#### `create_resume_pdf(filepath, name, subtitle, contact, content) -> str`

Create a one-page resume PDF with tight spacing.

| Parameter | Type | Description |
|-----------|------|-------------|
| `filepath` | `str` | Output file path |
| `name` | `str` | Full name (large, centered) |
| `subtitle` | `str` | Role tagline (e.g., `"QA ENGINEER \| AUTOMATION"`) |
| `contact` | `str` | Contact info line |
| `content` | `str` | Markdown body (## sections, ### job titles, bullets) |

#### `create_word(filepath, title, content, metadata=None) -> str`

Create a formatted Word document. Requires `pip install docforge[word]`.

Same parameters as `create_pdf`.

---

## Theme

**Module:** `docforge.theme`

Dataclass that defines all visual properties for document generation.

See [Theming Guide](theming-guide.md) for full property reference and examples.

```python
from docforge import Theme

theme = Theme(
    name="my-brand",
    brand_name="My Company",
    primary="#3B82F6",
    footer_text="My Company — Confidential",
)
```

---

## Invoice Generation

**Module:** `docforge.invoice`

### InvoiceLineItem

```python
@dataclass
class InvoiceLineItem:
    description: str
    amount: float
    quantity: int = 1
    included: bool = False
```

### InvoiceData

```python
@dataclass
class InvoiceData:
    invoice_number: str
    issue_date: str
    due_date: str = "Upon Receipt"
    project: str = ""
    client_name: str = ""
    business_name: str = ""
    client_location: str = ""
    items: list[InvoiceLineItem] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    payment_methods: list[str] = field(default_factory=...)
    remittance_notes: list[str] = field(default_factory=list)
```

**Computed properties:**

- `subtotal` — Sum of non-included items (`amount * quantity`)
- `total` — Currently equals subtotal

### generate_invoice

```python
generate_invoice(filepath: str, data: InvoiceData, theme: Theme | None = None) -> str
```

Generate a branded invoice PDF. Returns the filepath written to.

If no theme is provided, uses a default HLN-branded theme.

---

## PDF Components

**Module:** `docforge.pdf.components`

Low-level flowable components for building custom document layouts.

### accent_divider

```python
accent_divider(
    theme: Theme | None = None,
    use_secondary: bool = False,
    thickness: int = 2,
    space_before: int = 6,
    space_after: int = 12,
) -> HRFlowable
```

Themed horizontal divider line. Set `use_secondary=True` to use the secondary color.

### cover_page

```python
cover_page(
    story, styles, title, doc_type, date_str, author, organization,
    location="", tagline="", theme=None, client="",
) -> None
```

Build a professional cover page and append it to the story. Includes a page break and template switch to "Standard" for subsequent pages.

### section_header / subsection_header

```python
section_header(story, styles, title, new_page=True, theme=None) -> None
subsection_header(story, styles, title) -> None
```

### Content Helpers

```python
add_paragraph(story, styles, text) -> None
add_bullet_list(story, styles, items: list[str]) -> None
add_numbered_list(story, styles, items: list[str]) -> None
add_callout(story, styles, text) -> None
```

### add_table

```python
add_table(
    story, data: list[list], col_widths=None,
    style="standard", theme=None,
) -> None
```

| `style` value | Description |
|---------------|-------------|
| `"standard"` | Themed header + alternating row backgrounds |
| `"simple"` | Themed header only |

### add_metadata_table

```python
add_metadata_table(story, metadata_pairs: list[list[str]], theme=None) -> None
```

Key-value pair table with gray label column.

### Markdown Parsers

```python
parse_markdown_content(content: str, story, styles, theme=None) -> None
parse_resume_content(content: str, story, styles, theme=None) -> None
convert_markdown_inline(text: str) -> str
```

---

## PDF Documents

**Module:** `docforge.pdf.document`

### ForgeDocument

Full document with cover page and standard page templates. Uses `draw_cover_footer` on the first page and `draw_footer` on subsequent pages.

### SimpleForgeDocument

Simpler document with a single page template. All pages use `draw_footer`.

Both accept `filepath` and an optional `theme` parameter.

---

## Chat Export

**Module:** `docforge.export`

```python
from docforge.export import ChatExportService, ChatMessage, ExportMetadata

messages = [
    ChatMessage(role="user", content="Hello"),
    ChatMessage(role="assistant", content="Hi there!"),
]

metadata = ExportMetadata(title="Support Chat", brand_name="Acme Corp")

ChatExportService.export(messages, metadata, fmt="pdf", export_dir="./exports")
```

**Supported formats:** `txt`, `pdf`, `csv`, `xlsx`

---

## Style Builders

**Module:** `docforge.theme`

```python
build_styles(theme: Theme | None = None) -> dict[str, ParagraphStyle]
build_resume_styles(theme: Theme | None = None) -> dict[str, ParagraphStyle]
table_style(theme: Theme | None = None) -> list
simple_table_style(theme: Theme | None = None) -> list
```

## Footer Renderers

**Module:** `docforge.theme`

```python
draw_footer(canvas, doc, theme=None)        # Standard pages with page numbers
draw_cover_footer(canvas, doc, theme=None)   # Cover page with centered branding
```
