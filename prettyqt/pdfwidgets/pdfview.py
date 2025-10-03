from __future__ import annotations

import os
from typing import TYPE_CHECKING, Literal

from prettyqt import core, pdf, widgets
from prettyqt.qt import QtPdfWidgets
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


PageModeStr = Literal[
    "single",
    "multi",
]

PAGE_MODE: bidict[PageModeStr, QtPdfWidgets.QPdfView.PageMode] = bidict(
    single=QtPdfWidgets.QPdfView.PageMode.SinglePage,
    multi=QtPdfWidgets.QPdfView.PageMode.MultiPage,
)

ZoomModeStr = Literal[
    "custom",
    "fit_to_width",
    "fit_in_view",
]

ZOOM_MODE: bidict[ZoomModeStr, QtPdfWidgets.QPdfView.ZoomMode] = bidict(
    custom=QtPdfWidgets.QPdfView.ZoomMode.Custom,
    fit_to_width=QtPdfWidgets.QPdfView.ZoomMode.FitToWidth,
    fit_in_view=QtPdfWidgets.QPdfView.ZoomMode.FitInView,
)


class PdfView(widgets.AbstractScrollAreaMixin, QtPdfWidgets.QPdfView):
    """PDF viewer widget ."""

    def __init__(self, parent: widgets.QWidget | None = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.setDocument(pdf.PdfDocument(self))

    def get_document_margins(self) -> core.Margins:
        return core.Margins(self.documentMargins())

    def set_file(self, path: datatypes.PathType):
        doc = pdf.PdfDocument(self)
        doc.load(os.fspath(path))
        self.setDocument(doc)

    def set_page_mode(self, mode: PageModeStr | QtPdfWidgets.QPdfView.PageMode):
        """Set the page mode.

        Args:
            mode: page mode
        """
        self.setPageMode(PAGE_MODE.get_enum_value(mode))

    def get_page_mode(self) -> PageModeStr:
        """Return current page mode.

        Returns:
            page mode
        """
        return PAGE_MODE.inverse[self.pageMode()]

    def set_zoom_mode(self, mode: ZoomModeStr | QtPdfWidgets.QPdfView.ZoomMode):
        """Set the zoom mode.

        Args:
            mode: zoom mode
        """
        self.setZoomMode(ZOOM_MODE.get_enum_value(mode))

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
    app.exec()
