# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui


class StandardItemModel(QtGui.QStandardItemModel):

    def __repr__(self):
        return f"StandardItemModel: {self.count()} children"

    def __getitem__(self, index):
        return self.item(index)

    def __iter__(self):
        return iter(self.get_children())

    def get_children(self):
        return [self.item(index) for index in range(self.rowCount())]

    def __getstate__(self):
        return dict(items=self.get_children())

    def __setstate__(self, state):
        self.__init__()
        for item in state["items"]:
            self.appendRow(item)

    def __add__(self, other):
        if isinstance(other, QtGui.QStandardItem):
            self.appendRow(other)
            return self

    def add_item(self, label):
        item = gui.StandardItem(label)
        self.appendRow(item)


if __name__ == "__main__":
    import pickle
    from prettyqt import widgets
    model = gui.StandardItemModel()
    model.add_item("test")
    app = widgets.Application.create_default_app()
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
