from __future__ import annotations

import logging

from prettyqt import constants, core, eventfilters
from prettyqt.qt import QtGui, QtWidgets

logger = logging.getLogger(__name__)


class WidgetPropertiesModel(core.AbstractTableModel):
    HEADER = [
        "Property name",
        "Value",
        "Type",
        "User property",
        "Readable",
        "Writable",
        "Resettable",
        "Bindable",
        "Designable",
        "Constant",
        "Final",
        "Required",
        "Valid",
        "Stored",
        "Notifier",
        "User Type",
        # "Enumerator",
    ]

    def __init__(self, widget: QtWidgets.QWidget, **kwargs):
        self._widget = None
        self._metaobj = None
        self.event_catcher = None
        self._handles: list[core.QMetaObject.Connection] = []
        super().__init__(**kwargs)
        self.set_widget(widget)

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, QtWidgets.QWidget)

    def set_widget(self, widget):
        if self._widget:
            self.unhook()
        self._widget = widget
        self._metaobj = core.MetaObject(self._widget.metaObject())
        self.event_catcher = eventfilters.EventCatcher(
            include=["resize", "move"], parent=self._widget
        )
        logger.debug(f"Connected {self._widget!r} to {self!r}")
        self.event_catcher.caught.connect(self.force_layoutchange)
        self._widget.installEventFilter(self.event_catcher)
        self._handles = self._metaobj.connect_signals(
            self._widget, self.force_layoutchange, only_notifiers=True
        )
        self.update_all()

    def unhook(self):
        for handle in self._handles:
            self._widget.disconnect(handle)
        self._widget.removeEventFilter(self.event_catcher)
        logger.debug(f"Disconnected {self._widget!r} from {self!r}")

    def columnCount(self, parent=None) -> int:
        return len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self.HEADER[section]
            case constants.VERTICAL, constants.DISPLAY_ROLE:
                prop = self._metaobj.get_property(section)
                return prop.propertyIndex()

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        prop = self._metaobj.get_property(index.row())
        match role, index.column():
            case constants.BACKGROUND_ROLE, _:
                return QtGui.QColor("lightblue") if prop.isUser() else None
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
            case constants.CHECKSTATE_ROLE, 7:
                return prop.isBindable()
            case constants.CHECKSTATE_ROLE, 8:
                return prop.isDesignable()
            case constants.CHECKSTATE_ROLE, 9:
                return prop.isConstant()
            case constants.CHECKSTATE_ROLE, 10:
                return prop.isFinal()
            case constants.CHECKSTATE_ROLE, 11:
                return prop.isRequired()
            case constants.CHECKSTATE_ROLE, 12:
                return prop.isValid()
            case constants.CHECKSTATE_ROLE, 13:
                return prop.isStored()
            case constants.DISPLAY_ROLE, 14:
                notifier = prop.get_notify_signal()
                return "" if notifier is None else notifier.get_name()
            case constants.DISPLAY_ROLE, 15:
                return prop.userType()
            # case constants.DISPLAY_ROLE, 8:
            #     enumerator = prop.get_enumerator()
            #     return "" if enumerator is None else enumerator.get_name()
            case constants.USER_ROLE, _:
                return prop.read(self._widget)

    def setData(
        self,
        index: core.ModelIndex,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return None
        prop = self._metaobj.get_property(index.row())
        match role, index.column():
            case constants.USER_ROLE | constants.EDIT_ROLE, _:
                prop.write(self._widget, value)
                self.update_row(index.row())
                return True
        return False

    def rowCount(self, parent: core.QModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else self._metaobj.propertyCount()

    def flags(self, index: core.QModelIndex) -> constants.ItemFlag:
        prop = self._metaobj.get_property(index.row())
        if index.column() == 1 and prop.isWritable():
            return super().flags(index) | constants.IS_EDITABLE
        return super().flags(index)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    widget = debugging.example_widget()
    view = widgets.TableView()
    view.set_icon("mdi.folder")
    with app.debug_mode():
        model = WidgetPropertiesModel(widget)
        model.dataChanged.connect(view.repaint)
        view.set_model(model)
        view.set_selection_behavior("rows")
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("variant", column=1)
        view.show()
        widget.show()
        view.resize(500, 300)
        app.exec()
