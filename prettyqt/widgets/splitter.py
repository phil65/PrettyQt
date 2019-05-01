# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets


class Splitter(QtWidgets.QSplitter):

    def __init__(self, orientation="horizontal", parent=None):
        o = QtCore.Qt.Vertical if orientation == "vertical" else QtCore.Qt.Horizontal
        super().__init__(o, parent)

    @classmethod
    def from_widgets(cls, widgets, horizontal: bool = False, parent=None):
        orientation = QtCore.Qt.Horizontal if horizontal else QtCore.Qt.Vertical
        splitter = cls(orientation, parent=parent)
        for widget in widgets:
            splitter.addWidget(widget)
        return splitter

    def set_expanding(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Splitter()
    widget.show()
    app.exec_()
