from __future__ import annotations

import logging

from prettyqt import constants, core, custom_models
from prettyqt.utils import treeitem

logger = logging.getLogger(__name__)


class BaseClassTreeModel(custom_models.TreeModel):
    """Base Tree Model to display class tree structures."""

    HEADER = ["Name", "Docstrings", "Module"]

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole,
    ) -> str | None:
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.HEADER[section]
        return None

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        klass = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return klass.__name__
            case constants.DISPLAY_ROLE, 1:
                return klass.__doc__
            case constants.DISPLAY_ROLE, 2:
                return klass.__module__
            case constants.USER_ROLE, _:
                return klass


class SubClassTreeModel(BaseClassTreeModel):
    """Model to display the subclass tree of a python class."""

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        return [treeitem.TreeItem(obj=i) for i in item.obj.__subclasses__()]

    def hasChildren(self, parent: core.ModelIndex | None = None) -> bool:
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return False
        item = self.data_by_index(parent)
        if self._show_root and item == self._root_item:
            return True
        if item.obj is None:
            return False
        return len(item.obj.__subclasses__()) > 0


class ParentClassTreeModel(BaseClassTreeModel):
    """Model to display the parentclass tree of a python class."""

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        return [treeitem.TreeItem(obj=i) for i in item.obj.__bases__]

    def hasChildren(self, parent: core.ModelIndex | None = None) -> bool:
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return False
        item = self.data_by_index(parent)
        if self._show_root and item == self._root_item:
            return True
        if item.obj is None:
            return False
        return len(item.obj.__bases__) > 0


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_widgets import filtercontainer

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    model = SubClassTreeModel(widgets.QWidget, show_root=True, parent=view)
    view.set_model(model)
    container = filtercontainer.FilterContainer(view)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("variant")
    view.resize(1000, 1000)
    container.show()
    with app.debug_mode():
        app.main_loop()
