from typing import Literal

from qtpy import QtCore, QtGui

from prettyqt import core, gui
from prettyqt.utils import InvalidParamError, bidict


MODES = bidict(
    clipboard=QtGui.QClipboard.Clipboard,
    selection=QtGui.QClipboard.Selection,
    find_buffer=QtGui.QClipboard.FindBuffer,
)

ModeStr = Literal["clipboard", "selection", "find_buffer"]


QtGui.QClipboard.__bases__ = (core.Object,)


class Clipboard:
    def __init__(self, item: QtGui.QClipboard):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_pixmap(self, pixmap: QtGui.QImage, mode: ModeStr = "clipboard"):
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        self.item.setPixmap(pixmap, MODES[mode])

    def get_pixmap(self, mode: ModeStr = "clipboard") -> gui.Pixmap:
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        return gui.Pixmap(self.item.pixmap(MODES[mode]))

    def set_image(self, image: QtGui.QImage, mode: ModeStr = "clipboard"):
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        self.item.setImage(image, MODES[mode])

    def get_image(self, mode: ModeStr = "clipboard") -> gui.Image:
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        return gui.Image(self.item.image(MODES[mode]))

    def set_mimedata(self, mimedata: QtCore.QMimeData, mode: ModeStr = "clipboard"):
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        self.item.setMimeData(mimedata, MODES[mode])

    def get_mimedata(self, mode: ModeStr = "clipboard") -> QtCore.QMimeData:
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        return self.item.mimeData(MODES[mode])

    def set_text(self, text: str, mode: ModeStr = "clipboard"):
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        self.item.setText(text, MODES[mode])

    def get_text(self, mode: ModeStr = "clipboard") -> str:
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        return self.item.text(MODES[mode])
