from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


class UndoGroupMixin(core.ObjectMixin):
    def __len__(self) -> int:
        return len(self.stacks())

    def __getitem__(self, index: int) -> QtWidgets.QUndoStack:
        return self.stacks()[index]


class UndoGroup(UndoGroupMixin, QtWidgets.QUndoGroup):
    pass
