"""Provides QtLocation classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtLocation import *
elif PYQT6:
    from PyQt6.QtLocation import *
elif PYSIDE6:
    from PySide6.QtLocation import *  # type: ignore
else:
    raise PythonQtError("No Qt bindings could be found")
