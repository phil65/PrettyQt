from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtGui


class UndoGroupMixin(core.ObjectMixin):
    def __len__(self) -> int:
        return len(self.stacks())

    def __getitem__(self, index: int) -> QtGui.QUndoStack:
        return self.stacks()[index]


class UndoGroup(UndoGroupMixin, QtGui.QUndoGroup):
    pass
