from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class ConcatenateTablesProxyModel(
    core.AbstractItemModelMixin, QtCore.QConcatenateTablesProxyModel
):
    pass
