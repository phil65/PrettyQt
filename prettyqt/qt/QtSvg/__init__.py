"""Provides QtSvg classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtSvg import *
elif PYQT6:
    from PyQt6.QtSvg import *
elif PYSIDE2:
    from PySide2.QtSvg import *
elif PYSIDE6:
    from PySide6.QtSvg import *
    from PySide6.QtSvgWidgets import QGraphicsSvgItem, QSvgWidget  # type: ignore
else:
    raise PythonQtError("No Qt bindings could be found")
