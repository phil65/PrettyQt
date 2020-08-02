# -*- coding: utf-8 -*-

from qtpy import QtWidgets


class UndoCommand(QtWidgets.QUndoCommand):
    def __len__(self) -> int:
        return self.childCount()

    def __getitem__(self, index) -> QtWidgets.QUndoCommand:
        return self.child(index)

    def serialize_fields(self):
        return dict(children=[self.child(i) for i in range(self.childCount())])

    def __setstate__(self, state):
        self.__init__()
        for c in state["children"]:
            c.setParent(self)
