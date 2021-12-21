from __future__ import annotations

from typing import Any

from prettyqt import constants, custom_models, widgets
from prettyqt.qt import QtCore


class JsonTreeItem(custom_models.NestedItem):
    def __repr__(self):
        return str(self.as_json())

    def __init__(self, key="", value="", **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.value = value
        self.type = None

    @classmethod
    def from_json(cls, node_dict: dict[str, Any]) -> JsonTreeItem:
        return cls(
            count=node_dict.get("id"),
            dynamic_name=node_dict.get("dynamic_name"),
            key=node_dict.get("key"),
            value=node_dict.get("value"),
            children=[cls.from_json(c) for c in node_dict.get("children", [])],
        )

    @classmethod
    def load(cls, value, parent=None, sort: bool = False):
        root_item = cls(key="root", parent=parent)
        if isinstance(value, dict):
            items = sorted(value.items()) if sort else value.items()
            for key, value in items:
                child = cls.load(value, root_item)
                child.key = key
                child.type = type(value)
                root_item.append_child(child)

        elif isinstance(value, (list, tuple)):
            for index, value in enumerate(value):
                child = cls.load(value, root_item)
                child.key = str(index)
                child.type = type(value)
                root_item.append_child(child)

        else:
            root_item.value = value
            root_item.type = type(value)

        return root_item

    def as_json(self):
        if self.type is dict:
            return {ch.key: ch.as_json() for ch in self}
        elif self.type in (list, tuple):
            return [ch.as_json() for ch in self]
        else:
            return self.value


class JsonModel(custom_models.NestedModel):

    HEADER = ["Key", "Value", "Type"]

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self.root = JsonTreeItem()  # type: ignore
        self.items = self.root.children

    def __repr__(self):
        return str(self.root.as_json())  # type: ignore

    def load(self, document):
        """Load from dictionary.

        Arguments:
            document (dict): JSON-compatible dictionary

        """
        assert isinstance(
            document, (dict, list, tuple)
        ), "`document` must be of dict, list or tuple, " "not %s" % type(document)

        with self.reset_model():
            self.root = JsonTreeItem.load(document)
            self.root.type = type(document)  # type: ignore
            self.items = self.root.children
        return True

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()
        if role in [constants.DISPLAY_ROLE, constants.EDIT_ROLE]:
            if index.column() == 0:
                return repr(item.key)
            elif index.column() == 1:
                if item.type in (dict, list, tuple):
                    return ""
                else:
                    if role == constants.DISPLAY_ROLE:
                        return repr(item.value)
                    else:
                        return item.value
            elif index.column() == 2:
                return item.type.__name__

    def setData(self, index, value, role):
        if role == constants.EDIT_ROLE:
            if index.column() == 1:
                item = index.internalPointer()
                item.value = str(value)
                self.update_row(index.row())
                return True
        return False


if __name__ == "__main__":
    app = widgets.app()
    view = widgets.TreeView()
    model = JsonModel()

    view.set_model(model)

    dct = {
        "lastName": "Smith",
        "age": 25,
        "address": {"streetAddress": "21 2nd Street", "postalCode": "10021"},
        "phoneNumber": [
            {"type": "home", "number": "212 555-1234"},
            {"type": "fax", "number": ("646 555-4567")},
        ],
    }

    model.load(dct)
    view.show()
    view.resize(500, 300)
    app.main_loop()
