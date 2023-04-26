from __future__ import annotations

import os
from typing import Literal

from prettyqt import core, pdf, widgets
from prettyqt.qt import QtPdf, QtWidgets
from prettyqt.utils import bidict, datatypes


ROLE = bidict(
    title=QtPdf.QPdfBookmarkModel.Role.Title,
    level=QtPdf.QPdfBookmarkModel.Role.Level,
    page=QtPdf.QPdfBookmarkModel.Role.Page,
    location=QtPdf.QPdfBookmarkModel.Role.Location,
    zoom=QtPdf.QPdfBookmarkModel.Role.Zoom,
)

RoleStr = Literal[
    "title",
    "level",
    "page",
    "location",
    "zoom",
]


class PdfBookmarkModel(core.AbstractItemModelMixin, QtPdf.QPdfBookmarkModel):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setDocument(pdf.PdfDocument(self))

    def set_document(self, document: datatypes.PathType | QtPdf.QPdfDocument):
        if not isinstance(document, QtPdf.QPdfDocument):
            path = os.fspath(document)
            document = pdf.PdfDocument(self)
            document.load(path)
        self.setDocument(document)


if __name__ == "__main__":
    app = widgets.app()
    view = PdfBookmarkModel()
    view.show()
    app.main_loop()
