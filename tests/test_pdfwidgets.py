"""Tests for `prettyqt` package."""

from prettyqt import pdfwidgets


def test_pdfview(qapp):
    widget = pdfwidgets.PdfView()
    assert widget.get_page_mode() == "single"
    assert widget.get_zoom_mode() == "custom"
