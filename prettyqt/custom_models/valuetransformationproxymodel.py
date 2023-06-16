from __future__ import annotations

import dataclasses
import logging
from typing import Any

from collections.abc import Callable

from prettyqt import constants, core
from prettyqt.utils import helpers
from prettyqt.qt import QtCore

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Transformer:
    fn: Callable[[Any], Any]
    role: int | QtCore.Qt.ItemDataRole
    selector: Callable[[Any], bool]
    selector_role: int | QtCore.Qt.ItemDataRole


class ValueTransformationProxyModel(core.IdentityProxyModel):
    """A simple transformation proxy model with settable transformers.

    Example:
        >>> proxy = ValueTransformationProxyModel()
        >>> proxy.add_transformer(lambda value: value < 1)
    """

    ID = "value_transformation"

    def __init__(self, indexer=0, parent=None, **kwargs):
        if isinstance(indexer, int):
            indexer = (indexer, slice(None))
        super().__init__(parent, **kwargs)
        self._indexer = indexer
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

    def data(self, index: core.ModelIndex, role: constants.ItemDataRole):
        val = super().data(index, role)
        for t in self._transformers:
            if (
                helpers.is_position_in_index(index.column(), index.row(), self._indexer)
                and t.role == role
            ):
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
    view.show()
    with app.debug_mode():
        app.main_loop()
