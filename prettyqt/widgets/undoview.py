from __future__ import annotations

from prettyqt import gui, iconprovider, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import datatypes


class UndoView(widgets.ListViewMixin, QtWidgets.QUndoView):
    def __getitem__(self, index: int) -> QtGui.QUndoCommand:
        return self.stack().command(index)

    def set_clean_icon(self, icon: datatypes.IconType):
        """Set the icon for the clean button.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setCleanIcon(icon)

    def set_value(self, value: QtGui.QUndoGroup | QtGui.QUndoStack):
        if isinstance(value, QtGui.QUndoGroup):
            self.setGroup(value)
        else:
            self.setStack(value)


if __name__ == "__main__":
    app = widgets.app()
    view = UndoView()
    stack = gui.UndoStack()
    stack.add_command("test", redo=lambda: print("redo"), undo=lambda: print("undo"))
    view.setStack(stack)
    view.show()
    app.main_loop()
