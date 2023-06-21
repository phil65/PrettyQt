from __future__ import annotations

import os
from typing import Literal

from prettyqt import core, pdf
from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import bidict, datatypes


ROLE = bidict(
    url=QtWebEngineCore.QWebEngineHistoryModel.Roles.UrlRole,
    title=QtWebEngineCore.QWebEngineHistoryModel.Roles.TitleRole,
    offset=QtWebEngineCore.QWebEngineHistoryModel.Roles.OffsetRole,
    icon_url=QtWebEngineCore.QWebEngineHistoryModel.Roles.IconUrlRole,
)

RoleStr = Literal[
    "url",
    "title",
    "offset",
    "icon_url",
]


class WebEngineHistoryModel(
    core.AbstractListModelMixin, QtWebEngineCore.QWebEngineHistoryModel
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDocument(pdf.PdfDocument(self))

    def set_document(self, document: datatypes.PathType | QtWebEngineCore.QPdfDocument):
        if not isinstance(document, QtWebEngineCore.QPdfDocument):
            path = os.fspath(document)
            document = pdf.PdfDocument(self)
            document.load(path)
        self.setDocument(document)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    # model = WebEngineHistoryModel()
    widget = widgets.TableView()
    # widget.set_model(model)
    widget.show()
    app.exec()
