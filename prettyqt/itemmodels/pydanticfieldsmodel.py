from __future__ import annotations

import logging

import pydantic

from prettyqt import constants, core, itemmodels
from prettyqt.qt import QtGui


logger = logging.getLogger(__name__)


class PydanticFieldsModel(itemmodels.BaseFieldsModel):
    """Table model to display the fields and their metadata of a pydantic model.

    More information about pydantic can be found [here][https://www.pydantic.dev/].

    Frozen BaseModels / frozen fields read-only.
    """

    SUPPORTS = pydantic.BaseModel
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
        value = getattr(self._instance, field_name)
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return repr(value)
            case constants.EDIT_ROLE, 0:
                return value
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
                return value

    def _is_writable(self, field_name: str):
        model_frozen = self._instance.model_config.get("frozen")
        field_frozen = self._instance.model_fields[field_name].frozen
        frozen = model_frozen or field_frozen
        return not frozen


if __name__ == "__main__":
    from prettyqt import widgets

    class BaseSetting(pydantic.BaseModel):
        name: str = pydantic.Field("test", frozen=True)
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
        view.set_delegate("editor", column=0)
        view.show()
        view.resize(500, 300)
        app.exec()
