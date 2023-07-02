from __future__ import annotations

from collections.abc import Sequence
import logging

import pydantic

from prettyqt import constants, core, custom_models


logger = logging.getLogger(__name__)


class PydanticModel(custom_models.BaseDataclassModel):
    def __init__(self, items: Sequence[pydantic.BaseModel], **kwargs):
        super().__init__(items, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (pydantic.BaseModel(), *_):
                return True
            case _:
                return False

    def get_fields(self) -> list:
        return self.Class.model_fields

    def flags(self, parent: core.ModelIndex) -> constants.ItemFlag:
        if not parent.isValid():
            return super().flags(parent)
        if self.Class.model_config.get("frozen"):
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
    with app.debug_mode():
        items = [
            BaseSetting(name=f"test{i}", label="some label", description="jhaj")
            for i in range(5)
        ]
        view = widgets.TableView()
        view.set_icon("mdi.folder")
        model = PydanticModel(items, parent=view)
        view.set_model(model)
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("variant")
        view.resize(1000, 1000)
        view.show()
        app.exec()
