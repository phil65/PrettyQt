"""Provides QtScxml classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtScxml import *
elif PYSIDE6:
    from PySide6.QtScxml import *
else:
    raise PythonQtError("No Qt bindings could be found")
