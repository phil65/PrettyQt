# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
import qtawesome as qta


class Dialog(QtWidgets.QDialog):

    DEFAULT_SIZE = (1500, 1000)

    def __init__(self, title="", icon=None, parent=None, horizontal=False):
        super().__init__(parent=parent)
        self.resize(*self.DEFAULT_SIZE)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle(title)
        self.set_icon(icon)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if horizontal:
            self.layout = QtWidgets.QHBoxLayout()
        else:
            self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

    def delete_on_close(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def add_widget(self, widget):
        self.layout.addWidget(widget)

    def set_icon(self, icon):
        if icon:
            if isinstance(icon, str):
                icon = qta.icon(icon, color="lightgray")
            self.setWindowIcon(icon)

    def add_buttonbox(self):
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                                QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accepted)
        button_box.rejected.connect(self.reject)
        self.layout.addWidget(button_box)

    def accepted(self):
        self.close()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_F11:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
        else:
            super().keyPressEvent(e)

    def open(self):
        self.show()
        self.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Dialog()
    widget.showMaximized()
    app.exec_()
