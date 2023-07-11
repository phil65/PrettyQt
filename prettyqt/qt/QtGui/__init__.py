"""Provides QtGui classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6
from prettyqt.utils import get_repr

if PYQT6:
    from PyQt6.QtGui import *

    for cls in (QPalette,):
        for attr in dir(cls):
            if not attr[0].isupper():
                continue
            ns = getattr(cls, attr)
            for name, val in vars(ns).items():
                if not name.startswith("_"):
                    setattr(cls, name, val)

    def pos(self, *a):
        _pos = self.position(*a)
        return _pos.toPoint()

    QMouseEvent.pos = pos  # type: ignore

    # mightBeRichText is strangely in QtGui.Qt for PySide6..
    from PyQt6.QtCore import Qt


elif PYSIDE6:
    from PySide6.QtGui import *  # type: ignore
else:
    raise ModuleNotFoundError("No Qt bindings could be found")


def __repr__(self):
    return get_repr(self, self.red(), self.green(), self.blue(), self.alpha())


QColor.__repr__ = __repr__
