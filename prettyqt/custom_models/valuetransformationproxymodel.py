from __future__ import annotations

import dataclasses
import logging
from typing import Any

from collections.abc import Callable

from prettyqt import constants, core, custom_models
from prettyqt.qt import QtCore

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Transformer:
    fn: Callable[[Any], Any]
    role: int | QtCore.Qt.ItemDataRole
    selector: Callable[[Any], bool]
    selector_role: int | QtCore.Qt.ItemDataRole


class ValueTransformationProxyModel(custom_models.SliceIdentityProxyModel):
    """A simple transformation proxy model with settable transformers.

    Example:
        >>> proxy = ValueTransformationProxyModel()
        >>> proxy.add_transformer(lambda value: value < 1)
    """

    ID = "value_transformation"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._transformers: list[Transformer] = []

    def clear(self):
        self._transformers = []

    def add_transformer(
        self,
        fn: Callable[[Any], Any],
        role: QtCore.Qt.ItemDataRole = constants.DISPLAY_ROLE,
        selector: Callable[[Any], bool] | None = None,
        selector_role: QtCore.Qt.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        tr = Transformer(
            fn=fn,
            role=role,
            selector=selector,
            selector_role=selector_role,
        )
        self._transformers.append(tr)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        val = super().data(index, role)
        for t in self._transformers:
            if self.indexer_contains(index) and t.role == role:
                selector_val = super().data(index, t.selector_role)
                if t.selector is None or t.selector(selector_val):
                    val = t.fn(selector_val)
        return val


if __name__ == "__main__":
    from prettyqt import debugging, widgets
    from prettyqt.qt import QtGui

    app = widgets.app()
    view = debugging.example_table()
    model = view.proxifier.get_proxy("value_transformation")
    model.add_transformer(lambda x: f"{str(x)}test")
    model.add_transformer(
        lambda x: QtGui.QColor("red"),
        role=constants.BACKGROUND_ROLE,
        selector=lambda x: True,
    )
    model.set_column_slice(slice(0, 2))
    view.show()
    with app.debug_mode():
        app.main_loop()
