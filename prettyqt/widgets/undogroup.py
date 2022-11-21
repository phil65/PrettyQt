from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


QtWidgets.QUndoGroup.__bases__ = (core.Object,)


class UndoGroup(QtWidgets.QUndoGroup):
    def __len__(self) -> int:
        return len(self.stacks())

    def __getitem__(self, index: int) -> QtWidgets.QUndoStack:
        return self.stacks()[index]
