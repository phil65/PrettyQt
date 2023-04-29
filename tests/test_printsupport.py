"""Tests for `prettyqt` package."""

import pytest

from prettyqt import printsupport
from prettyqt.utils import InvalidParamError


def test_printer():
    printer = printsupport.Printer()
    assert printer.get_duplex() == "none"
    printer.set_pdf_version("v1_6")
    assert printer.get_pdf_version() == "v1_6"
    with pytest.raises(InvalidParamError):
        printer.set_pdf_version("test")
