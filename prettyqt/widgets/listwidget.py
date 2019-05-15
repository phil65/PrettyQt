# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
import qtawesome as qta

from prettyqt import widgets


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

    def add_item(self,
                 label: str,
                 data=None,
                 icon=None):
        if data is None:
            data = label
        item = widgets.ListWidgetItem(label)
        if icon is not None:
            if isinstance(icon, str):
                icon = qta.icon(icon)
            item.setIcon(icon)
        item.setData(QtCore.Qt.UserRole, data)
        self.addItem(item)


ListWidget.__bases__[0].__bases__ = (widgets.ListView,)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = ListWidget()
    widget.add_item("test", icon="mdi.timer")
    widget.add_item("test", icon="mdi.timer")
    widget.show()
    app.exec_()
