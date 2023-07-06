from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
import functools

from typing import Any

from prettyqt import constants, core, iconprovider, widgets
from prettyqt.qt import QtGui
from prettyqt.utils import datatypes, listdelegators


class NoData:
    pass


class ListWidget(widgets.ListViewMixin, widgets.QListWidget):
    value_changed = core.Signal(object)

    def __init__(self, *args, selection_mode: str = "single", **kwargs):
        super().__init__(*args, selection_mode=selection_mode, **kwargs)
        self.itemSelectionChanged.connect(self.on_index_change)

    def __repr__(self):
        return f"{type(self).__name__}: {self.count()} items"

    def __getitem__(
        self, row: int | slice
    ) -> widgets.QListWidgetItem | listdelegators.ListDelegator[widgets.QListWidgetItem]:
        match row:
            case int():
                item = self.item(row)
                if item is None:
                    raise KeyError(row)
                return item
            case slice():
                count = self.itemCount() if row.stop is None else row.stop
                values = list(range(count)[row])
                ls = [self.item(i) for i in values]
                return listdelegators.ListDelegator(ls)
            case _:
                raise TypeError(row)

    def __delitem__(self, row: int):
        self.takeItem(row)

    def __add__(self, other: widgets.QListWidgetItem):
        self.addItem(other)
        return self

    def __iter__(self) -> Iterator[widgets.QListWidgetItem]:
        return iter(self.get_children())

    def __len__(self) -> int:
        return self.count()

    def sort(self, reverse: bool = False):
        order = constants.DESCENDING if reverse else constants.ASCENDING
        self.sortItems(order)

    def on_index_change(self):
        data = self.get_value()
        self.value_changed.emit(data)

    def get_children(self) -> listdelegators.ListDelegator[widgets.QListWidgetItem]:
        items = [self.item(row) for row in range(self.count())]
        return listdelegators.ListDelegator(items)

    def add_items(self, items: Iterable | Mapping):
        match items:
            case Mapping():
                for k, v in items.items():
                    self.add(v, k)
            case Iterable():
                for i in items:
                    if isinstance(i, tuple | list):
                        self.add(*i)
                    else:
                        self.add(i)
            case _:
                raise TypeError(items)

    @functools.singledispatchmethod
    def add_item(
        self,
        name: str = "",
        icon: datatypes.IconType = None,
        data: dict | None = None,
        foreground: QtGui.QBrush | None = None,
        background: QtGui.QBrush | None = None,
        font: QtGui.QFont | None = None,
        selected: bool = None,
        status_tip: str = "",
        tool_tip: str = "",
        whats_this: str | None = None,
        # text_alignment: Optional[str] = None,
        checkstate: constants.StateStr | constants.CheckState | None = None,
        flags: constants.ItemFlag | None = None,
        size_hint: datatypes.SizeType | None = None,
        is_user_type: bool = False,
    ) -> widgets.ListWidgetItem:
        typ = 1 if is_user_type else 0
        item = widgets.ListWidgetItem(name, self, typ)
        if icon is not None:
            icon = iconprovider.get_icon(icon)
            item.setIcon(icon)
        if data is not None:
            for k, v in data.items():
                item.set_data(k, v)
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
            item.set_size_hint(size_hint)
        if checkstate is not None:
            item.set_checkstate(checkstate)
        self.addItem(item)
        return item

    @add_item.register
    def _(self, listitem: widgets.QListWidgetItem):
        self.addItem(listitem)

    def add(self, label: str, data=NoData, icon: datatypes.IconType = None):
        if data is NoData:
            data = label
        item = widgets.ListWidgetItem(label)
        item.set_icon(icon)
        item.setData(constants.USER_ROLE, data)  # type: ignore
        self.addItem(item)

    def get_value(self) -> list[Any]:
        return [i.data(constants.USER_ROLE) for i in self.selectedItems()]  # type: ignore

    def set_value(self, value):
        for i in self.get_children():
            if i.data(constants.USER_ROLE) in value:  # type: ignore
                self.setCurrentItem(i)
                break

    def scroll_to_item(
        self,
        item: widgets.QListWidgetItem,
        mode: widgets.abstractitemview.ScrollHintStr
        | widgets.QAbstractItemView.ScrollHint = "ensure_visible",
    ):
        self.scrollToItem(item, widgets.abstractitemview.SCROLL_HINT.get_enum_value(mode))

    def find_items(
        self,
        text: str,
        column: int = 0,
        mode: constants.MatchFlagStr | constants.MatchFlag = "exact",
        recursive: bool = False,
        case_sensitive: bool = False,
    ) -> listdelegators.ListDelegator[widgets.QListWidgetItem]:
        flag = constants.MATCH_FLAGS.get_enum_value(mode)
        if recursive:
            flag |= constants.MatchFlag.MatchRecursive
        if case_sensitive:
            flag |= constants.MatchFlag.MatchCaseSensitive
        items = self.findItems(text, flag, column)  # type: ignore
        return listdelegators.ListDelegator(items)


if __name__ == "__main__":
    app = widgets.app()
    widget = ListWidget()
    for i in range(100):
        widget.add_item(str(i))
    widget.add("test", icon="mdi.timer")
    widget.add("test", icon="mdi.timer")
    widget.show()
    app.exec()
