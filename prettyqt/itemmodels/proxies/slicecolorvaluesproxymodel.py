from __future__ import annotations

import enum
import logging
from typing import TYPE_CHECKING, Literal

from prettyqt import constants, core, gui, itemmodels
from prettyqt.utils import bidict, colors, helpers


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


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


class SliceColorValuesProxyModel(itemmodels.SliceIdentityProxyModel):
    """Model to color cells of a numerical table based on their value.

    By default, "high" numbers are colored red, "low" are colored green.

    Possible modes are:
    * All: Highlight all cells within given slice
    * Column: Highlight all cells of same column as current if cell is within given slice.
    * Row: Highlight all cells of same row as current if cell is within given slice.

    The last two modes have the advantage that nothing needs to be computed in advance,
    min/max values are calculated on-the fly.

    ### Example

    ```py
    model = MyModel()
    table = widgets.TableView()
    table.set_model(model)
    table[:, :3].proxify.color_values(mode="all")
    table.show()
    # or
    indexer = (slice(None), slice(None, 3))
    proxy = itemmodels.SliceColorValuesProxyModel(indexer=indexer)
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```

    === "Without proxy"

        ```py
        val_range = range(0, 100, 10)
        data = dict(
            a=random.sample(val_range, k=10),
            b=random.sample(val_range, k=10),
            c=random.sample(val_range, k=10),
        )
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        # table.proxifier[:, :].color_values()
        ```
        <figure markdown>
          ![Image title](../../images/slicecolorvaluesproxymodel_before.png)
        </figure>

    === "With proxy"

        ```py
        val_range = range(0, 100, 10)
        data = dict(
            a=random.sample(val_range, k=10),
            b=random.sample(val_range, k=10),
            c=random.sample(val_range, k=10),
        )
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        table.proxifier[:, :].color_values()
        ```
        <figure markdown>
          ![Image title](../../images/slicecolorvaluesproxymodel_after.png)
        </figure>


    """

    ID = "color_values"
    ICON = "mdi.palette-outline"
    ColorMode = ColorMode
    core.Enum(ColorMode)

    def __init__(self, *args, mode: ColorMode = ColorMode.Visible, **kwargs):
        self._mode = mode
        self._low_color = gui.QColor("green")
        self._high_color = gui.QColor("red")
        super().__init__(*args, **kwargs)
        self._max = 0.0
        self._role = constants.EDIT_ROLE
        self._last_span = ((-1, -1), (-1, -1))

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"colorMode": COLOR_MODE}
        return maps

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not self.indexer_contains(index):
            return super().data(index, role)
        val = super().data(index, self._role)
        match role:
            case constants.BACKGROUND_ROLE if isinstance(val, int | float):
                return self.get_color_for_index(index)
            case _:
                return super().data(index, role)

    def get_color_for_index(self, index: core.ModelIndex) -> gui.QColor:
        match self._mode:
            case self.ColorMode.Seen:
                data = index.data(self._role)
                new_max = max(self._max, abs(data))
                if new_max != self._max:
                    self._max = new_max
                    self.update_all()
                value = data / self._max
                return self.get_color_for_value(abs(value))
            case self.ColorMode.Visible:
                widget = self.parent()
                h_span = widget.get_visible_section_span("horizontal")
                v_span = widget.get_visible_section_span("vertical")
                if (span := (h_span, v_span)) != self._last_span:
                    self._last_span = span
                    model = self.sourceModel()
                    # TODO: we probably should clamp based on self._indexer.
                    delegator = model[v_span[0] : v_span[1], h_span[0] : h_span[1]]
                    data = delegator.data(self._role)
                    data = [i for i in data if isinstance(i, int | float)]
                    max_ = max(data) if data else 1.0
                    self._max = max_
                    top_left = self.index(v_span[0], h_span[0])
                    bottom_right = self.index(v_span[1], h_span[1])
                    # or do we need to update_all()?
                    self.dataChanged.emit(top_left, bottom_right)
                else:
                    max_ = self._max
                data = abs(index.data(self._role))
                max_ = abs(max(abs(max_), data))
                return self.get_color_for_value(data / max_)

    def get_color_for_value(self, value: float) -> gui.QColor:
        col = helpers.get_color_percentage(
            self._low_color.getRgb(), self._high_color.getRgb(), value * 100
        )
        return gui.QColor(*col)

    def set_low_color(self, color: datatypes.ColorType):
        self._low_color = colors.get_color(color).as_qt()

    def set_high_color(self, color: datatypes.ColorType):
        self._high_color = colors.get_color(color).as_qt()

    def get_low_color(self) -> gui.QColor:
        return self._low_color

    def get_high_color(self) -> gui.QColor:
        return self._high_color

    def set_color_mode(self, mode: SliceColorValuesProxyModel.ColorMode | ColorModeStr):
        self._mode = COLOR_MODE.get_enum_value(mode)

    def get_color_mode(self) -> SliceColorValuesProxyModel.ColorMode:
        return self._mode

    color_mode = core.Property(
        ColorMode,
        get_color_mode,
        set_color_mode,
        doc="Mode to use for coloring",
    )
    low_color = core.Property(
        gui.QColor,
        get_low_color,
        set_low_color,
        doc="Color for lower end of color spectrum",
    )
    high_color = core.Property(
        gui.QColor,
        get_high_color,
        set_high_color,
        doc="Color for upper end of color spectrum",
    )


if __name__ == "__main__":
    import random

    from prettyqt import widgets

    app = widgets.app()

    val_range = range(0, 100, 10)
    data = dict(
        a=random.sample(val_range, k=10),
        b=random.sample(val_range, k=10),
        c=random.sample(val_range, k=10),
    )
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    # table.proxifier[:, :].color_values()
    table.set_size_adjust_policy("content")
    table.setWindowTitle("Color values")
    table.set_icon("mdi.palette")
    table.show()
    table.adjustSize()
    with app.debug_mode():
        app.exec()
