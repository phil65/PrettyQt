from __future__ import annotations

from typing import Callable

from prettyqt import constants
from prettyqt.qt import QtCore


class SelectionMixin:

    CHECKSTATE: dict[int, Callable] = {}  # column: identifier
    dataChanged: QtCore.Signal
    DATA_ROLE: int

    def __init__(self):
        super().__init__()
        self.selected = {}

    def setData(self, index: QtCore.QModelIndex, value, role) -> bool:
        if not index.isValid():
            return False
        elif role == constants.CHECKSTATE_ROLE:
            name = self._get_selection_id(index)
            self.selected[name] = not self.selected[name]
            self.dataChanged.emit(index, index)
            return True
        return super().setData(index, value, role)  # type: ignore

    def data(self, index: QtCore.QModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return False
        if role == constants.CHECKSTATE_ROLE:
            if index.column() == 0:
                name = self._get_selection_id(index)
                selected = self.selected.get(name, False)
                if name not in self.selected:
                    self.selected[name] = selected
                return selected
        return super().data(index, role)  # type: ignore

    def flags(self, index: QtCore.QModelIndex):
        flags = super().flags(index)  # type: ignore
        if index.column() in self.CHECKSTATE:
            return flags | constants.IS_CHECKABLE
        return flags

    def _get_selection_id(self, index: QtCore.QModelIndex):
        item = index.data(self.DATA_ROLE)
        id_fn = self.CHECKSTATE.get(index.column())
        if id_fn:
            return id_fn(item)
