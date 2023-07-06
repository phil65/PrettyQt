from __future__ import annotations

import enum
import logging

from prettyqt import constants, core, itemmodels
from prettyqt.utils import classhelpers


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


class BaseHierarchyModel(itemmodels.TreeModel):
    class Roles(enum.IntEnum):
        """Custom roles."""

        WidgetRole = constants.USER_ROLE + 23324

    def __init__(
        self,
        obj: type[core.QObject],
        show_root: bool = True,
        parent: core.QObject | None = None,
    ):
        self.BaseClass = None
        self.props = None
        super().__init__(obj=obj, show_root=show_root, parent=parent)
        self.set_base_class("QWidget")

    def set_base_class(self, klass: str | type[core.QObject]):
        if isinstance(klass, str):
            for kls in classhelpers.get_subclasses(core.QObject):
                if kls.__name__ == klass:
                    klass = kls
                    break
            else:
                klass = core.QObject
        with self.reset_model():
            self.BaseClass = klass
            metaobj = klass.staticMetaObject
            self.props = core.MetaObject(metaobj).get_properties(only_stored=True)
            self.props.insert(0, FakeClassNameProp())
            if issubclass(klass, widgets.QWidget):
                self.props.insert(1, FakeLayoutProp())
            self.props.insert(1, FakeUserPropertyNameProp())
            self.props.insert(1, FakeUserPropertyValueProp())

    def get_base_class_name(self) -> str:
        return self.BaseClass.__name__

    def get_base_class(self) -> type[core.QObject]:
        return self.BaseClass

    def columnCount(self, parent=None):
        return len(self.props)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
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
        prop = self.props[index.column()]
        val = prop.read(widget)
        is_bool = isinstance(val, bool)
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE if not is_bool:
                return val
            case constants.CHECKSTATE_ROLE if is_bool:
                return self.to_checkstate(val)
            case constants.USER_ROLE:
                prop = self.props[index.column()]
                return val
            case self.Roles.WidgetRole:
                return widget
            case constants.SIZE_HINT_ROLE:
                return core.QSize(250, 35)

    def setData(
        self,
        index: core.ModelIndex,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        prop = self.props[index.column()]
        widget = self.data_by_index(index).obj
        match role:
            case constants.EDIT_ROLE | constants.USER_ROLE:
                with self.change_layout():
                    prop.write(widget, value)
                # self.update_row(index.row())
                return True
            case constants.CHECKSTATE_ROLE:
                with self.change_layout():
                    prop.write(widget, bool(value))
                return True
        return False

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        prop = self.props[index.column()]
        widget = self.data_by_index(index).obj
        val = prop.read(widget)
        flag = constants.IS_CHECKABLE if isinstance(val, bool) else constants.IS_EDITABLE
        default = super().flags(index)
        return (default | flag) if prop.isWritable() else default

    base_class_name = core.Property(str, get_base_class_name, set_base_class)
    # base_class = core.Property(type, get_base_class, set_base_class, stored=False)


class WidgetHierarchyModel(BaseHierarchyModel):
    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, core.QObject)

    def _fetch_object_children(
        self, item: WidgetHierarchyModel.TreeItem
    ) -> list[WidgetHierarchyModel.TreeItem]:
        return [
            self.TreeItem(obj=i)
            for i in item.obj.findChildren(
                self.BaseClass, None, constants.FindChildOption.FindDirectChildrenOnly
            )
        ]

    def _has_children(self, item: WidgetHierarchyModel.TreeItem) -> bool:
        return bool(
            item.obj.findChildren(
                self.BaseClass, None, constants.FindChildOption.FindDirectChildrenOnly
            )
        )


class LayoutHierarchyModel(BaseHierarchyModel):
    @classmethod
    def supports(cls, instance) -> bool:
        from prettyqt import widgets

        return isinstance(instance, widgets.QWidget)

    def _fetch_object_children(
        self, item: LayoutHierarchyModel.TreeItem
    ) -> list[LayoutHierarchyModel.TreeItem]:
        from prettyqt import widgets

        match item.obj:
            case (
                widgets.QSplitter()
                | widgets.QToolBox()
                | widgets.QStackedWidget()
                | widgets.QTabWidget()
            ):
                items = [item.obj.widget(i) for i in range(item.obj.count())]
            case widgets.QWidget():
                layout = item.obj.layout()
                items = [layout.itemAt(i) for i in range(layout.count())]
                items = [w if (w := i.widget()) else i.layout() for i in items]
            case widgets.QLayout():
                layout = item.obj
                items = [layout.itemAt(i) for i in range(layout.count())]
                items = [w if (w := i.widget()) else i.layout() for i in items]
            case _:
                raise ValueError(item)
        return [self.TreeItem(obj=i) for i in items]

    def _has_children(self, item: LayoutHierarchyModel.TreeItem) -> bool:
        from prettyqt import widgets

        match item.obj:
            case (
                widgets.QSplitter()
                | widgets.QToolBox()
                | widgets.QStackedWidget()
                | widgets.QTabWidget()
                | widgets.QLayout()
            ):
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

    model = WidgetHierarchyModel(widget, parent=view)
    view = debugging.ProxyComparerWidget(model, itemview="tree")
    # view.set_model(model)
    # view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    # view.set_delegate("editor")
    # view.resize(1000, 1000)
    view.show()
    # widget.show()
    with app.debug_mode():
        app.exec()
