# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui, core


class StandardItemModel(QtGui.QStandardItemModel):

    def __getitem__(self, index):
        return self.item(index)

    def __iter__(self):
        return iter(self.get_children())

    def __getstate__(self):
        return dict(items=self.get_children())

    def __setstate__(self, state):
        self.__init__()
        for item in state["items"]:
            self.appendRow(item)

    def __add__(self, other):
        if isinstance(other, (QtGui.QStandardItem, str)):
            self.add_item(other)
            return self
        raise TypeError("wrong type for addition")

    def get_children(self):
        return [self.item(index) for index in range(self.rowCount())]

    def add_item(self, item) -> int:
        if isinstance(item, str):
            item = gui.StandardItem(item)
        self.appendRow(item)
        return self.rowCount()


StandardItemModel.__bases__[0].__bases__ = (core.AbstractItemModel,)


if __name__ == "__main__":
    import pickle
    from prettyqt import widgets
    model = gui.StandardItemModel()
    model.add_item("test")
    app = widgets.app()
    w = widgets.ListView()
    w.setModel(model)
    model += gui.StandardItem("Item")
    for item in model:
        pass
    with open("data.pkl", "wb") as jar:
        pickle.dump(model, jar)
    with open("data.pkl", "rb") as jar:
        model = pickle.load(jar)
    model += gui.StandardItem("Item2")
    w.show()
    app.exec_()
