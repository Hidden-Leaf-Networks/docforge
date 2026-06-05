"""Invoice generation for HLN agency clients.

Produces branded PDF invoices matching the established HLN document style.
Uses DocForge theming and components for consistent output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from docforge.pdf.components import accent_divider
from docforge.pdf.document import SimpleForgeDocument
from docforge.theme import Theme, build_styles


@dataclass
class InvoiceLineItem:
    """A single line item on an invoice."""
    description: str
    amount: float
    quantity: int = 1
    included: bool = False  # If True, shows "Included" instead of amount


@dataclass
class InvoiceData:
    """All data needed to generate an invoice."""
    # Invoice metadata
    invoice_number: str
    issue_date: str
    due_date: str = "Upon Receipt"
    project: str = ""

    # Client
    client_name: str = ""
    business_name: str = ""
    client_location: str = ""

    # Line items
    items: list[InvoiceLineItem] = field(default_factory=list)

    # Notes (bullet points)
    notes: list[str] = field(default_factory=list)

    # Payment methods
    payment_methods: list[str] = field(default_factory=lambda: [
        "Cash App, PayPal, bank transfer, or approved digital payment method."
    ])

    # Remittance notes
    remittance_notes: list[str] = field(default_factory=list)

    @property
    def subtotal(self) -> float:
        return sum(
            item.amount * item.quantity
            for item in self.items
            if not item.included
        )

    @property
    def total(self) -> float:
        return self.subtotal


def generate_invoice(
    filepath: str,
    data: InvoiceData,
    theme: Theme | None = None,
) -> str:
    """Generate a branded HLN invoice PDF.

    Args:
        filepath: Output path for the PDF.
        data: InvoiceData with all invoice details.
        theme: Optional theme override.

    Returns:
        The filepath written to.
    """
    t = theme or Theme(
        name="hln",
        brand_name="Hidden Leaf Networks, LLC",
        footer_text="\u00a9 2026 Hidden Leaf Networks LLC",
        primary="#14B8A6",
    )
    styles = build_styles(t)
    doc = SimpleForgeDocument(filepath, theme=t)
    story: list = []

    # ── Title ──
    title_style = styles["CoverTitle"].clone("InvoiceTitle")
    title_style.fontSize = 26
    title_style.leading = 32
    title_style.textColor = t.primary_color

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 0.15 * inch))

    # ── From ──
    from_style = styles["Body"].clone("InvoiceFrom")
    from_style.alignment = 1  # CENTER
    from_style.fontSize = 10
    from_style.spaceAfter = 2

    story.append(Paragraph(t.brand_name, from_style))
    story.append(Spacer(1, 0.25 * inch))

    # ── Bill To ──
    h2_style = styles["H2"]
    story.append(Paragraph("Bill To:", h2_style))

    bill_to_style = styles["Body"].clone("BillTo")
    bill_to_style.spaceAfter = 2

    story.append(Paragraph(f"<b>{data.client_name}</b>", bill_to_style))
    if data.business_name:
        story.append(Paragraph(data.business_name, bill_to_style))
    if data.client_location:
        story.append(Paragraph(data.client_location, bill_to_style))
    story.append(Spacer(1, 0.2 * inch))

    # ── Metadata table ──
    meta_data = [
        ["Field", "Value"],
        ["Invoice #", data.invoice_number],
        ["Issue Date", data.issue_date],
        ["Due Date", data.due_date],
    ]
    if data.project:
        meta_data.append(["Project", data.project])

    meta_table = Table(meta_data, colWidths=[1.8 * inch, 4.5 * inch])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), t.primary_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), t.font_heading),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("FONTNAME", (0, 1), (-1, -1), t.font_body),
        ("GRID", (0, 0), (-1, -1), 0.5, t.grid),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.3 * inch))

    # ── Invoice Summary ──
    if data.project:
        story.append(Paragraph("Invoice Summary", h2_style))
        summary_style = styles["Body"].clone("Summary")
        summary_style.fontSize = 10
        story.append(Paragraph(
            f"Website upgrade and related services for {data.project}.",
            summary_style,
        ))
        story.append(Spacer(1, 0.15 * inch))

    # ── Itemized Charges ──
    story.append(Paragraph("Itemized Charges", h2_style))

    charges_header = ["Item", "Description", "Qty", "Amount"]
    charges_rows = [charges_header]

    for i, item in enumerate(data.items, 1):
        amount_str = "Included" if item.included else f"${item.amount:,.2f}"
        charges_rows.append([
            f"{i:02d}",
            item.description,
            str(item.quantity),
            amount_str,
        ])

    # Wrap long descriptions in Paragraph for proper text wrapping
    cell_style = styles["Body"].clone("TableCell")
    cell_style.fontSize = 9.5
    cell_style.spaceAfter = 0
    cell_style.alignment = 0  # TA_LEFT

    wrapped_rows = [charges_header]
    for i, item in enumerate(data.items, 1):
        amount_str = "Included" if item.included else f"${item.amount:,.2f}"
        wrapped_rows.append([
            f"{i:02d}",
            Paragraph(item.description, cell_style),
            str(item.quantity),
            amount_str,
        ])

    charges_table = Table(
        wrapped_rows,
        colWidths=[0.5 * inch, 3.6 * inch, 0.5 * inch, 1.2 * inch],
    )
    charges_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), t.primary_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), t.font_heading),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("FONTNAME", (0, 1), (-1, -1), t.font_body),
        ("GRID", (0, 0), (-1, -1), 0.5, t.grid),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("ALIGN", (3, 0), (3, -1), "RIGHT"),
    ]))
    story.append(charges_table)
    story.append(Spacer(1, 0.25 * inch))

    # ── Notes + Totals side by side ──
    if data.notes:
        notes_style = styles["Body"].clone("Notes")
        notes_style.fontSize = 9
        notes_style.spaceAfter = 3

        story.append(Paragraph("<b>Notes</b>", styles["H3"]))
        for note in data.notes:
            story.append(Paragraph(f"\u2022 {note}", notes_style))
        story.append(Spacer(1, 0.1 * inch))

    # ── Totals ──
    totals_data = [
        ["Subtotal", f"${data.subtotal:,.2f}"],
        ["Tax", "$0.00"],
        ["Total Due", f"${data.total:,.2f}"],
    ]
    totals_table = Table(totals_data, colWidths=[1.5 * inch, 1.5 * inch])
    totals_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), t.font_body),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (0, -1), "RIGHT"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        # Total Due row — bold and colored
        ("FONTNAME", (0, -1), (-1, -1), t.font_heading),
        ("FONTSIZE", (0, -1), (-1, -1), 14),
        ("TEXTCOLOR", (0, -1), (-1, -1), t.primary_color),
        ("LINEABOVE", (0, -1), (-1, -1), 1, t.grid),
        ("TOPPADDING", (0, -1), (-1, -1), 8),
    ]))

    # Right-align the totals table
    wrapper = Table(
        [[totals_table]],
        colWidths=[6.3 * inch],
        hAlign="RIGHT",
    )
    wrapper.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "RIGHT"),
    ]))
    story.append(wrapper)
    story.append(Spacer(1, 0.3 * inch))

    # ── Payment Terms ──
    story.append(accent_divider(t, thickness=1, space_before=8, space_after=12))
    story.append(Paragraph("Payment Terms", h2_style))

    terms_data = [
        ["Accepted Payment Methods", "Remittance Note"],
    ]
    methods_text = "<br/>".join(f"\u2022 {m}" for m in data.payment_methods)
    remittance_text = "<br/>".join(
        f"\u2022 {r}" for r in (
            data.remittance_notes or [
                f"Please reference invoice {data.invoice_number} with payment.",
                "Project work begins after invoice payment is received.",
            ]
        )
    )
    terms_data.append([methods_text, remittance_text])

    cell_style = styles["Body"].clone("TermsCell")
    cell_style.fontSize = 9
    cell_style.spaceAfter = 2

    terms_formatted = [
        terms_data[0],
        [
            Paragraph(methods_text, cell_style),
            Paragraph(remittance_text, cell_style),
        ],
    ]

    terms_table = Table(terms_formatted, colWidths=[3.15 * inch, 3.15 * inch])
    terms_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), t.primary_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), t.font_heading),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 1), (-1, -1), t.font_body),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, t.grid),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(terms_table)
    story.append(Spacer(1, 0.3 * inch))

    # ── Closing ──
    closing_style = styles["CoverTagline"].clone("Closing")
    closing_style.fontSize = 10
    closing_style.textColor = t.text_gray_color
    story.append(Paragraph(
        f"<i>Thank you for choosing {t.brand_name}.</i>",
        closing_style,
    ))

    doc.build(story)
    return filepath
