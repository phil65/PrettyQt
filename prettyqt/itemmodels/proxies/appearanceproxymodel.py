from __future__ import annotations

import collections
from collections.abc import Callable
from typing import Any

from prettyqt import constants, core
from prettyqt.qt import QtGui


class AppearanceProxyModel(core.IdentityProxyModel):
    """Proxy model for changing the "style roles" of the source model.

    In contrast to
    [SliceAppearanceProxyModel](../proxymodels/sliceappearanceproxymodel.md),
    this one works in a more "static" way, meaning that you can change the
    color / font / alignment of indexes via model.setData even when the source model
    is not item-based (like a StandardItemModel).

    ### Example:
    ```py
    model = MyModel()
    proxy = itemmodels.AppearanceProxyModel()
    proxy.set_source_model(model)
    proxy.setData(proxy.index(0, 0), gui.QColor("red"), role=constants.FOREGROUND_ROLE)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "appearance"
    ICON = "mdi.palette-outline"

    def __init__(
        self,
        foreground_default=None,
        background_default=None,
        font_default=None,
        alignment_default=None,
        **kwargs,
    ):
        self._foregrounds = collections.defaultdict(lambda: None)
        self._backgrounds = collections.defaultdict(lambda: None)
        self._alignments = collections.defaultdict(lambda: None)
        self._fonts = collections.defaultdict(lambda: None)
        self._foreground_default = foreground_default
        self._background_default = background_default
        self._font_default = font_default
        self._alignment_default = alignment_default
        super().__init__(**kwargs)

    # def setSourceModel(self, model):
    #     if (curr_model := self.sourceModel()) is not None:
    #         # curr_model.dataChanged.disconnect(self._reset)
    #         curr_model.columnsInserted.disconnect(self._reset)
    #         curr_model.columnsRemoved.disconnect(self._reset)
    #         curr_model.columnsMoved.disconnect(self._reset)

    #     with self.reset_model():
    #         super().setSourceModel(model)

    #     # model.dataChanged.connect(self._reset)
    #     model.columnsInserted.connect(self._reset)
    #     model.columnsRemoved.connect(self._reset)
    #     model.columnsMoved.connect(self._reset)

    # def _reset(self):
    #     self._foregrounds = collections.defaultdict(lambda: None)
    #     self._backgrounds = collections.defaultdict(lambda: None)
    #     self._alignments = collections.defaultdict(lambda: None)
    #     self._fonts = collections.defaultdict(lambda: None)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        key = self.get_index_key(index, include_column=True)
        match role:
            case constants.FOREGROUND_ROLE:
                self._foregrounds[key] = value
                self.dataChanged.emit(index, index)
                return True
            case constants.BACKGROUND_ROLE:
                self._backgrounds[key] = value
                self.dataChanged.emit(index, index)
                return True
            case constants.FONT_ROLE:
                self._fonts[key] = value
                self.dataChanged.emit(index, index)
                return True
            case constants.ALIGNMENT_ROLE:
                self._alignments[key] = value
                self.dataChanged.emit(index, index)
                return True
            case _:
                return super().setData(index, value, role)

    def data(  # noqa: PLR0911
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        key = self.get_index_key(index, include_column=True)
        match role:
            case constants.FOREGROUND_ROLE:
                if val := self._foregrounds[key]:
                    return val
                match self._foreground_default:
                    case type() | Callable():
                        return self._foreground_default()
                    case None:
                        return super().data(index, role)
                    case _:
                        return self._foreground_default
            case constants.BACKGROUND_ROLE:
                if val := self._backgrounds[key]:
                    return val
                match self._background_default:
                    case type() | Callable():
                        return self._background_default()
                    case None:
                        return super().data(index, role)
                    case _:
                        return self._background_default
            case constants.FONT_ROLE:
                if val := self._fonts[key]:
                    return val
                match self._font_default:
                    case type() | Callable():
                        return self._font_default()
                    case None:
                        return super().data(index, role)
                    case _:
                        return self._font_default
            case constants.ALIGNMENT_ROLE:
                val = self._alignments[key]
                return val or self._alignment_default
            case _:
                return super().data(index, role)

    def set_font_default(self, font: QtGui.QFont | str):
        self._font_default = QtGui.QFont(font)
        self._fonts = collections.defaultdict(lambda: None)
        self.update_all()

    def get_font_default(self) -> QtGui.QFont:
        return self._font_default

    def set_foreground_default(self, foreground: QtGui.QColor | QtGui.QBrush | str):
        if isinstance(foreground, str):
            foreground = QtGui.QColor(foreground)
        self._foreground_default = foreground
        self._foregrounds = collections.defaultdict(lambda: None)
        self.update_all()

    def get_foreground_default(self) -> QtGui.QColor:
        return self._foreground_default

    def set_background_default(self, background: QtGui.QColor | QtGui.QBrush | str):
        if isinstance(background, str):
            background = QtGui.QColor(background)
        self._background_default = background
        self._backgrounds = collections.defaultdict(lambda: None)
        self.update_all()

    def get_background_default(self) -> QtGui.QFont:
        return self._background_default

    def set_alignment_default(
        self, alignment: constants.AlignmentFlag | constants.AlignmentStr
    ):
        if isinstance(alignment, str):
            alignment = constants.ALIGNMENTS[alignment]
        self._alignment_default = alignment
        self._alignments = collections.defaultdict(lambda: None)
        self.update_all()

    def get_alignment_default(self) -> constants.AlignmentFlag:
        return self._alignment_default

    font_default = core.Property(
        QtGui.QFont,
        get_font_default,
        set_font_default,
        doc="Default font for whole table",
    )
    foreground_default = core.Property(
        object,
        get_foreground_default,
        set_foreground_default,
        doc="Default foreground for whole table",
    )
    background_default = core.Property(
        object,
        get_background_default,
        set_background_default,
        doc="Default background for whole table",
    )
    alignment_default = core.Property(
        constants.AlignmentFlag,
        get_alignment_default,
        set_alignment_default,
        doc="Default alignment for whole table",
    )


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app()
    table = widgets.TableView()
    table.setSortingEnabled(True)
    _source_model = core.StringListModel(["a", "b", "b", "b"])
    model = AppearanceProxyModel(parent=table)
    model.setSourceModel(_source_model)
    model.set_font_default(gui.Font.mono().family())
    model.set_background_default("green")
    index = model.index(0, 0)
    model.setData(index, QtGui.QColor("red"), constants.BACKGROUND_ROLE)
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.exec()
