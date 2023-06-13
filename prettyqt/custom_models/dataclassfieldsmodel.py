from __future__ import annotations

import dataclasses
import logging

from prettyqt import constants, custom_models
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import datatypes

logger = logging.getLogger(__name__)


class DataClassFieldsModel(custom_models.BaseFieldsModel):
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
        super().__init__(instance, **kwargs)

    @classmethod
    def supports(cls, typ):
        return isinstance(typ, datatypes.IsDataclass)

    def get_fields(self, instance: datatypes.IsDataclass):
        return dataclasses.fields(instance)

    def data(self, index: QtCore.QModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        field = self._fields[index.row()]
        match role, index.column():
            case constants.FONT_ROLE, 0:
                font = QtGui.QFont()
                font.setBold(True)
                return font
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, 0:
                return repr(getattr(self._instance, field.name))
            case constants.DISPLAY_ROLE, 1:
                return field.type
            case constants.FONT_ROLE, 1:
                font = QtGui.QFont()
                font.setItalic(True)
                return font
            case constants.DISPLAY_ROLE, 2:
                return field.default
            case constants.CHECKSTATE_ROLE, 3:
                return field.init
            case constants.CHECKSTATE_ROLE, 4:
                return field.repr
            case constants.CHECKSTATE_ROLE, 5:
                return field.compare
            case constants.CHECKSTATE_ROLE, 6:
                return field.hash
            case constants.DISPLAY_ROLE, 7:
                return str(field.metadata)
            case constants.CHECKSTATE_ROLE, 8:
                return field.kw_only
            case constants.USER_ROLE, _:
                return getattr(self._instance, field.name)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        if index.column() == 0 and not self._instance.__dataclass_params__.frozen:
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
        view.set_delegate("variant", column=0)
        view.show()
        view.resize(500, 300)
        app.main_loop()
