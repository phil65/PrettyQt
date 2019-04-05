# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class ProgressBar(QtWidgets.QProgressBar):
    """Progress dialog

    wrapper for QtWidgets.QProgressBar
    """

    def set_range(self, start, end):
        self.setRange(start, end)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = ProgressBar()
    widget.show()
    app.exec_()
