from __future__ import annotations

import collections
from collections.abc import Callable
from prettyqt import constants, core
from prettyqt.qt import QtCore, QtGui


class AppearanceProxyModel(core.IdentityProxyModel):
    ID = "appearance"

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

    def setData(self, index, value, role=constants.EDIT_ROLE):
        key = self.get_index_key(index)
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

    def data(self, index, role=constants.DISPLAY_ROLE):
        key = self.get_index_key(index)
        match role:
            case constants.FOREGROUND_ROLE:
                if val := self._foregrounds[key]:
                    return val
                match self._foreground_default:
                    case type() | Callable():
                        return self._foreground_default()
                    case _:
                        return self._foreground_default
            case constants.BACKGROUND_ROLE:
                if val := self._backgrounds[key]:
                    return val
                match self._background_default:
                    case type() | Callable():
                        return self._background_default()
                    case _:
                        return self._background_default
            case constants.FONT_ROLE:
                if val := self._fonts[key]:
                    return val
                match self._font_default:
                    case type() | Callable():
                        return self._font_default()
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
        self, alignment: QtCore.Qt.AlignmentFlag | constants.AlignmentStr
    ):
        if isinstance(alignment, str):
            alignment = constants.ALIGNMENTS[alignment]
        self._alignment_default = alignment
        self._alignments = collections.defaultdict(lambda: None)
        self.update_all()

    def get_alignment_default(self) -> QtCore.Qt.AlignmentFlag:
        return self._alignment_default

    font_default = core.Property(QtGui.QFont, get_font_default, set_font_default)
    foreground_default = core.Property(
        object, get_foreground_default, set_foreground_default
    )
    background_default = core.Property(
        object, get_background_default, set_background_default
    )
    alignment_default = core.Property(
        QtCore.Qt.AlignmentFlag, get_alignment_default, set_alignment_default
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
    model = model.proxifier.get_proxy("sort_filter")
    index = model.index(0, 0)
    model.setData(index, QtGui.QColor("red"), constants.BACKGROUND_ROLE)
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.main_loop()
