from __future__ import annotations

import enum
import inspect
import logging

from prettyqt import constants, core, custom_models, gui
from prettyqt.utils import treeitem

logger = logging.getLogger(__name__)


class BaseClassTreeModel(custom_models.TreeModel):
    """Base Tree Model to display class tree structures."""

    HEADER = ["Name", "Docstrings", "Module", "Comments", "File", "Is Abstract"]

    @core.Enum
    class Roles(enum.IntEnum):
        """Item roles."""

        SourceRole = constants.USER_ROLE + 1

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
                doc = inspect.getdoc(klass)
                return inspect.cleandoc(doc)
            case constants.DISPLAY_ROLE, 2:
                return inspect.getmodule(klass)
            case constants.DISPLAY_ROLE, 3:
                return inspect.getcomments(klass)
            case constants.DISPLAY_ROLE, 4:
                return inspect.getfile(klass)
            case constants.CHECKSTATE_ROLE, 5:
                return inspect.isabstract(klass)
            case constants.USER_ROLE, _:
                return klass
            case constants.FONT_ROLE, 1 | 3:
                return gui.Font.mono(as_qt=True)
            case self.Roles.SourceRole, _:
                return inspect.getsource(klass)


class SubClassTreeModel(BaseClassTreeModel):
    """Model to display the subclass tree of a python class."""

    @classmethod
    def supports(cls, typ):
        return isinstance(typ, type)

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

    @classmethod
    def supports(cls, typ):
        return isinstance(typ, type)

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
