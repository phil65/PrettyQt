"""Provides QtSvg classes and functions."""

from typing import TYPE_CHECKING

from prettyqt.qt import PYQT6, PYSIDE6


# Type checkers see PySide6 only (see prettyqt/qt/__init__.py).
if TYPE_CHECKING:
    from PySide6.QtSvg import *
    from PySide6.QtSvgWidgets import QGraphicsSvgItem, QSvgWidget  # type: ignore
elif PYQT6:
    from PyQt6.QtSvg import *
elif PYSIDE6:
    from PySide6.QtSvg import *
    from PySide6.QtSvgWidgets import QGraphicsSvgItem, QSvgWidget  # type: ignore
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
