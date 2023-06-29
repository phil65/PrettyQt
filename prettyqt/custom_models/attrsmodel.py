from __future__ import annotations

from collections.abc import Sequence
import logging

import attrs

from prettyqt import custom_models
from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class AttrsModel(custom_models.BaseDataclassModel):
    def __init__(self, items: Sequence[datatypes.IsAttrs], **kwargs):
        super().__init__(items, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (datatypes.IsAttrs(), *_):
                return True
            case _:
                return False

    def get_fields(self):
        return list(attrs.fields(self.Class))


if __name__ == "__main__":
    from prettyqt import widgets

    @attrs.define
    class BaseSetting:
        name: str
        label: str
        description: str
        requires_restart: bool = False

    @attrs.define(frozen=True)
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
    model = AttrsModel(items, parent=view)
    view.set_model(model)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("variant")
    view.resize(1000, 1000)
    with app.debug_mode():
        view.show()
        app.exec()
