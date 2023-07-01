from __future__ import annotations

from collections.abc import Callable
import dataclasses
import logging

from typing import Any

from prettyqt import constants, core, custom_models


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Transformer:
    fn: Callable[[Any], Any]
    role: int | constants.ItemDataRole
    selector: Callable[[Any], bool]
    selector_role: int | constants.ItemDataRole


class SliceValueTransformationProxyModel(custom_models.SliceIdentityProxyModel):
    """A proxy model which transforms cell contents based on a Callable.

    Example:
    ```py
    model = MyModel()
    table = widgets.TableView()
    table.set_model(model)
    table.proxifier[::2, 2:].modify(xyz)
    table.show()
    ```

    or

    ```py
    indexer = (slice(None, None, 2), slice(2, None))
    proxy = custom_models.SliceValueTransformationProxyModel(indexer=indexer)
    proxy.set_source_model(model)
    proxy.add_transformer(lambda x: x + "something", selector=lambda x: "abc" in x)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "value_transformation"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._transformers: list[Transformer] = []

    def clear(self):
        """Clear all transformers."""
        self._transformers = []

    def add_transformer(
        self,
        fn: Callable[[Any], Any],
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        selector: Callable[[Any], bool] | None = None,
        selector_role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        """Add a transformer for given role.

        If a selector callable is given, the transformer will only be applied if the
        selector returns True.
        The selector receives the content of given data role as an argument.

        Arguments:
            fn: Callable to transform data of given role
            role: Data role to transform
            selector: Callable to filter the indexes which should be transformed
            selector_role: Role to use for the selector callable
        """
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
    model.add_transformer(lambda x: f"{x}test")
    model.add_transformer(
        lambda x: QtGui.QColor("red"),
        role=constants.BACKGROUND_ROLE,
        selector=lambda x: True,
    )
    model.set_column_slice(slice(0, 2))
    view.show()
    with app.debug_mode():
        app.exec()
