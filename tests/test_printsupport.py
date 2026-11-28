"""Tests for `prettyqt` package."""

import pytest

from prettyqt import printsupport
from prettyqt.utils import InvalidParamError


def test_printer(qapp):
    printer = printsupport.Printer()
    assert printer.get_duplex() == "none"
    printer.set_pdf_version("v1_6")
    assert printer.get_pdf_version() == "v1_6"
    with pytest.raises(InvalidParamError):
        printer.set_pdf_version("test")
    assert (
        printsupport.printer.PAGE_ORDER["first_page_first"]
        == printsupport.QPrinter.PageOrder.FirstPageFirst
    )
    assert "collate_copies" in printsupport.printengine.PRINT_ENGINE_PROPERTY_KEY


def test_printdialog(qapp):
    dlg = printsupport.PrintDialog()
    assert dlg is not None


def test_pagesetupdialog(qapp):
    dlg = printsupport.PageSetupDialog()
    assert dlg is not None


def test_printpreviewdialog(qapp):
    dlg = printsupport.PrintPreviewDialog()
    assert dlg is not None


def test_printpreviewwidget(qapp):
    widget = printsupport.PrintPreviewWidget()
    widget.set_view_mode("facing_pages")
    assert widget.get_view_mode() == "facing_pages"
    widget.set_zoom_mode("fit_to_width")
    assert widget.get_zoom_mode() == "fit_to_width"
