from __future__ import annotations

from collections.abc import Iterator

from prettyqt import constants, core, gui, iconprovider
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, types


QtGui.QStandardItemModel.__bases__ = (core.AbstractItemModel,)


class StandardItemModel(QtGui.QStandardItemModel):
    def __getitem__(
        self, index: int | tuple[int, int] | QtCore.QModelIndex
    ) -> QtGui.QStandardItem:
        if isinstance(index, int):
            item = self.item(index)
        elif isinstance(index, tuple):
            item = self.item(*index)
        else:
            item = self.itemFromIndex(index)
        if item is None:
            raise KeyError(index)
        return item

    def __delitem__(self, index: int | tuple[int, int]):
        if isinstance(index, int):
            item = self.takeRow(index)
        elif isinstance(index, tuple):
            item = self.takeItem(*index)
        if item is None:
            raise KeyError(index)
        return item

    def __iter__(self) -> Iterator[QtGui.QStandardItem]:
        return iter(self.get_children())

    def __getstate__(self):
        return dict(items=self.get_children())

    def __setstate__(self, state):
        for item in state["items"]:
            self.appendRow([item])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: str | QtGui.QStandardItem) -> StandardItemModel:
        if isinstance(other, (QtGui.QStandardItem, str)):
            self.add(other)
            return self
        raise TypeError("wrong type for addition")

    @classmethod
    def create_single_item_model(cls, *args, **kwargs):
        mdl = cls(1, 1)
        mdl.add_item(*args, **kwargs)
        return mdl

    def get_children(self) -> list[QtGui.QStandardItem]:
        return [self.item(index) for index in range(self.rowCount())]

    def add(self, *item: str | QtGui.QStandardItem):
        for i in item:
            if isinstance(i, str):
                i = gui.StandardItem(i)
            self.appendRow([i])

    def find_items(
        self, text: str, column: int = 0, mode: constants.MatchFlagStr = "exact"
    ) -> list[QtGui.QStandardItem]:
        if mode not in constants.MATCH_FLAGS:
            raise InvalidParamError(mode, constants.MATCH_FLAGS)
        return self.findItems(text, constants.MATCH_FLAGS[mode], column)  # type: ignore

    def add_item(
        self,
        name: str = "",
        icon: types.IconType = None,
        data: dict | None = None,
        foreground: QtGui.QBrush | None = None,
        background: QtGui.QBrush | None = None,
        font: QtGui.QFont | None = None,
        selectable: bool = True,
        enabled: bool = True,
        editable: bool = False,
        status_tip: str | None = None,
        tool_tip: str | None = None,
        whats_this: str | None = None,
        # text_alignment: Optional[str] = None,
        checkstate: constants.StateStr | None = None,
        flags: QtCore.Qt.ItemFlags | None = None,
        size_hint: types.SizeType | None = None,
        is_user_type: bool = False,
    ) -> gui.StandardItem:
        item = gui.StandardItem(name)
        if icon is not None:
            icon = iconprovider.get_icon(icon)
            item.setIcon(icon)
        if data is not None:
            for k, v in data.items():
                item.setData(v, k)
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

    model = gui.StandardItemModel()
    model.add("test")
    app = widgets.app()
    w = widgets.ListView()
    w.set_model(model)
    model += gui.StandardItem("Item")
    for item in model:
        pass
    with open("data.pkl", "wb") as writer:
        pickle.dump(model, writer)
    with open("data.pkl", "rb") as reader:
        model = pickle.load(reader)
    model += gui.StandardItem("Item2")
    w.show()
    app.main_loop()
