from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


class AbstractItemDelegateMixin(core.ObjectMixin):
    pass


class AbstractItemDelegate(AbstractItemDelegateMixin, QtWidgets.QAbstractItemDelegate):
    pass
