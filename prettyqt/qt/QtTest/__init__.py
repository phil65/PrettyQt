"""Provides QtTest classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtTest import *
elif PYSIDE6:
    from PySide6.QtTest import *  # type: ignore
else:
    raise PythonQtError("No Qt bindings could be found")
