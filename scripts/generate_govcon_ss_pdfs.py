#!/usr/bin/env python3
"""
Render all Sources Sought / AOI response drafts to branded PDFs.

Usage:
    cd /mnt/fast-data/Projects/hidden-leaf/docforge
    python scripts/generate_govcon_ss_pdfs.py
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from docforge import DocumentGenerator, Theme

# HLN Federal theme — professional, restrained
HLN_FEDERAL_THEME = Theme(
    name="hln-federal",
    brand_name="Hidden Leaf Networks, LLC",
    footer_text="Hidden Leaf Networks LLC — Detroit, Michigan — hiddenleafnetworks.com",
    footer_url="hiddenleafnetworks.com",
    primary="#14B8A6",      # HLN teal
    secondary="#F97316",    # Orange accent
    text_dark="#111827",
    text_gray="#374151",
)

# Source and output directories
DRAFTS_DIR = Path("/mnt/fast-data/Projects/hidden-leaf/aria-api/docs/sources_sought_drafts")
OUTPUT_DIR = Path(os.path.join(os.path.dirname(__file__), "..", "output", "govcon"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

gen = DocumentGenerator(theme=HLN_FEDERAL_THEME)

# Process all markdown drafts
drafts = sorted(DRAFTS_DIR.glob("*.md"))
print(f"Found {len(drafts)} drafts to render\n")

success = 0
failed = 0

for draft in drafts:
    md_content = draft.read_text()

    # Extract title from first few lines
    title = "Sources Sought Response"
    for line in md_content.split("\n"):
        if line.startswith("**Subject:**"):
            title = line.replace("**Subject:**", "").strip()
            break
        if line.startswith("**Title:**"):
            title = line.replace("**Title:**", "").strip()
            break

    pdf_name = draft.stem + ".pdf"
    pdf_path = OUTPUT_DIR / pdf_name

    try:
        gen.create_pdf(
            filepath=str(pdf_path),
            title=title,
            content=md_content,
            metadata={
                "document_type": "proposal",
                "author": "Carl E. Jones III",
                "company": "Hidden Leaf Networks, LLC",
                "location": "Detroit, MI",
            },
        )
        size_kb = pdf_path.stat().st_size / 1024
        print(f"  ✓ {pdf_name} ({size_kb:.0f} KB)")
        success += 1
    except Exception as e:
        print(f"  ✗ {pdf_name}: {e}")
        failed += 1

print(f"\nDone: {success} rendered, {failed} failed")
print(f"Output: {OUTPUT_DIR}")
