from __future__ import annotations

import pathlib
from typing import Union, Optional, Dict, Tuple, List


import qtawesome as qta
from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError

MODES = bidict(
    normal=QtGui.QIcon.Normal,
    disabled=QtGui.QIcon.Disabled,
    active=QtGui.QIcon.Active,
    selected=QtGui.QIcon.Selected,
)

STATES = bidict(off=QtGui.QIcon.Off, on=QtGui.QIcon.On)

IconType = Union[QtGui.QIcon, str, pathlib.Path, None]

key_type = Tuple[Optional[str], Optional[str], bool]
icon_cache: Dict[key_type, QtGui.QIcon] = dict()


def get_icon(
    icon: IconType, color: Optional[str] = None, as_qicon: bool = False
) -> QtGui.QIcon:
    """Get icon with given color.

    Qtawesome already caches icons, but since we construct our own subclassed icon,
    we cache, too.
    """
    if isinstance(icon, QtGui.QIcon):
        return icon if as_qicon else Icon(icon)
    if isinstance(icon, pathlib.Path):
        icon = str(icon)
    if (icon, color, as_qicon) in icon_cache:
        return icon_cache[(icon, color, as_qicon)]
    if isinstance(icon, str) and icon.startswith("mdi."):
        if color is not None:
            new = qta.icon(icon, color=color)
        else:
            new = qta.icon(icon)
    else:
        new = QtGui.QIcon(icon)
    icon = new if as_qicon else Icon(new)
    icon_cache[(icon, color, as_qicon)] = icon
    return icon


def set_defaults(*args, **kwargs):
    qta.set_defaults(*args, **kwargs)


class Icon(QtGui.QIcon):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __bool__(self):
        return not bool(self.isNull())

    def __getstate__(self):
        pixmap = self.pixmap(256, 256)
        return core.DataStream.create_bytearray(pixmap)

    def __setstate__(self, ba):
        px = QtGui.QPixmap()
        core.DataStream.write_bytearray(ba, px)
        super().__init__(px)

    @classmethod
    def for_color(cls, color_str: str) -> Icon:
        color = gui.Color.from_text(color_str)
        if color.isValid():
            bitmap = gui.Pixmap(16, 16)
            bitmap.fill(color)
            icon = cls(bitmap)
        else:
            icon = cls(qta.icon("mdi.card-outline"))
        return icon

    @classmethod
    def from_image(cls, image: QtGui.QImage):
        return cls(gui.Pixmap.fromImage(image))

    def get_available_sizes(
        self, mode: str = "normal", state: str = "off"
    ) -> List[core.Size]:
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        if state not in STATES:
            raise InvalidParamError(state, STATES)
        return [core.Size(i) for i in self.availableSizes(MODES[mode], STATES[state])]

    def add_pixmap(self, data: Union[QtCore.QByteArray, QtGui.QPixmap, bytes]):
        if isinstance(data, bytes):
            data = QtCore.QByteArray(data)
        if isinstance(data, QtCore.QByteArray):
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
        else:
            pixmap = data
        self.addPixmap(pixmap)

    def get_pixmap(self, size: int) -> QtGui.QPixmap:
        size = core.Size(size, size)
        return self.pixmap(size)


if __name__ == "__main__":
    app = gui.app()
    icon = Icon.for_color("green")
