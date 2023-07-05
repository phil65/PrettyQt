from __future__ import annotations

from collections.abc import Sequence
import dataclasses
import logging

from typing import Any

from prettyqt import constants, core, custom_models
from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class DataClassModel(custom_models.BaseDataclassModel):
    """Table model to display a list of dataclasses.

    !!! info
        For being able to edit more types, using the
        [EditorDelegate](/features/delegates/editordelegate.md) is recommended.
    """

    def __init__(self, items: Sequence[datatypes.IsDataclass], **kwargs):
        super().__init__(items, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (datatypes.IsDataclass(), *_):
                return True
            case _:
                return False

    def get_fields(self) -> dict[str, Any]:
        fields = dataclasses.fields(self.Class)
        return {field.name: field for field in fields}

    def flags(self, parent: core.ModelIndex) -> constants.ItemFlag:
        if not parent.isValid():
            return super().flags(parent)
        if self.Class.__dataclass_params__.frozen:
            super().flags(parent)
        field_name = self._field_names[parent.column()]
        instance = self.items[parent.row()]
        # need to cover not parent.isValid()?
        val = getattr(instance, field_name)
        if isinstance(val, bool):
            return super().flags(parent) | constants.IS_CHECKABLE
        else:
            return super().flags(parent) | constants.IS_EDITABLE


if __name__ == "__main__":
    from prettyqt import widgets

    @dataclasses.dataclass
    class BaseSetting:
        name: str
        label: str
        description: str
        requires_restart: bool = False

    @dataclasses.dataclass
    class SelectionSetting(BaseSetting):
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
    items = [BaseSetting(name="test", label="some label", description="jhaj"), app_style]
    klasses = [type(i) for i in items]
    view = widgets.TableView()
    view.set_icon("mdi.folder")
    model = DataClassModel(items, parent=view)
    view.set_model(model)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("editor")
    view.resize(1000, 1000)
    with app.debug_mode():
        view.show()
        app.exec()
