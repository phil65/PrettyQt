from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class MultiLineLayout(widgets.BoxLayout):
    def __init__(self, vertical: bool = True, row_number: int = 10, *args, **kwargs):
        self._items = []
        self.row_nb = row_number
        self.cindex = 0
        self.layouts = []
        direction = self.Direction.TopToBottom if vertical else self.Direction.LeftToRight
        super().__init__(direction, **kwargs)

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout) -> MultiLineLayout:
        if not isinstance(other, QtWidgets.QWidget | QtWidgets.QLayout):
            raise TypeError()
        self.add(other)
        return self

    def set_direction(self, direction: widgets.BoxLayout.Direction):
        super().setDirection(direction)
        direction = (
            self.Direction.LeftToRight
            if self.get_direction() == "top_to_bottom"
            else self.Direction.TopToBottom
        )
        for layout in self.layouts:
            layout.setDirection(direction)
        self.repaint()

    # def __del__(self):
    #     item = self.takeAt(0)
    #     while item:
    #         item = self.takeAt(0)

    def addWidget(self, widget: QtWidgets.QWidget):
        if self.cindex == 0:
            direction = (
                self.Direction.LeftToRight
                if self.get_direction() == "top_to_bottom"
                else self.Direction.TopToBottom
            )
            self.col_layout = widgets.BoxLayout(direction)
            super().addLayout(self.col_layout)
            self.layouts.append(self.col_layout)
        self.col_layout.add(widget)
        self.cindex = (self.cindex + 1) % self.row_nb

    def addLayout(self, layout: QtWidgets.QLayout):
        widget = widgets.Widget()
        widget.setLayout(layout)
        self.addWidget(widget)

    def addItem(self, item):
        self._items.append(item)

    def itemAt(self, idx):
        try:
            return self._items[idx]
        except IndexError:
            pass

    # def takeAt(self, idx):
    #     layout_idx = idx % len(self.layouts)
    #     try:
    #         self.layouts[layout_idx].takeAt(idx)
    #         for i, layout in enumerate(self.layouts[layout_idx:]):
    #             prev_layout = self.layouts[layout_idx + i - 1]
    #             layout.addItem(prev_layout.takeAt(prev_layout.count() - 1))
    #         return self._items.pop(idx)
    #     except IndexError:
    #         pass

    def count(self):
        return len(self._items)


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.Widget()
    layout = MultiLineLayout(parent=widget)
    layout.add(widgets.PushButton("Short"))
    layout.add(widgets.PushButton("Longer"))
    layout.add(widgets.PushButton("Different text"))
    layout.add(widgets.PushButton("More text"))
    layout.add(widgets.PushButton("Even longer button text"))
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
