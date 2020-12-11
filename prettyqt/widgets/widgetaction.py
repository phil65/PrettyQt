from typing import Optional

from qtpy import QtWidgets, QtCore

from prettyqt import widgets


QtWidgets.QWidgetAction.__bases__ = (widgets.Action,)


class WidgetAction(QtWidgets.QWidgetAction):
    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)

    #     self.set_text(text)
    #     self.set_icon(icon)
    #     self.set_shortcut(shortcut)
    #     self.set_tooltip(tooltip)
