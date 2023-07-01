from __future__ import annotations

import dataclasses
import logging

from typing import Any

from prettyqt import constants, core, custom_models
from prettyqt.qt import QtGui
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
    def supports(cls, instance) -> bool:
        return isinstance(instance, datatypes.IsDataclass)

    def get_fields(self, instance: datatypes.IsDataclass) -> dict[str, Any]:
        fields = dataclasses.fields(instance)
        return {field.name: field for field in fields}

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        field_name = self._field_names[index.row()]
        field = self._fields[field_name]
        match role, index.column():
            case constants.FONT_ROLE, 0:
                font = QtGui.QFont()
                font.setBold(True)
                return font
            case constants.DISPLAY_ROLE, 0:
                return repr(getattr(self._instance, field_name))
            case constants.EDIT_ROLE, 0:
                return getattr(self._instance, field_name)
            case constants.DISPLAY_ROLE, 1:
                return field.type
            case constants.FONT_ROLE, 1:
                font = QtGui.QFont()
                font.setItalic(True)
                return font
            case constants.DISPLAY_ROLE, 2:
                return field.default
            case constants.CHECKSTATE_ROLE, 3:
                return self.to_checkstate(field.init)
            case constants.CHECKSTATE_ROLE, 4:
                return self.to_checkstate(field.repr)
            case constants.CHECKSTATE_ROLE, 5:
                return self.to_checkstate(field.compare)
            case constants.CHECKSTATE_ROLE, 6:
                return self.to_checkstate(field.hash)
            case constants.DISPLAY_ROLE, 7:
                return str(field.metadata)
            case constants.CHECKSTATE_ROLE, 8:
                return self.to_checkstate(field.kw_only)
            case constants.USER_ROLE, _:
                return getattr(self._instance, field_name)

    def _is_writable(self, field_name: str) -> bool:
        return not self._instance.__dataclass_params__.frozen


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
        app.exec()
