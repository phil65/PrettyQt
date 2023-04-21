from __future__ import annotations

import os
from typing import Literal

from prettyqt import core, pdf, widgets
from prettyqt.qt import QtPdfWidgets, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, datatypes


PAGE_MODE = bidict(
    single=QtPdfWidgets.QPdfView.PageMode.SinglePage,
    multi=QtPdfWidgets.QPdfView.PageMode.MultiPage,
)

PageModeStr = Literal[
    "single",
    "multi",
]

ZOOM_MODE = bidict(
    custom=QtPdfWidgets.QPdfView.ZoomMode.Custom,
    fit_to_width=QtPdfWidgets.QPdfView.ZoomMode.FitToWidth,
    fit_in_view=QtPdfWidgets.QPdfView.ZoomMode.FitInView,
)

ZoomModeStr = Literal[
    "custom",
    "fit_to_width",
    "fit_in_view",
]


class PdfView(widgets.AbstractScrollAreaMixin, QtPdfWidgets.QPdfView):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setDocument(pdf.PdfDocument(self))

    def get_document_margins(self) -> core.Margins:
        return core.Margins(self.documentMargins())

    def set_file(self, path: datatypes.PathType):
        doc = pdf.PdfDocument(self)
        doc.load(os.fspath(path))
        self.setDocument(doc)

    def set_page_mode(self, mode: PageModeStr):
        """Set the page mode.

        Args:
            mode: page mode

        Raises:
            InvalidParamError: page mode does not exist
        """
        if mode not in PAGE_MODE:
            raise InvalidParamError(mode, PAGE_MODE)
        self.setPageMode(PAGE_MODE[mode])

    def get_page_mode(self) -> PageModeStr:
        """Return current page mode.

        Returns:
            page mode
        """
        return PAGE_MODE.inverse[self.pageMode()]

    def set_zoom_mode(self, mode: ZoomModeStr):
        """Set the zoom mode.

        Args:
            mode: zoom mode

        Raises:
            InvalidParamError: zoom mode does not exist
        """
        if mode not in ZOOM_MODE:
            raise InvalidParamError(mode, ZOOM_MODE)
        self.setZoomMode(ZOOM_MODE[mode])

    def get_zoom_mode(self) -> ZoomModeStr:
        """Return current zoom mode.

        Returns:
            zoom mode
        """
        return ZOOM_MODE.inverse[self.zoomMode()]


if __name__ == "__main__":
    app = widgets.app()
    view = PdfView()
    view.show()
    app.main_loop()
