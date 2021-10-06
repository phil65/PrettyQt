from __future__ import annotations

from typing import Literal

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, bidict


MODES = bidict(
    clipboard=QtGui.QClipboard.Mode.Clipboard,
    selection=QtGui.QClipboard.Mode.Selection,
    find_buffer=QtGui.QClipboard.Mode.FindBuffer,
)

ModeStr = Literal["clipboard", "selection", "find_buffer"]


QtGui.QClipboard.__bases__ = (core.Object,)


class Clipboard:
    def __init__(self, item: QtGui.QClipboard):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_pixmap(self, pixmap: QtGui.QPixmap | None, mode: ModeStr = "clipboard"):
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        if pixmap is None:
            pixmap = QtGui.QPixmap()
        self.item.setPixmap(pixmap, MODES[mode])

    def get_pixmap(self, mode: ModeStr = "clipboard") -> gui.Pixmap | None:
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        pix = gui.Pixmap(self.item.pixmap(MODES[mode]))
        if pix.isNull():
            return None
        return pix

    def set_image(self, image: QtGui.QImage | None, mode: ModeStr = "clipboard"):
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        if image is None:
            image = QtGui.QImage()
        self.item.setImage(image, MODES[mode])

    def get_image(self, mode: ModeStr = "clipboard") -> gui.Image | None:
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        img = gui.Image(self.item.image(MODES[mode]))
        if img.isNull():
            return None
        return img

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
