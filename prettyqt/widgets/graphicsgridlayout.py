from __future__ import annotations

from collections.abc import Iterable, Iterator

from prettyqt import constants, widgets
from prettyqt.utils import helpers, listdelegators


class GraphicsGridLayout(widgets.GraphicsLayoutMixin, widgets.QGraphicsGridLayout):
    """Grid layout for managing widgets in Graphics View."""

    def __getitem__(
        self, index: tuple[int | slice, int | slice] | int
    ) -> widgets.QGraphicsLayoutItem | None:
        rowcount = self.rowCount()
        colcount = self.columnCount()
        match index:
            case int() as row, int() as col:
                if row >= rowcount or col >= rowcount:
                    raise IndexError(index)
                return self.itemAt(row, col)
            case (row, col):
                items = [
                    item
                    for i, j in helpers.iter_positions(row, col, rowcount, colcount)
                    if (item := self.itemAt(i, j)) is not None
                ]
                return listdelegators.ListDelegator(list(set(items)))
            case int() as row:
                if row >= rowcount:
                    raise IndexError(index)
                return self.itemAt(row)
            case slice() as rowslice:
                count = rowcount if rowslice.stop is None else rowslice.stop
                items = [self.itemAt(i) for i in range(count)[rowslice]]
                return listdelegators.ListDelegator(list(set(item)))
            case str():
                return self.find_child(widgets.QGraphicsWidget, index)
            case _:
                raise TypeError(index)

    def __setitem__(
        self,
        idx: tuple[int | slice, int | slice],
        value: widgets.QGraphicsLayoutItem,
    ):
        row, col = idx
        rowspan = row.stop - row.start + 1 if isinstance(row, slice) else 1
        colspan = col.stop - col.start + 1 if isinstance(col, slice) else 1
        rowstart = row.start if isinstance(row, slice) else row
        colstart = col.start if isinstance(col, slice) else col
        self.add(value, rowstart, colstart, rowspan, colspan)

    def serialize_fields(self):
        items = []
        positions = []
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.itemAt(row, col)
                if item is not None:
                    items.append(item)
                    positions.append((row, col))
        return dict(widgets=items, positions=positions)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __setstate__(self, state):
        for item, pos in zip(state["widgets"], state["positions"]):
            x, y, w, h = pos
            self[x : x + w - 1, y : y + h - 1] = item

    def __iter__(self) -> Iterator[widgets.QWidget | widgets.QLayout]:
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __add__(
        self,
        other: (Iterable[widgets.QGraphicsLayoutItem] | widgets.QGraphicsLayoutItem),
    ):
        if isinstance(other, Iterable):
            for i, control in enumerate(other):
                self[self.rowCount(), i] = control
        else:
            self[self.rowCount(), 0 : self.columnCount() - 1] = other
        return self

    def add(
        self,
        item: widgets.QGraphicsLayoutItem,
        rowstart: int,
        colstart: int,
        rowspan: int = 1,
        colspan: int = 1,
    ):
        self.addItem(item, rowstart, colstart, rowspan, colspan)

    def append(self, item: widgets.QGraphicsLayoutItem):
        self[self.rowCount(), 0 : self.columnCount() - 1] = item

    def set_column_alignment(
        self, column: int, alignment: constants.AlignmentStr | constants.AlignmentFlag
    ):
        self.setColumnAlignment(column, constants.ALIGNMENTS.get_enum_value(alignment))

    def set_row_alignment(
        self, row: int, alignment: constants.AlignmentStr | constants.AlignmentFlag
    ):
        self.setRowAlignment(row, constants.ALIGNMENTS.get_enum_value(alignment))


if __name__ == "__main__":
    app = widgets.app()
    layout = GraphicsGridLayout()
    item = widgets.GraphicsProxyWidget()
    item.setWidget(widgets.RadioButton("Test"))
    item2 = widgets.GraphicsProxyWidget()
    item2.setWidget(widgets.RadioButton("Test"))
    layout[1, 5:6] = item
    layout += item2
    widget = widgets.GraphicsWidget()
    widget.set_layout(layout)
    scene = widgets.GraphicsScene()
    scene.add(widget)
    view = widgets.GraphicsView(scene)
    view.show()
    app.exec()
