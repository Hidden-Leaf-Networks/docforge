# Markdown Support

DocForge parses a subset of Markdown and converts it to styled PDF elements using ReportLab. This document covers every supported syntax element.

## Headings

```markdown
# Heading 1
## Heading 2
### Heading 3
```

| Syntax | PDF Behavior |
|--------|-------------|
| `# H1` | Section header with page break (standard docs) |
| `## H2` | Section header with themed accent divider |
| `### H3` | Subsection header with spacing |

In resume mode (`parse_resume_content`), `## H2` headers do not trigger page breaks and use tighter spacing.

## Inline Formatting

```markdown
This is **bold** text.
This is *italic* text.
This is `inline code`.
```

| Syntax | Renders As |
|--------|-----------|
| `**text**` | **Bold** (`<b>` tag) |
| `*text*` | *Italic* (`<i>` tag) |
| `` `text` `` | Monospace (Courier font) |

## Lists

### Bullet Lists

```markdown
- First item
- Second item
- Third item
```

Also supports `*` as a bullet marker:

```markdown
* First item
* Second item
```

### Numbered Lists

```markdown
1. First step
2. Second step
3. Third step
```

Both `1.` and `1)` formats are recognized.

## Tables

```markdown
| Name | Role | Location |
|------|------|----------|
| Jane | Lead | Detroit |
| Alex | Dev  | Remote   |
```

Tables require:

- Rows that start and end with `|`
- A separator row (`|---|---|`) between the header and body rows (this row is filtered out of the output)

Tables are rendered with the simple table style: themed header row, clean grid, no alternating row backgrounds.

## Horizontal Rules

```markdown
---
***
___
```

Any of these three syntaxes produce a themed accent divider. In standard documents, the divider uses `primary` color with moderate spacing. In resume mode, it uses tighter spacing.

## Bold Standalone Lines

```markdown
**Key Competencies:**
```

A line that is entirely bold (with or without a trailing colon) is detected as a subsection header and rendered with `H3` styling.

## All-Caps Lines

```markdown
PROFESSIONAL EXPERIENCE
```

A line that is entirely uppercase (under 60 characters, no colons) is treated as a section header.

## Paragraphs

Any text that doesn't match the patterns above is collected into body paragraphs. Consecutive non-empty lines are joined with spaces. Blank lines separate paragraphs.

```markdown
This is the first paragraph. It continues
on the next line.

This is a second paragraph.
```

## Resume Mode

The `parse_resume_content` function applies special rules for tight one-page layouts:

- `## H2` headers have no page break and minimal divider spacing
- `### H3` headers are treated as job titles
- The first non-bullet paragraph after a `### H3` is rendered as metadata (employer/date line) using the `Meta` style
- Dividers use thinner lines and less whitespace

## Known Limitations

- No nested lists (indented sub-items are treated as body text)
- No images or embedded media
- No links (URLs appear as plain text)
- No blockquotes (use `add_callout()` from the component API for quote blocks)
- No fenced code blocks (triple backticks are not rendered as code blocks)
- Tables do not support column alignment (`:---`, `:---:`, `---:`)

## What's Next

- [Quick Start Guide](quick-start.md) — Generate your first document
- [API Reference](api-reference.md) — Complete method and class reference
- [Theming Guide](theming-guide.md) — Customize how markdown elements are styled
