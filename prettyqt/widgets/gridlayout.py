from __future__ import annotations

from collections.abc import Iterator

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError


class GridLayout(widgets.LayoutMixin, QtWidgets.QGridLayout):
    ID = "grid"

    def __getitem__(
        self, idx: tuple[int, int] | int | str
    ) -> QtWidgets.QWidget | QtWidgets.QLayout | None:
        match idx:
            case (int(), int()):
                item = self.itemAtPosition(*idx)
            case int():
                item = self.itemAt(idx)
            case str():
                return self.find_child(QtCore.QObject, idx)
            case _:
                raise TypeError(idx)
        return item.widget() if item.widget() is not None else item.layout()

    def __setitem__(
        self,
        idx: tuple[int | slice, int | slice],
        value: QtWidgets.QWidget | QtWidgets.QLayout | QtWidgets.QLayoutItem,
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

    def __iter__(self) -> Iterator[QtWidgets.QWidget | QtWidgets.QLayout]:
        return iter(item for i in range(self.count()) if (item := self[i]) is not None)

    def __add__(
        self,
        other: (
            tuple | list | QtWidgets.QWidget | QtWidgets.QLayout | QtWidgets.QLayoutItem
        ),
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
        item: QtWidgets.QWidget | QtWidgets.QLayout | QtWidgets.QLayoutItem,
        rowstart: int,
        colstart: int,
        rowspan: int = 1,
        colspan: int = 1,
        alignment: constants.AlignmentStr | None = None,
    ):
        flag = constants.ALIGNMENTS[alignment or "none"]
        match item:
            case QtWidgets.QWidget():
                self.addWidget(item, rowstart, colstart, rowspan, colspan, flag)
            case QtWidgets.QLayout():
                self.addLayout(item, rowstart, colstart, rowspan, colspan, flag)
            case QtWidgets.QLayoutItem():
                self.addItem(item, rowstart, colstart, rowspan, colspan, flag)

    def append(self, item: QtWidgets.QWidget | QtWidgets.QLayout | QtWidgets.QLayoutItem):
        self[self.rowCount(), 0 : self.columnCount() - 1] = item

    def set_origin_corner(self, corner: constants.CornerStr):
        """Set the origin corner.

        Args:
            corner: origin corner

        Raises:
            InvalidParamError: corner does not exist
        """
        if corner not in constants.CORNER:
            raise InvalidParamError(corner, constants.CORNER)
        self.setOriginCorner(constants.CORNER[corner])

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
    app.main_loop()
