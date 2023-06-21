from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets


class TableWidgetMixin(widgets.TableViewMixin):
    def __getitem__(self, index: tuple[int, int]) -> QtWidgets.QTableWidgetItem:
        item = self.item(*index)
        if item is None:
            raise KeyError(index)
        return item

    def __setitem__(self, index: tuple[int, int], value: QtWidgets.QTableWidgetItem):
        self.setItem(index[0], index[1], value)

    def __delitem__(self, index: tuple[int, int]):
        self.takeItem(*index)

    def sort(self, column: int = 0, reverse: bool = False):
        order = constants.DESCENDING if reverse else constants.ASCENDING
        self.sortItems(column, order)

    def openPersistentEditor(
        self, index: QtCore.QModelIndex | QtWidgets.QTableWidgetItem
    ):
        if isinstance(index, QtCore.QModelIndex):
            index = self.itemFromIndex(index)
        super().openPersistentEditor(index)

    def closePersistentEditor(
        self, index: QtCore.QModelIndex | QtWidgets.QTableWidgetItem
    ):
        if isinstance(index, QtCore.QModelIndex):
            index = self.itemFromIndex(index)
        super().closePersistentEditor(index)

    def isPersistentEditorOpen(
        self, index: QtCore.QModelIndex | QtWidgets.QTableWidgetItem
    ) -> bool:
        if isinstance(index, QtCore.QModelIndex):
            index = self.itemFromIndex(index)
        return super().isPersistentEditorOpen(index)

    def scroll_to_item(
        self,
        item: QtWidgets.QTableWidgetItem,
        scroll_hint: widgets.abstractitemview.ScrollHintStr = "ensure_visible",
    ):
        self.scrollToItem(item, widgets.abstractitemview.SCROLL_HINT[scroll_hint])


class TableWidget(TableWidgetMixin, QtWidgets.QTableWidget):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = TableWidget()
    widget.setHorizontalHeaderLabels(["testus"])
    widget.setColumnCount(1)
    widget.insertRow(0)
    widget[0, 0] = widgets.TableWidgetItem("test")
    widget.show()
    app.exec()
