# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

from prettyqt import widgets


class FlowLayout(widgets.Layout):

    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        if parent is not None:
            self.set_margin(margin)
        self.setSpacing(spacing)
        self.items = []

    def __repr__(self):
        return f"FlowLayout: {self.count()} children"

    def __getstate__(self):
        return dict(items=self.get_children())

    def __add__(self, other):
        if isinstance(other, (QtWidgets.QWidget, QtWidgets.QLayout)):
            self.add_item(other)
            return self

    def __setstate__(self, state):
        self.__init__()
        for item in state["items"]:
            self.add_item(item)

    def __getitem__(self, index):
        item = self.itemAt(index)
        widget = item.widget()
        if widget is None:
            widget = item.layout()
        return widget

    def __iter__(self):
        return iter(self.get_children())

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def get_children(self):
        return [self[i] for i in range(self.count())]

    def addItem(self, item):
        self.items.append(item)

    def add_item(self, item):
        if isinstance(item, QtWidgets.QWidget):
            self.addWidget(item)
        else:
            self.addLayout(item)

    def count(self) -> int:
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
        height = self.do_layout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.items:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.contentsMargins().top(),
                             2 * self.contentsMargins().top())
        return size

    def do_layout(self, rect, test_only):
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

            if not test_only:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    layout = FlowLayout()
    layout += widgets.PushButton("Short")
    layout += widgets.PushButton("Longer")
    layout += widgets.PushButton("Different text")
    layout += widgets.PushButton("More text")
    layout += widgets.PushButton("Even longer button text")
    widget.setLayout(layout)
    widget.show()
    sys.exit(app.exec_())
