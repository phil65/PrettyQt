# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Dict, Callable
from contextlib import contextmanager

from qtpy import QtWidgets, QtCore, QtGui

from prettyqt import widgets, core


POLICIES = dict(custom=QtCore.Qt.CustomContextMenu,
                showhide_menu="showhide_menu")


class Widget(QtWidgets.QWidget):

    def __getstate__(self):
        return dict(layout=self.layout())

    def __setstate__(self, state):
        self.__init__()
        self.set_layout(state["layout"])

    def resize(self, *size):
        if isinstance(size[0], tuple):
            super().resize(*size[0])
        else:
            super().resize(*size)

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    @contextmanager
    def block_signals(self):
        self.blockSignals(True)
        yield None
        self.blockSignals(False)

    def set_expanding(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)

    def set_color(self, color):
        self.setStyleSheet(f"background-color: {color};")

    def set_stylesheet(self, item, dct: Dict[str, str]) -> str:
        ss = "; ".join(f"{k.replace('_', '-')}: {v}" for k, v in dct.items())
        stylesheet = f"{item} {{{ss};}}"
        self.setStyleSheet(stylesheet)
        return stylesheet

    def set_contextmenu_policy(self, policy):
        self.setContextMenuPolicy(POLICIES[policy])

    def set_custom_menu(self, method: Callable):
        self.set_contextmenu_policy("custom")
        self.customContextMenuRequested.connect(method)

    def set_layout(self, layout):
        if layout in ["horizontal", "vertical"]:
            self.box = widgets.BoxLayout(layout)
        elif layout == "grid":
            self.box = widgets.GridLayout()
        elif layout == "form":
            self.box = widgets.FormLayout()
        elif layout == "stacked":
            self.box = widgets.StackedLayout()
        elif layout == "flow":
            from prettyqt import custom_widgets
            self.box = custom_widgets.FlowLayout()
        else:
            self.box = layout
        if self.box is not None:
            self.setLayout(self.box)


Widget.__bases__[0].__bases__ = (core.Object, QtGui.QPaintDevice)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec_()
