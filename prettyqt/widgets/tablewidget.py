from __future__ import annotations

from prettyqt import constants, core, widgets


class TableWidgetMixin(widgets.TableViewMixin):
    def __getitem__(self, index: tuple[int, int]) -> widgets.QTableWidgetItem:
        item = self.item(*index)
        if item is None:
            raise KeyError(index)
        return item

    def __setitem__(self, index: tuple[int, int], value: widgets.QTableWidgetItem):
        self.setItem(index[0], index[1], value)

    def __delitem__(self, index: tuple[int, int]):
        self.takeItem(*index)

    def sort(self, column: int = 0, reverse: bool = False):
        order = constants.DESCENDING if reverse else constants.ASCENDING
        self.sortItems(column, order)

    def openPersistentEditor(self, index: core.ModelIndex | widgets.QTableWidgetItem):
        if isinstance(index, core.ModelIndex):
            index = self.itemFromIndex(index)
        super().openPersistentEditor(index)

    def closePersistentEditor(self, index: core.ModelIndex | widgets.QTableWidgetItem):
        if isinstance(index, core.ModelIndex):
            index = self.itemFromIndex(index)
        super().closePersistentEditor(index)

    def isPersistentEditorOpen(
        self, index: core.ModelIndex | widgets.QTableWidgetItem
    ) -> bool:
        if isinstance(index, core.ModelIndex):
            index = self.itemFromIndex(index)
        return super().isPersistentEditorOpen(index)

    def scroll_to_item(
        self,
        item: widgets.QTableWidgetItem,
        scroll_hint: widgets.abstractitemview.ScrollHintStr = "ensure_visible",
    ):
        self.scrollToItem(item, widgets.abstractitemview.SCROLL_HINT[scroll_hint])


class TableWidget(TableWidgetMixin, widgets.QTableWidget):
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
