from __future__ import annotations

from typing import Iterator, List, Optional, Tuple, Union

from qtpy import QtCore, QtGui

from prettyqt import constants, core, gui
from prettyqt.utils import InvalidParamError


QtGui.QStandardItemModel.__bases__ = (core.AbstractItemModel,)


class StandardItemModel(QtGui.QStandardItemModel):
    def __getitem__(
        self, index: Union[int, Tuple[int, int], QtCore.QModelIndex]
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

    def __delitem__(self, index: Union[int, Tuple[int, int]]):
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

    def __add__(self, other: Union[str, QtGui.QStandardItem]) -> StandardItemModel:
        if isinstance(other, (QtGui.QStandardItem, str)):
            self.add(other)
            return self
        raise TypeError("wrong type for addition")

    def get_children(self) -> List[QtGui.QStandardItem]:
        return [self.item(index) for index in range(self.rowCount())]

    def add(self, *item: Union[str, QtGui.QStandardItem]):
        for i in item:
            if isinstance(i, str):
                i = gui.StandardItem(i)
            self.appendRow([i])

    def find_items(
        self, text: str, column: int = 0, mode: constants.MatchFlagStr = "exact"
    ) -> List[QtGui.QStandardItem]:
        if mode not in constants.MATCH_FLAGS:
            raise InvalidParamError(mode, constants.MATCH_FLAGS)
        return self.findItems(text, constants.MATCH_FLAGS[mode], column)

    def add_item(
        self,
        name: str = "",
        icon: gui.icon.IconType = None,
        data: Optional[dict] = None,
        foreground: Optional[QtGui.QBrush] = None,
        background: Optional[QtGui.QBrush] = None,
        font: Optional[QtGui.QFont] = None,
        selectable: bool = True,
        enabled: bool = True,
        editable: bool = False,
        status_tip: Optional[str] = None,
        tool_tip: Optional[str] = None,
        whats_this: Optional[str] = None,
        # text_alignment: Optional[str] = None,
        checkstate: Optional[constants.StateStr] = None,
        flags: Optional[int] = None,
        size_hint: Optional[QtCore.QSize] = None,
        is_user_type: bool = False,
    ) -> gui.StandardItem:
        item = gui.StandardItem(name)
        if icon is not None:
            icon = gui.icon.get_icon(icon)
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
            item.setSizeHint(size_hint)
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
    with open("data.pkl", "wb") as jar:
        pickle.dump(model, jar)
    with open("data.pkl", "rb") as jar:
        model = pickle.load(jar)
    model += gui.StandardItem("Item2")
    w.show()
    app.main_loop()
