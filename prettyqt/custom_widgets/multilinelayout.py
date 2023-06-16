from __future__ import annotations

from prettyqt import widgets


class MultiLineLayout(widgets.BoxLayout):
    """Nested Boxlayout."""

    def __init__(self, vertical: bool = True, row_number: int = 3, **kwargs):
        self._items = []
        self.row_nb = row_number
        self.layouts = []
        direction = self.Direction.TopToBottom if vertical else self.Direction.LeftToRight
        super().__init__(direction, **kwargs)

    def set_direction(
        self, direction: widgets.BoxLayout.Direction | widgets.boxlayout.DirectionStr
    ):
        super().set_direction(direction)
        direction = self.get_sub_direction()
        for layout in self.layouts:
            layout.set_direction(direction)

    # def __del__(self):
    #     item = self.takeAt(0)
    #     while item:
    #         item = self.takeAt(0)

    def get_sub_direction(self) -> widgets.BoxLayout.Direction:
        return (
            self.Direction.LeftToRight
            if self.get_direction() == "top_to_bottom"
            else self.Direction.TopToBottom
        )

    def addWidget(self, widget: widgets.QWidget):
        if not self.layouts or self.layouts[-1].count() == self.row_nb:
            direction = self.get_sub_direction()
            col_layout = widgets.BoxLayout(direction)
            super().addLayout(col_layout)
            self.layouts.append(col_layout)
        else:
            col_layout = self.layouts[-1]
        col_layout.add(widget)

    def addLayout(self, layout: widgets.QLayout):
        widget = widgets.Widget()
        widget.setLayout(layout)
        self.addWidget(widget)

    def addItem(self, item):
        self._items.append(item)

    def itemAt(self, idx: int):
        try:
            return self._items[idx]
        except IndexError:
            pass

    def takeAt(self, idx: int):
        layout_idx, item_idx = divmod(idx, len(self.layouts))
        self.layouts[layout_idx - 1].takeAt(item_idx)
        for i, layout in enumerate(self.layouts[layout_idx:]):
            prev_layout = self.layouts[layout_idx + i - 1]
            layout.addItem(prev_layout.takeAt(-1))
        return self._items.pop(idx)

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
    layout.add(widgets.PushButton("Even longer button text"))
    # layout.set_direction("left_to_right")
    # layout.takeAt(4)
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
