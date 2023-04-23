from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class ScrollArea(widgets.AbstractScrollAreaMixin, QtWidgets.QScrollArea):
    def set_widget(self, widget: QtWidgets.QWidget):
        self.setWidget(widget)
