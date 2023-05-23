from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtCore, QtGui, QtWidgets


class WidgetPropertiesModel(core.AbstractTableModel):
    HEADER = [
        "Property name",
        "Value",
        "Type",
        "User property",
        "Readable",
        "Writable",
        "Resettable",
    ]

    def __init__(self, widget: QtWidgets.QWidget, **kwargs):
        super().__init__(**kwargs)
        self._widget = widget
        self._metaobj = core.MetaObject(self._widget.metaObject())

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self.HEADER[section]
            case constants.VERTICAL, constants.DISPLAY_ROLE:
                prop = self._metaobj.get_property(section)
                return prop.propertyIndex()

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        prop = self._metaobj.get_property(index.row())
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return prop.name()
            case constants.FONT_ROLE, 0:
                font = QtGui.QFont()
                font.setBold(True)
                return font
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, 1:
                return prop.read(self._widget)
            case constants.DISPLAY_ROLE, 2:
                return prop.get_meta_type().get_name()
            case constants.FONT_ROLE, 2:
                font = QtGui.QFont()
                font.setItalic(True)
                return font
            case constants.CHECKSTATE_ROLE, 3:
                return prop.isUser()
            case constants.CHECKSTATE_ROLE, 4:
                return prop.isReadable()
            case constants.CHECKSTATE_ROLE, 5:
                return prop.isWritable()
            case constants.CHECKSTATE_ROLE, 6:
                return prop.isResettable()
            case constants.USER_ROLE, _:
                return prop.read(self._widget)

    def setData(self, index, value, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        prop = self._metaobj.get_property(index.row())
        match role, index.column():
            case constants.USER_ROLE, _:
                prop.write(self._widget, value)
                self.update_row(index.row())
                return True
        return False

    def rowCount(self, parent=None):
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else self._metaobj.propertyCount()

    def flags(self, index):
        prop = self._metaobj.get_property(index.row())
        if index.column() == 1 and prop.isWritable():
            return (
                super().flags(index)
                | constants.IS_EDITABLE
                | constants.IS_ENABLED
                | constants.IS_SELECTABLE
            )
        return super().flags(index)


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_delegates import variantdelegate

    app = widgets.app()
    view = widgets.TableView()
    view.set_icon("mdi.folder")
    model = WidgetPropertiesModel(view)
    model.dataChanged.connect(view.repaint)
    delegate = variantdelegate.VariantDelegate(parent=view)
    view.set_model(model)
    view.set_selection_behavior("rows")
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate(delegate, column=1)
    view.show()
    view.resize(500, 300)
    with app.debug_mode():
        app.main_loop()