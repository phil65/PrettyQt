# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QScrollArea.__bases__ = (widgets.AbstractScrollArea,)


class ScrollArea(QtWidgets.QScrollArea):
    def __getstate__(self):
        return dict(widget=self.widget(), resizable=self.widgetResizable())

    def __setstate__(self, state):
        self.__init__()
        self.set_widget(state["widget"])
        self.setWidgetResizable(state["resizable"])

    def set_widget(self, widget):
        self.setWidget(widget)
