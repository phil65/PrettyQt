from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from prettyqt import custom_models
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


# class NameColumn(custom_models.ColumnItem):
#     name="Name"
#     doc="Name"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return x.obj.key

# class ValueColumn(custom_models.ColumnItem):
#     name="Value"
#     doc="Value"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return repr(x.obj.value)


# class TypeColumn(custom_models.ColumnItem):
#     name="Type"
#     doc="Type"

#     def get_data(self, item, role):
#         match role:
#             case constants.DISPLAY_ROLE:
#                 return repr(x.obj.typ)


COLUMNS = [COL_NAME, COL_VALUE, COL_TYPE]


@dataclass
class JsonItem:
    key: str | int
    value: Any
    typ: type | None = None


class JsonModel(custom_models.ColumnItemModel):
    def __init__(
        self,
        obj: Any,
        show_root: bool = True,
        **kwargs,
    ):
        super().__init__(
            obj=JsonItem(key="", value=obj, typ=type(obj)),
            columns=COLUMNS,
            show_root=show_root,
            **kwargs,
        )

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, Mapping)

    def _has_children(self, item: treeitem.TreeItem) -> bool:
        return isinstance(item.obj.value, dict | list | set) and bool(item.obj.value)

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
    table = widgets.TreeView()
    model = JsonModel(dist, parent=table)
    table.set_model(model)
    table.proxifier.modify(lambda x: x * 2, column=0)
    table.proxifier.modify(lambda x: x * 4, column=1)
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.show()
    app.main_loop()
