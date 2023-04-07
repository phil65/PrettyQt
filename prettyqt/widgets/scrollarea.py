from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class ScrollArea(widgets.AbstractScrollAreaMixin, QtWidgets.QScrollArea):
    def serialize_fields(self):
        return dict(widget=self.widget(), resizable=self.widgetResizable())

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_widget(state["widget"])
        self.setWidgetResizable(state["resizable"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_widget(self, widget: QtWidgets.QWidget):
        self.setWidget(widget)
