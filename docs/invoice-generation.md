# Invoice Generation Tutorial

This guide walks through creating branded PDF invoices with DocForge, from a basic invoice to customized payment terms and theming.

## Overview

DocForge invoices include:

- Branded header with your organization name
- Bill-to section with client details
- Metadata table (invoice number, dates, project)
- Itemized charges with quantities and amounts
- Automatic subtotal and total calculation
- Notes section
- Payment terms table
- Themed footer

## Basic Invoice

```python
from docforge.invoice import InvoiceData, InvoiceLineItem, generate_invoice
from docforge.theme import Theme

theme = Theme(
    brand_name="Acme Consulting, LLC",
    primary="#14B8A6",
    footer_text="© 2026 Acme Consulting LLC",
)

invoice = InvoiceData(
    invoice_number="ACM-INV-2026-001",
    issue_date="July 1, 2026",
    due_date="July 15, 2026",
    project="Website Redesign",
    client_name="John Smith",
    business_name="Smith & Associates",
    client_location="Detroit, Michigan",
    items=[
        InvoiceLineItem(description="Website design and development", amount=2500.00),
        InvoiceLineItem(description="Domain registration (1 year)", amount=15.00),
        InvoiceLineItem(description="Hosting setup", amount=0, included=True),
    ],
)

generate_invoice("invoice.pdf", invoice, theme=theme)
```

## InvoiceData Fields

| Field | Type | Description |
|-------|------|-------------|
| `invoice_number` | `str` | Unique invoice identifier |
| `issue_date` | `str` | Date the invoice was issued |
| `due_date` | `str` | Payment deadline (default: "Upon Receipt") |
| `project` | `str` | Project name (appears in metadata and summary) |
| `client_name` | `str` | Client's full name |
| `business_name` | `str` | Client's business name (optional) |
| `client_location` | `str` | Client's location (optional) |
| `items` | `list[InvoiceLineItem]` | Line items (see below) |
| `notes` | `list[str]` | Bullet-point notes section |
| `payment_methods` | `list[str]` | Accepted payment methods |
| `remittance_notes` | `list[str]` | Instructions for payment |

## InvoiceLineItem Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | `str` | What the charge is for |
| `amount` | `float` | Dollar amount |
| `quantity` | `int` | Number of units (default: 1) |
| `included` | `bool` | If `True`, displays "Included" instead of a dollar amount |

Items marked `included=True` are excluded from the subtotal calculation. This is useful for services bundled at no extra cost.

## Computed Properties

`InvoiceData` provides two computed properties:

- **`subtotal`** — Sum of all non-included line items (`amount * quantity`)
- **`total`** — Currently equals subtotal (tax support can be added)

## Adding Notes

Notes appear as bullet points between the charges table and the totals:

```python
invoice = InvoiceData(
    # ... other fields ...
    notes=[
        "Covers July 2026 services.",
        "Next invoice will be issued August 1, 2026.",
    ],
)
```

## Customizing Payment Terms

Override the default payment methods and remittance instructions:

```python
invoice = InvoiceData(
    # ... other fields ...
    payment_methods=[
        "Bank transfer (ACH)",
        "PayPal: billing@acme.com",
        "Check payable to Acme Consulting, LLC",
    ],
    remittance_notes=[
        "Please reference ACM-INV-2026-001 with payment.",
        "Late payments subject to 1.5% monthly fee.",
    ],
)
```

If `remittance_notes` is not provided, DocForge generates default instructions using the invoice number.

## Theming Your Invoice

The invoice inherits all visual properties from the `Theme` you pass in:

```python
theme = Theme(
    brand_name="My Agency",
    primary="#4A2070",       # Purple headers and accents
    secondary="#D4A745",     # Gold (available for dividers)
    text_dark="#1A1A1A",
    grid_color="#D1D5DB",
    footer_text="© 2026 My Agency",
)

generate_invoice("invoice.pdf", invoice, theme=theme)
```

The theme controls:

- Header/accent colors on tables
- Body and metadata text colors
- Grid/border line colors
- Footer text
- Font families

## What's Next

- [Theming Guide](theming-guide.md) — Deep dive into theme configuration
- [API Reference](api-reference.md) — Full `InvoiceData` and `generate_invoice` reference
