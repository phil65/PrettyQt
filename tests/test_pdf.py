"""Tests for `prettyqt` package."""

from prettyqt import pdf


def test_pdfdocument(qapp):
    doc = pdf.PdfDocument(qapp)
    assert doc.get_error() == "none"
    assert doc.get_status() == "null"


def test_pdfsearchmodel(qapp):
    model = pdf.PdfSearchModel(qapp)
    assert model is not None
    assert "context_before" in pdf.pdfsearchmodel.ROLE
