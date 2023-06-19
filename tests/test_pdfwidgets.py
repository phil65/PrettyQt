"""Tests for `prettyqt` package."""

import sys
import pytest

from prettyqt import pdfwidgets
import prettyqt

@pytest.mark.skipif(
    sys.platform == "linux" and prettyqt.qt.API.startswith("pyside"),
    reason="Segmentation fault",
)
def test_pdfview(qapp):
    widget = pdfwidgets.PdfView()
    assert widget.get_page_mode() == "single"
    assert widget.get_zoom_mode() == "custom"
