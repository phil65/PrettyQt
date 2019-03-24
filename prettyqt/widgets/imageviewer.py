# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys
from qtpy import QtWidgets

from prettyqt import widgets


class ImageViewer(QtWidgets.QWidget):

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        path = "decisiontree.png"
        self.image = widgets.Image.from_path(path, parent=self)
        self.show()


def show():
    """
    open dialog and start eventloop
    """
    form = ImageViewer()
    form.show()
    form.exec_()
    return form


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = ImageViewer()
    sys.exit(app.exec_())
