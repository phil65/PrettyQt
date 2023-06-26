from __future__ import annotations

from typing import Literal

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import bidict


ModeStr = Literal["clipboard", "selection", "find_buffer"]

MODES: bidict[ModeStr, QtGui.QClipboard.Mode] = bidict(
    clipboard=QtGui.QClipboard.Mode.Clipboard,
    selection=QtGui.QClipboard.Mode.Selection,
    find_buffer=QtGui.QClipboard.Mode.FindBuffer,
)


class Clipboard(core.ObjectMixin):
    def __init__(self, item: QtGui.QClipboard):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_pixmap(
        self,
        pixmap: QtGui.QPixmap | None,
        mode: ModeStr | QtGui.QClipboard.Mode = "clipboard",
    ):
        if pixmap is None:
            pixmap = QtGui.QPixmap()
        self.item.setPixmap(pixmap, MODES.get_enum_value(mode))

    def get_pixmap(
        self, mode: ModeStr | QtGui.QClipboard.Mode = "clipboard"
    ) -> gui.Pixmap | None:
        val = MODES.get_enum_value(mode)
        pix = gui.Pixmap(self.item.pixmap(val))
        return None if pix.isNull() else pix

    def set_image(
        self,
        image: QtGui.QImage | None,
        mode: ModeStr | QtGui.QClipboard.Mode = "clipboard",
    ):
        if image is None:
            image = QtGui.QImage()
        self.item.setImage(image, MODES.get_enum_value(mode))

    def get_image(
        self, mode: ModeStr | QtGui.QClipboard.Mode = "clipboard"
    ) -> gui.Image | None:
        img = gui.Image(self.item.image(MODES.get_enum_value(mode)))
        return None if img.isNull() else img

    def set_mimedata(
        self,
        mimedata: QtCore.QMimeData,
        mode: ModeStr | QtGui.QClipboard.Mode = "clipboard",
    ):
        self.item.setMimeData(mimedata, MODES.get_enum_value(mode))

    def get_mimedata(
        self, mode: ModeStr | QtGui.QClipboard.Mode = "clipboard"
    ) -> QtCore.QMimeData:
        return self.item.mimeData(MODES.get_enum_value(mode))

    def set_text(self, text: str, mode: ModeStr | QtGui.QClipboard.Mode = "clipboard"):
        self.item.setText(text, MODES.get_enum_value(mode))

    def get_text(self, mode: ModeStr | QtGui.QClipboard.Mode = "clipboard") -> str:
        return self.item.text(MODES.get_enum_value(mode))
