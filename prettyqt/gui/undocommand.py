from __future__ import annotations

from prettyqt.qt import QtGui


class UndoCommand(QtGui.QUndoCommand):
    def __len__(self) -> int:
        return self.childCount()

    def __getitem__(self, index: int) -> QtGui.QUndoCommand:
        if index >= self.childCount():
            raise IndexError(index)
        return self.child(index)

    # def __setstate__(self, state):
    #     for c in state["children"]:
    #         c.setParent(self)

    # def __reduce__(self):
    #     return type(self), (), self.__getstate__()
