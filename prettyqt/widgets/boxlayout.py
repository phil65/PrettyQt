# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

MODES = dict(maximum=QtWidgets.QLayout.SetMaximumSize,
             fixed=QtWidgets.QLayout.SetFixedSize)

ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                  right=QtCore.Qt.AlignRight,
                  top=QtCore.Qt.AlignTop,
                  bottom=QtCore.Qt.AlignBottom)


class BoxLayout(QtWidgets.QBoxLayout):

    def __init__(self, orientation="horizontal", parent=None):
        o = self.TopToBottom if orientation == "vertical" else self.LeftToRight
        super().__init__(o, parent)

    def __repr__(self):
        return f"BoxLayout: {self.count()} children"

    def __getitem__(self, index):
        item = self.itemAt(index)
        widget = item.widget()
        if widget is None:
            widget = item.layout()
        return widget

    def __getstate__(self):
        return dict(items=self.get_children(),
                    direction=int(self.direction()))

    def __setstate__(self, state):
        self.__init__()
        direction = self.Direction(state["direction"])
        self.setDirection(direction)
        for item in state["items"]:
            self.add_item(item)

    def __iter__(self):
        return iter(self.get_children())

    def __len__(self):
        return self.count()

    def __add__(self, other):
        if isinstance(other, (QtWidgets.QWidget, QtWidgets.QLayout)):
            self.add_item(other)
            return self

    def add_item(self, item):
        if isinstance(item, QtWidgets.QWidget):
            self.addWidget(item)
        else:
            self.addLayout(item)

    def get_children(self):
        return [self[i] for i in range(self.count())]

    def set_size_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"{mode} not a valid size mode.")
        self.setSizeConstraint(MODES[mode])

    def set_alignment(self, alignment: str):
        if alignment not in ALIGNMENTS:
            raise ValueError(f"{alignment} not a valid alignment.")
        self.setAlignment(ALIGNMENTS[alignment])

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    layout = BoxLayout("vertical")
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    layout += widget2
    widget.setLayout(layout)
    widget.show()
    app.exec_()
