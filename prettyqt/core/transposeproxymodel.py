from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class TransposeProxyModel(core.AbstractProxyModelMixin, QtCore.QTransposeProxyModel):
    pass
