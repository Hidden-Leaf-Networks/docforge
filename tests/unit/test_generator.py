"""Tests for the high-level DocumentGenerator."""

import os
import tempfile

from docforge.generator import DOC_TYPE_LABELS, DocumentGenerator
from docforge.theme import Theme


class TestDocumentGenerator:
    def test_init_default_theme(self):
        gen = DocumentGenerator()
        assert gen.theme.name == "default"

    def test_init_custom_theme(self):
        t = Theme(name="custom", brand_name="Acme")
        gen = DocumentGenerator(theme=t)
        assert gen.theme.brand_name == "Acme"

    def test_create_pdf_from_string(self):
        gen = DocumentGenerator()
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            result = gen.create_pdf(path, "Test Doc", "# Hello\n\nWorld")
            assert result == path
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_create_pdf_from_sections(self):
        gen = DocumentGenerator()
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            content = {"sections": {"intro": "Introduction text", "body": "Body text"}}
            result = gen.create_pdf(path, "Sections Test", content)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            os.unlink(path)

    def test_create_pdf_from_generated_content(self):
        gen = DocumentGenerator()
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            content = {"generated_content": "## AI Output\n\nGenerated text here."}
            result = gen.create_pdf(path, "AI Doc", content)
            assert os.path.exists(result)
        finally:
            os.unlink(path)

    def test_create_pdf_with_metadata(self):
        gen = DocumentGenerator()
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            meta = {
                "author": "Jane Doe",
                "organization": "Acme Corp",
                "document_type": "business_plan",
                "location": "San Francisco, CA",
            }
            result = gen.create_pdf(path, "Business Plan", "Content", metadata=meta)
            assert os.path.exists(result)
        finally:
            os.unlink(path)

    def test_create_simple_pdf(self):
        gen = DocumentGenerator()
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            result = gen.create_simple_pdf(path, "Simple", "Just some text.")
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            os.unlink(path)

    def test_custom_theme_pdf(self):
        t = Theme(name="red", primary="#FF0000", brand_name="Red Corp")
        gen = DocumentGenerator(theme=t)
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            result = gen.create_pdf(path, "Red Doc", "Content")
            assert os.path.exists(result)
        finally:
            os.unlink(path)


class TestDocTypeLabels:
    def test_known_types(self):
        assert "BUSINESS PLAN" in DOC_TYPE_LABELS.values()
        assert "REPORT" in DOC_TYPE_LABELS.values()
        assert "WHITEPAPER" in DOC_TYPE_LABELS.values()
