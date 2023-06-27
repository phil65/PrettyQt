from __future__ import annotations

from typing import Literal

from prettyqt import core, gui
from prettyqt.utils import bidict


ModeStr = Literal["clipboard", "selection", "find_buffer"]

MODES: bidict[ModeStr, gui.QClipboard.Mode] = bidict(
    clipboard=gui.QClipboard.Mode.Clipboard,
    selection=gui.QClipboard.Mode.Selection,
    find_buffer=gui.QClipboard.Mode.FindBuffer,
)


class Clipboard(core.ObjectMixin):
    def __init__(self, item: gui.QClipboard):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_pixmap(
        self,
        pixmap: gui.QPixmap | None,
        mode: ModeStr | gui.QClipboard.Mode = "clipboard",
    ):
        if pixmap is None:
            pixmap = gui.QPixmap()
        self.item.setPixmap(pixmap, MODES.get_enum_value(mode))

    def get_pixmap(
        self, mode: ModeStr | gui.QClipboard.Mode = "clipboard"
    ) -> gui.Pixmap | None:
        val = MODES.get_enum_value(mode)
        pix = gui.Pixmap(self.item.pixmap(val))
        return None if pix.isNull() else pix

    def set_image(
        self,
        image: gui.QImage | None,
        mode: ModeStr | gui.QClipboard.Mode = "clipboard",
    ):
        if image is None:
            image = gui.QImage()
        self.item.setImage(image, MODES.get_enum_value(mode))

    def get_image(
        self, mode: ModeStr | gui.QClipboard.Mode = "clipboard"
    ) -> gui.Image | None:
        img = gui.Image(self.item.image(MODES.get_enum_value(mode)))
        return None if img.isNull() else img

    def set_mimedata(
        self,
        mimedata: core.QMimeData,
        mode: ModeStr | gui.QClipboard.Mode = "clipboard",
    ):
        self.item.setMimeData(mimedata, MODES.get_enum_value(mode))

    def get_mimedata(
        self, mode: ModeStr | gui.QClipboard.Mode = "clipboard"
    ) -> core.QMimeData:
        return self.item.mimeData(MODES.get_enum_value(mode))

    def set_text(self, text: str, mode: ModeStr | gui.QClipboard.Mode = "clipboard"):
        self.item.setText(text, MODES.get_enum_value(mode))

    def get_text(self, mode: ModeStr | gui.QClipboard.Mode = "clipboard") -> str:
        return self.item.text(MODES.get_enum_value(mode))
