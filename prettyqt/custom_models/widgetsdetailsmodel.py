from __future__ import annotations

from collections.abc import Sequence

from prettyqt import constants, core
from prettyqt.qt import QtCore, QtWidgets


class WidgetsDetailsModel(core.AbstractTableModel):
    def __init__(self, items: Sequence[QtWidgets.QWidget], **kwargs):
        super().__init__(**kwargs)
        self.items = items
        self._metaobj = widgets.Widget.get_static_metaobject()

    def columnCount(self, parent=None):
        return widgets.Widget.get_static_metaobject().propertyCount()

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole,
    ) -> str | None:
        match orientation, role, section:
            case constants.VERTICAL, constants.DISPLAY_ROLE, _:
                widget = self.items[section]
                return repr(widget)
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self._metaobj.get_property(section).get_name()

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        prop = self._metaobj.get_property(index.column())
        widget = self.items[index.row()]
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                return prop.read(widget)
            case constants.USER_ROLE:
                return prop.read(widget)

    def setData(self, index, value, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        prop = self._metaobj.get_property(index.column())
        widget = self.items[index.row()]
        match role:
            case constants.USER_ROLE:
                prop.write(widget, value)
                self.update_row(index.row())

    def rowCount(self, parent=None):
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self.items)

    def flags(self, index):
        prop = self._metaobj.get_property(index.column())
        if prop.isWritable():
            return (
                super().flags(index)
                | constants.IS_EDITABLE
                | constants.IS_ENABLED
                | constants.IS_SELECTABLE
            )
        return super().flags(index)


if __name__ == "__main__":
    import logging
    import sys

    from prettyqt import widgets
    from prettyqt.custom_delegates import variantdelegate

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    app = widgets.app()
    view = widgets.TableView()
    view.set_icon("mdi.folder")
    items = [widgets.RadioButton(), widgets.Widget()]
    model = WidgetsDetailsModel(items).transpose()
    delegate = variantdelegate.VariantDelegate(parent=view)
    view.set_model(model)
    view.set_selection_behavior("rows")
    view.setEditTriggers(
        view.EditTrigger.DoubleClicked | view.EditTrigger.SelectedClicked
    )
    view.set_delegate(delegate)
    view.show()
    view.resize(500, 300)
    with app.debug_mode():
        app.main_loop()
