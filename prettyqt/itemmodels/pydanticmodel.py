from collections.abc import Sequence
import logging

import pydantic

from prettyqt import itemmodels


logger = logging.getLogger(__name__)


class PydanticModel(itemmodels.BaseDataclassModel):
    """Table model to display a list of [pydantic](https://www.pydantic.dev/) BaseModels.

    Non-frozen fields can be edited.

    !!! note
        This ItemModel only supports Pydantic v2 BaseModels.
    """

    SUPPORTS = Sequence[pydantic.BaseModel]

    def __init__(self, items: Sequence[pydantic.BaseModel], **kwargs):
        super().__init__(items, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (pydantic.BaseModel(), *_):
                return True
            case _:
                return False

    def get_fields(self) -> dict:
        return self.Class.model_fields

    def _is_frozen(self) -> bool:
        return bool(self.Class.model_config.get("frozen"))

    def _is_writable(self, instance, field_name: str, value) -> bool:
        return not (self._is_frozen() or self._fields[field_name].frozen)


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
        view.set_delegate("editor")
        view.resize(1000, 1000)
        view.show()
        app.exec()
