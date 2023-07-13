from __future__ import annotations

import logging
import pathlib

from prettyqt import constants, core, itemmodels


logger = logging.getLogger(__name__)


class TupleTreeModel(itemmodels.TreeModel):
    """Base Tree Model to display a dict[tuple[Any], str] data structure.

    The dictionary keys are tuples of path parts, like ("path", "to", "something")

    ```py
    model = TupleTreeModel({("a"): "test2", ("a", "b"): "test", ("a", "b", "c"): "test3"})
    table = widgets.TreeView()
    table.set_model(model)
    table.show()
    ```
    """

    HEADER = [
        "Name",
    ]

    def __init__(self, mapping: dict, **kwargs):
        super().__init__((), **kwargs)
        self.mapping = {(): "root"} | mapping

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
                return self.mapping[tup]

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case dict() if all(
                isinstance(k, pathlib.Path | tuple) for k in instance.keys() and instance
            ):
                return True
        return False

    def _fetch_object_children(
        self, item: TupleTreeModel.TreeItem
    ) -> list[TupleTreeModel.TreeItem]:
        parts = item.obj.parts if isinstance(item.obj, pathlib.Path) else item.obj
        return [
            self.TreeItem(obj=k)
            for k in self.mapping.keys()
            if len(k) == len(parts) + 1
            and all(parent_part == k[i] for i, parent_part in enumerate(parts))
        ]

    def _has_children(self, item: TupleTreeModel.TreeItem) -> bool:
        parts = item.obj.parts if isinstance(item.obj, pathlib.Path) else item.obj
        return any(
            len(k) == len(parts) + 1
            and all(parent_part == k[i] for i, parent_part in enumerate(parts))
            for k in self.mapping.keys()
        )


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
