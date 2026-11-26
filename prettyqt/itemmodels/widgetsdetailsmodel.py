from collections.abc import Sequence
import logging

from prettyqt import constants, core
from prettyqt.utils import classhelpers


logger = logging.getLogger(__name__)


class WidgetsDetailsModel(core.AbstractTableModel):
    SUPPORTS = Sequence[core.QObject]

    def __init__(self, items: Sequence[core.QObject], **kwargs):
        super().__init__(**kwargs)
        self.items = items
        common_ancestor = classhelpers.find_common_ancestor([type(i) for i in self.items])
        logger.debug("%s: found common ancestor %s", type(self).__name__, common_ancestor)
        metaobject = common_ancestor.staticMetaObject  # ty: ignore[missing-attribute]
        self.props = core.MetaObject(metaobject).get_properties(only_stored=True)
        self.props.sort(key=lambda x: x.get_name())

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (core.QObject(), *_):
                return True
            case _:
                return False

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self.props)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.VERTICAL, constants.DISPLAY_ROLE if section < len(self.items):
                return repr(self.items[section])
            case constants.HORIZONTAL, constants.DISPLAY_ROLE if section < len(
                self.props
            ):
                return self.props[section].get_name()
        return None

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        prop = self.props[index.column()]
        widget = self.items[index.row()]
        value = prop.read(widget)
        match role:
            case constants.CHECKSTATE_ROLE if isinstance(value, bool):
                return self.to_checkstate(value)
            case constants.DISPLAY_ROLE if not isinstance(value, bool):
                return self.to_display_text(value)
            case constants.EDIT_ROLE | constants.USER_ROLE:
                return value
        return None

    def setData(
        self,
        index: core.ModelIndex,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return False
        prop = self.props[index.column()]
        widget = self.items[index.row()]
        match role:
            case constants.USER_ROLE | constants.EDIT_ROLE:
                pass
            case constants.CHECKSTATE_ROLE:
                value = self.from_checkstate(value)
            case _:
                return False
        if not prop.write(widget, value):
            return False
        self.dataChanged.emit(index, index)
        return True

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self.items)

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        flags = super().flags(index)
        if not index.isValid():
            return flags
        prop = self.props[index.column()]
        if not prop.isWritable():
            return flags
        if prop.get_python_type() is bool:
            return flags | constants.IS_CHECKABLE
        return flags | constants.IS_EDITABLE


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TableView()
    view.set_icon("mdi.folder")
    items = [widgets.TableWidget(), widgets.TableWidget()]
    model = WidgetsDetailsModel(items, parent=view)
    view.set_model(model)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("editor")
    view.resize(1000, 1000)
    with app.debug_mode():
        view.show()
        app.exec()
