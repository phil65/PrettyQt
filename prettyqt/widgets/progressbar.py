# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class ProgressBar(QtWidgets.QProgressBar):
    """Progress dialog

    wrapper for QtWidgets.QProgressBar
    """

    def set_range(self, start, end):
        self.setRange(start, end)


ProgressBar.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ProgressBar()
    widget.show()
    app.exec_()
