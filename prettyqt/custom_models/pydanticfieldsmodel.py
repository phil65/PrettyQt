from __future__ import annotations

import logging

import pydantic

from prettyqt import constants, core, custom_models
from prettyqt.qt import QtGui


logger = logging.getLogger(__name__)


class PydanticFieldsModel(custom_models.BaseFieldsModel):
    HEADER = [
        "Value",
        "Type",
        "Default",
        "Frozen",
        "Alias",
        "in repr",
    ]

    def __init__(self, instance: pydantic.BaseModel, **kwargs):
        super().__init__(instance, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, pydantic.BaseModel)

    def get_fields(self, instance: pydantic.BaseModel):
        return instance.model_fields

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
            case constants.DISPLAY_ROLE, 0:
                return repr(getattr(self._instance, field_name))
            case constants.EDIT_ROLE, 0:
                return getattr(self._instance, field_name)
            case constants.FONT_ROLE, 0:
                font = QtGui.QFont()
                font.setBold(True)
                return font
            case constants.DISPLAY_ROLE, 1:
                return repr(field.annotation)
            case constants.FONT_ROLE, 1:
                font = QtGui.QFont()
                font.setItalic(True)
                return font
            case constants.DISPLAY_ROLE, 2:
                return field.default
            case constants.CHECKSTATE_ROLE, 3:
                return self.to_checkstate(bool(field.frozen))
            case constants.DISPLAY_ROLE, 4:
                return field.alias
            case constants.CHECKSTATE_ROLE, 5:
                return self.to_checkstate(field.repr)
            case constants.USER_ROLE, _:
                return getattr(self._instance, field_name)


if __name__ == "__main__":
    from prettyqt import widgets

    class BaseSetting(pydantic.BaseModel):
        name: str
        label: str
        description: str
        requires_restart: bool = False
        options: list[str] | None = None
        minimum: float = 0.0
        maximum: float = 0.0
        pattern: str = ""

    class SelectionSetting(BaseSetting):
        options: list[str] | None = None
        minimum: float = 0.0
        maximum: float = 0.0
        pattern: str = ""
        requires_restart: bool = False

    app_style = BaseSetting(
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
        model = PydanticFieldsModel(app_style, parent=view)
        view.set_model(model)
        view.set_selection_behavior("rows")
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("variant", column=0)
        view.show()
        view.resize(500, 300)
        app.exec()
