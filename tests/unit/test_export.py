"""Tests for chat export service."""

import os
import tempfile
from datetime import datetime

from docforge.export.chat_export import ChatExportService, ChatMessage, ExportMetadata


def _messages():
    return [
        ChatMessage(role="user", content="Hello!", created_at=datetime(2026, 3, 19, 10, 0)),
        ChatMessage(role="assistant", content="Hi there! How can I help?", created_at=datetime(2026, 3, 19, 10, 1)),
        ChatMessage(role="user", content="What's the weather?", created_at=datetime(2026, 3, 19, 10, 2)),
    ]


def _metadata():
    return ExportMetadata(
        title="Test Chat",
        user_name="Test User",
        organization="Acme Corp",
        brand_name="DocForge",
    )


class TestChatMessage:
    def test_basic_fields(self):
        msg = ChatMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.created_at is None

    def test_optional_fields(self):
        msg = ChatMessage(role="assistant", content="Hi", tokens_used=50, model="gpt-4")
        assert msg.tokens_used == 50
        assert msg.model == "gpt-4"


class TestExportMetadata:
    def test_defaults(self):
        meta = ExportMetadata(title="Chat")
        assert meta.export_type == "chat"
        assert meta.brand_name == "DocForge"


class TestFilename:
    def test_generate_filename(self):
        meta = ExportMetadata(title="Test")
        name = ChatExportService.generate_filename(meta, "pdf")
        assert name.startswith("chat_chat_")
        assert name.endswith(".pdf")

    def test_generate_filename_with_session(self):
        meta = ExportMetadata(title="Test", session_id="42")
        name = ChatExportService.generate_filename(meta, "csv")
        assert name.startswith("session_42_")


class TestTxtExport:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export_to_txt(_messages(), _metadata(), d)
            assert os.path.exists(path)
            assert path.endswith(".txt")
            content = open(path).read()
            assert "Hello!" in content
            assert "Test User" in content


class TestPdfExport:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export_to_pdf(_messages(), _metadata(), d)
            assert os.path.exists(path)
            assert path.endswith(".pdf")
            assert os.path.getsize(path) > 0


class TestCsvExport:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export_to_csv(_messages(), _metadata(), d)
            assert os.path.exists(path)
            content = open(path).read()
            assert "Message #" in content
            assert "Hello!" in content

    def test_correct_row_count(self):
        import csv
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export_to_csv(_messages(), _metadata(), d)
            with open(path) as f:
                reader = csv.reader(f)
                rows = list(reader)
            assert len(rows) == 4  # header + 3 messages


class TestXlsxExport:
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export_to_xlsx(_messages(), _metadata(), d)
            assert os.path.exists(path)
            assert path.endswith(".xlsx")
            assert os.path.getsize(path) > 0


class TestExportDispatch:
    def test_txt_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export(_messages(), _metadata(), "txt", d)
            assert path.endswith(".txt")

    def test_pdf_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export(_messages(), _metadata(), "pdf", d)
            assert path.endswith(".pdf")

    def test_csv_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export(_messages(), _metadata(), "csv", d)
            assert path.endswith(".csv")

    def test_xlsx_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export(_messages(), _metadata(), "xlsx", d)
            assert path.endswith(".xlsx")

    def test_unsupported_format_raises(self):
        import pytest
        with tempfile.TemporaryDirectory() as d:
            with pytest.raises(ValueError, match="Unsupported format"):
                ChatExportService.export(_messages(), _metadata(), "html", d)

    def test_case_insensitive(self):
        with tempfile.TemporaryDirectory() as d:
            path = ChatExportService.export(_messages(), _metadata(), "TXT", d)
            assert path.endswith(".txt")
