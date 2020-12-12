from __future__ import annotations

from typing import List, Iterator, Union, Tuple

from qtpy import QtCore, QtGui

from prettyqt import core, gui
from prettyqt.utils import InvalidParamError

QtGui.QStandardItemModel.__bases__ = (core.AbstractItemModel,)

MATCH_FLAGS = dict(
    exact=QtCore.Qt.MatchExactly,
    contains=QtCore.Qt.MatchContains,
    starts_with=QtCore.Qt.MatchStartsWith,
    ends_with=QtCore.Qt.MatchEndsWith,
    wildcard=QtCore.Qt.MatchWildcard,
    regex=QtCore.Qt.MatchRegExp,
)


class StandardItemModel(QtGui.QStandardItemModel):
    def __getitem__(
        self, index: Union[int, Tuple[int, int], QtCore.QModelIndex]
    ) -> QtGui.QStandardItem:
        if isinstance(index, int):
            return self.item(index)
        elif isinstance(index, tuple):
            return self.item(*index)
        else:
            return self.itemFromIndex(index)

    def __delitem__(self, index: Union[int, Tuple[int, int]]):
        if isinstance(index, int):
            self.takeRow(index)
        elif isinstance(index, tuple):
            self.takeItem(*index)

    def __iter__(self) -> Iterator[QtGui.QStandardItem]:
        return iter(self.get_children())

    def __getstate__(self):
        return dict(items=self.get_children())

    def __setstate__(self, state):
        for item in state["items"]:
            self.appendRow(item)

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
            self.appendRow(i)

    def find_items(
        self, text: str, column: int = 0, mode: str = "exact"
    ) -> List[QtGui.QStandardItem]:
        if mode not in MATCH_FLAGS:
            raise InvalidParamError(mode, MATCH_FLAGS)
        return self.findItems(text, MATCH_FLAGS[mode], column)


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
