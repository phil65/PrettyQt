from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import bidict


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

WebEngineHistoryModel = QtWebEngineCore.QWebEngineHistoryModel

# cant subclass.

# class WebEngineHistoryModel(
#     core.AbstractListModelMixin, QtWebEngineCore.QWebEngineHistoryModel
# ):
#     pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    model = WebEngineHistoryModel()
    widget = widgets.TableView()
    # widget.set_model(model)
    widget.show()
    app.exec()
