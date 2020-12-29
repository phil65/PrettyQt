import pathlib
from typing import Union

from prettyqt.qt import QtCore, QtGui


IconType = Union[QtGui.QIcon, str, pathlib.Path, None]

ColorType = Union[str, int, QtCore.Qt.GlobalColor, QtGui.QColor, tuple, None]
ColorAndBrushType = Union[ColorType, QtGui.QBrush]
