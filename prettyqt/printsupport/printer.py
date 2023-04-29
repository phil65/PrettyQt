from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtPrintSupport
from prettyqt.utils import InvalidParamError, bidict


COLOR_MODE = bidict(
    color=QtPrintSupport.QPrinter.ColorMode.Color,
    gray_scale=QtPrintSupport.QPrinter.ColorMode.GrayScale,
)

ColorModeStr = Literal["color", "gray_scale"]

DUPLEX_MODE = bidict(
    none=QtPrintSupport.QPrinter.DuplexMode.DuplexNone,
    auto=QtPrintSupport.QPrinter.DuplexMode.DuplexAuto,
    long_side=QtPrintSupport.QPrinter.DuplexMode.DuplexLongSide,
    short_side=QtPrintSupport.QPrinter.DuplexMode.DuplexShortSide,
)

DuplexModeStr = Literal["none", "auto", "long_side", "short_side"]


class Printer(gui.PagedPaintDeviceMixin, QtPrintSupport.QPrinter):
    # def get_source(self) -> pathlib.Path:
    #     return pathlib.Path(self.source().toLocalFile())

    def get_duplex(self) -> DuplexModeStr:
        return DUPLEX_MODE.inverse[self.duplex()]

    def get_pdf_version(self) -> gui.pagedpaintdevice.PdfVersionStr:
        return gui.pagedpaintdevice.PDF_VERSION.inverse[self.pdfVersion()]

    def set_pdf_version(self, version: gui.pagedpaintdevice.PdfVersionStr):
        """Set pdf version.

        Args:
            version: pdf version

        Raises:
            InvalidParamError: pdf version does not exist
        """
        if version not in gui.pagedpaintdevice.PDF_VERSION:
            raise InvalidParamError(version, gui.pagedpaintdevice.PDF_VERSION)
        self.setPdfVersion(gui.pagedpaintdevice.PDF_VERSION[version])
