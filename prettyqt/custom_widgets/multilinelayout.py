from __future__ import annotations

import itertools

from prettyqt import widgets
from prettyqt.utils import listdelegators


class MultiLineLayout(widgets.BoxLayout):
    """Nested Boxlayout."""

    def __init__(self, vertical: bool = True, row_number: int = 3, **kwargs):
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

    def get_sub_direction(self) -> widgets.BoxLayout.Direction:
        return (
            self.Direction.LeftToRight
            if self.get_direction() == "top_to_bottom"
            else self.Direction.TopToBottom
        )

    def _add_sub_layout(self):
        direction = self.get_sub_direction()
        layout = widgets.BoxLayout(direction)
        super().addLayout(layout)
        self.layouts.append(layout)

    def addWidget(self, widget: widgets.QWidget, **kwargs):
        if not self.layouts or self.layouts[-1].count() == self.row_nb:
            self._add_sub_layout()
        self.layouts[-1].add(widget, **kwargs)

    def addLayout(self, layout: widgets.QLayout):
        if not self.layouts or self.layouts[-1].count() == self.row_nb:
            self._add_sub_layout()
        self.layouts[-1].add(layout)

    def addItem(self, item):
        if not self.layouts or self.layouts[-1].count() == self.row_nb:
            self._add_sub_layout()
        self.layouts[-1].add(item)

    def get_items(self) -> listdelegators.BaseListDelegator[widgets.QLayoutItem]:
        items = [i.get_items() for i in self.layouts]
        return listdelegators.BaseListDelegator(itertools.chain(*items))

    def itemAt(self, idx: int) -> widgets.QLayoutItem | None:
        if len(self.layouts) == 0 or len(self.get_items()) == 0:
            raise IndexError(idx)
        # doesnt seem right?
        return None if idx == len(self.get_items()) else self.get_items()[idx]

    def takeAt(self, idx: int) -> widgets.QLayoutItem | None: # or 0 according to docs?
        layout_idx, item_idx = divmod(idx, len(self.layouts))
        layout = self.layouts[layout_idx]
        item = layout.takeAt(item_idx)
        for i, layout in enumerate(self.layouts[layout_idx:-1], start=layout_idx):
            item = self.layouts[i + 1].takeAt(0)
            layout.addItem(item)
        if len(self.layouts[-1]) == 0:
            super().takeAt(super().count() - 1)
        return item

    def count(self) -> int:
        return len(self.get_items())

    def indexOf(self, item: widgets.QLayoutItem) -> int:
        return self.get_items().index(item)


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.Widget()
    layout = MultiLineLayout(parent=widget)
    layout.addWidget(widgets.PushButton("Short"))
    layout.addWidget(widgets.PushButton("Longer"))
    layout.addWidget(widgets.PushButton("Different text"))
    layout.addWidget(widgets.PushButton("More text"))
    layout.addWidget(widgets.PushButton("Even longer button text"))
    layout.addWidget(widgets.PushButton("Even longer button text"))
    layout.addWidget(widgets.PushButton("Last one"))
    layout.takeAt(0)
    # layout.set_direction("left_to_right")
    # print(layout.items())
    # print(layout.itemAt(5))
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
