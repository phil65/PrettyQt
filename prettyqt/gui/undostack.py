from __future__ import annotations

from collections.abc import Callable
import contextlib

from prettyqt import core, gui
from prettyqt.qt import QtGui


class UndoStackMixin(core.ObjectMixin):
    def __len__(self) -> int:
        return self.count()

    def __getitem__(self, index: int) -> QtGui.QUndoCommand:
        cmd = self.command(index)
        if cmd is None:
            raise KeyError(index)
        return cmd

    @contextlib.contextmanager
    def create_macro(self, text: str):
        self.beginMacro(text)
        yield None
        self.endMacro()

    def add_command(self, title: str, redo: Callable, undo: Callable) -> gui.UndoCommand:
        class MyCommand(gui.UndoCommand):
            def redo(self):
                return redo()

            def undo(self):
                return undo()

        cmd = MyCommand(title)
        self.push(cmd)
        return cmd


class UndoStack(UndoStackMixin, QtGui.QUndoStack):
    pass
