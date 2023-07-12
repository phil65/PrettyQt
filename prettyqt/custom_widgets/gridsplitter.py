from __future__ import annotations

import logging

from prettyqt import constants, widgets
from prettyqt.utils import helpers, listdelegators


logger = logging.getLogger(__name__)


class GridSplitter(widgets.Splitter):
    """Nested Splitter which keeps sections in sync.

    Currently only works properly if it is a proper grid.
    In future, this could be expanded to work with spans.
    """

    def __init__(self, **kwargs):
        self.sub_splitters = []
        super().__init__(constants.VERTICAL, **kwargs)

    def __getitem__(
        self, index: tuple[int | slice, int | slice] | int | str
    ) -> widgets.QWidget | listdelegators.ListDelegator[widgets.QWidget] | None:
        rowcount = self.rowCount()
        colcount = self.columnCount()
        match index:
            case int() as row, int() as col:
                if row >= rowcount or col >= colcount:
                    raise IndexError(index)
                return self.itemAtPosition(row, col)
            case (row, col):
                items = [
                    item
                    for i, j in helpers.iter_positions(row, col, rowcount, colcount)
                    if (item := self.itemAtPosition(i, j)) is not None
                ]
                return listdelegators.ListDelegator(list(set(items)))
            case int() as row:
                if row >= rowcount:
                    raise IndexError(index)
                return self.itemAt(row)
            case slice() as rowslice:
                count = rowcount if rowslice.stop is None else rowslice.stop
                items = [self.itemAt(i) for i in range(count)[rowslice]]
                return listdelegators.ListDelegator(list(set(items)))
            case str():
                return self.find_child(widgets.QWidget, index)
            case _:
                raise TypeError(index)

    def rowCount(self) -> int:
        return len(self.sub_splitters)

    def columnCount(self) -> int:
        return max(splitter.count() for splitter in self.sub_splitters)

    def itemAtPosition(self, row: int, col: int) -> widgets.QWidget:
        return self.sub_splitters[row].widget(col)

    def itemAt(self, row: int) -> widgets.QWidget:
        widgets = [w for s in self.sub_splitters for w in s.get_widgets()]
        return widgets[row]

    def __setitem__(
        self,
        idx: tuple[int, int],
        widget: widgets.QWidget,
    ):
        row, col = idx
        self.add(widget, row, col)

    def add(self, widget: widgets.QWidget, row: int, column: int):
        while len(self.sub_splitters) <= row:
            self._add_sub_splitter()
        splitter = self.sub_splitters[row]
        if len(splitter) > column:
            splitter.replaceWidget(column, widget)
        else:
            splitter.add(widget)
        # self.align_sizes()

    def _add_sub_splitter(self):
        splitter = widgets.Splitter(constants.HORIZONTAL)
        super().add(splitter)
        splitter.splitterMoved.connect(self._align_sizes)
        self.sub_splitters.append(splitter)

    def _on_handle_move(self, position: int, index: int):
        logger.debug(f"{position=} {index=}")
        sender = self.sender()
        receivers = [splitter for splitter in self.sub_splitters if splitter != sender]
        for rec in receivers:
            handle = rec.handle(index)
            if handle is not None:
                with rec.signals_blocked():
                    handle.moveSplitter(position)

    def show(self):
        super().show()
        # self.align_sizes()

    def _align_sizes(self):
        self.refresh()
        sizes = [splitter.sizes() for splitter in self.sub_splitters]
        max_sizes = [max(i) for i in zip(*sizes)]
        for splitter in self.sub_splitters:
            # for i, w in enumerate(splitter.get_widgets()):
            #     if i < len(max_sizes):
            #         w.resize(max_sizes[i], w.height())
            splitter.setSizes(max_sizes[: splitter.count()])


if __name__ == "__main__":
    app = widgets.app()
    splitter = GridSplitter()
    splitter.resize(500, 500)
    with app.debug_mode():
        splitter[0, 0] = widgets.Label("0, 0")
        splitter[0, 1] = widgets.Label("0, 1")
        # splitter[0, 2] = widgets.Label("0, 2")
        splitter[1, 0] = widgets.Label("1, 0")
        splitter[1, 1] = widgets.Label("1, 1")
        splitter[2, 0] = widgets.Label("2, 0")
        splitter[2, 1] = widgets.Label("2, 1")
        splitter.show()
        app.exec()
