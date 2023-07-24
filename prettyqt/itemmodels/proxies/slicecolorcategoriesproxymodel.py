from __future__ import annotations

import enum
import itertools
import logging

from typing import Literal

from prettyqt import constants, core, gui, itemmodels
from prettyqt.utils import bidict


logger = logging.getLogger(__name__)

ColorModeStr = Literal["all", "visible", "seen", "range"]


class ColorMode(enum.IntEnum):
    All = 1
    Visible = 2
    Seen = 3
    Range = 4


COLOR_MODE = bidict(
    all=ColorMode.All,
    visible=ColorMode.Visible,
    seen=ColorMode.Seen,
    range=ColorMode.Range,
)


class SliceColorCategoriesProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model to apply coloring to categories.

    ### Example

    ```py
    model = MyModel()
    table = widgets.TableView()
    table.set_model(model)
    table[:, :3].proxify.color_categories()
    table.show()
    # or
    indexer = (slice(None), slice(None, 3))
    proxy = itemmodels.SliceColorCategoriesProxyModel(indexer=indexer)
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "color_categories"
    ICON = "mdi.palette-outline"

    def __init__(self, *args, **kwargs):
        self._role = constants.DISPLAY_ROLE
        self._color_map = {}
        self.color_generator = itertools.cycle(gui.Palette().iter_colors())
        self._color_none = False
        self._cast_to_str = False
        super().__init__(*args, **kwargs)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not self.indexer_contains(index):
            return super().data(index, role)
        match role:
            case constants.BACKGROUND_ROLE:
                return self.get_color_for_index(index)
            case _:
                return super().data(index, role)

    def get_color_for_index(self, index):
        value = super().data(index, self._role)
        key = str(value) if self._cast_to_str else value
        match value:
            case None if not self._color_none:
                return None
            case _:
                if key in self._color_map:
                    return self._color_map[key]
                new = next(self.color_generator)
                self._color_map[key] = new
                return self._color_map[key]

    def is_none_colored(self) -> bool:
        return self._color_none

    def set_none_colored(self, val: bool):
        with self.change_layout():
            self._color_none = val

    def is_casted_to_str(self) -> bool:
        return self._cast_to_str

    def set_cast_to_str(self, val: bool):
        with self.change_layout():
            self._color_map = {}
            self.color_generator = itertools.cycle(gui.Palette().iter_colors())
            self._cast_to_str = val

    color_none = core.Property(
        bool,
        is_none_colored,
        set_none_colored,
        doc="Whether None-values should also get colored",
    )
    """Color ItemData with value `None`."""

    cast_to_str = core.Property(
        bool,
        is_casted_to_str,
        set_cast_to_str,
        doc="Cast values to string in order to color / group them",
    )
    """Cast all values to a string for deciding whether cells are in same category."""


if __name__ == "__main__":
    import random

    from prettyqt import debugging, widgets

    app = widgets.app()

    val_range = range(0, 50, 10)
    data = dict(
        a=random.sample(val_range, k=5),
        b=random.sample(val_range, k=5),
        c=random.sample(val_range, k=5),
    )
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.proxifier[:, :].color_categories()
    table.set_size_adjust_policy("content")
    table.setWindowTitle("Color values")
    table.set_icon("mdi.palette")
    # table.show()
    table.adjustSize()
    widget = debugging.ProxyComparerWidget(table.model())

    widget.show()
    with app.debug_mode():
        app.exec()
