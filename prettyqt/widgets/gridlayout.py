# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class GridLayout(QtWidgets.QGridLayout):

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            item = self.itemAtPosition(*idx)
        else:
            item = self.itemAt(idx)
        widget = item.widget()
        if widget is None:
            widget = item.layout()
        return widget

    def __setitem__(self, idx, value):
        row, col = idx
        rowspan = row.stop - row.start + 1 if isinstance(row, slice) else 1
        colspan = col.stop - col.start + 1 if isinstance(col, slice) else 1
        rowstart = row.start if isinstance(row, slice) else row
        colstart = col.start if isinstance(col, slice) else col
        self.add_item(value, rowstart, colstart, rowspan, colspan)

    def __getstate__(self):
        widgets = []
        positions = []
        for i, item in enumerate(list(self)):
            widgets.append(item)
            positions.append(self.getItemPosition(i))
        return dict(widgets=widgets, positions=positions)

    def __setstate__(self, state):
        self.__init__()
        for i, (item, pos) in enumerate(zip(state["widgets"], state["positions"])):
            x, y, w, h = pos
            self[x:x + w - 1, y:y + h - 1] = item

    def __iter__(self):
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __len__(self):
        return self.count()

    def __add__(self, other):
        self[self.rowCount(), 0:self.columnCount()] = other
        return self

    def add_item(self, item, rowstart, colstart, rowspan=1, colspan=1):
        fn = self.addWidget if isinstance(item, QtWidgets.QWidget) else self.addLayout
        fn(item, rowstart, colstart, rowspan, colspan)


GridLayout.__bases__[0].__bases__ = (widgets.Layout,)


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
    print(layout)
    widget.show()
    app.exec_()
