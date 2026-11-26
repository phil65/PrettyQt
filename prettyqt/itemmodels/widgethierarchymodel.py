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
        obj: core.QObject,
        show_root: bool = True,
        parent: core.QObject | None = None,
    ):
        # base class needs to be set before the root item gets fetched.
        self._set_base_class("QWidget")
        super().__init__(obj=obj, show_root=show_root, parent=parent)

    def _set_base_class(self, klass: str | type[core.QObject]):
        from prettyqt import widgets

        if isinstance(klass, str):
            for kls in classhelpers.get_subclasses(core.QObject):
                if kls.__name__ == klass:
                    klass = kls
                    break
            else:
                klass = core.QObject
        self.BaseClass = klass
        metaobj = klass.staticMetaObject
        self.props = core.MetaObject(metaobj).get_properties(only_stored=True)
        self.props.insert(0, FakeClassNameProp())
        if issubclass(klass, widgets.QWidget):
            self.props.insert(1, FakeLayoutProp())
        self.props.insert(1, FakeUserPropertyNameProp())
        self.props.insert(1, FakeUserPropertyValueProp())

    def set_base_class(self, klass: str | type[core.QObject]):
        with self.reset_model():
            self._set_base_class(klass)

    def get_base_class_name(self) -> str:
        return self.BaseClass.__name__

    def get_base_class(self) -> type[core.QObject]:
        return self.BaseClass

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        return len(self.props)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE if section < len(
                self.props
            ):
                return self.props[section].get_name()
        return None

    def _read(self, index: core.ModelIndex):
        widget = self.data_by_index(index).obj
        prop = self.props[index.column()]
        # props of the base class cant be read from other objects (like layouts)
        if not isinstance(widget, self.BaseClass) and isinstance(prop, core.MetaProperty):
            return widget, prop, None
        return widget, prop, prop.read(widget)

    def data(  # noqa: PLR0911
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        widget, _prop, val = self._read(index)
        is_bool = isinstance(val, bool)
        match role:
            case constants.DISPLAY_ROLE if not is_bool:
                return self.to_display_text(val)
            case constants.EDIT_ROLE if not is_bool:
                return val
            case constants.CHECKSTATE_ROLE if is_bool:
                return self.to_checkstate(val)
            case constants.USER_ROLE:
                return val
            case self.Roles.WidgetRole:
                return widget
            case constants.SIZE_HINT_ROLE:
                return core.QSize(250, 35)
        return None

    def setData(
        self,
        index: core.ModelIndex,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return False
        widget, prop, _ = self._read(index)
        match role:
            case constants.EDIT_ROLE | constants.USER_ROLE:
                pass
            case constants.CHECKSTATE_ROLE:
                value = self.from_checkstate(value)
            case _:
                return False
        if not prop.isWritable() or prop.write(widget, value) is False:
            return False
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        default = super().flags(index)
        if not index.isValid():
            return default
        _widget, prop, val = self._read(index)
        if val is None or not prop.isWritable():
            return default
        flag = constants.IS_CHECKABLE if isinstance(val, bool) else constants.IS_EDITABLE
        return default | flag

    base_class_name = core.Property(
        str,
        get_base_class_name,
        set_base_class,
        doc="Class to use for the columns.",
    )
    # base_class = core.Property(type, get_base_class, set_base_class, stored=False)


class WidgetHierarchyModel(BaseHierarchyModel):
    """Tree model showing the child tree of a QObject."""

    SUPPORTS = core.QObject

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
    """Tree model showing the layout hierarchy of widgets."""

    SUPPORTS = "widgets.QWidget"

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
            case widgets.QWidget() | widgets.QLayout():
                layout = (
                    item.obj
                    if isinstance(item.obj, widgets.QLayout)
                    else item.obj.layout()
                )
                if layout is None:
                    return []
                layout_items = [layout.itemAt(i) for i in range(layout.count())]
                # spacer items have neither a widget nor a layout, skip them.
                items = [i.widget() or i.layout() for i in layout_items]
            case _:
                raise ValueError(item)
        return [self.TreeItem(obj=i) for i in items if i is not None]

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
            case widgets.QWidget():
                layout = item.obj.layout()
                return False if layout is None else layout.count() > 0
        return False


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
