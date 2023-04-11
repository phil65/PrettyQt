"""Provides QtMultimedia classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYSIDE6:
    from PySide6.QtMultimedia import *
elif PYQT6:
    from PyQt6.QtMultimedia import *
else:
    raise PythonQtError("No Qt bindings could be found")
