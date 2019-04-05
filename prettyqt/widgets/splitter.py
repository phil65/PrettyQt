# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore


class Splitter(QtWidgets.QSplitter):

    def set_sizes(self):
        self.set_sizes()

    @classmethod
    def from_widgets(cls, widgets, horizontal: bool = False, parent=None):
        orientation = QtCore.Qt.Horizontal if horizontal else QtCore.Qt.Vertical
        splitter = cls(orientation, parent=parent)
        for widget in widgets:
            splitter.addWidget(widget)
        return splitter


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Splitter()
    widget.show()
    app.exec_()
