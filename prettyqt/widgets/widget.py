# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from contextlib import contextmanager

from qtpy import QtWidgets


class Widget(QtWidgets.QWidget):

    def __getstate__(self):
        return dict(layout=self.layout())

    def __setstate__(self, state):
        self.__init__()
        self.setLayout(state["layout"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    @contextmanager
    def block_signals(self):
        self.blockSignals(True)
        yield None
        self.blockSignals(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Widget()
    widget.show()
    app.exec_()
