from __future__ import annotations

import os
from typing import Literal

from prettyqt import core, pdf
from prettyqt.qt import QtCore, QtPdf
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
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self.setDocument(pdf.PdfDocument(self))

    def set_document(self, document: datatypes.PathType | QtPdf.QPdfDocument):
        """Set document for model."""
        if not isinstance(document, QtPdf.QPdfDocument):
            path = os.fspath(document)
            document = pdf.PdfDocument(self)
            document.load(path)
        self.setDocument(document)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    model = PdfBookmarkModel()
    widget = widgets.TableView()
    widget.set_model(model)
    widget.show()
    app.exec()
