from __future__ import annotations

from collections.abc import Sequence
import logging

from prettyqt import constants, core
from prettyqt.qt import QtWidgets
from prettyqt.utils import helpers


logger = logging.getLogger(__name__)


class WidgetsDetailsModel(core.AbstractTableModel):
    def __init__(self, items: Sequence[QtWidgets.QWidget], **kwargs):
        super().__init__(**kwargs)
        self.items = items
        common_ancestor = helpers.find_common_ancestor([type(i) for i in self.items])
        logger.debug(f"{type(self).__name__}: found common ancestor {common_ancestor}")
        self.props = core.MetaObject(common_ancestor.staticMetaObject).get_properties(
            only_stored=True
        )
        self.props.sort(key=lambda x: x.get_name())

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (QtWidgets.QWidget(), *_):
                return True
            case _:
                return False

    def columnCount(self, parent: core.ModelIndex | None = None):
        return len(self.props)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role, section:
            case constants.VERTICAL, constants.DISPLAY_ROLE, _:
                widget = self.items[section]
                return repr(widget)
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.props[section].get_name()

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
        if isinstance(value, bool) and role == constants.CHECKSTATE_ROLE:
            return self.to_checkstate(value)
        match role:
            case (
                constants.DISPLAY_ROLE | constants.EDIT_ROLE | constants.USER_ROLE
            ) if not isinstance(value, bool):
                return value

    def setData(
        self,
        index: core.ModelIndex,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        prop = self.props[index.column()]
        widget = self.items[index.row()]
        match role:
            case constants.USER_ROLE | constants.EDIT_ROLE:
                with self.reset_model():
                    prop.write(widget, value)
                # self.update_row(index.row())
                return True
            case constants.CHECKSTATE_ROLE:
                with self.reset_model():
                    prop.write(widget, bool(value))
                # self.update_row(index.row())
                return True
        return False

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self.items)

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        prop = self.props[index.column()]
        if prop.isWritable() and prop.get_python_type() is bool:
            return super().flags(index) | constants.IS_CHECKABLE
        if prop.isWritable():
            return super().flags(index) | constants.IS_EDITABLE
        return constants.IS_SELECTABLE


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
