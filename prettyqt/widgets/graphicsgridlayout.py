from __future__ import annotations

from collections.abc import Iterable

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


QtWidgets.QGraphicsGridLayout.__bases__ = (widgets.GraphicsLayout,)


class GraphicsGridLayout(QtWidgets.QGraphicsGridLayout):
    def __getitem__(
        self, idx: tuple[int, int] | int
    ) -> QtWidgets.QGraphicsLayoutItem | None:
        if isinstance(idx, tuple):
            return self.itemAt(*idx)
        else:
            return self.itemAt(idx)

    def __setitem__(
        self,
        idx: tuple[int | slice, int | slice],
        value: QtWidgets.QGraphicsLayoutItem,
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
        for i, (item, pos) in enumerate(zip(state["widgets"], state["positions"])):
            x, y, w, h = pos
            self[x : x + w - 1, y : y + h - 1] = item

    def __iter__(self):
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __add__(
        self,
        other: (Iterable[QtWidgets.QGraphicsLayoutItem] | QtWidgets.QGraphicsLayoutItem),
    ):
        if isinstance(other, Iterable):
            for i, control in enumerate(other):
                self[self.rowCount(), i] = control
        else:
            self[self.rowCount(), 0 : self.columnCount() - 1] = other
        return self

    def add(
        self,
        item: QtWidgets.QGraphicsLayoutItem,
        rowstart: int,
        colstart: int,
        rowspan: int = 1,
        colspan: int = 1,
    ):
        self.addItem(item, rowstart, colstart, rowspan, colspan)

    def append(self, item: QtWidgets.QGraphicsLayoutItem):
        self[self.rowCount(), 0 : self.columnCount() - 1] = item

    def set_column_alignment(self, column: int, alignment: constants.AlignmentStr):
        if alignment not in constants.ALIGNMENTS:
            raise InvalidParamError(alignment, constants.ALIGNMENTS)
        self.setColumnAlignment(column, constants.ALIGNMENTS[alignment])

    def set_row_alignment(self, row: int, alignment: constants.AlignmentStr):
        if alignment not in constants.ALIGNMENTS:
            raise InvalidParamError(alignment, constants.ALIGNMENTS)
        self.setRowAlignment(row, constants.ALIGNMENTS[alignment])


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
    app.main_loop()
