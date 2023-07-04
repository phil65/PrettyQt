from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, custom_models
from prettyqt.qt import QtGui
from prettyqt.utils import colors, datatypes


HighlightModeStr = Literal["column", "row", "all"]


class SliceHighlightCurrentProxyModel(custom_models.SliceIdentityProxyModel):
    """Proxy model which highlights all cells with same data as current index.

    Highlights all cells with same content in given role as currently focused cell
    with a user-specified color.

    Possible modes are:

    * `all`: Highlight all cells with same value.
    * `column`: Highlight all cells with same value and same column as current.
    * `row`: Highlight all cells with same value and same row as current.

    !!! note
        This is a slice proxy and can be selectively applied to a model.

    ### Example

    ```py
    model = MyModel()
    table = widgets.TableView()
    table.set_model(model)
    table[:, :3].proxify.highlight_current(mode="all")
    table.show()
    # or
    indexer = (slice(None), slice(None, 3))
    proxy = custom_models.SliceFilterProxyModel(indexer=indexer)
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "highlight_current"

    def __init__(
        self,
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
        super().__init__(**kwargs)
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

    def set_highlight_role(self, mode: constants.ItemDataRole):
        """Set highlight mode."""
        self._data_role = mode

    def get_highlight_role(self) -> constants.ItemDataRole:
        """Get highlight mode."""
        return self._data_role

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if (
            role == constants.BACKGROUND_ROLE
            and index.data(self._data_role) == self._current_value
            and self.indexer_contains(index)
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
    highlightRole = core.Property(
        constants.ItemDataRole, get_highlight_role, set_highlight_role
    )


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app(style="Windows")
    dct = dict(
        a=["a", "b", "a", "b"],
        b=["a", "b", "a", "b"],
        c=["a", "b", "a", "b"],
        d=["b", "a", "b", "a"],
        e=["a", "b", "a", "a"],
    )
    model = gui.StandardItemModel.from_dict(dct)
    table = widgets.TableView()
    table.set_model(model)
    # table.proxifier[:, ::2].highlight_current(mode="column")
    table.resize(500, 200)
    table.set_title("Example")
    table.set_icon("mdi.cursor-default-click-outline")
    table.show()
    table.h_header.resize_sections("stretch")
    with app.debug_mode():
        app.exec()
