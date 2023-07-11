from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import gui, iconprovider, widgets


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class UndoView(widgets.ListViewMixin, widgets.QUndoView):
    """Displays the contents of a QUndoStack."""

    def __getitem__(self, index: int) -> gui.QUndoCommand:
        return self.stack().command(index)

    def set_clean_icon(self, icon: datatypes.IconType):
        """Set the icon for the clean button.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setCleanIcon(icon)

    def set_value(self, value: gui.QUndoGroup | gui.QUndoStack):
        if isinstance(value, gui.QUndoGroup):
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
    app.exec()
