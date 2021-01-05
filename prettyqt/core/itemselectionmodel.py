from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QItemSelectionModel.__bases__ = (core.Object,)


class ItemSelectionModel(QtCore.QItemSelectionModel):
    pass
