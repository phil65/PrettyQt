"""Provides QtBluetooth classes and functions."""

from prettyqt.qt import PYSIDE6, PythonQtError


if PYSIDE6:
    from PySide6.QtBluetooth import *
else:
    raise PythonQtError("No Qt bindings could be found")
