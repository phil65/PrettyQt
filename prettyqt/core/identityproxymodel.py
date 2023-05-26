from __future__ import annotations

from prettyqt import core, qt
from prettyqt.qt import QtCore


class IdentityProxyModel(core.AbstractProxyModelMixin, QtCore.QIdentityProxyModel):
    ID = "identity"

    def parent(self, *args):
        # workaround: PyQt6 QIdentityproxymodel.parent() missing
        if not args and qt.API == "pyqt6":
            return QtCore.QAbstractProxyModel.parent(self)
        return super().parent(*args)
