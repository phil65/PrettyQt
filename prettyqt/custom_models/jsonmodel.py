from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from prettyqt import core, custom_models
from prettyqt.qt import QtCore
from prettyqt.utils import treeitem


COL_NAME = custom_models.ColumnItem(
    name="Name",
    doc="Name.",
    label=lambda x: x.obj.key,
)

COL_VALUE = custom_models.ColumnItem(
    name="Value",
    doc="Value.",
    label=lambda x: repr(x.obj.value),
)

COL_TYPE = custom_models.ColumnItem(
    name="Type",
    doc="Type.",
    label=lambda x: repr(x.obj.typ),
)


@dataclass
class JsonItem:
    key: str | int
    value: Any
    typ: type | None = None


class JsonModel(custom_models.ColumnItemModel):
    """Model that provides an interface to an objectree that is build of tree items."""

    def __init__(
        self,
        obj: Any,
        show_root: bool = True,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(
            obj=JsonItem(key="", value=obj, typ=type(obj)),
            columns=[COL_NAME, COL_VALUE, COL_TYPE],
            parent=parent,
            show_root=show_root,
        )

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return False
        if self.show_root and self.tree_item(parent) == self._root_item:
            return True
        return isinstance(self.tree_item(parent).obj.value, dict | list | set)

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        """Fetch the children of a Python object.

        Returns: list of treeitem.TreeItems
        """
        # items = []
        match item.obj.value:
            case Mapping():
                return [
                    treeitem.TreeItem(obj=JsonItem(key=k, value=v, typ=type(v)))
                    for k, v in item.obj.value.items()
                ]

            case Iterable() if not isinstance(item.obj.value, str):
                return [
                    treeitem.TreeItem(obj=JsonItem(key=k, value=v, typ=type(v)))
                    for k, v in enumerate(item.obj.value)
                ]
            case _:
                return [
                    treeitem.TreeItem(
                        obj=JsonItem(
                            key="key",
                            value=repr(item.obj.value),
                            typ=type(item.obj.value),
                        )
                    )
                ]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    dist = [dict(a=2, b={"a": 4, "b": [1, 2, 3], "jkjkjk": "tekjk"}), 6, "jkjk"]
    model = JsonModel(dist)
    table = widgets.TreeView()
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)
    table.show()
    app.main_loop()
