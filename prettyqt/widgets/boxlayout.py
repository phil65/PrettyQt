# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets

QtWidgets.QBoxLayout.__bases__ = (widgets.Layout,)


class BoxLayout(QtWidgets.QBoxLayout):

    def __init__(self, orientation="horizontal", parent=None, margin=None):
        o = self.TopToBottom if orientation == "vertical" else self.LeftToRight
        super().__init__(o, parent)
        if margin is not None:
            self.set_margin(margin)

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
            self.add(item)

    def __iter__(self):
        return iter(self.get_children())

    def __len__(self):
        return self.count()

    def __add__(self, other):
        if isinstance(other, (QtWidgets.QWidget, QtWidgets.QLayout)):
            self.add(other)
            return self

    def add(self, *item):
        for i in item:
            if isinstance(i, QtWidgets.QWidget):
                self.addWidget(i)
            else:
                self.addLayout(i)

    def get_children(self):
        return [self[i] for i in range(self.count())]

    def add_stretch(self, stretch: int = 0):
        self.addStretch(stretch)

    def add_spacing(self, size: int):
        self.addSpacing(size)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    layout = BoxLayout("vertical")
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    layout += widget2
    widget.set_layout(layout)
    widget.show()
    app.exec_()
