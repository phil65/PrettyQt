# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
import qtawesome as qta

from prettyqt import widgets


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
    app = widgets.Application.create_default_app()
    widget = MessageBox()
    widget.show()
    app.exec_()
