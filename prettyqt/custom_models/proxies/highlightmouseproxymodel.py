from __future__ import annotations

import logging

from typing import Literal

from prettyqt import constants, core
from prettyqt.qt import QtGui
from prettyqt.utils import colors, datatypes


HighlightModeStr = Literal["column", "row", "both", "single"]

logger = logging.getLogger(__name__)


class HighlightMouseProxyModel(core.IdentityProxyModel):
    """Proxy model which highlights all cells with same row / column as mouse position.

    The proxy can work in four different modes.

    * column: The column the mouse is currently hovering over is highlighted.
    * row: The row the mouse is currently hovering over is highlighted.
    * both: Combination of column and row mode.
    * single: only the hovered cell is highlighted.
    """

    ID = "highlight_mouse"
    ICON = "mdi.cursor-default-click-outline"

    def __init__(
        self,
        parent: widgets.QAbstractItemView,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        mode: HighlightModeStr = "both",
        highlight_color: datatypes.ColorType = "red",
        **kwargs,
    ):
        self._mode = mode
        self._current_value = ...  # Sentinel value
        self._data_role = role
        self._current_column = None
        self._current_row = None
        self._highlight_color = colors.get_color(highlight_color).as_qt()
        super().__init__(parent, **kwargs)
        parent.setMouseTracking(True)
        parent.entered.connect(self.cell_entered)
        parent.installEventFilter(self)

    def eventFilter(self, source, event):
        match event.type():
            case core.Event.Type.Leave:
                self._current_row = None
                self._current_column = None
                self.force_layoutchange()
        return False

    def cell_entered(self, index):
        self._current_row = index.row()
        self._current_column = index.column()
        self.force_layoutchange()

    def set_highlight_color(self, color: datatypes.ColorType):
        """Set color used for highlighting cells."""
        self._highlight_color = colors.get_color(color).as_qt()

    def get_highlight_color(self) -> QtGui.QColor:
        """Get color used for higlighting cells."""
        return self._highlight_color

    def set_highlight_mode(self, mode: HighlightModeStr):
        """Set highlight mode."""
        self._highlight_mode = mode

    def get_highlight_mode(self) -> HighlightModeStr:
        """Get highlight mode."""
        return self._highlight_mode

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role != constants.BACKGROUND_ROLE:
            return super().data(index, role)
        is_in_row = index.row() == self._current_row
        is_in_column = index.column() == self._current_column
        match self._mode:
            case "column" if is_in_column:
                return self._highlight_color
            case "row" if is_in_row:
                return self._highlight_color
            case "both" if is_in_row or is_in_column:
                return self._highlight_color
            case "single" if is_in_row and is_in_column:
                return self._highlight_color
            case _:
                return super().data(index, role)

    highlightMode = core.Property(str, get_highlight_mode, set_highlight_mode)
    highlightColor = core.Property(QtGui.QColor, get_highlight_color, set_highlight_color)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    table = debugging.example_table()
    table.proxifier.get_proxy("highlight_mouse")
    table.show()
    with app.debug_mode():
        app.exec()
