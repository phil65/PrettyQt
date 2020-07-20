# -*- coding: utf-8 -*-
"""
"""

import pathlib
from typing import Union, Optional, Dict, Tuple


import qtawesome as qta
from qtpy import QtCore, QtGui

from prettyqt import core, gui


IconType = Union[QtGui.QIcon, str, pathlib.Path, None]

key_type = Tuple[Optional[str], Optional[str], bool]
icon_cache: Dict[key_type, QtGui.QIcon] = dict()


def get_icon(icon: IconType, color: Optional[str] = None, as_qicon: bool = False):
    """
    qtawesome already caches icons, but since we construct our own subclassed icon,
    we cache, too
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
        ba = QtCore.QByteArray()
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.WriteOnly)
        pixmap = self.pixmap(QtCore.QSize(256, 256))
        stream << pixmap
        return ba

    def __setstate__(self, ba):
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.ReadOnly)
        px = QtGui.QPixmap()
        stream >> px
        super().__init__(px)

    @classmethod
    def for_color(cls, color_str: str) -> "Icon":
        color = gui.Color.from_text(color_str)
        if color.isValid():
            bitmap = gui.Pixmap(16, 16)
            bitmap.fill(color)
            icon = cls(bitmap)
        else:
            icon = cls(qta.icon("mdi.card-outline"))
        return icon

    def get_pixmap(self, size: int) -> QtGui.QPixmap:
        size = core.Size(size, size)
        return self.pixmap(size)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    icon = Icon.for_color("green")
