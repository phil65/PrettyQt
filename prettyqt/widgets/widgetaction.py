# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import widgets
from typing import Optional


QtWidgets.QWidgetAction.__bases__ = (widgets.Action,)


class WidgetAction(QtWidgets.QWidgetAction):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

    #     self.set_text(text)
    #     self.set_icon(icon)
    #     self.set_shortcut(shortcut)
    #     self.set_tooltip(tooltip)
