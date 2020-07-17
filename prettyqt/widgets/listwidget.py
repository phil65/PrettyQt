# -*- coding: utf-8 -*-
"""
"""

from typing import Union, Iterable, Mapping, List, Any

from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets

SCROLL_HINTS = widgets.abstractitemview.SCROLL_HINTS  # type: ignore

QtWidgets.QListWidget.__bases__ = (widgets.ListView,)


class NoData(object):
    pass


class ListWidget(QtWidgets.QListWidget):

    value_changed = core.Signal(object)

    def __init__(self, parent=None, selection_mode: str = "single"):
        super().__init__(parent)
        self.itemSelectionChanged.connect(self.on_index_change)
        self.set_selection_mode(selection_mode)

    def __repr__(self):
        return f"ListWidget: {self.count()} items"

    def __getitem__(self, row: int):
        return self.item(row)

    def __add__(self, other):
        if isinstance(other, QtWidgets.QListWidgetItem):
            self.addItem(other)
            return self

    def __iter__(self):
        return iter(self.get_children())

    def __len__(self):
        return self.count()

    def __getstate__(self):
        return dict(
            items=self.get_children(),
            selection_mode=self.get_selection_mode(),
            sorting_enabled=self.isSortingEnabled(),
            current_row=self.currentRow(),
        )

    def __setstate__(self, state):
        self.__init__()
        self.set_selection_mode(state["selection_mode"])
        self.setSortingEnabled(state["sorting_enabled"])
        self.setCurrentRow(state["current_row"])
        for item in state["items"]:
            self.addItem(item)

    def sort(self, reverse: bool = False):
        order = QtCore.Qt.DescendingOrder if reverse else QtCore.Qt.AscendingOrder
        self.sortItems(order)

    def on_index_change(self):
        data = self.get_value()
        self.value_changed.emit(data)

    def get_children(self) -> list:
        return [self.item(row) for row in range(self.count())]

    def add_items(self, items: Union[Iterable, Mapping]):
        if isinstance(items, Mapping):
            for k, v in items.items():
                self.add(v, k)
        else:
            for i in items:
                if isinstance(i, (tuple, list)):
                    self.add(*i)
                else:
                    self.add(i)

    def add(self, label: str, data=NoData, icon: gui.icon.IconType = None):
        if data is NoData:
            data = label
        item = widgets.ListWidgetItem(label)
        item.set_icon(icon)
        item.setData(QtCore.Qt.UserRole, data)
        self.addItem(item)

    def get_value(self) -> List[Any]:
        return [i.data(QtCore.Qt.UserRole) for i in self.selectedItems()]

    def set_value(self, value):
        for i in self.get_children():
            if i.data(QtCore.Qt.UserRole) in value:
                self.setCurrentItem(i)
                break

    def scroll_to_item(self, item, mode: str = "ensure_visible"):
        if mode not in SCROLL_HINTS:
            raise ValueError("Invalid scroll mode")
        self.scrollToItem(item, SCROLL_HINTS[mode])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ListWidget()
    widget.add("test", icon="mdi.timer")
    widget.add("test", icon="mdi.timer")
    widget.show()
    app.exec_()
