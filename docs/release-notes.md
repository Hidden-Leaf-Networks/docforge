# Release Notes

## v0.1.0 — Initial Release

**Released:** April 2026

### Highlights

DocForge v0.1.0 is the first public release of the document generation toolkit built by Hidden Leaf Networks.

### Features

- **DocumentGenerator API** — High-level interface for creating PDFs, Word documents, and resumes from markdown content and metadata
- **Configurable themes** — Full control over colors, fonts, margins, branding, and page layout through the `Theme` dataclass
- **Professional PDF generation** — Cover pages, section headers, subsection headers, themed accent dividers, and automatic page numbering
- **Markdown parser** — Converts headings, bold, italic, inline code, bullet lists, numbered lists, tables, and horizontal rules into styled PDF elements
- **Resume PDF mode** — Tight one-page layout with specialized styles for name, subtitle, contact info, job titles, employer/date metadata, and compact bullet points
- **Invoice generation** — Branded invoices with bill-to section, metadata table, itemized charges with quantities, automatic subtotal/total calculation, notes, and payment terms
- **Word document generation** — Structured `.docx` output with headers, footers, metadata tables, and markdown content parsing
- **Chat export** — Multi-format conversation export (TXT, PDF, CSV, XLSX) with styled output and metadata
- **Component library** — Reusable flowables for cover pages, sections, paragraphs, bullet lists, numbered lists, tables, metadata tables, callouts, and dividers
- **Table styles** — Two presets: `standard` (alternating row backgrounds) and `simple` (clean grid)
- **Footer system** — Standard pages with page numbers, cover pages with centered branding

### Known Limitations

- No nested list support
- No image embedding in markdown
- No link rendering (URLs appear as plain text)
- No fenced code blocks
- Table column alignment markers (`:---`) are not supported

### Dependencies

- **Required:** `reportlab`
- **Optional:** `python-docx` (Word), `openpyxl` (Excel)
