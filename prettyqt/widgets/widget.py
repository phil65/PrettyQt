# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Dict

from qtpy import QtWidgets


class WidgetMixin(QtWidgets.QWidget):

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_stylesheet(self, item, dct: Dict[str, str]) -> str:
        ss = "; ".join(f"{k}: {v}" for k, v in dct.items())
        self.setStyleSheet(f"{item} {{{ss};}}")


class Widget(WidgetMixin, QtWidgets.QWidget):
    pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Widget()
    widget.show()
    app.exec_()
