# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import QtGui, QtWidgets, QtCore
from prettyqt import widgets


H_ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                    right=QtCore.Qt.AlignRight,
                    center=QtCore.Qt.AlignHCenter,
                    justify=QtCore.Qt.AlignJustify)

V_ALIGNMENTS = dict(top=QtCore.Qt.AlignTop,
                    bottom=QtCore.Qt.AlignBottom,
                    center=QtCore.Qt.AlignVCenter,
                    baseline=QtCore.Qt.AlignBaseline)


class Image(widgets.Label):

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setScaledContents(True)
        self.set_alignment(horizontal="center")
        self.set_image(path, width=300)

    def set_image(self, path, width=300):
        self.setText("<html><head/><body><p>"
                     f'<img src="{path}" width="{width}"/>'
                     "</p></body></html>")

    @classmethod
    def from_path(cls, path: pathlib.Path, parent=None) -> "Image":
        with path.open(mode="rb") as f:
            data = f.read()
        # Create widget
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        label = widgets.Label(parent=parent)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Image(path="")
    widget.show()
    app.exec_()
