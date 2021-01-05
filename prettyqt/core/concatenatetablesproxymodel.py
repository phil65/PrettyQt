from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QConcatenateTablesProxyModel.__bases__ = (core.AbstractItemModel,)


class ConcatenateTablesProxyModel(QtCore.QConcatenateTablesProxyModel):

    pass
