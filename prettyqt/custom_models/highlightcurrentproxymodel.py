from __future__ import annotations

from typing import Literal

from prettyqt import constants, core
from prettyqt.qt import QtGui
from prettyqt.utils import colors, datatypes

HighlightModeStr = Literal["column", "row", "all"]


class HighlightCurrentProxyModel(core.IdentityProxyModel):
    """Highlights all cells which have same data as current index in given role."""

    ID = "highlight_current"

    def __init__(
        self,
        *args,
        role=constants.DISPLAY_ROLE,
        mode: HighlightModeStr = "column",
        highlight_color: datatypes.ColorType = "red",
        **kwargs,
    ):
        self._mode = mode
        self._current_value = ...  # Sentinel value
        self._data_role = role
        self._current_column = None
        self._current_row = None
        self._highlight_color = colors.get_color(highlight_color).as_qt()
        super().__init__(*args, **kwargs)
        parent: widgets.AbstractItemView = self.parent()  # type: ignore
        parent.model_changed.connect(self._on_model_change)
        if sel_model := parent.selectionModel():
            sel_model.currentChanged.connect(self._on_current_change)

    def _on_model_change(self, model):
        self.parent().selectionModel().currentChanged.connect(self._on_current_change)

    def _on_current_change(self, new, old):
        with self.change_layout():
            self._current_value = new.data(constants.DISPLAY_ROLE)
            self._current_column = new.column()
            self._current_row = new.row()

    def set_highlight_color(self, color: datatypes.ColorType):
        self._highlight_color = colors.get_color(color).as_qt()

    def get_highlight_color(self) -> QtGui.QColor:
        return self._highlight_color

    def set_highlight_mode(self, mode: HighlightModeStr):
        self._highlight_mode = mode

    def get_highlight_mode(self) -> HighlightModeStr:
        return self._highlight_mode

    def data(self, index, role=constants.DISPLAY_ROLE):
        if (
            role == constants.BACKGROUND_ROLE
            and index.data(self._data_role) == self._current_value
            and (
                (self._mode == "column" and index.column() == self._current_column)
                or (
                    self._mode == "row"
                    and (index.row() == self._current_row)
                    or self._mode == "all"
                )
            )
        ):
            return self._highlight_color
        return super().data(index, role)

    highlightMode = core.Property(str, get_highlight_mode, set_highlight_mode)
    highlightColor = core.Property(QtGui.QColor, get_highlight_color, set_highlight_color)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    table = widgets.TableView()
    table.set_model(["a", "b", "c", "d", "a"])
    table.model().setParent(table)
    model = table.model().proxifier.get_proxy("highlight_current", mode="all")
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.main_loop()
