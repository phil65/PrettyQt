from __future__ import annotations

import os
from typing import Literal

from prettyqt import core, pdf
from prettyqt.qt import QtPdf
from prettyqt.utils import bidict, datatypes


ROLE = bidict(
    page=QtPdf.QPdfSearchModel.Role.Page,
    index_on_page=QtPdf.QPdfSearchModel.Role.IndexOnPage,
    location=QtPdf.QPdfSearchModel.Role.Location,
    context_Before=QtPdf.QPdfSearchModel.Role.ContextBefore,
    context_after=QtPdf.QPdfSearchModel.Role.ContextAfter,
)

RoleStr = Literal[
    "page",
    "index_on_page",
    "location",
    "context_Before",
    "context_after",
]


class PdfSearchModel(core.AbstractItemModelMixin, QtPdf.QPdfSearchModel):
    def __init__(self, parent: core.QObject | None = None):
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
    model = PdfSearchModel()
    widget = widgets.TableView()
    widget.set_model(model)
    widget.show()
    app.exec()
