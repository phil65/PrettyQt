from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QTransposeProxyModel.__bases__ = (core.AbstractProxyModel,)


class TransposeProxyModel(QtCore.QTransposeProxyModel):
    pass
