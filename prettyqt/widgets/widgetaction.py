# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets

QtWidgets.QWidgetAction.__bases__ = (widgets.Action,)


class WidgetAction(QtWidgets.QWidgetAction):
    def __init__(self, parent=None):
        super().__init__(parent)
    #     self.set_text(text)
    #     self.set_icon(icon)
    #     self.set_shortcut(shortcut)
    #     self.set_tooltip(tooltip)
