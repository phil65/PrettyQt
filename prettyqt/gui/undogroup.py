from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtGui


if TYPE_CHECKING:
    _UndoGroupBase = QtGui.QUndoGroup
else:
    _UndoGroupBase = object


class UndoGroupMixin(core.ObjectMixin, _UndoGroupBase):
    def __len__(self) -> int:
        return len(self.stacks())

    def __getitem__(self, index: int) -> QtGui.QUndoStack:
        return self.stacks()[index]


class UndoGroup(UndoGroupMixin, QtGui.QUndoGroup):
    pass
