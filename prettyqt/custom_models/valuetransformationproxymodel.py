from __future__ import annotations

import dataclasses
import logging
from typing import Any

from collections.abc import Callable

from prettyqt import constants, core
from prettyqt.qt import QtCore

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Transformer:
    fn: Callable[[Any], Any]
    column: int | None
    row: int | None
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

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._transformers: list[Transformer] = []

    def clear(self):
        self._transformers = []

    def add_transformer(
        self,
        fn: Callable[[Any], Any],
        column: int | None = None,
        row: int | None = None,
        role: QtCore.Qt.ItemDataRole = constants.DISPLAY_ROLE,
        selector: Callable[[Any], bool] | None = None,
        selector_role: QtCore.Qt.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        tr = Transformer(
            fn=fn,
            column=column,
            row=row,
            role=role,
            selector=selector,
            selector_role=selector_role,
        )
        self._transformers.append(tr)

    def data(self, index, role):
        val = super().data(index, role)
        for t in self._transformers:
            if (
                (t.row is None or t.row == index.row())
                and (t.column is None or t.column == index.column())
                and (t.role == role)
            ):
                selector_val = super().data(index, t.selector_role)
                if t.selector is None or t.selector(selector_val):
                    val = t.fn(val)
        return val


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_models import JsonModel
    from prettyqt.qt import QtGui

    app = widgets.app()
    dist = [
        dict(
            assss=2,
            bffff={
                "a": 4,
                "b": [1, 2, 3],
                "jkjkjk": "tekjk",
                "sggg": "tekjk",
                "fdfdf": "tekjk",
                "xxxx": "xxx",
            },
        ),
        6,
        "jkjk",
    ]

    _source_model = JsonModel(dist)
    model = ValueTransformationProxyModel()
    model.add_transformer(lambda x: str(x) + "test")
    model.add_transformer(
        lambda x: QtGui.QColor("red"),
        role=constants.BACKGROUND_ROLE,
        selector=lambda x: isinstance(x, int),
    )
    model.setSourceModel(_source_model)
    table = widgets.TreeView()
    table.setRootIsDecorated(True)
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.main_loop()
