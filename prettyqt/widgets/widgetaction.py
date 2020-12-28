from typing import Optional

from prettyqt import widgets
from prettyqt.qt import QtCore, QtWidgets


QtWidgets.QWidgetAction.__bases__ = (widgets.Action,)


class WidgetAction(QtWidgets.QWidgetAction):
    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)  # type: ignore
        self._menu = None  # bc of PySide inheritance also defined here

    #     self.set_text(text)
    #     self.set_icon(icon)
    #     self.set_shortcut(shortcut)
    #     self.set_tooltip(tooltip)


if __name__ == "__main__":
    w = WidgetAction()
