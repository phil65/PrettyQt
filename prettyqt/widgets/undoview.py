from typing import Union

from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QUndoView.__bases__ = (widgets.ListView,)


class UndoView(QtWidgets.QUndoView):
    def __getitem__(self, index: int) -> QtWidgets.QUndoCommand:
        return self.stack().command(index)

    def set_clean_icon(self, icon: gui.icon.IconType):
        """Set the icon for the clean button.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setCleanIcon(icon)

    def set_value(self, value: Union[QtWidgets.QUndoGroup, QtWidgets.QUndoStack]):
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
