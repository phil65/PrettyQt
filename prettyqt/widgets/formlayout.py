# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets

MODES = dict(maximum=QtWidgets.QLayout.SetMaximumSize,
             fixed=QtWidgets.QLayout.SetFixedSize)

ROLES = dict(left=QtWidgets.QFormLayout.LabelRole,
             right=QtWidgets.QFormLayout.FieldRole,
             both=QtWidgets.QFormLayout.SpanningRole)


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

    def __iter__(self):
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __len__(self):
        """needed for PySide2
        """
        return self.rowCount()

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
            self.set_widget(item, pos[0], pos[1])

    def set_size_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"{mode} not a valid size mode.")
        self.setSizeConstraint(MODES[mode])

    def set_label_widget(self, row: int, widget):
        """set a widget for the label position at given row

        Args:
            row: Row offset
            widget: widget to get added to layout
        """
        self.set_widget(widget, row, "left")

    def set_field_widget(self, row: int, widget):
        """set a widget for the field position at given row

        Args:
            row: Row offset
            widget: widget / layout to get added to layout
        """
        self.set_widget(widget, row, "right")

    def set_spanning_widget(self, row: int, widget):
        """set a widget spanning label and field position at given row

        Args:
            row: Row offset
            widget: widget / layout to get added to layout
        """
        self.set_widget(widget, row, "both")

    def set_widget(self, widget, row, role: str = "both"):
        if isinstance(widget, str):
            widget = widgets.Label(widget)
        if isinstance(widget, QtWidgets.QLayout):
            self.setLayout(row, self.SpanningRole, widget)
        else:
            self.setWidget(row, self.SpanningRole, widget)

    def get_widget(self, row: int, role: str = "both"):
        item = self.itemAt(row, ROLES[role])
        widget = item.widget()
        if widget is None:
            widget = item.layout()
        return widget

    @classmethod
    def from_dict(cls, dct, parent=None):
        formlayout = FormLayout(parent)
        for i, (k, v) in enumerate(dct.items(), start=1):
            if k is not None:
                formlayout.set_label_widget(i, k)
            if v is not None:
                formlayout.set_field_widget(i, v)
        return formlayout


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    dct = {"key": widgets.Label("test"),
           None: widgets.Label("test 2")}
    layout = FormLayout.from_dict(dct)
    layout.set_spanning_widget(3, "hallo")
    print(layout.get_widget(3, role="both"))
    widget = widgets.Widget()
    widget.setLayout(layout)
    widget.show()
    app.exec_()
