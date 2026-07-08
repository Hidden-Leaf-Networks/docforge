# Troubleshooting

Common issues and their solutions when working with DocForge.

---

## Installation Issues

### `ModuleNotFoundError: No module named 'reportlab'`

ReportLab is a core dependency and should install automatically with DocForge. If it didn't:

```bash
pip install reportlab
```

### `ModuleNotFoundError: No module named 'docx'`

Word document generation requires the optional `word` extra:

```bash
pip install docforge[word]
```

### `ModuleNotFoundError: No module named 'openpyxl'`

Excel export requires the optional `excel` extra:

```bash
pip install docforge[all]
```

---

## PDF Generation

### Cover page is blank or missing content

Check that you're passing `metadata` with at least an `author` or `organization` key. The cover page uses these values for the "Prepared by" and "Prepared for" lines.

```python
gen.create_pdf(
    "output.pdf",
    title="My Report",
    content="## Content here",
    metadata={
        "author": "Jane Doe",
        "organization": "Acme Corp",
        "document_type": "report",
    },
)
```

### Document type label shows "DOCUMENT" instead of expected type

The `document_type` metadata value must match one of the supported types exactly:

`business_plan`, `grant_application`, `marketing_plan`, `financial_projection`, `executive_summary`, `pitch_deck`, `report`, `proposal`, `whitepaper`

Unrecognized values are uppercased and displayed as-is.

### Table columns are uneven or overflow

When using `add_table()` directly, pass explicit `col_widths` to control column sizing. The available content width is approximately `6.3 inches` with default margins.

```python
from reportlab.lib.units import inch

add_table(
    story,
    data=[["Name", "Amount"], ["Item A", "$500"]],
    col_widths=[4.0 * inch, 2.3 * inch],
    theme=theme,
)
```

### Markdown bold/italic not rendering

Ensure there are no spaces between the asterisks and the text:

```markdown
**correct bold**
** broken bold **

*correct italic*
* broken italic *
```

### Text overflows the page margins

If you're building custom layouts with direct ReportLab components, ensure your content width respects the theme margins. Use the theme's margin properties:

```python
available_width = theme.page_size[0] - theme.ml - theme.mr
```

---

## Invoice Generation

### All line items show "$0.00"

Check that `amount` is set as a float, not a string:

```python
# Correct
InvoiceLineItem(description="Service", amount=250.00)

# Wrong — amount must be numeric
InvoiceLineItem(description="Service", amount="250.00")
```

### "Included" items are counted in the total

Items with `included=True` are excluded from `subtotal` and `total` by design. If an included item still shows a dollar amount, check that `included=True` is set:

```python
InvoiceLineItem(description="Hosting setup", amount=0, included=True)
```

---

## Word Generation

### Word document has no formatting

Content passed as a plain string is parsed line by line. Use markdown headings (`#`, `##`, `###`) to create structure:

```python
gen.create_word(
    "report.docx",
    title="Report",
    content="## Section One\n\nParagraph text.\n\n## Section Two\n\nMore text.",
)
```

### Import error when generating Word documents

Ensure `python-docx` is installed:

```bash
pip install docforge[word]
```

---

## Chat Export

### XLSX export fails with ImportError

Excel export requires `openpyxl`:

```bash
pip install docforge[all]
```

### Exported PDF has no styling

Ensure you're passing an `ExportMetadata` object with a `brand_name`:

```python
metadata = ExportMetadata(title="Chat Log", brand_name="My Company")
```

---

## General Tips

- **Check your Python version.** DocForge requires Python 3.10+ for `X | Y` type syntax.
- **Use virtual environments.** Avoid dependency conflicts with `python -m venv .venv`.
- **Test with a minimal example first.** If a complex document fails, isolate the issue by generating a simple document with the same theme.
