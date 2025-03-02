from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import constants, widgets
from prettyqt.utils import helpers, listdelegators


if TYPE_CHECKING:
    from collections.abc import Iterator


class GridLayout(widgets.LayoutMixin, widgets.QGridLayout):
    """Lays out widgets in a grid."""

    ID = "grid"

    def __getitem__(
        self, index: tuple[int | slice, int | slice] | int | str
    ) -> (
        widgets.QWidget
        | widgets.QLayout
        | listdelegators.ListDelegator[widgets.QWidget | widgets.QLayout]
        | None
    ):
        rowcount = self.rowCount()
        colcount = self.columnCount()
        match index:
            case int() as row, int() as col:
                if row < 0:
                    row = rowcount + row
                if col < 0:
                    col = colcount + col
                if row >= rowcount or row < 0 or col >= colcount or col < 0:
                    raise IndexError(index)
                item = self.itemAtPosition(row, col)
                return i if (i := item.widget()) is not None else item.layout()
            case (row, col):
                items = [
                    item
                    for i, j in helpers.iter_positions(row, col, rowcount, colcount)
                    if (item := self.itemAtPosition(i, j)) is not None
                ]
                items = [
                    w if (w := i.widget()) is not None else i.layout() for i in items
                ]
                return listdelegators.ListDelegator(list(set(items)))
            case int() as row:
                if row < 0:
                    row = rowcount + row
                if row >= rowcount or row < 0:
                    raise IndexError(index)
                item = self.itemAt(row)
                return i if (i := item.widget()) is not None else item.layout()
            case slice() as rowslice:
                count = rowcount if rowslice.stop is None else rowslice.stop
                items = [self.itemAt(i) for i in range(count)[rowslice]]
                items = [
                    w if (w := i.widget()) is not None else i.layout() for i in items
                ]
                return listdelegators.ListDelegator(list(set(items)))
            case str():
                return self.find_child(widgets.QWidget | widgets.QLayout, index)
            case _:
                raise TypeError(index)

    def __setitem__(
        self,
        idx: tuple[int | slice, int | slice],
        value: widgets.QWidget | widgets.QLayout | widgets.QLayoutItem,
    ):
        row, col = idx
        rowspan = row.stop - row.start + 1 if isinstance(row, slice) else 1
        colspan = col.stop - col.start + 1 if isinstance(col, slice) else 1
        rowstart = row.start if isinstance(row, slice) else row
        colstart = col.start if isinstance(col, slice) else col
        self.add(value, rowstart, colstart, rowspan, colspan)

    # def __setstate__(self, state):
    #     for item, pos in zip(state["widgets"], state["positions"]):
    #         x, y, w, h = pos
    #         self[x : x + w - 1, y : y + h - 1] = item

    # def __reduce__(self):
    #     return type(self), (), self.__getstate__()

    def __iter__(self) -> Iterator[widgets.QWidget | widgets.QLayout]:
        return iter(
            item for i in range(self.count()) if (item := self.itemAt(i)) is not None
        )

    def __add__(
        self,
        other: (tuple | list | widgets.QWidget | widgets.QLayout | widgets.QLayoutItem),
    ):
        if isinstance(other, tuple | list):
            for i, _control in enumerate(other):
                self[self.rowCount(), i] = other  # type: ignore
        else:
            self[self.rowCount(), 0 : self.columnCount() - 1] = other
        return self

    def __iadd__(self, item, *args, **kwargs):
        self.__add__(item, *args, **kwargs)
        return self

    def add(
        self,
        item: widgets.QWidget | widgets.QLayout | widgets.QLayoutItem,
        rowstart: int,
        colstart: int,
        rowspan: int = 1,
        colspan: int = 1,
        alignment: constants.AlignmentStr | constants.AlignmentFlag | None = None,
    ):
        if alignment is None:
            alignment = "none"
        flag = constants.ALIGNMENTS.get_enum_value(alignment)
        match item:
            case widgets.QWidget():
                self.addWidget(item, rowstart, colstart, rowspan, colspan, flag)
            case widgets.QLayout():
                self.addLayout(item, rowstart, colstart, rowspan, colspan, flag)
            case widgets.QLayoutItem():
                self.addItem(item, rowstart, colstart, rowspan, colspan, flag)

    def append(self, item: widgets.QWidget | widgets.QLayout | widgets.QLayoutItem):
        self[self.rowCount(), 0 : self.columnCount() - 1] = item

    def set_origin_corner(self, corner: constants.CornerStr | constants.Corner):
        """Set the origin corner.

        Args:
            corner: origin corner
        """
        self.setOriginCorner(constants.CORNER.get_enum_value(corner))

    def get_origin_corner(self) -> constants.CornerStr:
        """Return current origin corner.

        Returns:
            origin corner
        """
        return constants.CORNER.inverse[self.originCorner()]


if __name__ == "__main__":
    app = widgets.app()
    layout = GridLayout()
    layout[1, 5:6] = widgets.RadioButton("1 2 3 jk jkjl j kföldsjfköj")
    layout[3:5, 7:8] = widgets.RadioButton("2")
    layout[3:5, 1:4] = widgets.RadioButton("3")
    layout += widgets.RadioButton("3")
    layout += widgets.RadioButton("4")
    widget = widgets.Widget()
    widget.set_layout(layout)
    widget.show()
    app.exec()
