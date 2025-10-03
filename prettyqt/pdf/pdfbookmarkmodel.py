from __future__ import annotations

import os
from typing import TYPE_CHECKING, Literal

from prettyqt import core, pdf
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


ROLE = bidict(
    title=pdf.QPdfBookmarkModel.Role.Title,
    level=pdf.QPdfBookmarkModel.Role.Level,
    page=pdf.QPdfBookmarkModel.Role.Page,
    location=pdf.QPdfBookmarkModel.Role.Location,
    zoom=pdf.QPdfBookmarkModel.Role.Zoom,
)

RoleStr = Literal[
    "title",
    "level",
    "page",
    "location",
    "zoom",
]


class PdfBookmarkModel(core.AbstractItemModelMixin, pdf.QPdfBookmarkModel):
    """Holds a tree of of links within a PDF document, such as the table of contents."""

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
    model = PdfBookmarkModel()
    widget = widgets.TableView()
    widget.set_model(model)
    widget.show()
    app.exec()
