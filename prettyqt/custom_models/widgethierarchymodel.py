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


class FakeWidgetProp:
    def isWritable(self):
        return False

    def get_name(self):
        return "Widget class"

    def read(self, widget):
        return widget.__class__.__name__

    def write(self, widget, value):
        pass


class FakeLayoutProp:
    def isWritable(self):
        return False

    def get_name(self):
        return "Layout"

    def read(self, widget):
        if widget.layout() is None:
            return ""
        return widget.layout().__class__.__name__

    def write(self, widget, value):
        pass


class WidgetHierarchyModel(custom_models.TreeModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BaseClass = QtWidgets.QWidget
        self.props = core.MetaObject(self.BaseClass.staticMetaObject).get_properties()
        self.props = [i for i in self.props if i.get_name() not in TO_FILTER]
        self.props.insert(0, FakeWidgetProp())
        self.props.insert(1, FakeLayoutProp())
        # self.props.sort(key=lambda x: x.get_name())

    def columnCount(self, parent=None):
        return len(self.props)

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole,
    ) -> str | None:
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.props[section].get_name()

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        widget = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, _:
                prop = self.props[index.column()]
                return prop.read(widget)
            case constants.USER_ROLE, _:
                prop = self.props[index.column()]
                return prop.read(widget)

    def setData(self, index, value, role=constants.DISPLAY_ROLE):
        prop = self.props[index.column()]
        widget = self.data_by_index(index).obj
        match role:
            case constants.USER_ROLE:
                with self.change_layout():
                    prop.write(widget, value)
                # self.update_row(index.row())
                return True
        return False

    def flags(self, index):
        prop = self.props[index.column()]
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


class LayoutHierarchyModel(WidgetHierarchyModel):
    def _fetch_object_children(self, item) -> list:
        match item.obj:
            case QtWidgets.QWidget():
                layout = item.obj.layout()
            case QtWidgets.QLayout():
                layout = item.obj
            case _:
                raise ValueError(item)
        items = [layout.itemAt(i) for i in range(layout.count())]
        items = [i.widget() if i.widget() is not None else i.layout() for i in items]
        return [treeitem.TreeItem(obj=i) for i in items]

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return False
        item = self.data_by_index(parent)
        if self._show_root and item == self._root_item:
            return True
        layout = item.obj.layout()
        return False if layout is None else layout.count() > 0


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_delegates import variantdelegate

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    view.set_icon("mdi.folder")
    parent = widgets.Widget()
    parent.set_layout("horizontal")
    parent.box.add(widgets.Widget())
    item = widgets.TableWidget(parent)
    model = LayoutHierarchyModel(parent, show_root=True, parent=view)
    delegate = variantdelegate.VariantDelegate(parent=view)
    view.set_model(model)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate(delegate)
    view.resize(1000, 1000)
    with app.debug_mode():
        view.show()
        app.main_loop()
