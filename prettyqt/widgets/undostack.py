from __future__ import annotations

from collections.abc import Callable
import contextlib

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class UndoStackMixin(core.ObjectMixin):
    def __len__(self) -> int:
        return self.count()

    def __getitem__(self, index: int) -> QtWidgets.QUndoCommand:
        cmd = self.command(index)
        if cmd is None:
            return KeyError(index)
        return cmd

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


class UndoStack(UndoStackMixin, QtWidgets.QUndoStack):
    pass
