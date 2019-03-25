# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtWidgets, QtCore


class Image(QtWidgets.QLabel):

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setScaledContents(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("<html><head/><body><p>"
                     f'<img src="{path}" width="300"/>'
                     "</p></body></html>")

    @classmethod
    def from_path(cls, path, parent=None) -> "Image":
        with open(path, mode="rb") as f:
            data = f.read()
        # Create widget
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        label = cls(parent=parent)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Image(path="")
    widget.show()
    app.exec_()
