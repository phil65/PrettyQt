# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
import qtawesome as qta


class MessageBox(QtWidgets.QMessageBox):

    def set_horizontal(self):
        self.setOrientation(QtCore.Qt.Horizontal)

    def set_vertical(self):
        self.setOrientation(QtCore.Qt.Vertical)

    def set_icon(self, icon):
        if icon:
            if isinstance(icon, str):
                icon = qta.icon(icon, color="lightgray")
            self.setWindowIcon(icon)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = MessageBox()
    widget.show()
    app.exec_()
