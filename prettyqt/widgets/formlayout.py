# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


ROLES = bidict(
    left=QtWidgets.QFormLayout.LabelRole,
    right=QtWidgets.QFormLayout.FieldRole,
    both=QtWidgets.QFormLayout.SpanningRole,
)


QtWidgets.QFormLayout.__bases__ = (widgets.Layout,)


class FormLayout(QtWidgets.QFormLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_mode("maximum")
        self.setVerticalSpacing(8)

    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            row = index[0]
            role = index[1]
        else:
            row = index
            role = "both"
        self.set_widget(value, row, role)

    def __iter__(self):
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __len__(self):
        """needed for PySide2
        """
        return self.rowCount()

    def __add__(self, other):
        if isinstance(other, (QtWidgets.QWidget, QtWidgets.QLayout, tuple)):
            self.add(other)
            return self
        raise TypeError("Wrong type for addition")

    def __getstate__(self):
        widget_list = []
        positions = []
        for i, item in enumerate(list(self)):
            widget_list.append(item)
            positions.append(self.get_item_pos(i))
        return dict(widgets=widget_list, positions=positions)

    def __setstate__(self, state):
        self.__init__()
        for i, (item, pos) in enumerate(zip(state["widgets"], state["positions"])):
            self.set_widget(item, pos[0], pos[1])

    def set_widget(self, widget, row, role: str = "both"):
        if isinstance(widget, str):
            widget = widgets.Label(widget)
        if isinstance(widget, QtWidgets.QLayout):
            self.set_layout(row, ROLES[role], widget)
        else:
            self.setWidget(row, ROLES[role], widget)

    def get_widget(self, row: int, role: str = "both"):
        item = self.itemAt(row, ROLES[role])
        widget = item.widget()
        if widget is None:
            widget = item.layout()
        return widget

    def get_item_pos(self, index):
        pos = self.getItemPosition(index)
        return pos[0], ROLES.inv[pos[1]]

    @classmethod
    def build_from_dict(cls, dct, parent=None):
        formlayout = cls(parent)
        for i, (k, v) in enumerate(dct.items(), start=1):
            if k is not None:
                formlayout.set_widget(k, i, "left")
            if v is not None:
                formlayout.set_widget(v, i, "right")
        return formlayout

    def add(self, *items):
        for i in items:
            if isinstance(i, (QtWidgets.QWidget, QtWidgets.QLayout)):
                self.addRow(i)
            if isinstance(i, tuple):
                self.addRow(*i)


if __name__ == "__main__":
    app = widgets.app()
    dct = {"key": widgets.Label("test"), None: widgets.Label("test 2")}
    layout = FormLayout.build_from_dict(dct)
    layout[3] = "hellooo"
    w = widgets.Widget()
    w.set_layout(layout)
    w.show()
    app.exec_()
