# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets
from prettyqt import widgets


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)

        if parent is not None:
            self.setMargin(margin)

        self.setSpacing(spacing)

        self.items = []

    def __getitem__(self, index):
        return self.itemAt(index)

    def __iter__(self):
        return iter(self[i] for i in range(self.count()))

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.items.append(item)

    def count(self):
        return len(self.items)

    def itemAt(self, index):
        if 0 <= index < len(self.items):
            return self.items[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.items:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.contentsMargins().top(),
                             2 * self.contentsMargins().top())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        line_height = 0

        for item in self.items:
            wid = item.widget()
            pb = widgets.SizePolicy.PushButton
            spaceX = self.spacing() + wid.style().layoutSpacing(pb,
                                                                pb,
                                                                QtCore.Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(pb,
                                                                pb,
                                                                QtCore.Qt.Vertical)
            next_x = x + item.sizeHint().width() + spaceX
            if next_x - spaceX > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + spaceY
                next_x = x + item.sizeHint().width() + spaceX
                line_height = 0

            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    layout = FlowLayout()
    layout.addWidget(QtWidgets.QPushButton("Short"))
    layout.addWidget(QtWidgets.QPushButton("Longer"))
    layout.addWidget(QtWidgets.QPushButton("Different text"))
    layout.addWidget(QtWidgets.QPushButton("More text"))
    layout.addWidget(QtWidgets.QPushButton("Even longer button text"))
    widget.setLayout(layout)
    widget.show()
    sys.exit(app.exec_())
