"""Tests for `prettyqt` package."""

from prettyqt import pdf


def test_pdfdocument(qapp):
    doc = pdf.PdfDocument(qapp)
    assert doc.get_error() == "none"
    assert doc.get_status() == "null"
