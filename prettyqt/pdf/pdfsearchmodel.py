from __future__ import annotations

import os
from typing import TYPE_CHECKING, Literal

from prettyqt import core, pdf
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


RoleStr = Literal[
    "page",
    "index_on_page",
    "location",
    "context_Before",
    "context_after",
]

ROLE = bidict[RoleStr, pdf.QPdfSearchModel.Role](
    page=pdf.QPdfSearchModel.Role.Page,
    index_on_page=pdf.QPdfSearchModel.Role.IndexOnPage,
    location=pdf.QPdfSearchModel.Role.Location,
    context_Before=pdf.QPdfSearchModel.Role.ContextBefore,
    context_after=pdf.QPdfSearchModel.Role.ContextAfter,
)


class PdfSearchModel(core.AbstractItemModelMixin, pdf.QPdfSearchModel):
    """Searches for a string in a PDF document and holds the results."""

    def __init__(self, parent: core.QObject | None = None):
        super().__init__(parent)
        doc = pdf.PdfDocument(self)
        self.setDocument(doc)

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
