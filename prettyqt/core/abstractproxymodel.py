from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QAbstractProxyModel.__bases__ = (core.AbstractItemModel,)


class AbstractProxyModel(QtCore.QAbstractProxyModel):
    pass
