import itertools

from prettyqt import core, custom_widgets, widgets
from prettyqt.utils import listdelegators


class MultiLineLayout(widgets.BoxLayout):
    """Nested Boxlayout."""

    def __init__(self, vertical: bool = True, row_number: int = 3, **kwargs):
        self.row_nb = row_number
        self.layouts: list[
            widgets.BoxLayout
            | MultiLineLayout
            | widgets.GridLayout
            | custom_widgets.FlowLayout
            | widgets.StackedLayout
        ] = []
        self._sub_layout_type = "box"
        direction = self.Direction.TopToBottom if vertical else self.Direction.LeftToRight
        super().__init__(direction, **kwargs)

    def set_direction(
        self, direction: widgets.BoxLayout.Direction | widgets.boxlayout.DirectionStr
    ):
        super().set_direction(direction)
        direction = self.get_sub_direction()
        for layout in self.layouts:
            if isinstance(layout, widgets.BoxLayout):
                layout.set_direction(direction)

    def get_sub_direction(self) -> widgets.BoxLayout.Direction:
        return (
            self.Direction.LeftToRight
            if self.get_direction() == "top_to_bottom"
            else self.Direction.TopToBottom
        )

    def _add_sub_layout(self):
        match self._sub_layout_type:
            case "box":
                direction = self.get_sub_direction()
                layout = widgets.BoxLayout(direction)
            case "grid":
                layout = widgets.GridLayout()
            case "flow":
                layout = custom_widgets.FlowLayout()
            case "stacked":
                layout = widgets.StackedLayout()
            case "nested":
                direction = self.get_sub_direction()
                layout = MultiLineLayout(direction == self.Direction.TopToBottom)
        super().addLayout(layout)
        self.layouts.append(layout)

    def _add_to_sub_layout(self, item, **kwargs):
        if not self.layouts or self.layouts[-1].count() == self.row_nb:
            self._add_sub_layout()
        sub = self.layouts[-1]
        if isinstance(sub, widgets.GridLayout):
            idx = sub.count()
            row, col = (
                (0, idx)
                if self.get_sub_direction() == self.Direction.LeftToRight
                else (idx, 0)
            )
            sub.add(item, row, col, **kwargs)
        else:
            sub.add(item, **kwargs)

    def addWidget(self, widget: widgets.QWidget, **kwargs):
        self._add_to_sub_layout(widget, **kwargs)

    def addLayout(self, layout: widgets.QLayout):
        self._add_to_sub_layout(layout)

    def addItem(self, item):
        self._add_to_sub_layout(item)

    def get_items(self) -> listdelegators.ListDelegator[widgets.QLayoutItem]:
        items = [i.get_items() for i in self.layouts]
        return listdelegators.ListDelegator(itertools.chain(*items))

    def itemAt(self, idx: int) -> widgets.QLayoutItem | None:
        if len(self.layouts) == 0 or len(self.get_items()) == 0:
            raise IndexError(idx)
        # doesnt seem right?
        return None if idx == len(self.get_items()) else self.get_items()[idx]

    def takeAt(self, idx: int) -> widgets.QLayoutItem | None:  # or 0 according to docs?
        if idx < 0 or not self.layouts:
            return None
        layout_idx, item_idx = divmod(idx, self.row_nb)
        if layout_idx >= len(self.layouts):
            return None
        layout = self.layouts[layout_idx]
        item = layout.takeAt(item_idx)
        for i, sub_layout in enumerate(self.layouts[layout_idx:-1], start=layout_idx):
            next_item = self.layouts[i + 1].takeAt(0)
            if next_item is not None:
                sub_layout.addItem(next_item)
        if len(self.layouts[-1]) == 0:
            self.layouts.pop()
            super().takeAt(super().count() - 1)
        return item

    def count(self) -> int:
        return len(self.get_items())

    def indexOf(self, item: widgets.QLayoutItem) -> int:
        return self.get_items().index(item)

    def set_sub_layout_type(self, layout_type: str):
        self._sub_layout_type = layout_type

    def get_sub_layout_type(self) -> str:
        return self._sub_layout_type

    sub_layout_type = core.Property(
        str,
        get_sub_layout_type,
        set_sub_layout_type,
        doc="Layout for the sub layouts",
    )


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
    app.exec()
