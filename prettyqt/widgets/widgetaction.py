from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtCore, QtWidgets


class WidgetAction(gui.ActionMixin, QtWidgets.QWidgetAction):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)  # type: ignore
        self._menu = None  # bc of PySide inheritance also defined here

    #     self.set_text(text)
    #     self.set_icon(icon)
    #     self.set_shortcut(shortcut)
    #     self.set_tooltip(tooltip)


if __name__ == "__main__":
    w = WidgetAction()
