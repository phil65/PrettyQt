# -*- coding: utf-8 -*-
"""

for full list, see:
- https://cdn.materialdesignicons.com/3.0.39/
"""

from typing import Union

from qtpy import QtGui, QtCore
from prettyqt import gui


ColorType = Union[str, int, QtGui.QRgba64, QtCore.Qt.GlobalColor,
                  QtGui.QColor, tuple, None]


def get_color(color: ColorType) -> gui.Color:
    if isinstance(color, (tuple, list)):
        return gui.Color(*color)
    return gui.Color(color)
