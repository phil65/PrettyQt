from __future__ import annotations

import attrs
import logging

from prettyqt import constants, custom_models
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import datatypes

logger = logging.getLogger(__name__)


class AttrsFieldsModel(custom_models.BaseFieldsModel):
    HEADER = [
        "Field name",
        "Value",
        "Type",
        "Default",
        "In __init__",
        "In __repr__",
        "Eq",
        "Hash",
        "Metadata",
        "Keyword only",
        "Inherited",
        "Validator",
    ]

    def __init__(self, instance: datatypes.IsAttrs, **kwargs):
        super().__init__(instance, **kwargs)

    def get_fields(self, instance: datatypes.IsAttrs):
        return attrs.fields(type(instance))

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
                return field.eq
            case constants.CHECKSTATE_ROLE, 7:
                return field.hash
            case constants.DISPLAY_ROLE, 8:
                return str(field.metadata)
            case constants.CHECKSTATE_ROLE, 9:
                return field.kw_only
            case constants.CHECKSTATE_ROLE, 10:
                return field.inherited
            case constants.CHECKSTATE_ROLE, 11:
                return field.validator is not None
            case constants.USER_ROLE, _:
                return getattr(self._instance, field.name)


if __name__ == "__main__":
    from prettyqt import widgets

    @attrs.define(frozen=True)
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
        model = AttrsFieldsModel(app_style)
        print(dir(app_style))
        print(dir(app_style.__attrs_attrs__))
        model.dataChanged.connect(view.repaint)
        view.set_model(model)
        view.set_selection_behavior("rows")
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("variant", column=1)
        view.show()
        view.resize(500, 300)
        app.main_loop()
