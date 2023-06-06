from __future__ import annotations

from typing import Literal

from prettyqt import printsupport
from prettyqt.qt import QtPrintSupport
from prettyqt.utils import bidict


PrintEnginePropertyKey = QtPrintSupport.QPrintEngine.PrintEnginePropertyKey

PRINT_ENGINE_PROPERTY_KEY = bidict(
    collate_copies=PrintEnginePropertyKey.PPK_CollateCopies,
    color_mode=PrintEnginePropertyKey.PPK_ColorMode,
    creator=PrintEnginePropertyKey.PPK_Creator,
    duplex=PrintEnginePropertyKey.PPK_Duplex,
    document_name=PrintEnginePropertyKey.PPK_DocumentName,
    font_embedding=PrintEnginePropertyKey.PPK_FontEmbedding,
    full_page=PrintEnginePropertyKey.PPK_FullPage,
    number_of_copies=PrintEnginePropertyKey.PPK_NumberOfCopies,
    orientation=PrintEnginePropertyKey.PPK_Orientation,
    output_file_name=PrintEnginePropertyKey.PPK_OutputFileName,
    page_order=PrintEnginePropertyKey.PPK_PageOrder,
    page_rect=PrintEnginePropertyKey.PPK_PageRect,
    page_size=PrintEnginePropertyKey.PPK_PageSize,
    paper_rect=PrintEnginePropertyKey.PPK_PaperRect,
    paper_source=PrintEnginePropertyKey.PPK_PaperSource,
    paper_sources=PrintEnginePropertyKey.PPK_PaperSources,
    paper_name=PrintEnginePropertyKey.PPK_PaperName,
    # paper_size=PrintEnginePropertyKey.PPK_PaperSize,
    printer_name=PrintEnginePropertyKey.PPK_PrinterName,
    printer_program=PrintEnginePropertyKey.PPK_PrinterProgram,
    resolution=PrintEnginePropertyKey.PPK_Resolution,
    selection_option=PrintEnginePropertyKey.PPK_SelectionOption,
    supported_resolutions=PrintEnginePropertyKey.PPK_SupportedResolutions,
    windows_page_size=PrintEnginePropertyKey.PPK_WindowsPageSize,
    custom_paper_size=PrintEnginePropertyKey.PPK_CustomPaperSize,
    page_margins=PrintEnginePropertyKey.PPK_PageMargins,
    copy_count=PrintEnginePropertyKey.PPK_CopyCount,
    supports_multiple_copies=PrintEnginePropertyKey.PPK_SupportsMultipleCopies,
    qpagesize=PrintEnginePropertyKey.PPK_QPageSize,
    qpagemargins=PrintEnginePropertyKey.PPK_QPageMargins,
    qpagelayout=PrintEnginePropertyKey.PPK_QPageLayout,
    custom_base=PrintEnginePropertyKey.PPK_CustomBase,
)


PrintEnginePropertyKeyStr = Literal["none", "auto", "long_side", "short_side"]


class PrintEngine(QtPrintSupport.QPrintEngine):
    def get_printer_state(self) -> PrintEnginePropertyKeyStr:
        return printsupport.printer.PRINTER_STATE.inverse[self.printerState()]
