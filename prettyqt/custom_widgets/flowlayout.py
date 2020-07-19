# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets


class FlowLayout(widgets.Layout):
    def __init__(self, parent=None, margin=None, spacing=-1):
        super().__init__(parent)
        if margin is not None:
            self.set_margin(margin)
        self.set_spacing(spacing)
        self.items = []

    def __getstate__(self):
        return dict(items=self.get_children())

    def __add__(self, other):
        if isinstance(other, (QtWidgets.QWidget, QtWidgets.QLayout)):
            self.add(other)
            return self

    def __setstate__(self, state):
        self.__init__()
        for item in state["items"]:
            self.add(item)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.items.append(item)

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int):
        if 0 <= index < len(self.items):
            return self.items[index]

        return None

    def takeAt(self, index: int):
        if 0 <= index < len(self.items):
            return self.items.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int):
        return self.do_layout(core.Rect(0, 0, width, 0), True)

    def setGeometry(self, rect: QtCore.QRect):
        super().setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self) -> core.Size:
        return self.minimumSize()

    def minimumSize(self):
        size = core.Size()

        for item in self.items:
            size = size.expandedTo(item.minimumSize())

        margin_width = 2 * self.contentsMargins().top()
        size += core.Size(margin_width, margin_width)
        return size

    def do_layout(self, rect: QtCore.QRect, test_only: bool):
        x = rect.x()
        y = rect.y()
        line_height = 0

        for item in self.items:
            wid = item.widget()
            pb = widgets.SizePolicy.PushButton
            space = self.spacing()
            space_x = space + wid.style().layoutSpacing(pb, pb, QtCore.Qt.Horizontal)
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                space_y = space + wid.style().layoutSpacing(pb, pb, QtCore.Qt.Vertical)
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(core.Rect(core.Point(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.Widget()
    layout = FlowLayout()
    layout += FlowLayout()
    layout += widgets.PushButton("Short")
    layout += widgets.PushButton("Longer")
    layout += widgets.PushButton("Different text")
    layout += widgets.PushButton("More text")
    layout += widgets.PushButton("Even longer button text")
    widget.set_layout(layout)
    widget.show()
    app.exec_()
