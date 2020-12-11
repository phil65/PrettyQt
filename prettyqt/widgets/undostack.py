import contextlib
from typing import Callable

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QUndoStack.__bases__ = (core.Object,)


class UndoStack(QtWidgets.QUndoStack):
    def __len__(self) -> int:
        return self.count()

    def __getitem__(self, index: int) -> QtWidgets.QUndoCommand:
        return self.command(index)

    @contextlib.contextmanager
    def create_macro(self, text: str):
        self.beginMacro(text)
        yield None
        self.endMacro()

    def add_command(
        self, title: str, redo: Callable, undo: Callable
    ) -> widgets.UndoCommand:
        class MyCommand(widgets.UndoCommand):
            def redo(self):
                return redo()

            def undo(self):
                return undo()

        cmd = MyCommand(title)
        self.push(cmd)
        return cmd
