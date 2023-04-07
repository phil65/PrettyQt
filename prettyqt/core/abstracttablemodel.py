from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class AbstractTableModelMixin(core.AbstractItemModelMixin):
    pass


class AbstractTableModel(AbstractTableModelMixin, QtCore.QAbstractTableModel):
    pass
