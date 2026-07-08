# Case Study: Building DocForge

How a document generation toolkit was designed, documented, and deployed to support a growing web development agency.

---

## Problem

Hidden Leaf Networks needed to produce professional branded documents — invoices, grant applications, outreach proposals, resumes, and client reports — at a pace that matched its growing client pipeline. Manual document creation in Google Docs or Canva was time-consuming, inconsistent, and didn't integrate with existing automation workflows.

The requirements:

- Generate documents programmatically from Python scripts and AI agents
- Consistent branding across all output (colors, fonts, logos, footer text)
- Support multiple document types: reports, proposals, invoices, resumes, chat exports
- Accept markdown content so documents could be generated from LLM output
- Themeable per client or brand (agency clients each have distinct brand guidelines)

## Audience

- **Primary:** The founding engineer, using DocForge as part of automated agent workflows (proposal generation, invoice creation, outreach document assembly)
- **Secondary:** Future contributors or agency team members who need to generate documents without touching ReportLab directly

## Documentation Goals

1. Enable a new user to generate their first PDF within 5 minutes
2. Provide a complete API reference covering every public class and function
3. Document the theming system so any brand preset can be created without reading source code
4. Cover supported markdown syntax so content authors know what renders and what doesn't
5. Address common errors before they become support requests

## Information Architecture

```
docs/
  quick-start.md          → Onboarding (first 5 minutes)
  invoice-generation.md   → Procedural tutorial (step-by-step)
  theming-guide.md        → Conceptual guide (how themes work)
  markdown-support.md     → Reference (supported syntax)
  api-reference.md        → Reference (classes, methods, parameters)
  troubleshooting.md      → Problem-solution pairs
  release-notes.md        → Version history
  case-study.md           → Portfolio context (this document)
```

This follows the Diataxis framework:

- **Tutorials:** Quick Start, Invoice Generation
- **How-to guides:** Theming Guide
- **Reference:** API Reference, Markdown Support
- **Explanation:** Case Study

## Documents Created

| Document | Type | Purpose |
|----------|------|---------|
| Quick Start Guide | Tutorial | Zero-to-first-PDF onboarding |
| Invoice Generation | Tutorial | Step-by-step invoice creation |
| Theming Guide | How-to | Configure brand presets |
| Markdown Support | Reference | Supported syntax and limitations |
| API Reference | Reference | All classes, methods, parameters |
| Troubleshooting | Reference | Common errors and fixes |
| Release Notes | Reference | Version history and changelog |

## Tools Used

- **Python** — Core language
- **ReportLab** — PDF generation engine
- **python-docx** — Word document generation
- **openpyxl** — Excel export
- **Markdown** — Documentation format
- **Git/GitHub** — Version control and public portfolio hosting

## Outcome

DocForge reduced document creation time from 30-60 minutes per document (manual layout) to under 5 seconds (scripted generation). It currently powers:

- Agency client invoices (monthly billing for web development care plans)
- Grant application packets (Walmart Spark Good, Forgotten Harvest, Meijer)
- Corporate outreach proposals (branded one-pagers with themed headers)
- Resume generation (one-page PDFs with tight spacing for job applications)
- Chat/conversation exports (multi-format output from AI agent sessions)

The documentation set serves as both internal reference and a public technical writing portfolio demonstrating documentation structure, API documentation, procedural writing, and troubleshooting guides.

## Future Improvements

- Add image embedding support for logos and screenshots
- Support custom font loading beyond ReportLab built-ins
- Add a CLI interface (`docforge generate report.md --theme corporate`)
- Template system for reusable document structures
- HTML export format
