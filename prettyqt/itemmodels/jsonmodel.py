from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from prettyqt import constants, itemmodels


class NameColumn(itemmodels.ColumnItem):
    name = "Name"
    doc = "Name"

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj.key


class ValueColumn(itemmodels.ColumnItem):
    name = "Value"
    doc = "Value"
    editable = True

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return repr(item.obj.value)
            case constants.EDIT_ROLE:
                return item.obj.value

    def set_data(self, item, value, role):
        match role:
            case constants.EDIT_ROLE:
                item.obj.value = value
                return True
        return False


class TypeColumn(itemmodels.ColumnItem):
    name = "Type"
    doc = "Type"

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return repr(item.obj.typ)


@dataclass
class JsonItem:
    key: str | int
    value: Any
    typ: type | None = None


class JsonModel(itemmodels.ColumnItemModel):
    COLUMNS = [NameColumn, ValueColumn, TypeColumn]
    SUPPORTS = Mapping

    def __init__(
        self,
        obj: Any,
        show_root: bool = True,
        **kwargs,
    ):
        super().__init__(
            obj=JsonItem(key="", value=obj, typ=type(obj)),
            columns=self.COLUMNS,
            show_root=show_root,
            **kwargs,
        )

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, Mapping)

    def _has_children(self, item: JsonModel.TreeItem) -> bool:
        return isinstance(item.obj.value, dict | list | set) and bool(item.obj.value)

    def _fetch_object_children(
        self, item: JsonModel.TreeItem
    ) -> list[JsonModel.TreeItem]:
        """Fetch the children of a Python object.

        Returns: list of treeitem.TreeItems
        """
        # items = []
        match item.obj.value:
            case Mapping():
                return [
                    self.TreeItem(obj=JsonItem(key=k, value=v, typ=type(v)))
                    for k, v in item.obj.value.items()
                ]

            case Iterable() if not isinstance(item.obj.value, str):
                return [
                    self.TreeItem(obj=JsonItem(key=k, value=v, typ=type(v)))
                    for k, v in enumerate(item.obj.value)
                ]
            case _:
                return [
                    self.TreeItem(
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
    table = widgets.TreeView()
    model = JsonModel(dist, parent=table)
    table.set_model(model)
    table.proxifier[0].modify(lambda x: x * 2)
    table.proxifier[1].modify(lambda x: x * 4)
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.show()
    app.exec()
