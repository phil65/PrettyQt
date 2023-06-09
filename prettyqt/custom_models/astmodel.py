from __future__ import annotations

import ast

import logging

from prettyqt import constants, core, custom_models
from prettyqt.qt import QtCore
from prettyqt.utils import treeitem


logger = logging.getLogger(__name__)


class AstModel(custom_models.TreeModel):
    HEADER = [
        "Node type",
        "Line number",
        "Column offset",
        "End line number",
        "End column offset",
    ]

    def __init__(self, ast_tree, **kwargs):
        super().__init__(ast_tree.body, **kwargs)
        self.ast_tree = ast_tree.body

    def set_ast(self, tree: ast.AST | str = ""):
        with self.reset_model():
            self.ast_tree = tree

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def parent_node_for_index(self, index):
        # note: if index data is a node itself, it will get returned.
        while not hasattr(node := index.data(constants.USER_ROLE), "lineno"):
            index = index.parent()
        return node

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole,
    ) -> str | None:
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.HEADER[section]
        return None

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        node = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return type(node).__name__
            case constants.DISPLAY_ROLE, 1:
                if hasattr(node, "lineno"):
                    return node.lineno
            case constants.USER_ROLE, _:
                return node

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        if isinstance(item.obj, list):
            return [treeitem.TreeItem(obj=i) for i in item.obj]
        return [treeitem.TreeItem(obj=getattr(item.obj, i)) for i in item.obj._fields]

    def hasChildren(self, parent: core.ModelIndex | None = None) -> bool:
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return False
        item = self.data_by_index(parent)
        if self._show_root and item == self._root_item:
            return True
        match item.obj:
            case list():
                return len(item.obj)
            case ast.AST():
                return len(item.obj._fields) > 0
            case ast.Name():
                return 0
        return 0


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_widgets import filtercontainer

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    tree = ast.parse(
        """\
for a in b:
    if a > 5:
        break
    else:
        continue

"""
    )

    model = AstModel(tree, show_root=True, parent=view)
    view.set_model(model)
    container = filtercontainer.FilterContainer(view)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("variant")
    view.resize(1000, 1000)
    container.show()
    with app.debug_mode():
        app.main_loop()
