from __future__ import annotations

from prettyqt.qt import QtWidgets


class UndoCommand(QtWidgets.QUndoCommand):
    def __len__(self) -> int:
        return self.childCount()

    def __getitem__(self, index: int) -> QtWidgets.QUndoCommand:
        child = self.child(index)
        if child is None:
            raise KeyError(index)
        return child

    def serialize_fields(self):
        return dict(children=[self.child(i) for i in range(self.childCount())])

    def __setstate__(self, state):
        for c in state["children"]:
            c.setParent(self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()
