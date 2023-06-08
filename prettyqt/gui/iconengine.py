from __future__ import annotations

import os
from typing import Literal

from prettyqt import core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import (
    InvalidParamError,
    bidict,
    datatypes,
    get_repr,
    serializemixin,
)


ICON_ENGINE_HOOK = bidict(
    # available_sizes=QtGui.QIconEngine.AvailableSizesHook,
    # icon_name=QtGui.QIconEngine.IconNameHook,
    is_null=QtGui.QIconEngine.IconEngineHook.IsNullHook,
    scaled_pixmap=QtGui.QIconEngine.IconEngineHook.ScaledPixmapHook,
)

IconEngineHookStr = Literal["available_sizes", "icon_name", "is_null", "scaled_pixmap"]


class IconEngine(serializemixin.SerializeMixin, QtGui.QIconEngine):
    def __repr__(self):
        return get_repr(self)

    def __bool__(self):
        return not self.isNull()

    def add_file(
        self,
        path: datatypes.PathType,
        size: datatypes.SizeType | int,
        mode: gui.icon.ModeStr,
        state: gui.icon.StateStr,
    ):
        if mode not in gui.icon.MODE:
            raise InvalidParamError(mode, gui.icon.MODE)
        if state not in gui.icon.STATE:
            raise InvalidParamError(state, gui.icon.STATE)
        match size:
            case (int(), int()):
                size = core.Size(*size)
            case int():
                size = core.Size(size, size)
            case core.QSize():
                pass
            case _:
                raise TypeError(size)
        self.addFile(os.fspath(path), size, gui.icon.MODE[mode], gui.icon.STATE[state])

    def add_pixmap(
        self,
        pixmap: QtGui.QPixmap,
        mode: gui.icon.ModeStr,
        state: gui.icon.StateStr,
    ):
        if mode not in gui.icon.MODE:
            raise InvalidParamError(mode, gui.icon.MODE)
        if state not in gui.icon.STATE:
            raise InvalidParamError(state, gui.icon.STATE)
        self.addPixmap(pixmap, gui.icon.MODE[mode], gui.icon.STATE[state])

    def get_actual_size(
        self,
        size: datatypes.SizeType | int,
        mode: gui.icon.ModeStr = "normal",
        state: gui.icon.StateStr = "off",
    ) -> core.Size:
        if mode not in gui.icon.MODE:
            raise InvalidParamError(mode, gui.icon.MODE)
        if state not in gui.icon.STATE:
            raise InvalidParamError(state, gui.icon.STATE)
        match size:
            case (int(), int()):
                size = core.Size(*size)
            case int():
                size = core.Size(size, size)
            case core.QSize():
                pass
            case _:
                raise TypeError(size)
        return core.Size(
            self.actualSize(size, gui.icon.MODE[mode], gui.icon.STATE[state])
        )

    def get_available_sizes(
        self, mode: gui.icon.ModeStr = "normal", state: gui.icon.StateStr = "off"
    ) -> list[core.Size]:
        if mode not in gui.icon.MODE:
            raise InvalidParamError(mode, gui.icon.MODE)
        if state not in gui.icon.STATE:
            raise InvalidParamError(state, gui.icon.STATE)
        return [
            core.Size(i)
            for i in self.availableSizes(gui.icon.MODE[mode], gui.icon.STATE[state])
        ]

    def get_pixmap(
        self,
        size: datatypes.SizeType | int,
        mode: gui.icon.ModeStr = "normal",
        state: gui.icon.StateStr = "off",
        scale: float | None = None,
    ) -> gui.Pixmap:
        if mode not in gui.icon.MODE:
            raise InvalidParamError(mode, gui.icon.MODE)
        if state not in gui.icon.STATE:
            raise InvalidParamError(state, gui.icon.STATE)
        match size:
            case (int(), int()):
                size = core.Size(*size)
            case int():
                size = core.Size(size, size)
            case core.QSize():
                pass
            case _:
                raise TypeError(size)
        if scale is None:
            return gui.Pixmap(
                self.pixmap(size, gui.icon.MODE[mode], gui.icon.STATE[state])
            )
        else:
            return gui.Pixmap(
                self.scaledPixmap(size, gui.icon.MODE[mode], gui.icon.STATE[state], scale)
            )


if __name__ == "__main__":
    app = gui.app()
    engine = IconEngine()
    print(repr(engine))
