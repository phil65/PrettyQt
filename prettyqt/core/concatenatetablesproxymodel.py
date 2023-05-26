from __future__ import annotations

from prettyqt import core, qt
from prettyqt.qt import QtCore


class ConcatenateTablesProxyModel(
    core.AbstractItemModelMixin, QtCore.QConcatenateTablesProxyModel
):
    ID = "concatenate"

    def parent(self, *args):
        # workaround: PyQt6 QConcatenateTablesProxyModel.parent() missing
        if not args and qt.API == "pyqt6":
            return QtCore.QAbstractItemModel.parent(self)
        return super().parent(*args)
