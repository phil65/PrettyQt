# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

from prettyqt import widgets

MODES = dict(maximum=QtWidgets.QLayout.SetMaximumSize,
             fixed=QtWidgets.QLayout.SetFixedSize)

ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                  right=QtCore.Qt.AlignRight,
                  top=QtCore.Qt.AlignTop,
                  bottom=QtCore.Qt.AlignBottom)


class GridLayout(QtWidgets.QGridLayout):

    def __setitem__(self, idx, value):
        row, col = idx
        rowspan = row.stop - row.start + 1 if isinstance(row, slice) else 1
        colspan = col.stop - col.start + 1 if isinstance(col, slice) else 1
        rowstart = row.start if isinstance(row, slice) else row
        colstart = col.start if isinstance(col, slice) else col
        if isinstance(value, QtWidgets.QWidget):
            self.addWidget(value, rowstart, colstart, rowspan, colspan)
        else:
            self.addLayout(value, rowstart, colstart, rowspan, colspan)

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            return self.itemAtPosition(*idx)
        else:
            return self.itemAt(idx)

    def __iter__(self):
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __len__(self):
        return self.count()

    def set_size_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"{mode} not a valid size mode.")
        self.setSizeConstraint(MODES[mode])

    def set_alignment(self, alignment: str):
        if alignment not in ALIGNMENTS:
            raise ValueError(f"{alignment} not a valid alignment.")
        self.setAlignment(ALIGNMENTS[alignment])


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    layout = GridLayout()
    layout[1, 5:6] = widgets.RadioButton("1")
    layout[3:5, 7:8] = widgets.RadioButton("2")
    layout[3:5, 1:4] = widgets.RadioButton("3")
    widget = widgets.Widget()
    widget.setLayout(layout)
    widget.show()
    app.exec_()
