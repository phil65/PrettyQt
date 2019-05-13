# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
import qtawesome as qta

from prettyqt import widgets

SELECTION_MODES = dict(single=QtWidgets.QAbstractItemView.SingleSelection,
                       extended=QtWidgets.QAbstractItemView.ExtendedSelection,
                       multi=QtWidgets.QAbstractItemView.MultiSelection,
                       none=QtWidgets.QAbstractItemView.NoSelection)


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
        return dict(items=self.get_children())

    def __setstate__(self, state):
        self.__init__()
        for item in state["items"]:
            self.addItem(item)

    def get_children(self):
        return [self.item(index) for index in range(self.count())]

    def set_selection_mode(self, mode: str):
        """set selection mode for given item view

        Allowed values are "single", "extended", "multi" or "none"

        Args:
            mode: selection mode to use

        Raises:
            ValueError: mode does not exist
        """
        if mode not in SELECTION_MODES:
            raise ValueError("Format must be either 'single', 'extended',"
                             "'multi' or 'None'")
        self.setSelectionMode(SELECTION_MODES[mode])

    def toggle_select_all(self):
        """
        select all items from list (deselect when all selected)
        """
        if self.selectionModel() is None:
            return None
        if self.selectionModel().hasSelection():
            self.clearSelection()
        else:
            self.selectAll()

    def add_item(self,
                 label: str,
                 data=None,
                 icon=None):
        item = widgets.ListWidgetItem(label)
        if icon is not None:
            if isinstance(icon, str):
                icon = qta.icon(icon)
            item.setIcon(icon)
        item.setData(QtCore.Qt.UserRole, data)
        self.addItem(item)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = ListWidget()
    widget.add_item("test", icon="mdi.timer")
    widget.add_item("test", icon="mdi.timer")
    widget.show()
    app.exec_()
