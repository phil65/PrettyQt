# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets


class UndoCommand(QtWidgets.QUndoCommand):
    def __len__(self) -> int:
        return self.childCount()

    def __getitem__(self, index) -> QtWidgets.QUndoCommand:
        return self.child(index)
