from __future__ import annotations

import logging

from prettyqt import constants, core, custom_models
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import treeitem


logger = logging.getLogger(__name__)


TO_FILTER = {
    "minimumHeight",
    "minimumWidth",
    "maximumHeight",
    "maximumWidth",
    "x",
    "y",
    "width",
    "height",
}


class WidgetHierarchyModel(custom_models.TreeModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BaseClass = QtWidgets.QWidget
        self.props = core.MetaObject(self.BaseClass.staticMetaObject).get_properties()
        self.props = [i for i in self.props if i.get_name() not in TO_FILTER]
        # self.props.sort(key=lambda x: x.get_name())

    def columnCount(self, parent=None):
        return len(self.props) + 1

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole,
    ) -> str | None:
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, 0:
                return "Type"
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.props[section - 1].get_name()

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        widget = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, 0:
                return type(widget).__name__
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, _:
                prop = self.props[index.column() - 1]
                return prop.read(widget)
            case constants.USER_ROLE, 0:
                return widget
            case constants.USER_ROLE, _:
                prop = self.props[index.column() - 1]
                return prop.read(widget)

    def setData(self, index, value, role=constants.DISPLAY_ROLE):
        prop = self.props[index.column() - 1]
        widget = self.data_by_index(index).obj
        match role:
            case constants.USER_ROLE:
                with self.change_layout():
                    prop.write(widget, value)
                # self.update_row(index.row())
                return True
        return False

    def flags(self, index):
        match index.column():
            case 0:
                return super().flags(index)
            case _:
                prop = self.props[index.column() - 1]
                if prop.isWritable():
                    return (
                        super().flags(index)
                        | constants.IS_EDITABLE
                        | constants.IS_ENABLED
                        | constants.IS_SELECTABLE
                    )
                return super().flags(index)

    def _fetch_object_children(self, item) -> list:
        return [treeitem.TreeItem(obj=i) for i in item.obj.findChildren(self.BaseClass)]

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return False
        item = self.data_by_index(parent)
        if self._show_root and item == self._root_item:
            return True
        return bool(item.obj.findChildren(self.BaseClass))


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_delegates import variantdelegate

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    view.set_icon("mdi.folder")
    parent = widgets.Widget()
    item = widgets.TableWidget(parent)
    model = WidgetHierarchyModel(parent, show_root=True, parent=view)
    delegate = variantdelegate.VariantDelegate(parent=view)
    view.set_model(model)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate(delegate)
    view.resize(1000, 1000)
    with app.debug_mode():
        view.show()
        app.main_loop()
