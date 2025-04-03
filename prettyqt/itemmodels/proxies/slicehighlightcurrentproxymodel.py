from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, itemmodels
from prettyqt.qt import QtGui
from prettyqt.utils import colors, datatypes


HighlightModeStr = Literal["column", "row", "all"]


class SliceHighlightCurrentProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model which highlights all cells with same data as current index.

    Highlights all cells with same content in given role as currently focused cell
    with a user-specified color.

    Possible modes are:

    * `all`: Highlight all cells with same value.
    * `column`: Highlight all cells with same value and same column as current.
    * `row`: Highlight all cells with same value and same row as current.

    === "Without proxy"

        ```py
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
        # apply proxy to every 2nd column
        # table.proxifier[:, ::2].highlight_current(mode="column")
        ```
        <figure markdown>
          ![Image title](../../images/slicehighlightcurrentproxymodel_none.png)
        </figure>

    === "Row mode"

        ```py
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
        # apply proxy to every 2nd column
        table.proxifier[:, ::2].highlight_current(mode="row")
        ```
        <figure markdown>
          ![Image title](../../images/slicehighlightcurrentproxymodel_row.png)
        </figure>

    === "Column mode"

        ```py
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
        # apply proxy to every 2nd column
        table.proxifier[:, ::2].highlight_current(mode="column")
        ```
        <figure markdown>
          ![Image title](../../images/slicehighlightcurrentproxymodel_column.png)
        </figure>

    === "All mode"

        ```py
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
        # apply proxy to every 2nd column
        table.proxifier[:, ::2].highlight_current(mode="all")
        ```
        <figure markdown>
          ![Image title](../../images/slicehighlightcurrentproxymodel_all.png)
        </figure>


    ### Example

    ```py
    model = MyModel()
    table = widgets.TableView()
    table.set_model(model)
    table[:, :3].proxify.highlight_current(mode="all")
    table.show()
    # or
    indexer = (slice(None), slice(None, 3))
    proxy = itemmodels.SliceFilterProxyModel(indexer=indexer)
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.selectionModel().currentChanged.connect(proxy.highlight_index)
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

    def set_highlight_column(self, column: int):
        with self.change_layout():
            self._current_column = column

    def get_highlight_column(self) -> int:
        return self._current_column

    def set_highlight_row(self, row: int):
        with self.change_layout():
            self._current_row = row

    def get_highlight_row(self) -> int:
        return self._current_row

    def set_current_value(self, value):
        with self.change_layout():
            self._current_value = value

    def highlight_index(self, index: core.ModelIndex):
        with self.change_layout():
            self._current_value = index.data(self._data_role)  # super().data(index, role)
            self._current_row = index.row()
            self._current_column = index.column()

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
                    (self._mode == "row" and (index.row() == self._current_row))
                    or self._mode == "all"
                )
            )
        ):
            return self._highlight_color
        return super().data(index, role)

    highlightMode = core.Property(  # noqa: N815
        str,
        get_highlight_mode,
        set_highlight_mode,
        doc="Highlight mode",
    )
    highlightColor = core.Property(  # noqa: N815
        QtGui.QColor,
        get_highlight_color,
        set_highlight_color,
        doc="Color to use for highlighting",
    )
    highlightRole = core.Property(  # noqa: N815
        constants.ItemDataRole,
        get_highlight_role,
        set_highlight_role,
        doc="ItemRole to use for highlighting",
    )
    highlight_column = core.Property(
        int,
        get_highlight_column,
        set_highlight_column,
        doc="Currently highlighted column",
    )
    highlight_row = core.Property(
        int,
        get_highlight_row,
        set_highlight_row,
        doc="Currently highlighted row",
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
    table.proxifier[:, ::2].highlight_current(mode="column")
    table.resize(500, 200)
    table.set_title("Example")
    table.set_icon("mdi.cursor-default-click-outline")
    table.show()
    table.h_header.resize_sections("stretch")
    with app.debug_mode():
        app.exec()
