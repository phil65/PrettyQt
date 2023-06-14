from __future__ import annotations

from collections.abc import Iterator

from prettyqt import constants, core, gui, iconprovider
from prettyqt.utils import InvalidParamError, datatypes, listdelegators


class StandardItemModel(core.AbstractItemModelMixin, gui.QStandardItemModel):
    def __getitem__(
        self, index: int | slice | tuple[int | slice, int | slice] | core.QModelIndex
    ) -> gui.QStandardItem | listdelegators.BaseListDelegator[gui.QStandardItem]:
        match index:
            case int():
                return self.item(index)
            case slice():
                return self.__getitem__(index, 0)
            case slice() as row, slice() as col:
                rowcount = self.rowCount() if row.stop is None else row.stop
                colcount = self.columnCount() if col.stop is None else col.stop
                rowvalues = list(range(rowcount)[row])
                colvalues = list(range(colcount)[col])
                ls = [self.item(i, j) for i in rowvalues for j in colvalues]
                return listdelegators.BaseListDelegator(ls)
            case slice() as row, int() as col:
                count = self.rowCount() if row.stop is None else row.stop
                values = list(range(count)[row])
                ls = [self.item(i, col) for i in values]
                return listdelegators.BaseListDelegator(ls)
            case int() as row, slice() as col:
                count = self.columnCount() if col.stop is None else col.stop
                values = list(range(count)[col])
                ls = [self.item(row, i) for i in values]
                return listdelegators.BaseListDelegator(ls)
            case int() as row, int() as col:
                return self.item(row, col)
            case core.QModelIndex():
                return self.itemFromIndex(index)
            case _:
                raise TypeError(index)

    def __delitem__(self, index: int | tuple[int, int]):
        match index:
            case int():
                item = self.takeRow(index)
            case (int(), int()):
                item = self.takeItem(*index)
        if item is None:
            raise KeyError(index)
        return item

    def __iter__(self) -> Iterator[gui.QStandardItem]:
        return iter(self.get_children())

    def __getstate__(self):
        return dict(items=[self.item(index) for index in range(self.rowCount())])

    def __setstate__(self, state):
        for item in state["items"]:
            self.appendRow([item])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: str | gui.QStandardItem) -> StandardItemModel:
        match other:
            case gui.QStandardItem() | str():
                self.add(other)
                return self
            case _:
                raise TypeError("wrong type for addition")

    def get_children(self) -> listdelegators.BaseListDelegator[gui.QStandardItem]:
        items = [self.item(index) for index in range(self.rowCount())]
        return listdelegators.BaseListDelegator(items)

    def add(self, *item: str | gui.QStandardItem):
        for i in item:
            new_item = gui.StandardItem(i) if isinstance(i, str) else i
            self.appendRow([new_item])

    def find_items(
        self,
        text: str,
        column: int = 0,
        mode: constants.MatchFlagStr = "exact",
        recursive: bool = False,
        case_sensitive: bool = False,
    ) -> listdelegators.BaseListDelegator[gui.QStandardItem]:
        if mode not in constants.MATCH_FLAGS:
            raise InvalidParamError(mode, constants.MATCH_FLAGS)
        flag = constants.MATCH_FLAGS[mode]
        if recursive:
            flag |= constants.MatchFlag.MatchRecursive
        if case_sensitive:
            flag |= constants.MatchFlag.MatchCaseSensitive
        items = self.findItems(text, flag, column)  # type: ignore
        return listdelegators.BaseListDelegator(items)

    def add_item(
        self,
        name: str = "",
        icon: datatypes.IconType = None,
        data: dict | None = None,
        foreground: gui.QBrush | None = None,
        background: gui.QBrush | None = None,
        font: gui.QFont | None = None,
        selectable: bool = True,
        enabled: bool = True,
        editable: bool = False,
        status_tip: str = "",
        tool_tip: str = "",
        whats_this: str | None = None,
        # text_alignment: Optional[str] = None,
        checkstate: constants.StateStr | None = None,
        flags: constants.ItemFlag | None = None,
        size_hint: datatypes.SizeType | None = None,
        is_user_type: bool = False,
    ) -> gui.StandardItem:
        item = gui.StandardItem(name)
        if icon is not None:
            icon = iconprovider.get_icon(icon)
            item.setIcon(icon)
        if data is not None:
            for k, v in data.items():
                item.set_data(v, k)
        if foreground is not None:
            item.setForeground(foreground)
        if background is not None:
            item.setBackground(background)
        if font is not None:
            item.setFont(font)
        if flags is not None:
            item.setFlags(flags)
        if enabled:
            item.setEnabled(enabled)
        if editable:
            item.setEditable(editable)
        if selectable:
            item.setSelectable(selectable)
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
        self.appendRow([item])
        return item


if __name__ == "__main__":
    import pickle

    from prettyqt import widgets

    model = StandardItemModel()
    model.add("test")
    app = widgets.app()
    w = widgets.ListView()
    w.set_model(model)
    model += gui.StandardItem("Item")
    with open("data.pkl", "wb") as writer:
        pickle.dump(model, writer)
    with open("data.pkl", "rb") as reader:
        model = pickle.load(reader)
    model += gui.StandardItem("Item2")
    w.show()
    app.main_loop()
