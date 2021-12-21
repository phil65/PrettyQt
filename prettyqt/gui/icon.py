from __future__ import annotations

from typing import Literal

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, bidict, types


MODE = bidict(
    normal=QtGui.QIcon.Mode.Normal,
    disabled=QtGui.QIcon.Mode.Disabled,
    active=QtGui.QIcon.Mode.Active,
    selected=QtGui.QIcon.Mode.Selected,
)

ModeStr = Literal["normal", "disabled", "active", "selected"]

STATE = bidict(off=QtGui.QIcon.State.Off, on=QtGui.QIcon.State.On)

StateStr = Literal["off", "on"]


class Icon(QtGui.QIcon):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def __bool__(self):
        return not self.isNull()

    def __getstate__(self):
        pixmap = self.pixmap(256, 256)
        return bytes(core.DataStream.create_bytearray(pixmap))

    def __setstate__(self, ba):
        px = QtGui.QPixmap()
        core.DataStream.write_bytearray(ba, px)
        super().__init__(px)

    @classmethod
    def for_color(cls, color_str: str) -> Icon:
        color = gui.Color.from_text(color_str)
        if not color.isValid():
            raise TypeError()
        bitmap = gui.Pixmap(16, 16)
        bitmap.fill(color)
        return cls(bitmap)

    @classmethod
    def from_char(cls, char: str, background="black", color="white"):
        """Create a QIcon with a given character."""
        icon = cls()
        for size in (16, 32, 64):
            px = gui.Pixmap.create_char(
                char, background=background, color=color, size=size
            )
            icon.addPixmap(px)
        return icon

    @classmethod
    def from_image(cls, image: QtGui.QImage):
        return cls(gui.Pixmap.fromImage(image))

    def get_available_sizes(
        self, mode: ModeStr = "normal", state: StateStr = "off"
    ) -> list[core.Size]:
        if mode not in MODE:
            raise InvalidParamError(mode, MODE)
        if state not in STATE:
            raise InvalidParamError(state, STATE)
        return [core.Size(i) for i in self.availableSizes(MODE[mode], STATE[state])]

    def add_pixmap(
        self,
        data: QtCore.QByteArray | QtGui.QPixmap | bytes,
        mode: ModeStr = "normal",
        state: StateStr = "off",
    ):
        if mode not in MODE:
            raise InvalidParamError(mode, MODE)
        if state not in STATE:
            raise InvalidParamError(state, STATE)
        if isinstance(data, bytes):
            data = QtCore.QByteArray(data)
        if isinstance(data, QtCore.QByteArray):
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
        else:
            pixmap = data
        self.addPixmap(pixmap, MODE[mode], STATE[state])

    def get_pixmap(
        self,
        size: types.SizeType | int,
        mode: ModeStr = "normal",
        state: StateStr = "off",
    ) -> QtGui.QPixmap:
        if mode not in MODE:
            raise InvalidParamError(mode, MODE)
        if state not in STATE:
            raise InvalidParamError(state, STATE)
        if isinstance(size, tuple):
            size = core.Size(*size)
        elif isinstance(size, int):
            size = core.Size(size, size)
        return self.pixmap(size, MODE[mode], STATE[state])

    def get_actual_size(
        self,
        size: types.SizeType | int,
        mode: ModeStr = "normal",
        state: StateStr = "off",
    ) -> core.Size:
        if mode not in MODE:
            raise InvalidParamError(mode, MODE)
        if state not in STATE:
            raise InvalidParamError(state, STATE)
        if isinstance(size, tuple):
            size = core.Size(*size)
        elif isinstance(size, int):
            size = core.Size(size, size)
        return core.Size(self.actualSize(size, MODE[mode], STATE[state]))


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    icon = Icon.from_char("A")
    window = widgets.MainWindow()
    window.set_icon(icon)
    window.show()
    app.main_loop()
