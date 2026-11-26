from collections.abc import Hashable
import logging
import pathlib
from typing import TYPE_CHECKING, ClassVar

from prettyqt import constants, itemmodels


if TYPE_CHECKING:
    from prettyqt import core


logger = logging.getLogger(__name__)


class TupleTreeModel(itemmodels.TreeModel):
    """Base Tree Model to display a dict[tuple[Any], str] data structure.

    The dictionary keys are tuples of path parts, like ("path", "to", "something")

    ```py
    mapping = {("a",): "test2", ("a", "b"): "test", ("a", "b", "c"): "test3"}
    model = TupleTreeModel(mapping)
    table = widgets.TreeView()
    table.set_model(model)
    table.show()
    ```
    """

    SUPPORTS = dict[tuple[Hashable, ...] | pathlib.PurePath, str]
    HEADER: ClassVar = ["Name"]

    def __init__(self, mapping: dict, **kwargs):
        self.mapping = {(): "root"} | {_to_tuple(k): v for k, v in mapping.items()}
        super().__init__((), **kwargs)

    def columnCount(self, parent: core.ModelIndex | None = None):
        return len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.HEADER[section]
        return None

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        tup = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                # intermediate nodes may not be part of the mapping.
                value = self.mapping.get(tup)
                return str(tup[-1] if value is None and tup else value)
            case constants.USER_ROLE, _:
                return tup
        return None

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case dict() if instance and all(
                isinstance(k, pathlib.PurePath | tuple) for k in instance
            ):
                return True
        return False

    def _child_keys(self, parts: tuple) -> list[tuple]:
        depth = len(parts)
        # dict keeps insertion order and removes duplicates
        children = {
            k[: depth + 1]: None
            for k in self.mapping
            if len(k) > depth and k[:depth] == parts
        }
        return list(children)

    def _fetch_object_children(
        self, item: TupleTreeModel.TreeItem
    ) -> list[TupleTreeModel.TreeItem]:
        return [self.TreeItem(obj=k) for k in self._child_keys(item.obj)]

    def _has_children(self, item: TupleTreeModel.TreeItem) -> bool:
        depth = len(item.obj)
        return any(len(k) > depth and k[:depth] == item.obj for k in self.mapping)


def _to_tuple(key) -> tuple:
    match key:
        case pathlib.PurePath():
            return key.parts
        case tuple():
            return key
    return (key,)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    mapping = {"a": "test", ("a", "b"): "test", ("a", "b", "c"): "test"}
    model = TupleTreeModel(mapping)
    view.set_model(model)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("editor")
    view.resize(1000, 1000)
    view.show()
    with app.debug_mode():
        app.exec()
