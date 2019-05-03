# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets


class Splitter(QtWidgets.QSplitter):

    def __init__(self, orientation="horizontal", parent=None):
        o = QtCore.Qt.Vertical if orientation == "vertical" else QtCore.Qt.Horizontal
        super().__init__(o, parent)

    def __getitem__(self, index):
        return self.widget(index)

    def __iter__(self):
        return iter(self[i] for i in range(self.count()))

    def __len__(self):
        return self.count()

    def add_widget(self, widget):
        self.addWidget(widget)

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
