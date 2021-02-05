from __future__ import annotations

from prettyqt import iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


QtWidgets.QUndoView.__bases__ = (widgets.ListView,)


class UndoView(QtWidgets.QUndoView):
    def __getitem__(self, index: int) -> QtWidgets.QUndoCommand:
        return self.stack().command(index)

    def set_clean_icon(self, icon: types.IconType):
        """Set the icon for the clean button.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setCleanIcon(icon)

    def set_value(self, value: QtWidgets.QUndoGroup | QtWidgets.QUndoStack):
        if isinstance(value, QtWidgets.QUndoGroup):
            self.setGroup(value)
        else:
            self.setStack(value)


if __name__ == "__main__":
    app = widgets.app()
    view = UndoView()
    stack = widgets.UndoStack()
    stack.add_command("test", redo=lambda: print("redo"), undo=lambda: print("undo"))
    view.setStack(stack)
    view.show()
    app.main_loop()
