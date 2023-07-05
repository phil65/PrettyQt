from __future__ import annotations

import logging

import attr
import attrs

from prettyqt import constants, core, custom_models, gui
from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class AttrsFieldsModel(custom_models.BaseFieldsModel):
    """Table model to display the fields and their metadata of an dataclass.

    More information about attrs can be found [here](https://www.attrs.org/).

    Frozen dataclasses are read-only, otherwise the data can be modified.

    !!! info
        For being able to edit more types, using the
        [EditorDelegate](/features/delegates/editordelegate.md) is recommended.
    """

    HEADER = [
        "Value",
        "Type",
        "Default",
        "Metadata",
        "In __init__",
        "In __repr__",
        "Eq",
        "Hash",
        "Keyword only",
        "Inherited",
        "Validator",
    ]

    def __init__(self, instance: datatypes.IsAttrs, **kwargs):
        super().__init__(instance, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, datatypes.IsAttrs)

    def get_fields(self, instance: datatypes.IsAttrs):
        fields = attrs.fields(type(instance))
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
        value = getattr(self._instance, field_name)
        match role, index.column():
            case constants.FONT_ROLE, 0:
                font = gui.QFont()
                font.setBold(True)
                return font
            case constants.DISPLAY_ROLE, 0:
                return repr(value)
            case constants.EDIT_ROLE, 0:
                return value
            case constants.DISPLAY_ROLE, 1:
                return field.type
            case constants.FONT_ROLE, 1:
                font = gui.QFont()
                font.setItalic(True)
                return font
            case constants.DISPLAY_ROLE, 2:
                return field.default
            case constants.DISPLAY_ROLE, 3:
                return str(field.metadata)
            case constants.EDIT_ROLE, 3:
                return field.metadata
            case constants.CHECKSTATE_ROLE, 4:
                return self.to_checkstate(field.init)
            case constants.CHECKSTATE_ROLE, 5:
                return self.to_checkstate(field.repr)
            case constants.CHECKSTATE_ROLE, 6:
                return self.to_checkstate(field.eq)
            case constants.CHECKSTATE_ROLE, 7:
                return self.to_checkstate(field.hash)
            case constants.CHECKSTATE_ROLE, 8:
                return self.to_checkstate(field.kw_only)
            case constants.CHECKSTATE_ROLE, 9:
                return self.to_checkstate(field.inherited)
            case constants.CHECKSTATE_ROLE, 10:
                return self.to_checkstate(field.validator is not None)
            case constants.USER_ROLE, _:
                return value

    def _is_writable(self, field_name: str) -> bool:
        # return all(
        #     base_cls.__setattr__ is not attr._make._frozen_setattrs
        #     for base_cls in type(self._instance).__bases__
        # )
        return not attr._make._has_frozen_base_class(type(self._instance))

    def flags(self, index: core.ModelIndex):
        match index.column():
            case 0 | 1 | 2 | 3:
                return super().flags(index)
            case _:
                return super().flags(index) & ~constants.IS_ENABLED


if __name__ == "__main__":
    from prettyqt import widgets

    @attrs.define
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
        model = AttrsFieldsModel(app_style)
        print(dir(app_style))
        print(dir(app_style.__attrs_attrs__))
        model.dataChanged.connect(view.repaint)
        view.set_model(model)
        view.set_selection_behavior("rows")
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("editor", column=0)
        view.show()
        view.resize(500, 300)
        app.exec()
