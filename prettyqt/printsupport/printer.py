from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtPrintSupport
from prettyqt.utils import bidict


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

OUTPUT_FORMAT = bidict(
    native=QtPrintSupport.QPrinter.OutputFormat.NativeFormat,
    pdf=QtPrintSupport.QPrinter.OutputFormat.PdfFormat,
)

OutputFormatStr = Literal["native", "pdf"]

PAGE_ORDER = bidict(
    first_page_last=QtPrintSupport.QPrinter.PageOrder.FirstPageFirst,
    last_page_first=QtPrintSupport.QPrinter.PageOrder.LastPageFirst,
)

PageOrderStr = Literal["first_page_last", "last_page_first"]

PRINT_RANGE = bidict(
    all_pages=QtPrintSupport.QPrinter.PrintRange.AllPages,
    selection=QtPrintSupport.QPrinter.PrintRange.Selection,
    page_range=QtPrintSupport.QPrinter.PrintRange.PageRange,
    current_page=QtPrintSupport.QPrinter.PrintRange.CurrentPage,
)

PrintRangeStr = Literal["all_pages", "selection", "page_range", "current_page"]

PRINTER_MODE = bidict(
    screen_resolution=QtPrintSupport.QPrinter.PrinterMode.ScreenResolution,
    printer_resolution=QtPrintSupport.QPrinter.PrinterMode.PrinterResolution,
    high_resolution=QtPrintSupport.QPrinter.PrinterMode.HighResolution,
)

PrinterModeStr = Literal["screen_resolution", "printer_resolution", "high_resolution"]

PRINTER_STATE = bidict(
    idle=QtPrintSupport.QPrinter.PrinterState.Idle,
    active=QtPrintSupport.QPrinter.PrinterState.Active,
    aborted=QtPrintSupport.QPrinter.PrinterState.Aborted,
    error=QtPrintSupport.QPrinter.PrinterState.Error,
)

PrinterStateStr = Literal["idle", "active", "aborted", "error"]


class Printer(gui.PagedPaintDeviceMixin, QtPrintSupport.QPrinter):
    """Paint device that paints on a printer."""

    # def get_source(self) -> pathlib.Path:
    #     return pathlib.Path(self.source().toLocalFile())

    def get_duplex(self) -> DuplexModeStr:
        return DUPLEX_MODE.inverse[self.duplex()]

    def get_pdf_version(self) -> gui.pagedpaintdevice.PdfVersionStr:
        return gui.pagedpaintdevice.PDF_VERSION.inverse[self.pdfVersion()]

    def set_pdf_version(
        self,
        version: gui.pagedpaintdevice.PdfVersionStr | gui.PagedPaintDevice.PdfVersion,
    ):
        """Set pdf version.

        Args:
            version: pdf version
        """
        self.setPdfVersion(gui.pagedpaintdevice.PDF_VERSION.get_enum_value(version))
