# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

MODES = dict(maximum=QtWidgets.QLayout.SetMaximumSize,
             fixed=QtWidgets.QLayout.SetFixedSize)


class StackedLayout(QtWidgets.QStackedLayout):

    def __getitem__(self, index):
        item = self.itemAt(index)
        widget = item.widget()
        if widget is None:
            widget = item.layout()
        return widget

    def __getstate__(self):
        return dict(items=self.get_children())

    def __setstate__(self, state):
        self.__init__()
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

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    layout = StackedLayout()
    widget = widgets.Widget()
    widget2 = widgets.RadioButton("Test")
    widget3 = widgets.RadioButton("Test 2")
    layout += widget2
    layout += widget3
    widget.setLayout(layout)
    widget.show()
    app.exec_()
