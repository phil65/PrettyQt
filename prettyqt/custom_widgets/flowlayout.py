from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets


class FlowLayout(widgets.Layout):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        margin: int | None = None,
        spacing: int = -1,
    ):
        super().__init__(parent)  # type: ignore
        if margin is not None:
            self.set_margin(margin)
        self.set_spacing(spacing)
        self.items: list[QtWidgets.QLayoutItem] = []

    def serialize_fields(self):
        return dict(items=self.get_children())

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout) -> FlowLayout:
        if not isinstance(other, (QtWidgets.QWidget, QtWidgets.QLayout)):
            raise TypeError()
        self.add(other)
        return self

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __setstate__(self, state):
        for item in state["items"]:
            self.add(item)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QtWidgets.QLayoutItem):
        self.items.append(item)

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int) -> QtWidgets.QLayoutItem | None:  # type: ignore
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def takeAt(self, index: int) -> QtWidgets.QLayoutItem | None:  # type: ignore
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    # def expandingDirections(self) -> QtCore.Qt.Orientations:
    #     return QtCore.Qt.Orientations(0)

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        rect = QtCore.QRect(0, 0, width, 0)
        return self.do_layout(rect, True)

    def setGeometry(self, rect: QtCore.QRect):
        super().setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self) -> QtCore.QSize:
        return self.minimumSize()

    def minimumSize(self) -> QtCore.QSize:
        size = QtCore.QSize()

        for item in self.items:
            size = size.expandedTo(item.minimumSize())

        margin_width = 2 * self.contentsMargins().top()
        size += QtCore.QSize(margin_width, margin_width)
        return size

    def do_layout(self, rect: QtCore.QRect, test_only: bool) -> int:
        x = rect.x()
        y = rect.y()
        line_height = 0
        space = self.spacing()
        pb = widgets.SizePolicy.ControlType.PushButton
        for item in self.items:
            wid = item.widget()
            space_x = space + wid.style().layoutSpacing(pb, pb, constants.HORIZONTAL)
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                space_y = space + wid.style().layoutSpacing(pb, pb, constants.VERTICAL)
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
    layout.add(widgets.PushButton("Short"))
    layout.add(widgets.PushButton("Longer"))
    layout.add(widgets.PushButton("Different text"))
    layout.add(widgets.PushButton("More text"))
    layout.add(widgets.PushButton("Even longer button text"))
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
