from typing import Any, Iterable, Iterator, List, Mapping, Optional, Union

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import InvalidParamError


QtWidgets.QListWidget.__bases__ = (widgets.ListView,)


class NoData:
    pass


class ListWidget(QtWidgets.QListWidget):

    value_changed = core.Signal(object)

    def __init__(
        self, parent: Optional[QtWidgets.QWidget] = None, selection_mode: str = "single"
    ):
        super().__init__(parent)
        self.itemSelectionChanged.connect(self.on_index_change)
        self.set_selection_mode(selection_mode)

    def __repr__(self):
        return f"ListWidget: {self.count()} items"

    def __getitem__(self, row: int) -> QtWidgets.QListWidgetItem:
        return self.item(row)

    def __delitem__(self, row: int):
        self.takeItem(row)

    def __add__(self, other: QtWidgets.QListWidgetItem):
        self.addItem(other)
        return self

    def __iter__(self) -> Iterator[QtWidgets.QListWidgetItem]:
        return iter(self.get_children())

    def __len__(self) -> int:
        return self.count()

    def __setstate__(self, state):
        self.set_selection_mode(state["selection_mode"])
        self.setSortingEnabled(state["sorting_enabled"])
        self.setCurrentRow(state["current_row"])
        for item in state["items"]:
            self.addItem(item)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self):
        return dict(
            items=self.get_children(),
            selection_mode=self.get_selection_mode(),
            sorting_enabled=self.isSortingEnabled(),
            current_row=self.currentRow(),
        )

    def sort(self, reverse: bool = False):
        order = QtCore.Qt.DescendingOrder if reverse else QtCore.Qt.AscendingOrder
        self.sortItems(order)

    def on_index_change(self):
        data = self.get_value()
        self.value_changed.emit(data)

    def get_children(self) -> List[QtWidgets.QListWidgetItem]:
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

    def add_item(
        self,
        name: str = "",
        icon: gui.icon.IconType = None,
        data: Optional[dict] = None,
        foreground: Optional[QtGui.QBrush] = None,
        background: Optional[QtGui.QBrush] = None,
        font: Optional[QtGui.QFont] = None,
        selected: bool = None,
        status_tip: Optional[str] = None,
        tool_tip: Optional[str] = None,
        whats_this: Optional[str] = None,
        # text_alignment: Optional[str] = None,
        checkstate: Optional[constants.StateStr] = None,
        flags: Optional[int] = None,
        size_hint: Optional[QtCore.QSize] = None,
        is_user_type: bool = False,
    ) -> widgets.ListWidgetItem:
        typ = 1 if is_user_type else 0
        item = widgets.ListWidgetItem(name, self, typ)
        if icon is not None:
            icon = gui.icon.get_icon(icon)
            item.setIcon(icon)
        if data is not None:
            for k, v in data.items():
                item.setData(k, v)
        if foreground is not None:
            item.setForeground(foreground)
        if background is not None:
            item.setBackground(background)
        if font is not None:
            item.setFont(font)
        if flags is not None:
            item.setFlags(flags)
        if selected:
            item.setSelected(selected)
        if status_tip:
            item.setStatusTip(status_tip)
        if tool_tip:
            item.setToolTip(tool_tip)
        if whats_this:
            item.setWhatsThis(whats_this)
        if size_hint is not None:
            item.setSizeHint(size_hint)
        if checkstate is not None:
            item.set_checkstate(checkstate)
        self.addItem(item)
        return item

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

    def scroll_to_item(
        self,
        item: QtWidgets.QListWidgetItem,
        mode: widgets.abstractitemview.ScrollHintStr = "ensure_visible",
    ):
        if mode not in widgets.abstractitemview.SCROLL_HINT:
            raise InvalidParamError(mode, widgets.abstractitemview.SCROLL_HINT)
        self.scrollToItem(item, widgets.abstractitemview.SCROLL_HINT[mode])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ListWidget()
    widget.add("test", icon="mdi.timer")
    widget.add("test", icon="mdi.timer")
    widget.show()
    app.main_loop()
