from __future__ import annotations

import os

from typing import Literal

from prettyqt import core, pdf
from prettyqt.utils import bidict, datatypes


ROLE = bidict(
    page=pdf.QPdfSearchModel.Role.Page,
    index_on_page=pdf.QPdfSearchModel.Role.IndexOnPage,
    location=pdf.QPdfSearchModel.Role.Location,
    context_Before=pdf.QPdfSearchModel.Role.ContextBefore,
    context_after=pdf.QPdfSearchModel.Role.ContextAfter,
)

RoleStr = Literal[
    "page",
    "index_on_page",
    "location",
    "context_Before",
    "context_after",
]


class PdfSearchModel(core.AbstractItemModelMixin, pdf.QPdfSearchModel):
    def __init__(self, parent: core.QObject | None = None):
        super().__init__(parent)
        self.setDocument(pdf.PdfDocument(self))

    def set_document(self, document: datatypes.PathType | pdf.QPdfDocument):
        """Set document for model."""
        if not isinstance(document, pdf.QPdfDocument):
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
