# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

from prettyqt import widgets


QtWidgets.QListWidget.__bases__ = (widgets.ListView,)


class NoData(object):
    pass


class ListWidget(QtWidgets.QListWidget):

    def __repr__(self):
        return f"ListWidget: {self.count()} children"

    def __getitem__(self, index):
        return self.item(index)

    def __add__(self, other):
        if isinstance(other, QtWidgets.QListWidgetItem):
            self.addItem(other)
            return self

    def __iter__(self):
        return iter(self.get_children())

    def __len__(self):
        return self.count()

    def __getstate__(self):
        return dict(items=self.get_children(),
                    selection_mode=self.get_selection_mode(),
                    sorting_enabled=self.isSortingEnabled(),
                    current_row=self.currentRow())

    def __setstate__(self, state):
        self.__init__()
        self.set_selection_mode(state["selection_mode"])
        self.setSortingEnabled(state["sorting_enabled"])
        self.setCurrentRow(state["current_row"])
        for item in state["items"]:
            self.addItem(item)

    def get_children(self):
        return [self.item(index) for index in range(self.count())]

    def add_items(self, items):
        for i in items:
            if isinstance(i, (tuple, list)):
                self.add(*i)
            else:
                self.add(i)

    def add(self,
            label: str,
            data=NoData,
            icon=None):
        if data is NoData:
            data = label
        item = widgets.ListWidgetItem(label)
        item.set_icon(icon)
        item.setData(QtCore.Qt.UserRole, data)
        self.addItem(item)

    def get_value(self):
        return [i.data(QtCore.Qt.UserRole) for i in self.selectedItems()]

    def set_value(self, value):
        for i in self.get_children():
            if i.data(QtCore.Qt.UserRole) in value:
                self.setSelected(i)
                break


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ListWidget()
    widget.add("test", icon="mdi.timer")
    widget.add("test", icon="mdi.timer")
    widget.show()
    app.exec_()
