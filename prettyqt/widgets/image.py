# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtWidgets, QtCore

H_ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                    right=QtCore.Qt.AlignRight,
                    center=QtCore.Qt.AlignHCenter,
                    justify=QtCore.Qt.AlignJustify)

V_ALIGNMENTS = dict(top=QtCore.Qt.AlignTop,
                    bottom=QtCore.Qt.AlignBottom,
                    center=QtCore.Qt.AlignVCenter,
                    baseline=QtCore.Qt.AlignBaseline)


class Image(QtWidgets.QLabel):

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setScaledContents(True)
        self.set_alignment(horizontal="center")
        self.setText("<html><head/><body><p>"
                     f'<img src="{path}" width="300"/>'
                     "</p></body></html>")

    def set_alignment(self, h_alignment=None, v_alignment=None):
        if h_alignment is None and v_alignment is not None:
            flag = V_ALIGNMENTS.get(v_alignment)
        elif v_alignment is None and h_alignment is not None:
            flag = H_ALIGNMENTS.get(h_alignment)
        elif v_alignment is not None and h_alignment is not None:
            flag = V_ALIGNMENTS.get(v_alignment) | H_ALIGNMENTS.get(h_alignment)
        else:
            return
        self.setAlignment(flag)

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
