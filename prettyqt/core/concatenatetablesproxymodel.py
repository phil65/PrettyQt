from __future__ import annotations

from prettyqt import core, qt


class ConcatenateTablesProxyModel(
    core.AbstractItemModelMixin, core.QConcatenateTablesProxyModel
):
    ID = "concatenate"

    def parent(self, *args):
        # workaround: PyQt6 QConcatenateTablesProxyModel.parent() missing
        if not args and qt.API == "pyqt6":
            return core.QAbstractItemModel.parent(self)
        return super().parent(*args)
