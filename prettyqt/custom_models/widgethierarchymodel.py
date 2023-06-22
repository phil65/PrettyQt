from __future__ import annotations

import enum
import logging

from prettyqt import constants, core, custom_models
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import treeitem


logger = logging.getLogger(__name__)


class FakeClassNameProp:
    def isWritable(self):
        return False

    def get_name(self):
        return "Class"

    def read(self, qobject):
        return qobject.__class__.__name__

    def write(self, qobject, value):
        pass


class FakeUserPropertyNameProp:
    def isWritable(self):
        return False

    def get_name(self):
        return "User property name"

    def read(self, qobject):
        userprop = qobject.metaObject().userProperty()
        return userprop.name() if userprop.isValid() else ""

    def write(self, qobject, value):
        pass


class FakeUserPropertyValueProp:
    def isWritable(self):
        return True

    def get_name(self):
        return "User property value"

    def read(self, qobject):
        userprop = qobject.metaObject().userProperty()
        return userprop.read(qobject)

    def write(self, qobject, value):
        userprop = qobject.metaObject().userProperty()
        return userprop.write(qobject, value)


class FakeLayoutProp:
    def isWritable(self):
        return False

    def get_name(self):
        return "Layout"

    def read(self, qobject):
        # check for layout attr to support QObjects
        if not hasattr(qobject, "layout") or qobject.layout() is None:
            return ""
        return qobject.layout().__class__.__name__

    def write(self, qobject, value):
        pass


class WidgetHierarchyModel(custom_models.TreeModel):
    class Roles(enum.IntEnum):
        """Custom roles."""

        WidgetRole = constants.USER_ROLE + 23324

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BaseClass = QtWidgets.QWidget
        self.props = core.MetaObject(self.BaseClass.staticMetaObject).get_properties(
            only_stored=True
        )
        self.props.insert(0, FakeClassNameProp())
        self.props.insert(1, FakeLayoutProp())
        self.props.insert(1, FakeUserPropertyNameProp())
        self.props.insert(1, FakeUserPropertyValueProp())
        # self.props.sort(key=lambda x: x.get_name())

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, QtWidgets.QWidget)

    def columnCount(self, parent=None):
        return len(self.props)

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.props[section].get_name()

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
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
            case self.Roles.WidgetRole, _:
                return widget
            case constants.SIZE_HINT_ROLE, _:
                return QtCore.QSize(250, 35)

    def setData(self, index: core.ModelIndex, value, role=constants.DISPLAY_ROLE):
        prop = self.props[index.column()]
        widget = self.data_by_index(index).obj
        match role:
            case constants.USER_ROLE:
                with self.change_layout():
                    prop.write(widget, value)
                # self.update_row(index.row())
                return True
        return False

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        prop = self.props[index.column()]
        if prop.isWritable():
            return (
                super().flags(index)
                | constants.IS_EDITABLE
                | constants.IS_ENABLED
                | constants.IS_SELECTABLE
            )
        return super().flags(index)

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        return [
            treeitem.TreeItem(obj=i)
            for i in item.obj.findChildren(
                self.BaseClass, None, QtCore.Qt.FindChildOption.FindDirectChildrenOnly
            )
        ]

    def _has_children(self, item: treeitem.TreeItem) -> bool:
        return bool(
            item.obj.findChildren(
                self.BaseClass, None, QtCore.Qt.FindChildOption.FindDirectChildrenOnly
            )
        )


class LayoutHierarchyModel(WidgetHierarchyModel):
    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        match item.obj:
            case (
                QtWidgets.QSplitter()
                | QtWidgets.QToolBox()
                | QtWidgets.QStackedWidget()
                | QtWidgets.QTabWidget()
            ):
                items = [item.obj.widget(i) for i in range(item.obj.count())]
            case QtWidgets.QWidget():
                layout = item.obj.layout()
                items = [layout.itemAt(i) for i in range(layout.count())]
                items = [w if (w := i.widget()) else i.layout() for i in items]
            case QtWidgets.QLayout():
                layout = item.obj
                items = [layout.itemAt(i) for i in range(layout.count())]
                items = [w if (w := i.widget()) else i.layout() for i in items]
            case _:
                raise ValueError(item)
        return [treeitem.TreeItem(obj=i) for i in items]

    def _has_children(self, item: treeitem.TreeItem) -> bool:
        match item.obj:
            case QtWidgets.QSplitter():
                return item.obj.count() > 0
            case _:
                layout = item.obj.layout()
                return False if layout is None else layout.count() > 0


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    widget = debugging.example_widget()

    model = WidgetHierarchyModel(widget, show_root=True, parent=view)
    view.set_model(model)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("variant")
    view.resize(1000, 1000)
    view.show()
    widget.show()
    with app.debug_mode():
        app.exec()
