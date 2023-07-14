from __future__ import annotations

import logging

from prettyqt import constants, core
from prettyqt.utils import baseresolver


logger = logging.getLogger(__name__)


class ItemModelResolver(baseresolver.BaseResolver):
    """Allows globbing ItemModels."""

    def __init__(
        self,
        model: core.QAbstractItemModel,
        path_role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        ignore_case: bool = False,
    ):
        """Resolve any `ModelIndex` paths using role `path_role`.

        Arguments:
            model: Model to search
            path_role: ItemDataRole to be used for resolving
            ignore_case: Enable case insensisitve handling.
        """
        super().__init__(ignore_case=ignore_case)
        self.model = model
        self.path_role = path_role
        self.fetch_more = True

    def get_parent(self, node):
        return node.parent()

    def get_children(self, node):
        if self.fetch_more:
            while self.model.canFetchMore(node):
                self.model.fetchMore(node)
        return [self.model.index(i, 0, node) for i in range(self.model.rowCount(node))]

    def get_root(self, node):
        return core.ModelIndex()

    def get_attribute(self, node):
        return str(node.data(self.path_role))

    def get(self, path: str, root_node=None):
        path = f"/None{path}"
        return super().get(path, root_node or core.ModelIndex())

    def glob(self, path: str, root_node=None):
        path = f"/None{path}"
        return super().glob(path, root_node or core.ModelIndex())


if __name__ == "__main__":
    from prettyqt import itemmodels, widgets

    app = widgets.app()
    mapping = {"a": "test", ("a", "b"): "test", ("a", "b", "c"): "test"}
    model = itemmodels.TupleTreeModel(mapping)
    resolver = ItemModelResolver(model)
    indexes = resolver.glob("/root/test")
    print(indexes)
    # view = widgets.TreeView()
    # view.setRootIsDecorated(True)
    # view.set_model(model)
    # view.show()
    # with app.debug_mode():
    #     app.exec()
