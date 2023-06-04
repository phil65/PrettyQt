from __future__ import annotations

from collections.abc import Mapping

from prettyqt import core, custom_models
from prettyqt.utils import treeitem


class MappingModel(custom_models.ColumnItemModel):
    def __init__(
        self,
        obj: list[dict],
        nested_key=None,
        **kwargs,
    ):
        super().__init__(
            obj=obj,
            columns=[],
            show_root=False,
            **kwargs,
        )
        self.nested_key = nested_key
        columns = []
        for k, v in obj[0].items():

            def get_repr(x, k=k, v=v):
                return repr(v) if isinstance(x.obj, Mapping) else repr(x.obj)

            col = custom_models.ColumnItem(
                name=k,
                doc=k,
                label=get_repr,
            )
            columns.append(col)
        self.set_columns(columns)

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return False
        item = self.data_by_index(parent)
        if item in [self._root_item, self.inspected_item]:
            return True
        if self.nested_key is None:
            return False
        return isinstance(item.obj.get(self.nested_key), Mapping)

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        match item.obj:
            # case Mapping():
            #     return [
            #         treeitem.TreeItem(obj=v)
            #         for k, v in item.obj.items()
            #     ]
            case list():
                return [treeitem.TreeItem(obj=item) for item in item.obj]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    dct = dict(a=2, b="hallo", c="hall")
    dct2 = dict(a=2, b="hallo2", c="hallo3")
    model = MappingModel([dct, dct2])
    table = widgets.TreeView()
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)
    table.show()
    app.main_loop()
