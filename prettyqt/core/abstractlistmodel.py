from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class AbstractListModelMixin(core.AbstractItemModelMixin):
    pass


class AbstractListModel(AbstractListModelMixin, QtCore.QAbstractListModel):
    pass
