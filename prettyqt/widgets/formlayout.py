# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets

from prettyqt import widgets

ROLES = bidict(dict(left=QtWidgets.QFormLayout.LabelRole,
                    right=QtWidgets.QFormLayout.FieldRole,
                    both=QtWidgets.QFormLayout.SpanningRole))


class FormLayout(QtWidgets.QFormLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_mode("maximum")
        self.setVerticalSpacing(8)

    def __getitem__(self, index):
        item = self.itemAt(index)
        widget = item.widget()
        if widget is None:
            widget = item.layout()
        return widget

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
        if isinstance(other, (QtWidgets.QWidget, QtWidgets.QLayout)):
            self.addRow(other)
            return self
        if isinstance(other, tuple):
            self.addRow(*other)
            return self

    def __getstate__(self):
        widgets = []
        positions = []
        for i, item in enumerate(list(self)):
            widgets.append(item)
            positions.append(self.get_item_pos(i))
        return dict(widgets=widgets, positions=positions)

    def __setstate__(self, state):
        self.__init__()
        for i, (item, pos) in enumerate(zip(state["widgets"], state["positions"])):
            self.set_widget(item, pos[0], pos[1])

    def set_widget(self, widget, row, role: str = "both"):
        if isinstance(widget, str):
            widget = widgets.Label(widget)
        if isinstance(widget, QtWidgets.QLayout):
            self.setLayout(row, ROLES[role], widget)
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
    def from_dict(cls, dct, parent=None):
        formlayout = cls(parent)
        for i, (k, v) in enumerate(dct.items(), start=1):
            if k is not None:
                formlayout[i, "left"] = k
            if v is not None:
                formlayout[i, "right"] = v
        return formlayout


FormLayout.__bases__[0].__bases__ = (widgets.Layout,)


if __name__ == "__main__":
    app = widgets.app()
    dct = {"key": widgets.Label("test"),
           None: widgets.Label("test 2")}
    layout = FormLayout.from_dict(dct)
    layout[3] = "hellooo"
    widget = widgets.Widget()
    widget.setLayout(layout)
    widget.show()
    app.exec_()
