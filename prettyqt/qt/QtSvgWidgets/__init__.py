"""Provides QtSvg classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtSvgWidgets import *
elif PYSIDE6:
    from PySide6.QtSvgWidgets import *
else:
    raise PythonQtError("No Qt bindings could be found")
