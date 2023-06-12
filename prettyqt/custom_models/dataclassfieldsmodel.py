from __future__ import annotations

import dataclasses
import logging

from prettyqt import constants, core
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import datatypes

logger = logging.getLogger(__name__)


class DataClassFieldsModel(core.AbstractTableModel):
    HEADER = [
        "Field name",
        "Value",
        "Type",
        "Default",
        "In __init__",
        "In __repr__",
        "Compare",
        "Hash",
        "Metadata",
        "Keyword only",
    ]

    def __init__(self, instance: datatypes.IsDataclass, **kwargs):
        self._instance = instance
        self._fields = dataclasses.fields(instance)
        self.event_catcher = None
        super().__init__(**kwargs)
        self.set_instance(instance)

    def set_instance(self, instance):
        self._instance = instance
        self._fields = dataclasses.fields(instance)
        self.update_all()

    def columnCount(self, parent=None) -> int:
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
                return str(section)

    def data(self, index: QtCore.QModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        field = self._fields[index.row()]
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return field.name
            case constants.FONT_ROLE, 0:
                font = QtGui.QFont()
                font.setBold(True)
                return font
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, 1:
                return getattr(self._instance, field.name)
            case constants.DISPLAY_ROLE, 2:
                return field.type
            case constants.FONT_ROLE, 2:
                font = QtGui.QFont()
                font.setItalic(True)
                return font
            case constants.DISPLAY_ROLE, 3:
                return field.default
            case constants.CHECKSTATE_ROLE, 4:
                return field.init
            case constants.CHECKSTATE_ROLE, 5:
                return field.repr
            case constants.CHECKSTATE_ROLE, 6:
                return field.compare
            case constants.CHECKSTATE_ROLE, 7:
                return field.hash
            case constants.DISPLAY_ROLE, 8:
                return str(field.metadata)
            case constants.CHECKSTATE_ROLE, 9:
                return field.kw_only
            case constants.USER_ROLE, _:
                return getattr(self._instance, field.name)

    def setData(self, index: QtCore.QModelIndex, value, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        field = self._fields[index.row()]
        match role, index.column():
            case constants.USER_ROLE, _:
                setattr(self._instance, field.name, value)
                self.update_row(index.row())
                return True
        return False

    def rowCount(self, parent: QtCore.QModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self._fields)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        if index.column() == 1 and not self._instance.__dataclass_params__.frozen:
            return super().flags(index) | constants.IS_EDITABLE
        return super().flags(index)


if __name__ == "__main__":
    from prettyqt import widgets

    @dataclasses.dataclass
    class SelectionSetting:
        name: str
        label: str
        description: str
        requires_restart: bool = False
        options: list[str] | None = None
        minimum: float = 0.0
        maximum: float = 0.0
        pattern: str = ""
        requires_restart: bool = False

    app_style = SelectionSetting(
        name="app_style",
        label="App style",
        description="Some longer text",
        options=[],
        requires_restart=True,
    )

    app = widgets.app()
    view = widgets.TableView()
    view.set_icon("mdi.folder")
    with app.debug_mode():
        model = DataClassFieldsModel(app_style)
        model.dataChanged.connect(view.repaint)
        view.set_model(model)
        view.set_selection_behavior("rows")
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("variant", column=1)
        view.show()
        view.resize(500, 300)
        app.main_loop()
