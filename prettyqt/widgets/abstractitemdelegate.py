from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtWidgets


class AbstractItemDelegateMixin(core.ObjectMixin):
    def _data_for_index(self, index, role=constants.USER_ROLE):
        # using index.data() sometimes casts stuff in PyQt6
        model = index.model()
        data = model.data(index, role)
        return data


class AbstractItemDelegate(AbstractItemDelegateMixin, QtWidgets.QAbstractItemDelegate):
    pass
