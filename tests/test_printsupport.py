"""Tests for `prettyqt` package."""

import sys

import pytest

import prettyqt

from prettyqt import printsupport
from prettyqt.utils import InvalidParamError


pytestmark = pytest.mark.skipif(
    sys.platform == "linux" and prettyqt.qt.API.startswith("pyside"),
    reason="Segmentation fault",
)


def test_printer():
    printer = printsupport.Printer()
    assert printer.get_duplex() == "none"
    printer.set_pdf_version("v1_6")
    assert printer.get_pdf_version() == "v1_6"
    with pytest.raises(InvalidParamError):
        printer.set_pdf_version("test")


def test_printdialog():
    dlg = printsupport.PrintDialog()
    assert dlg is not None


def test_pagesetupdialog():
    dlg = printsupport.PageSetupDialog()
    assert dlg is not None


def test_printpreviewdialog():
    dlg = printsupport.PrintPreviewDialog()
    assert dlg is not None


def test_printpreviewwidget():
    widget = printsupport.PrintPreviewWidget()
    widget.set_view_mode("facing_pages")
    assert widget.get_view_mode() == "facing_pages"
    widget.set_zoom_mode("fit_to_width")
    assert widget.get_zoom_mode() == "fit_to_width"
